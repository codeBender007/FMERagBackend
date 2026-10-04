import os

import re

import decimal

from datetime import date, datetime, time

from collections import Counter

from typing import Any, Iterable



from sqlalchemy import inspect, text

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



# Initialize ChromaDB schema catalog vector store & retriever (k=6 for authoritative semantic retrieval)

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

schema_retriever = vector_db.as_retriever(search_kwargs={"k": 6})



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

def _dedupe_valid_tables(candidates: Iterable[str]) -> list[str]:
    """Return unique physical table names while preserving order."""
    result: list[str] = []
    for table_name in candidates:
        if table_name in TABLE_NAMES and table_name not in result:
            result.append(table_name)
    return result


def _looks_like_entity_query(question: str) -> bool:
    """Detect person/entity lookup intent without depending on schema table names."""
    if not question:
        return False

    intent_keywords = {
        "who", "whom", "belong", "employee", "operator", "worker", "user",
        "staff", "trainer", "designation", "profile", "contact", "email",
        "empid", "fullname", "attendance", "kaun", "person", "member",
        "phone", "mobile", "details", "detail",
    }
    tokens = {
        token.lower()
        for token in re.findall(r"[A-Za-z][A-Za-z0-9_]*", question)
    }
    if tokens & intent_keywords:
        return True

    # Proper noun heuristic such as "Amit Sharma". This is intentionally
    # schema-agnostic and only influences retrieval recall/prioritisation.
    return bool(
        re.search(
            r"\b[A-Z][a-zA-Z'\-]+(?:\s+[A-Z][a-zA-Z'\-]+)+\b",
            question,
        )
    )


def _table_metadata_blob(table_name: str) -> str:
    """Render catalog metadata into searchable text regardless of metadata shape."""
    meta = TABLE_METADATA.get(table_name, {}) if isinstance(TABLE_METADATA, dict) else {}
    if isinstance(meta, dict):
        parts: list[str] = [table_name]
        for key, value in meta.items():
            parts.append(str(key))
            if isinstance(value, (list, tuple, set)):
                parts.extend(str(item) for item in value)
            elif isinstance(value, dict):
                parts.extend(f"{k} {v}" for k, v in value.items())
            else:
                parts.append(str(value))
        return " ".join(parts).lower()
    return f"{table_name} {meta}".lower()


def _entity_master_priority(table_name: str) -> int:
    """
    Rank tables likely to contain primary entity/person records using catalog
    metadata only. Lower scores are preferred. No physical table name is baked
    into the routing logic.
    """
    blob = _table_metadata_blob(table_name)
    strong_terms = (
        "fullname", "full name", "employee id", "empid", "user name",
        "username", "designation", "email", "phone", "mobile", "profile",
    )
    weak_terms = ("employee", "operator", "worker", "staff", "person", "user")

    strong_hits = sum(term in blob for term in strong_terms)
    weak_hits = sum(term in blob for term in weak_terms)

    if strong_hits:
        return 0
    if weak_hits:
        return 1
    return 2


def select_tables_node(state: AgentState) -> dict:
    """
    Stage 1: dynamic table routing.

    ChromaDB (k=6) remains the primary selector. For entity/person questions we
    perform an additional high-recall semantic query and prioritise tables using
    catalog metadata rather than hard-coded physical table names. Existing
    keyword and LLM selectors remain fallbacks when vector retrieval is empty.
    """
    question = str(state.get("question") or "").strip()

    if GREETING_PATTERN.match(question):
        final_tables: list[str] = []
        print(f"[DEBUG select_tables_node] Question: {question}")
        print(f"[DEBUG select_tables_node] Final tables sent to LLM: {final_tables}")
        return {
            "selected_tables": [],
            "schema_context": "",
            "sql_query": "",
            "query_result": [],
            "error": None,
            "final_answer": (
                "Hello! I am your database assistant. You can ask me questions "
                "about the information available in the database."
            ),
        }

    conversation_context = build_conversation_context(state)
    extracted_tables: list[str] = []
    entity_intent = _looks_like_entity_query(question)

    # Primary selector: semantic retrieval. The retriever is globally fixed at k=6.
    retrieval_queries = [question]
    if entity_intent:
        retrieval_queries.append(
            "person employee operator staff profile identity full name employee id "
            "contact designation affiliation department section line " + question
        )

    try:
        for search_query in retrieval_queries:
            docs = schema_retriever.invoke(search_query)
            for doc in docs:
                table_name = doc.metadata.get("table_name") or doc.metadata.get("table")
                if table_name and table_name in TABLE_NAMES and table_name not in extracted_tables:
                    extracted_tables.append(table_name)
    except Exception as exc:
        print(f"[WARN select_tables_node] ChromaDB retrieval error: {exc}")

    # Existing deterministic domain fallback, only when vector retrieval is empty.
    if not extracted_tables:
        extracted_tables.extend(_match_domain_tables(question))

    # Existing LLM table-selector fallback, only when still empty.
    if not extracted_tables:
        try:
            chain = TABLE_SELECTOR_PROMPT | llm
            response = chain.invoke({
                "catalog": COMPACT_TABLE_CATALOG,
                "conversation_context": conversation_context,
                "question": question,
            })
            extracted_tables.extend(_tables_from_llm_output(response.content.strip()))
        except Exception as exc:
            print(f"[WARN select_tables_node] LLM table selector error: {exc}")

    # Existing conversation-context fallback.
    if not extracted_tables:
        combined_text = f"{conversation_context}\n{question}"
        extracted_tables.extend(_match_domain_tables(combined_text))

    extracted_tables = _dedupe_valid_tables(extracted_tables)

    # For entity queries, place likely master/entity tables before supporting
    # lookup/activity tables so the strict cap does not discard the core entity.
    if entity_intent and extracted_tables:
        indexed = list(enumerate(extracted_tables))
        indexed.sort(key=lambda item: (_entity_master_priority(item[1]), item[0]))
        extracted_tables = [table_name for _, table_name in indexed]

    # Final physical-table whitelist and strict safety cap.
    final_tables = [t for t in extracted_tables if t in TABLE_NAMES][:5]

    print(f"[DEBUG select_tables_node] Question: {question}")
    print(f"[DEBUG select_tables_node] Final tables sent to LLM: {final_tables}")

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
    """
    Extract one executable T-SQL SELECT/CTE statement from model output.

    Removes Markdown fences, leading/trailing prose, trailing semicolons and
    common non-T-SQL LIMIT syntax. It does not rewrite joins or schema names.
    """
    text_value = _normalise_content(raw_text).strip()
    if not text_value:
        return ""

    # Prefer the first fenced SQL/code block when present.
    fenced = re.search(r"```(?:sql|tsql)?\s*([\s\S]*?)```", text_value, re.IGNORECASE)
    candidate = fenced.group(1).strip() if fenced else text_value

    # Remove any remaining fence markers.
    candidate = re.sub(r"^```(?:sql|tsql)?\s*", "", candidate, flags=re.IGNORECASE).strip()
    candidate = re.sub(r"\s*```$", "", candidate).strip()

    # Ignore conversational text before the first WITH/SELECT token.
    statement_match = re.search(r"\b(WITH|SELECT)\b[\s\S]*", candidate, re.IGNORECASE)
    if statement_match:
        candidate = statement_match.group(0).strip()

    # Stop at common prose markers that appear after the query on a new line.
    prose_marker = re.search(
        r"\n\s*(?:explanation|note|reason|why|this query|the query|result)\s*:\s*",
        candidate,
        re.IGNORECASE,
    )
    if prose_marker:
        candidate = candidate[:prose_marker.start()].strip()

    # Remove a final Markdown fence/prose-free semicolon sequence.
    candidate = candidate.rstrip().rstrip(";").strip()

    # Repair a trailing TOP n emitted in the wrong location.
    trailing_top = re.search(r"\s+TOP\s+\(?(\d+)\)?\s*$", candidate, re.IGNORECASE)
    if trailing_top:
        limit_num = trailing_top.group(1)
        candidate = re.sub(
            r"\s+TOP\s+\(?\d+\)?\s*$",
            "",
            candidate,
            flags=re.IGNORECASE,
        ).strip()
        candidate = _inject_top(candidate, limit_num)

    # Convert the common accidental LIMIT n suffix to SQL Server TOP n.
    trailing_limit = re.search(
        r"\s+LIMIT\s+(\d+)\s*(?:OFFSET\s+\d+)?\s*$",
        candidate,
        re.IGNORECASE,
    )
    if trailing_limit:
        limit_num = trailing_limit.group(1)
        candidate = re.sub(
            r"\s+LIMIT\s+\d+\s*(?:OFFSET\s+\d+)?\s*$",
            "",
            candidate,
            flags=re.IGNORECASE,
        ).strip()
        candidate = _inject_top(candidate, limit_num)

    return candidate.rstrip().rstrip(";").strip()


def _build_schema_adherence_rules(schema_context: str) -> str:
    """Append generic, table-agnostic SQL Server join/type rules to live schema."""
    rules = """
GENERIC T-SQL SCHEMA-ADHERENCE RULES (MANDATORY):
- Treat the PHYSICAL SCHEMA CONTEXT as authoritative. Inspect the exact data type of every column used in SELECT, WHERE, JOIN, GROUP BY, ORDER BY and aggregate expressions.
- Prefer explicit foreign-key relationships shown in the schema. When a descriptor column and a numeric foreign-key column both exist, use the numeric foreign key only when the schema proves that relationship.
- NEVER compare or JOIN VARCHAR/NVARCHAR/CHAR/NCHAR text directly to INT/BIGINT/SMALLINT/TINYINT numeric identifiers.
- Do not CAST or TRY_CAST arbitrary descriptive text to an integer merely to force a JOIN to succeed.
- If the requested human-readable descriptor is already stored in the primary table, select it directly instead of adding an unnecessary lookup JOIN.
- If a schema-approved relationship joins two numeric identifiers, compare them directly without converting them to text.
- If two textual columns must be matched by value and no numeric foreign key exists, normalize both text expressions, for example:
  LOWER(LTRIM(RTRIM(CAST(t1.col AS NVARCHAR(255))))) = LOWER(LTRIM(RTRIM(CAST(t2.col AS NVARCHAR(255)))))
- Never invent columns, foreign keys, relationships, or table names that are absent from the supplied physical schema context.
- Generate Microsoft SQL Server T-SQL only. Use TOP instead of LIMIT.
""".strip()
    base = (schema_context or "").rstrip()
    return f"{base}\n\n{rules}" if base else rules


def _is_sqlserver_error_245(error_text: str) -> bool:
    """Return True for SQL Server conversion/type-mismatch error 245."""
    lowered = (error_text or "").lower()
    return (
        "245" in lowered
        or "conversion failed when converting" in lowered
        or "error 245" in lowered
    )


def _normalise_identifier(identifier: str) -> str:
    """Remove T-SQL identifier quoting while preserving the actual name."""
    value = (identifier or "").strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return value.strip()


def _sql_type_family(type_name: str) -> str:
    """Map SQL Server/SQLAlchemy type strings to broad comparison families."""
    value = (type_name or "").lower()
    if any(token in value for token in ("char", "text", "string", "unicode")):
        return "text"
    if any(token in value for token in (
        "bigint", "smallint", "tinyint", "integer", "int", "numeric",
        "decimal", "float", "real", "money", "smallmoney",
    )):
        return "numeric"
    if any(token in value for token in ("date", "time", "datetime")):
        return "datetime"
    if "uniqueidentifier" in value or "uuid" in value:
        return "uuid"
    if "bit" in value or "boolean" in value:
        return "boolean"
    if "binary" in value or "image" in value:
        return "binary"
    return "other"


def _get_live_column_types(table_names: Iterable[str]) -> dict[str, dict[str, str]]:
    """
    Read authoritative column types directly from SQL Server through SQLAlchemy.

    The lookup is entirely table-agnostic: only the currently selected physical
    tables are inspected, and no relationship/table/column name is assumed.
    """
    result: dict[str, dict[str, str]] = {}
    try:
        inspector = inspect(engine)
        for table_name in _dedupe_valid_tables(table_names):
            try:
                columns = inspector.get_columns(table_name)
            except Exception as exc:
                print(
                    "[WARN type_precheck] Could not inspect table "
                    f"{table_name}: {type(exc).__name__}: {exc}"
                )
                continue

            result[table_name.lower()] = {
                str(column.get("name") or "").lower(): str(column.get("type") or "")
                for column in columns
                if column.get("name")
            }
    except Exception as exc:
        print(f"[WARN type_precheck] SQLAlchemy inspector unavailable: {type(exc).__name__}: {exc}")
    return result


def _render_live_column_type_context(table_names: Iterable[str]) -> str:
    """Render authoritative live SQL Server column types for the selected tables."""
    type_map = _get_live_column_types(table_names)
    if not type_map:
        return ""

    lines = ["LIVE SQL SERVER COLUMN TYPES (AUTHORITATIVE):"]
    for table_name in _dedupe_valid_tables(table_names):
        columns = type_map.get(table_name.lower())
        if not columns:
            continue
        rendered = ", ".join(f"{column}: {type_name}" for column, type_name in columns.items())
        lines.append(f"Table {table_name}: {rendered}")
    return "\n".join(lines)


def _extract_sql_alias_map(sql: str) -> dict[str, str]:
    """
    Resolve FROM/JOIN aliases to physical selected table names.

    Supports common T-SQL forms such as:
      FROM table t
      FROM [table] AS t
      JOIN dbo.table AS t
      JOIN [dbo].[table] t
    """
    alias_map: dict[str, str] = {}
    pattern = re.compile(
        r"\b(?:FROM|JOIN)\s+"
        r"(?:(?:\[?[A-Za-z_][A-Za-z0-9_]*\]?)[.])?"
        r"(?P<table>\[?[A-Za-z_][A-Za-z0-9_]*\]?)"
        r"(?:\s+(?:AS\s+)?(?P<alias>\[?[A-Za-z_][A-Za-z0-9_]*\]?))?",
        re.IGNORECASE,
    )
    reserved = {
        "on", "where", "join", "inner", "left", "right", "full", "cross",
        "outer", "group", "order", "having", "union", "except", "intersect",
    }

    for match in pattern.finditer(sql or ""):
        table_name = _normalise_identifier(match.group("table"))
        alias_raw = _normalise_identifier(match.group("alias") or "")
        alias = alias_raw if alias_raw and alias_raw.lower() not in reserved else table_name
        alias_map[alias.lower()] = table_name
        alias_map.setdefault(table_name.lower(), table_name)

    return alias_map


def _find_incompatible_column_comparisons(
    sql: str,
    table_names: Iterable[str],
) -> list[dict[str, str]]:
    """
    Detect column-to-column equality predicates with incompatible live types.

    This is intentionally generic. It does not rewrite SQL and does not know
    anything about domain tables. It simply resolves aliases, reads live column
    types, and flags text<->numeric comparisons before SQL Server executes them.
    """
    alias_map = _extract_sql_alias_map(sql)
    if not alias_map:
        return []

    type_map = _get_live_column_types(table_names)
    if not type_map:
        return []

    comparison_pattern = re.compile(
        r"(?P<a1>\[?[A-Za-z_][A-Za-z0-9_]*\]?)\."
        r"(?P<c1>\[?[A-Za-z_][A-Za-z0-9_]*\]?)\s*=\s*"
        r"(?P<a2>\[?[A-Za-z_][A-Za-z0-9_]*\]?)\."
        r"(?P<c2>\[?[A-Za-z_][A-Za-z0-9_]*\]?)",
        re.IGNORECASE,
    )

    mismatches: list[dict[str, str]] = []
    for match in comparison_pattern.finditer(sql or ""):
        alias1 = _normalise_identifier(match.group("a1"))
        alias2 = _normalise_identifier(match.group("a2"))
        col1 = _normalise_identifier(match.group("c1"))
        col2 = _normalise_identifier(match.group("c2"))
        table1 = alias_map.get(alias1.lower())
        table2 = alias_map.get(alias2.lower())
        if not table1 or not table2:
            continue

        type1 = type_map.get(table1.lower(), {}).get(col1.lower())
        type2 = type_map.get(table2.lower(), {}).get(col2.lower())
        if not type1 or not type2:
            continue

        family1 = _sql_type_family(type1)
        family2 = _sql_type_family(type2)
        incompatible = {family1, family2} == {"text", "numeric"}
        if not incompatible:
            continue

        mismatches.append({
            "left_expression": f"{alias1}.{col1}",
            "left_table": table1,
            "left_column": col1,
            "left_type": type1,
            "right_expression": f"{alias2}.{col2}",
            "right_table": table2,
            "right_column": col2,
            "right_type": type2,
            "predicate": match.group(0),
        })

    return mismatches


def _format_type_mismatch_precheck(mismatches: list[dict[str, str]]) -> str:
    """Create a strong, machine-readable-enough reflection error for retries."""
    lines = [
        "TYPE-SAFETY PRECHECK FAILED: incompatible column data types were compared.",
        "The following predicates MUST NOT be reused unchanged:",
    ]
    for item in mismatches:
        lines.append(
            "- "
            f"{item['left_expression']} ({item['left_table']}.{item['left_column']} : {item['left_type']}) "
            "= "
            f"{item['right_expression']} ({item['right_table']}.{item['right_column']} : {item['right_type']})"
        )
    lines.extend([
        "Re-read the physical schema and choose only a schema-proven compatible relationship.",
        "Prefer an explicit foreign key when one exists. If the requested descriptor is already present in the primary table, select it directly and remove the unnecessary JOIN.",
        "Do not CAST descriptive text to an integer merely to preserve the failed relationship.",
    ])
    return "\n".join(lines)


def _build_type_repair_prompt(
    *,
    question: str,
    schema_context: str,
    conversation_context: str,
    previous_sql: str,
    error_context: str,
) -> str:
    """Dedicated reflection prompt for type/conversion failures."""
    return f"""
You are repairing a Microsoft SQL Server T-SQL SELECT query after a proven data-type failure.

USER QUESTION:
{question}

PHYSICAL SCHEMA CONTEXT (AUTHORITATIVE):
{schema_context}

CONVERSATION CONTEXT:
{conversation_context}

PREVIOUS FAILING SQL:
{previous_sql}

FAILURE / TYPE ANALYSIS:
{error_context}

MANDATORY REPAIR RULES:
1. Produce a materially corrected query; do NOT repeat any predicate explicitly identified as incompatible.
2. Inspect the exact physical column data types and explicit foreign-key relationships in the schema context.
3. NEVER compare or JOIN a VARCHAR/NVARCHAR/CHAR/NCHAR column directly with INT/BIGINT/SMALLINT/TINYINT/DECIMAL/NUMERIC.
4. NEVER cast arbitrary descriptive text to a numeric identifier just to make the failed join execute.
5. If the answer is already stored as a descriptive column in the primary entity table, select that column directly and remove the unnecessary lookup JOIN.
6. Otherwise, use only a schema-proven relationship whose operand types are compatible.
7. If a relationship is genuinely textual, normalize BOTH sides as text with LOWER/LTRIM/RTRIM and NVARCHAR casting.
8. Use Microsoft SQL Server syntax only. Use TOP instead of LIMIT.
9. Return ONLY the corrected executable SQL. No markdown fences. No explanation.
""".strip()


def _build_diagnostic_error_message(
    raw_error: str,
    schema_context: str,
    previous_sql: str = "",
) -> str:
    """Build table-agnostic repair context for the SQL regeneration attempt."""
    if not raw_error or raw_error.strip().lower() in {"none", ""}:
        return "None"

    err_str = str(raw_error).strip()
    failed_sql = extract_clean_sql(previous_sql) if previous_sql else ""
    failed_sql_block = f"\n\nPREVIOUS FAILING SQL:\n{failed_sql}" if failed_sql else ""

    if _is_sqlserver_error_245(err_str):
        return (
            "T-SQL ERROR 245 - DATA TYPE MISMATCH / CONVERSION FAILURE\n"
            f"DATABASE ERROR:\n{err_str}"
            f"{failed_sql_block}\n\n"
            "TARGETED REFLECTION INSTRUCTION:\n"
            "Your previous query failed with T-SQL Error 245 (data type mismatch). "
            "You attempted to compare, join, filter, or implicitly convert incompatible data types. "
            "Re-examine the exact DDL/schema types supplied in PHYSICAL SCHEMA CONTEXT. "
            "Use the real numeric foreign-key relationship when the schema defines one, or select an existing descriptive text column directly when no lookup join is needed. "
            "Never cast arbitrary VARCHAR/NVARCHAR descriptive values to INT/BIGINT to force compatibility. "
            "If the correct relationship is genuinely textual, normalize both text operands using NVARCHAR and trimming/case normalization. "
            "Return ONLY the corrected Microsoft SQL Server T-SQL query."
        )

    if "8120" in err_str or "is not contained in either an aggregate function or the group by clause" in err_str.lower():
        return (
            "T-SQL ERROR 8120 - AGGREGATE / GROUP BY VIOLATION\n"
            f"DATABASE ERROR:\n{err_str}"
            f"{failed_sql_block}\n\n"
            "REPAIR INSTRUCTION:\n"
            "Every selected non-aggregate expression must appear in GROUP BY, or the expression must be aggregated. "
            "Re-check the supplied physical schema and return ONLY corrected T-SQL."
        )

    if "207" in err_str or "invalid column name" in err_str.lower():
        return (
            "T-SQL ERROR 207 - INVALID COLUMN\n"
            f"DATABASE ERROR:\n{err_str}"
            f"{failed_sql_block}\n\n"
            "REPAIR INSTRUCTION:\n"
            "Use only exact column names present in PHYSICAL SCHEMA CONTEXT. Do not infer or invent conventional names. "
            "Return ONLY corrected T-SQL."
        )

    if "208" in err_str or "invalid object name" in err_str.lower():
        return (
            "T-SQL ERROR 208 - INVALID TABLE/OBJECT\n"
            f"DATABASE ERROR:\n{err_str}"
            f"{failed_sql_block}\n\n"
            "REPAIR INSTRUCTION:\n"
            "Use only tables/objects present in PHYSICAL SCHEMA CONTEXT. Return ONLY corrected T-SQL."
        )

    if "4104" in err_str or "multi-part identifier" in err_str.lower():
        return (
            "T-SQL ERROR 4104 - INVALID/UNBOUND ALIAS\n"
            f"DATABASE ERROR:\n{err_str}"
            f"{failed_sql_block}\n\n"
            "REPAIR INSTRUCTION:\n"
            "Check aliases in FROM/JOIN clauses and all qualified column references. Return ONLY corrected T-SQL."
        )

    if "102" in err_str or "incorrect syntax near" in err_str.lower():
        return (
            "T-SQL ERROR 102 - SYNTAX ERROR\n"
            f"DATABASE ERROR:\n{err_str}"
            f"{failed_sql_block}\n\n"
            "REPAIR INSTRUCTION:\n"
            "Generate valid Microsoft SQL Server T-SQL. Use TOP rather than LIMIT and return ONLY corrected SQL."
        )

    if "placeholder" in err_str.lower():
        return (
            "UNRESOLVED TEMPLATE PLACEHOLDER\n"
            f"ERROR:\n{err_str}"
            f"{failed_sql_block}\n\n"
            "REPAIR INSTRUCTION:\n"
            "Replace template placeholders with literal values derived from the user's question and return ONLY corrected T-SQL."
        )

    return (
        "PREVIOUS SQL EXECUTION ERROR:\n"
        f"{err_str}"
        f"{failed_sql_block}\n\n"
        "REPAIR INSTRUCTION:\n"
        "Re-check the exact physical schema, column data types, aliases, joins and T-SQL syntax. "
        "Return ONLY a corrected Microsoft SQL Server SELECT/CTE query."
    )


def generate_sql_node(state: AgentState) -> dict:
    """
    Stage 2: generate schema-grounded T-SQL and regenerate after execution errors.

    Retry behavior is table-agnostic: the failed SQL and exact DB error are fed
    back to the same generator together with the live schema and generic type
    safety rules.
    """
    if state.get("final_answer") and not state.get("selected_tables"):
        return {"sql_query": ""}

    try:
        conversation_context = build_conversation_context(state)
        raw_error = str(state.get("error") or "None")
        previous_sql = str(state.get("sql_query") or "").strip()

        base_schema_ctx = str(state.get("schema_context") or "")
        live_type_ctx = _render_live_column_type_context(
            state.get("selected_tables") or []
        )
        combined_schema_ctx = (
            f"{base_schema_ctx}\n\n{live_type_ctx}".strip()
            if live_type_ctx
            else base_schema_ctx
        )
        schema_ctx = _build_schema_adherence_rules(combined_schema_ctx)
        error_context = _build_diagnostic_error_message(
            raw_error,
            schema_ctx,
            previous_sql=previous_sql,
        )

        print(
            "[DEBUG generate_sql_node] "
            f"retry_count={state.get('retry_count', 0)} "
            f"has_error={raw_error.lower() != 'none'}"
        )

        if raw_error.lower() != "none" and (
            _is_sqlserver_error_245(raw_error)
            or "type-safety precheck failed" in raw_error.lower()
        ):
            repair_prompt = _build_type_repair_prompt(
                question=str(state["question"]),
                schema_context=schema_ctx,
                conversation_context=conversation_context,
                previous_sql=previous_sql,
                error_context=error_context,
            )
            response = llm.invoke(repair_prompt)
        else:
            chain = SQL_GENERATOR_PROMPT | llm
            response = chain.invoke({
                "schema_context": schema_ctx,
                "conversation_context": conversation_context,
                "question": state["question"],
                "error": error_context,
            })

        sql = extract_clean_sql(response.content)
        if not sql:
            return {
                "sql_query": "",
                "error": "SQL generator returned an empty query.",
            }

        placeholder_match = re.search(r"<([a-zA-Z_][a-zA-Z0-9_]*)>", sql)
        if placeholder_match:
            leaked_token = placeholder_match.group(0)
            return {
                "sql_query": "",
                "error": (
                    f"Prompt placeholder leak detected: '{leaked_token}'. "
                    "Replace all placeholders with actual values from the user question."
                ),
            }

        generation_mismatches = _find_incompatible_column_comparisons(
            sql,
            state.get("selected_tables") or [],
        )
        if generation_mismatches:
            mismatch_error = _format_type_mismatch_precheck(generation_mismatches)
            print(f"[WARN generate_sql_node] {mismatch_error}")
            return {
                "sql_query": sql,
                "error": mismatch_error,
            }

        print(f"[DEBUG generate_sql_node] Generated SQL: {sql}")
        return {"sql_query": sql, "error": None}

    except Exception as exc:
        print(f"[ERROR generate_sql_node] {type(exc).__name__}: {exc}")
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
    """
    Stage 3: validate, preflight and execute read-only T-SQL.

    Any SQL Server conversion/type mismatch is returned through the existing
    `error` field so LangGraph can route back to generate_sql_node. The failed
    SQL remains in `sql_query`, allowing the next generation step to reflect on
    the exact statement without changing AgentState or downstream signatures.
    """
    if state.get("final_answer") and not state.get("selected_tables"):
        return {"query_result": []}

    query = extract_clean_sql(str(state.get("sql_query") or ""))
    if not query:
        return {
            "error": state.get("error") or "No SQL query generated.",
            "query_result": None,
            "retry_count": state.get("retry_count", 0) + 1,
        }

    is_valid, validated_or_err = sanitize_and_validate_sql(query)
    if not is_valid:
        print(f"[WARN execute_sql_node] SQL validation failed: {validated_or_err}")
        return {
            "sql_query": query,
            "error": str(validated_or_err),
            "query_result": None,
            "retry_count": state.get("retry_count", 0) + 1,
        }

    validated_sql = extract_clean_sql(str(validated_or_err))

    type_mismatches = _find_incompatible_column_comparisons(
        validated_sql,
        state.get("selected_tables") or [],
    )
    if type_mismatches:
        mismatch_error = _format_type_mismatch_precheck(type_mismatches)
        print(f"[WARN execute_sql_node] {mismatch_error}")
        return {
            "sql_query": validated_sql,
            "error": mismatch_error,
            "query_result": None,
            "retry_count": state.get("retry_count", 0) + 1,
        }

    try:
        print(f"[DEBUG execute_sql_node] Executing SQL: {validated_sql}")
        with engine.connect() as connection:
            _preflight_mssql_select(connection, validated_sql)
            result = connection.execute(text(validated_sql))
            raw_rows = result.fetchall()

        rows = [
            {
                key: serialize_sql_value(value)
                for key, value in dict(row._mapping).items()
            }
            for row in raw_rows[:50]
        ]

        print(f"[DEBUG execute_sql_node] Rows returned: {len(rows)}")
        return {
            "query_result": rows,
            "error": None,
            "sql_query": validated_sql,
        }

    except Exception as exc:
        exact_error = str(exc)
        error_code = "245" if _is_sqlserver_error_245(exact_error) else "generic"
        print(
            "[ERROR execute_sql_node] "
            f"SQL Server error={error_code}; type={type(exc).__name__}; {exact_error}"
        )
        return {
            "sql_query": validated_sql,
            "error": f"SQL validation/execution failed: {exact_error}",
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