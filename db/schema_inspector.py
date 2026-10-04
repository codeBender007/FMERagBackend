# db/schema_inspector.py
from typing import List, Set, Dict, Tuple
from sqlalchemy import inspect, text
from db.connection import engine

EXCLUDED_COLUMNS: Set[str] = {
    "password",
    "refreshtoken",
    "resetpasswordtoken",
    "resetpasswordexpiry",
    "avatar",
    "loginhistory",
    "salt",
}

# Critical manual overrides for confusing columns
COLUMN_ANNOTATIONS = {
    "users": {
        "fullName": "fullName (NVARCHAR) [Employee Name - NOTE: users table has NO 'name' column, use fullName/userName]",
        "userName": "userName (NVARCHAR) [Username / System Login]",
        "empId": "empId (NVARCHAR) [Employee ID / Code]",
    },
    "ten_cycle_sheets": {
        "createdBy": "createdBy (NVARCHAR) [Author / Person who filled the sheet]",
    },
    "daily_5m_records": {
        "submittedBy": "submittedBy (INTEGER) [Person who inspected / submitted 5M]",
        "createdBy": "createdBy (NVARCHAR) [Person who created / recorded 5M]",
    },
    "section_heads": {
        "sectionId": "sectionId (INTEGER) [FK -> sections.id]",
    },
}

# Keywords to detect categorical/filter columns
CATEGORICAL_KEYWORDS = ("status", "department", "dept", "shift", "role", "category", "designation")

# In-memory cache: (table_name, column_name) -> "['val1', 'val2']"
_SAMPLE_VALUE_CACHE: Dict[Tuple[str, str], str] = {}


def _get_distinct_samples(table: str, col_name: str) -> str:
    """Fetch and cache top 3 distinct string values for categorical columns."""
    cache_key = (table, col_name)
    if cache_key in _SAMPLE_VALUE_CACHE:
        return _SAMPLE_VALUE_CACHE[cache_key]

    samples_str = ""
    # Check if column name matches categorical patterns
    if any(kw in col_name.lower() for kw in CATEGORICAL_KEYWORDS):
        try:
            query = text(
                f"SELECT DISTINCT TOP 3 CAST([{col_name}] AS NVARCHAR(100)) "
                f"FROM [{table}] "
                f"WHERE [{col_name}] IS NOT NULL AND CAST([{col_name}] AS NVARCHAR(100)) <> ''"
            )
            with engine.connect() as conn:
                results = conn.execute(query).fetchall()
                vals = [f"'{r[0]}'" for r in results if r[0] is not None]
                if vals:
                    samples_str = f" [Sample values: {', '.join(vals)}]"
        except Exception:
            # Query timeout or unsupported type - fail silently without breaking inspection
            samples_str = ""

    _SAMPLE_VALUE_CACHE[cache_key] = samples_str
    return samples_str


def get_table_schema_context(table_names: List[str]) -> str:
    """
    Dynamically inspects columns, data types, primary keys, foreign keys,
    and attaches top 3 distinct sample values for categorical columns.
    """
    if not table_names:
        return ""

    inspector = inspect(engine)
    all_db_tables = set(inspector.get_table_names())
    schema_parts = []

    for table in table_names:
        if table not in all_db_tables:
            continue
        try:
            # 1. Extract Columns & Types with Sample Values
            columns = inspector.get_columns(table)
            cols_desc = []
            table_ann = COLUMN_ANNOTATIONS.get(table, {})

            for col in columns:
                cname = col["name"]
                if cname.lower() in EXCLUDED_COLUMNS:
                    continue

                # Fetch distinct samples (cached)
                sample_note = _get_distinct_samples(table, cname)

                if cname in table_ann:
                    # Append sample values to existing annotation if present
                    cols_desc.append(f"{table_ann[cname]}{sample_note}")
                else:
                    cols_desc.append(f"{cname} ({str(col['type'])}){sample_note}")

            # 2. Extract Primary Key
            pk_data = inspector.get_pk_constraint(table)
            pk_cols = pk_data.get("constrained_columns", []) if pk_data else []

            # 3. Extract Foreign Keys
            fk_data = inspector.get_foreign_keys(table)
            fk_desc = []
            if fk_data:
                for fk in fk_data:
                    constrained = ", ".join(fk.get("constrained_columns", []))
                    ref_table = fk.get("referred_table", "")
                    ref_cols = ", ".join(fk.get("referred_columns", []))
                    if constrained and ref_table and ref_cols:
                        fk_desc.append(f"{constrained} -> {ref_table}({ref_cols})")

            # 4. Build Structured Context Block
            block_lines = [
                f"Table: {table}",
                f"Columns: {', '.join(cols_desc)}",
            ]
            if pk_cols:
                block_lines.append(f"Primary Key: {', '.join(pk_cols)}")
            if fk_desc:
                block_lines.append(f"Foreign Keys: {'; '.join(fk_desc)}")

            schema_parts.append("\n".join(block_lines))
        except Exception as exc:
            print(f"Error inspecting schema for table '{table}': {exc}")
            continue

    return "\n\n".join(schema_parts)