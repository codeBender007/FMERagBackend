import os
import re
import decimal
from datetime import date, datetime, time
from collections import Counter
from typing import Any, Iterable

from sqlalchemy import text
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

from core.config import settings
from core.security import sanitize_and_validate_sql
from db.connection import engine
from db.schema_inspector import get_table_schema_context
from services.ai_engine.state import AgentState
from services.ai_engine.catalog import COMPACT_TABLE_CATALOG, TABLE_NAMES, TABLE_METADATA
from services.ai_engine.prompts import (
    TABLE_SELECTOR_PROMPT,
    SQL_GENERATOR_PROMPT,
    FORMATTER_PROMPT,
)

llm = ChatOllama(
    base_url=settings.OLLAMA_BASE_URL,
    model=settings.OLLAMA_MODEL,
    temperature=0,
)

# Initialize ChromaDB schema catalog vector store & retriever (k=7 for rich relational retrieval)
CHROMA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "chroma_db"))

schema_embeddings = OllamaEmbeddings(
    base_url=settings.OLLAMA_BASE_URL,
    model="nomic-embed-text",
)

vector_db = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=schema_embeddings,
    collection_name="fme_schema_catalog",
)
schema_retriever = vector_db.as_retriever(search_kwargs={"k": 7})

# Casual greeting/chitchat guardrail regex pattern
GREETING_PATTERN = re.compile(
    r"^(hi|hello|hellop|hey|heyy|namaste|good\s*(morning|afternoon|evening)|how are you|who are you)[\s!?.Ready]*$",
    re.IGNORECASE,
)

# 100% English Fast-Path Domain Keyword Mapping (low-latency direct hits)
DOMAIN_KEYWORD_MAP = {
    r"\b(contractors?|vendors?|staffing agenc(y|ies)|supplier)\b": ["contractors"],
    r"\b(machines?|equipments?|workstations?|allotments?)\b": ["machines", "machine_assignments"],
    r"\b(dept[\s_-]?heads?|department[\s_-]?heads?|head of department|hod)\b": ["departments", "users"],
    r"\b(departments?|depts?|divisions?)\b": ["departments"],
    r"\b(section[\s_-]?heads?|head of section|section incharge|section leader|section lead)\b": ["section_heads", "sections", "users"],
    r"\b(sections?)\b": ["sections"],
    r"\b(lines?|assembly lines?|production lines?)\b": ["lines"],
    r"\b(sub[\s_-]?sections?|work cells?)\b": ["sub_sections"],
    r"\b(line requirements?|line manpower|manpower per line)\b": ["line_requirements", "line_requirement_history"],
    r"\b(certificate templates?|cert templates?)\b": ["certificate_templates"],
    r"\b(certificates?|certified)\b": ["certificates", "certificate_templates"],
    r"\b(email configs?|email configurations?|scheduled emails?)\b": ["email_configurations", "email_report_recipients"],
    r"\b(attendance|punch(es)?|present|absent|leave|overtime|ot|late arrival|early departure|hrs worked|hours worked|absenteeism)\b": ["attendance_logs"],
    r"\b(5m assignments?|daily 5m assignments?|5m duty|5m allocation)\b": ["daily_5m_assignments"],
    r"\b(5m|daily 5m|five m|5m records?|5m checklist|5m inspection)\b": ["daily_5m_records", "daily_5m_assignments"],
    r"\b(dpr|daily production reports?|production reports?|scrap|downtime|direct efficiency|kaizen|defects?)\b": ["daily_production_reports", "dpr_manual_statistics"],
    r"\b(dojo|dojo test|dojo evaluation|evaluation tests?|practical tests?|handover eligible)\b": ["evaluation_test_attempts", "evaluation_tests"],
    r"\b(ojt|on[\s_-]?job[\s_-]?trainings?|training score|shop floor training)\b": ["on_job_trainings"],
    r"\b(skill matrix|skill matrices|multiskilling|multi[\s_-]?skilling|competency|skill levels?)\b": ["skill_matrices", "skill_matrix_evaluations", "skill_upgradation_plans"],
    r"\b(ten cycle|10 cycle|ten cycle sheets?|ten cycle checks?)\b": ["ten_cycle_sheets", "ten_cycle_checks"],
    r"\b(3[\s_-]?day|three[\s_-]?day|3[\s_-]?day monitorings?)\b": ["three_day_monitorings"],
    r"\b(16[\s_-]?day|sixteen[\s_-]?day|16[\s_-]?day monitorings?|post-handover)\b": ["sixteen_day_monitorings"],
    r"\b(abnormal|abnormality|abnormal conditions?|line stoppages?|safety issues?)\b": ["abnormal_condition_sheets"],
    r"\b(handover sheets?|shift handovers?|charge handovers?)\b": ["handover_sheets"],
    r"\b(headcounts?|headcount reports?|monthly headcounts?|manpower summary)\b": ["headcount_reports"],
    r"\b(courses?|modules?|lessons?|syllabus|curriculum|training catalog)\b": ["courses", "modules", "lessons"],
    r"\b(quizzes?|exams?|tests?|assessments?|question papers?)\b": ["quizzes", "attempted_quizzes"],
    r"\b(attempted quiz(zes)?|quiz attempts?|quiz scores?|student scores?|who passed|who failed)\b": ["attempted_quizzes", "quizzes"],
    r"\b(assignments?|submissions?|homework|tasks?)\b": ["assignments", "submissions"],
    r"\b(enrollments?|enrolled students?)\b": ["enrollments", "courses"],
    r"\b(progress|learning progress|lesson progress|module progress)\b": ["progress"],
    r"\b(requirements?|manpower requirements?|sales plans?|prod plans?|production plans?|fn01|fn02)\b": ["requirements", "line_requirements"],
    r"\b(who is|profile of|employee profile|person details?|user details?)\b": ["users"],
    r"\b(users?|employees?|staff|workers?|operators?|workforce|persons?|roster)\b": ["users"],
}


def _match_domain_tables(text: str) -> list[str]:
    """Scan query text against DOMAIN_KEYWORD_MAP to identify deterministic tables."""
    if not text:
        return []
    matched: list[str] = []
    for pattern, tables in DOMAIN_KEYWORD_MAP.items():
        if re.search(pattern, text, re.IGNORECASE):
            for t in tables:
                if t in TABLE_NAMES and t not in matched:
                    matched.append(t)
    return matched


# -----------------------------------------------------------------------------
# Generic utilities
# -----------------------------------------------------------------------------
def serialize_sql_value(val: Any) -> Any:
    """Convert MSSQL values into JSON/string-safe Python values."""
    if isinstance(val, (datetime, date, time)):
        return val.isoformat()

    if isinstance(val, decimal.Decimal):
        return float(val) if val % 1 != 0 else int(val)

    if isinstance(val, bytes):
        return val.hex()

    return val


def _normalise_content(content: Any) -> str:
    """Best-effort conversion of LangChain/dict message content to plain text."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                if isinstance(item.get("text"), str):
                    parts.append(item["text"])
                elif isinstance(item.get("content"), str):
                    parts.append(item["content"])
            else:
                parts.append(str(item))
        return " ".join(p for p in parts if p).strip()
    return str(content).strip()


def _message_role_and_text(message: Any) -> tuple[str, str]:
    """Support LangChain BaseMessage objects, dictionaries, tuples and strings."""
    if isinstance(message, dict):
        role = str(message.get("role") or message.get("type") or "message")
        content = message.get("content", message.get("text", ""))
        return role, _normalise_content(content)

    if isinstance(message, (tuple, list)) and len(message) >= 2:
        return str(message[0]), _normalise_content(message[1])

    role = getattr(message, "type", None) or getattr(message, "role", None)
    content = getattr(message, "content", None)
    if role is not None or content is not None:
        return str(role or "message"), _normalise_content(content)

    return "message", _normalise_content(message)


def build_conversation_context(state: AgentState, max_messages: int = 10) -> str:
    """Read conversation history without mutating AgentState."""
    question = str(state.get("question") or "").strip()

    history_obj = None
    for key in ("messages", "conversation_history", "chat_history", "history"):
        value = state.get(key)
        if value:
            history_obj = value
            break

    lines: list[str] = []

    if isinstance(history_obj, str):
        text_history = history_obj.strip()
        if text_history:
            lines.append(text_history)
    elif isinstance(history_obj, Iterable) and not isinstance(history_obj, (bytes, bytearray, dict)):
        parsed: list[tuple[str, str]] = []
        for item in list(history_obj)[-max_messages:]:
            role, content = _message_role_and_text(item)
            if not content:
                continue
            parsed.append((role, content))

        removed_current = False
        for role, content in reversed(parsed):
            if not removed_current and question and content.strip() == question:
                removed_current = True
                continue
            lines.append(f"{role}: {content}")
        lines.reverse()

    optional_fields = (
        ("previous_question", "previous_user"),
        ("last_question", "previous_user"),
        ("previous_answer", "previous_assistant"),
        ("last_answer", "previous_assistant"),
        ("previous_sql_query", "previous_sql"),
        ("last_sql_query", "previous_sql"),
    )
    for key, label in optional_fields:
        value = state.get(key)
        if value:
            rendered = _normalise_content(value)
            if rendered and all(rendered not in existing for existing in lines):
                lines.append(f"{label}: {rendered}")

    context = "\n".join(lines).strip()

    if not context:
        session_id = state.get("session_id") or state.get("sessionId")
        if session_id:
            try:
                with engine.connect() as connection:
                    result = connection.execute(
                        text(
                            "SELECT TOP 10 sender, message_text, sql_executed, created_at "
                            "FROM AIChatMessage "
                            "WHERE session_id = :session_id "
                            "ORDER BY created_at DESC, id DESC"
                        ),
                        {"session_id": str(session_id)},
                    )
                    history_rows = list(reversed(result.fetchall()))

                db_lines = []
                skipped_current = False
                for row in history_rows:
                    mapping = dict(row._mapping)
                    message_text = _normalise_content(mapping.get("message_text"))
                    sender = _normalise_content(mapping.get("sender")) or "message"
                    if (
                        not skipped_current
                        and question
                        and message_text.strip() == question
                        and sender.lower() in {"user", "human"}
                    ):
                        skipped_current = True
                        continue
                    if message_text:
                        db_lines.append(f"{sender}: {message_text}")
                    if mapping.get("sql_executed"):
                        db_lines.append(f"sql: {_normalise_content(mapping['sql_executed'])}")
                context = "\n".join(db_lines).strip()
            except Exception as exc:
                print(f"History lookup skipped: {exc}")

    if not context:
        return "No prior conversation context available."

    return context[-8000:]


def _tables_from_llm_output(raw_text: str) -> list[str]:
    """Parse and whitelist table names against physical TABLE_NAMES."""
    candidates = []
    tokens = re.split(r"[,\s\n]+", raw_text)
    for token in tokens:
        cleaned = re.sub(r"[^a-zA-Z0-9_]", "", token.strip())
        if cleaned and cleaned in TABLE_NAMES and cleaned not in candidates:
            candidates.append(cleaned)
    return candidates


# -----------------------------------------------------------------------------
# LangGraph nodes
# -----------------------------------------------------------------------------
def select_tables_node(state: AgentState) -> dict:
    """Stage 1: dynamic table routing combining greeting guard, fast-path keywords, ChromaDB semantic vector retrieval (k=7), and LLM Table Selector."""
    question = str(state.get("question") or "").strip()

    # Step 0: Greeting & Chitchat Interception Guardrail
    if GREETING_PATTERN.match(question):
        return {
            "selected_tables": [],
            "schema_context": "",
            "sql_query": "",
            "query_result": [],
            "error": None,
            "final_answer": "Hello! I am your database assistant. You can ask me any question about employees, courses, machines, quizzes, attendance, or requirements.",
        }

    conversation_context = build_conversation_context(state)
    extracted_tables: list[str] = []

    # 1. Fast-path domain keyword match
    keyword_tables = _match_domain_tables(question)
    for t in keyword_tables:
        if t in TABLE_NAMES and t not in extracted_tables:
            extracted_tables.append(t)

    # 2. ChromaDB semantic vector search: ALWAYS retrieve semantic companion tables
    try:
        search_query = question
        docs = schema_retriever.invoke(search_query)
        for doc in docs:
            t_name = doc.metadata.get("table_name")
            if t_name and t_name in TABLE_NAMES and t_name not in extracted_tables:
                extracted_tables.append(t_name)
    except Exception as exc:
        print(f"ChromaDB retrieval error: {exc}")

    # 3. LLM Table Selector only if tables are still 0
    if len(extracted_tables) == 0:
        try:
            chain = TABLE_SELECTOR_PROMPT | llm
            response = chain.invoke({
                "catalog": COMPACT_TABLE_CATALOG,
                "conversation_context": conversation_context,
                "question": question,
            })
            llm_tables = _tables_from_llm_output(response.content.strip())
            for t in llm_tables:
                if t in TABLE_NAMES and t not in extracted_tables:
                    extracted_tables.append(t)
        except Exception as exc:
            print(f"LLM Table Selector error: {exc}")

    # 4. Fallback to general search across conversation context if still empty
    if not extracted_tables:
        combined_text = f"{conversation_context}\n{question}"
        for t in _match_domain_tables(combined_text):
            if t in TABLE_NAMES and t not in extracted_tables:
                extracted_tables.append(t)

    # Allow up to 6 relational tables so multi-table joins (e.g. section_heads -> sections -> users)
    # are never truncated before reaching the prompt
    final_tables = extracted_tables[:6]

    schema_info = get_table_schema_context(final_tables) if final_tables else ""

    return {
        "selected_tables": final_tables,
        "schema_context": schema_info,
    }


def _inject_top(sql: str, limit_num: int | str) -> str:
    """Inject TOP <limit_num> immediately after SELECT / SELECT DISTINCT if not already present."""
    if re.search(r"^\s*(?:WITH\s+[\s\S]+?\s+)?SELECT\s+(?:DISTINCT\s+|ALL\s+)?TOP\s+", sql, re.IGNORECASE):
        return sql

    pattern = r"^(\s*(?:WITH\s+[\s\S]+?\s+)?SELECT\s+(?:DISTINCT\s+|ALL\s+)?)"
    if re.match(pattern, sql, re.IGNORECASE):
        return re.sub(pattern, rf"\g<1>TOP {limit_num} ", sql, count=1, flags=re.IGNORECASE)
    return sql


def extract_clean_sql(raw_text: str) -> str:
    """Extract executable T-SQL only; strip markdown or trailing commentary and repair misplaced TOP/LIMIT."""
    fenced = re.search(r"```(?:sql)?\s*([\s\S]+?)```", raw_text, re.IGNORECASE)
    if fenced:
        candidate = fenced.group(1).strip()
    else:
        select_match = re.search(r"((?:WITH\s+[\s\S]+?\s+)?SELECT\s+[\s\S]+)", raw_text, re.IGNORECASE)
        candidate = select_match.group(1).strip() if select_match else raw_text.strip()

    lines = candidate.splitlines()
    valid_lines: list[str] = []
    for line in lines:
        lowered = line.strip().lower()
        if lowered.startswith(("```", "this query", "note:", "explanation:")):
            break
        valid_lines.append(line)

    clean_sql = "\n".join(valid_lines).strip().rstrip(";")

    # 1. Repair misplaced/trailing TOP N
    trailing_top = re.search(r"\s+TOP\s+\(?(\d+)\)?\s*$", clean_sql, re.IGNORECASE)
    if trailing_top:
        limit_num = trailing_top.group(1)
        clean_sql = re.sub(r"\s+TOP\s+\(?\d+\)?\s*$", "", clean_sql, flags=re.IGNORECASE).strip()
        clean_sql = _inject_top(clean_sql, limit_num)

    # 2. Repair trailing LIMIT N / LIMIT N OFFSET M
    trailing_limit = re.search(r"\s+LIMIT\s+(\d+)\s*(?:OFFSET\s+\d+)?\s*$", clean_sql, re.IGNORECASE)
    if trailing_limit:
        limit_num = trailing_limit.group(1)
        clean_sql = re.sub(r"\s+LIMIT\s+\d+\s*(?:OFFSET\s+\d+)?\s*$", "", clean_sql, flags=re.IGNORECASE).strip()
        clean_sql = _inject_top(clean_sql, limit_num)

    return clean_sql


def _build_diagnostic_error_message(raw_error: str, schema_context: str) -> str:
    """Format and enrich SQL Server errors with actionable repair rules for the LLM retry stage."""
    if not raw_error or raw_error.strip().lower() in ("none", ""):
        return "None"

    err_str = str(raw_error)

    # 1. SQL Server Error 8120: Column is invalid in select list (GROUP BY / Aggregate violation)
    if "8120" in err_str or "is not contained in either an aggregate function or the GROUP BY clause" in err_str:
        col_match = re.search(r"Column\s+'([^']+)'\s+is invalid", err_str, re.IGNORECASE)
        col_hint = f" Offending column: '{col_match.group(1)}'." if col_match else ""
        return (
            f"DIAGNOSTIC ERROR (SQL Server 8120 - Aggregate / GROUP BY Violation):\n{err_str}\n\n"
            f"REPAIR INSTRUCTION:{col_hint}\n"
            "- Wrap the offending column in SUM() (or COUNT(), AVG(), MAX(), MIN()), "
            "OR add all non-aggregated columns in the SELECT list to an explicit GROUP BY clause.\n"
            "- If computing both actual counts/totals and target requirements, aggregate both (e.g., `COUNT(DISTINCT u.id) AS actual, SUM(lr.quantity) AS required`) "
            "or use separate subqueries/CTEs.\n"
            "- NEVER leave a bare column in the SELECT list alongside aggregate functions without GROUP BY."
        )

    # 2. SQL Server Error 207: Invalid column name
    if "207" in err_str or "Invalid column name" in err_str:
        col_match = re.search(r"Invalid column name\s+'([^']+)'", err_str, re.IGNORECASE)
        col_name = col_match.group(1) if col_match else "unknown"

        special_hints = []
        if col_name.lower() in ("name", "user_name", "fullname") and "users" in (schema_context or "").lower():
            special_hints.append("- CRITICAL: In table 'users', use 'fullName' or 'userName'. Column 'name' does NOT exist in users.")

        valid_cols_summary = []
        for line in (schema_context or "").splitlines():
            if line.startswith("Columns:") or line.startswith("Table:") or line.startswith("Primary Key:") or line.startswith("Foreign Keys:"):
                valid_cols_summary.append(line)
        valid_cols_text = "\n".join(valid_cols_summary) if valid_cols_summary else schema_context
        hints_text = ("\n" + "\n".join(special_hints)) if special_hints else ""

        return (
            f"DIAGNOSTIC ERROR (SQL Server 207 - Invalid Column Name '{col_name}'):\n{err_str}\n\n"
            f"REPAIR INSTRUCTION:{hints_text}\n"
            f"- Column '{col_name}' does NOT exist in the physical database schema.\n"
            "- You MUST choose and pick ONLY from the exact list of valid columns from {schema_context} below:\n"
            f"{valid_cols_text}\n"
            "- Respect exact naming and casing (e.g. camelCase vs snake_case like requirementId, salesPlan, prodPlan, headCount, lineId, empId). "
            "Do NOT guess or assume standard naming conventions."
        )

    # 3. SQL Server Error 245: Conversion failed when converting varchar/nvarchar to int/date
    if "245" in err_str or "Conversion failed" in err_str:
        return (
            f"DIAGNOSTIC ERROR (SQL Server 245 - Data Type Conversion Failure):\n{err_str}\n\n"
            "REPAIR INSTRUCTION:\n"
            "- Incompatible data types were joined or compared (e.g. comparing NVARCHAR with INT).\n"
            "- Explicitly cast in the join condition or filter: `ON a.quiz = CAST(q.id AS NVARCHAR)` or `ON CAST(t.departmentId AS INT) = d.id`."
        )

    # 4. SQL Server Error 102: Incorrect syntax
    if "102" in err_str or "Incorrect syntax near" in err_str:
        return (
            f"DIAGNOSTIC ERROR (SQL Server 102 - T-SQL Syntax Error):\n{err_str}\n\n"
            "REPAIR INSTRUCTION:\n"
            "- Ensure valid Microsoft SQL Server (T-SQL) syntax.\n"
            "- Place `TOP <N>` directly after `SELECT` or `SELECT DISTINCT`.\n"
            "- Do NOT use `LIMIT` or place `TOP` at the end of the query."
        )

    # 5. SQL Server Error 208: Invalid object name
    if "208" in err_str or "Invalid object name" in err_str:
        tbl_match = re.search(r"Invalid object name\s+'([^']+)'", err_str, re.IGNORECASE)
        tbl_name = tbl_match.group(1) if tbl_match else "unknown"

        valid_tables = []
        for line in (schema_context or "").splitlines():
            if line.startswith("Table:"):
                valid_tables.append(line.replace("Table:", "").strip())
        valid_tables_text = ", ".join(valid_tables) if valid_tables else "tables provided in schema context"

        return (
            f"DIAGNOSTIC ERROR (SQL Server 208 - Invalid Table Name '{tbl_name}'):\n{err_str}\n\n"
            f"REPAIR INSTRUCTION:\n"
            f"- Table '{tbl_name}' does NOT exist in the physical database schema.\n"
            f"- You MUST select and query ONLY from the valid tables in PHYSICAL SCHEMA CONTEXT: {valid_tables_text}.\n"
            "- Do NOT invent, guess, or query table names outside the provided schema context."
        )

    # 6. SQL Server Error 4104: The multi-part identifier could not be bound
    if "4104" in err_str or "multi-part identifier" in err_str:
        alias_match = re.search(r'multi-part identifier "([^"]+)" could not be bound', err_str, re.IGNORECASE)
        alias_hint = f" Identifier: '{alias_match.group(1)}'." if alias_match else ""
        return (
            f"DIAGNOSTIC ERROR (SQL Server 4104 - Undeclared Table Alias):{alias_hint}\n{err_str}\n\n"
            "REPAIR INSTRUCTION:\n"
            "- A column prefix / alias was used without being declared on the table in the FROM or JOIN clause.\n"
            "- You MUST declare the alias on the table (e.g. `FROM requirements r`, `FROM users u`) or omit the alias prefix."
        )

    # 7. Template Placeholder Leak Error
    if "placeholder" in err_str.lower():
        return (
            f"DIAGNOSTIC ERROR (Unresolved Template Placeholder):\n{err_str}\n\n"
            "REPAIR INSTRUCTION:\n"
            "- Do NOT output placeholder tokens enclosed in angle brackets like '<search_term>', '<token>', or '<column>'.\n"
            "- Extract the literal value or entity name directly from the user's question (e.g., 'shivam') and embed it in the SQL filter."
        )

    return f"PREVIOUS SQL ERROR:\n{err_str}\n\nREPAIR INSTRUCTION:\nAnalyze the error above and regenerate a valid T-SQL query strictly using the provided physical schema context."


def generate_sql_node(state: AgentState) -> dict:
    """Stage 2: generate T-SQL from the selected live schema + conversation history with intelligent error self-correction."""
    # Fast exit if greeting was answered
    if state.get("final_answer") and not state.get("selected_tables"):
        return {"sql_query": ""}

    try:
        conversation_context = build_conversation_context(state)
        raw_error = state.get("error") or "None"
        schema_ctx = state.get("schema_context") or ""
        error_context = _build_diagnostic_error_message(raw_error, schema_ctx)

        chain = SQL_GENERATOR_PROMPT | llm
        response = chain.invoke({
            "schema_context": schema_ctx,
            "conversation_context": conversation_context,
            "question": state["question"],
            "error": error_context,
        })

        sql = extract_clean_sql(response.content.strip())
        if not sql:
            return {
                "sql_query": "",
                "error": "SQL generator returned an empty query.",
            }

        # Guardrail: Check for raw template placeholder leakage
        placeholder_match = re.search(r"<([a-zA-Z_]+)>", sql)
        if placeholder_match:
            leaked_token = placeholder_match.group(0)
            return {
                "sql_query": "",
                "error": (
                    f"Prompt placeholder leak detected: '{leaked_token}'. "
                    "You MUST replace all template placeholders with actual values or search terms extracted from the user question."
                ),
            }

        return {"sql_query": sql}
    except Exception as exc:
        print(f"Error in generate_sql_node: {exc}")
        return {
            "sql_query": "",
            "error": f"SQL generation failed: {exc}",
        }


def _preflight_mssql_select(connection, query: str) -> None:
    """Preflight check using sp_describe_first_result_set."""
    result = connection.execute(
        text("EXEC sys.sp_describe_first_result_set @tsql = :stmt"),
        {"stmt": query},
    )
    try:
        result.fetchall()
    except Exception:
        pass


def execute_sql_node(state: AgentState) -> dict:
    """Stage 3: security validation, MSSQL compile preflight, then SELECT execution."""
    if state.get("final_answer") and not state.get("selected_tables"):
        return {"query_result": []}

    query = (state.get("sql_query") or "").strip()
    if not query:
        return {
            "error": state.get("error") or "No SQL query generated.",
            "query_result": None,
            "retry_count": state.get("retry_count", 0) + 1,
        }

    is_valid, validated_or_err = sanitize_and_validate_sql(query)
    if not is_valid:
        return {
            "error": validated_or_err,
            "query_result": None,
            "retry_count": state.get("retry_count", 0) + 1,
        }

    try:
        with engine.connect() as connection:
            _preflight_mssql_select(connection, validated_or_err)
            result = connection.execute(text(validated_or_err))
            raw_rows = result.fetchall()

            rows = [
                {key: serialize_sql_value(value) for key, value in dict(row._mapping).items()}
                for row in raw_rows[:50]
            ]

            return {
                "query_result": rows,
                "error": None,
                "sql_query": validated_or_err,
            }
    except Exception as exc:
        return {
            "error": f"SQL validation/execution failed: {exc}",
            "query_result": None,
            "retry_count": state.get("retry_count", 0) + 1,
        }


def _md_escape(value: Any) -> str:
    if value is None:
        return "-"
    return str(value).replace("|", "\\|").replace("\n", " ")


def _is_employee_result(rows: list[dict]) -> bool:
    if not rows:
        return False
    keys = set(rows[0].keys())
    return bool({"fullName", "empId"} & keys) and "id" in keys


def _format_employee_result(rows: list[dict]) -> str:
    """Deterministically render employee lists."""
    status_counts = Counter(str(row.get("status") or "UNKNOWN") for row in rows)
    status_summary = ", ".join(f"{k}: {v}" for k, v in sorted(status_counts.items()))

    lines = [
        f"**Employees shown:** {len(rows)}",
    ]
    if status_summary:
        lines.append(f"**Status:** {status_summary}")

    lines.extend([
        "",
        "| # | Emp ID | Full Name | User Name | Department | Designation | Status |",
        "|---:|---|---|---|---|---|---|",
    ])

    for index, row in enumerate(rows, start=1):
        lines.append(
            "| {idx} | {emp} | {name} | {user} | {dept} | {desig} | {status} |".format(
                idx=index,
                emp=_md_escape(row.get("empId")),
                name=_md_escape(row.get("fullName")),
                user=_md_escape(row.get("userName")),
                dept=_md_escape(row.get("department")),
                desig=_md_escape(row.get("designation")),
                status=_md_escape(row.get("status")),
            )
        )

    return "\n".join(lines)


def _is_contractor_result(rows: list[dict]) -> bool:
    if not rows:
        return False
    keys = set(rows[0].keys())
    return "name" in keys and not bool({"fullName", "empId"} & keys) and bool({"location", "phoneNumber", "email"} & keys)


def _format_contractor_result(rows: list[dict]) -> str:
    """Deterministically render contractor lists."""
    lines = [
        f"**Total Contractors:** {len(rows)}",
        "",
        "| # | Contractor Name | Location | Phone Number | Email | Status |",
        "|---:|---|---|---|---|---|",
    ]

    for index, row in enumerate(rows, start=1):
        lines.append(
            "| {idx} | {name} | {loc} | {phone} | {email} | {status} |".format(
                idx=index,
                name=_md_escape(row.get("name")),
                loc=_md_escape(row.get("location")),
                phone=_md_escape(row.get("phoneNumber")),
                email=_md_escape(row.get("email")),
                status=_md_escape(row.get("status")),
            )
        )

    return "\n".join(lines)


def _format_generic_table(rows: list[dict]) -> str:
    """Deterministically render any list of tabular records as a clean Markdown table."""
    if not rows:
        return "No matching records were found in the database."

    first_row = rows[0]
    excluded_patterns = {"password", "refreshtoken", "resetpasswordtoken", "password_hash", "salt"}
    columns = [
        k for k in first_row.keys()
        if not any(pat in k.lower() for pat in excluded_patterns)
    ]
    if not columns:
        columns = list(first_row.keys())

    columns = columns[:15]

    lines = [
        f"**Total Records:** {len(rows)}",
        "",
        "| # | " + " | ".join(col.replace("_", " ").title() for col in columns) + " |",
        "|---:|" + "|".join("---" for _ in columns) + "|",
    ]

    for index, row in enumerate(rows, start=1):
        row_vals = [_md_escape(row.get(col)) for col in columns]
        lines.append(f"| {index} | " + " | ".join(row_vals) + " |")

    return "\n".join(lines)


def format_response_node(state: AgentState) -> dict:
    """
    Stage 4: Ultra-fast deterministic formatting.
    Eliminates redundant LLM formatter round-trips to prevent 90s request timeouts.
    """
    # 1. Agar greeting ya early guardrail answer pehle hi set hai
    if state.get("final_answer"):
        return {"final_answer": state["final_answer"]}

    # 2. Agar execution/validation error aaya hai
    if state.get("error") and state.get("query_result") is None:
        return {
            "final_answer": (
                "Sorry, the database query could not be completed after validation/retry. "
                f"Error: {state['error']}"
            )
        }

    query_res = state.get("query_result")

    # 3. Empty result set
    if query_res is not None and len(query_res) == 0:
        return {"final_answer": "No matching records were found in the database."}

    # 4. Fast path: Single scalar aggregate (COUNT, SUM, AVG, TOTAL, etc.)
    if isinstance(query_res, list) and len(query_res) == 1:
        row = query_res[0]
        if isinstance(row, dict) and len(row) == 1:
            key, value = next(iter(row.items()))
            clean_key = str(key).strip().lower()
            if (
                any(term in clean_key for term in ("count", "total", "sum", "avg", "actual", "required"))
                or isinstance(value, (int, float, decimal.Decimal))
                or clean_key == ""
            ):
                metric_label = "Total Count" if "count" in clean_key or clean_key == "" else clean_key.replace("_", " ").title()
                return {
                    "final_answer": f"**{metric_label}:** {value}\n\nMatching records result is **{value}**."
                }

    # 5. Deterministic Employee profile / list format
    if isinstance(query_res, list) and _is_employee_result(query_res):
        return {"final_answer": _format_employee_result(query_res)}

    # 6. Deterministic Contractor list format
    if isinstance(query_res, list) and _is_contractor_result(query_res):
        return {"final_answer": _format_contractor_result(query_res)}

    # 7. Generic tabular Markdown rendering (All 80+ tables ke liye direct & fast)
    if isinstance(query_res, list) and len(query_res) > 0 and isinstance(query_res[0], dict):
        return {"final_answer": _format_generic_table(query_res)}

    # 8. Fallback for non-dict or raw scalar shapes (Zero LLM latency)
    if isinstance(query_res, list):
        return {"final_answer": f"Query returned {len(query_res)} record(s):\n\n" + str(query_res)}

    return {"final_answer": str(query_res) if query_res is not None else "Query executed successfully."}

def should_retry_router(state: AgentState) -> str:
    """Allow at most two repair attempts after the original generation."""
    if state.get("final_answer") and not state.get("selected_tables"):
        return "format"
    if state.get("error") and state.get("retry_count", 0) <= 2:
        return "retry"
    return "format"