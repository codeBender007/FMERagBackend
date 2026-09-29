# db/schema_inspector.py
from typing import List, Set
from sqlalchemy import inspect
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

COLUMN_ANNOTATIONS = {
    "users": {
        "fullName": "fullName (NVARCHAR) [Employee Name - NOTE: users table has NO 'name' column, use fullName/userName]",
        "userName": "userName (NVARCHAR) [Username / System Login]",
        "empId": "empId (NVARCHAR) [Employee ID / Code]",
    },
    "ten_cycle_sheets": {
        "createdBy": "createdBy (NVARCHAR) [Author / Person who filled the sheet]",
        "status": "status (NVARCHAR) [Allowed values: 'Draft', 'Submitted']",
    },
    "ten_cycle_checks": {
        "createdBy": "createdBy (VARCHAR) [Author / Person who filled the check]",
    },
    "daily_5m_records": {
        "submittedBy": "submittedBy (INTEGER) [Person who inspected / submitted 5M]",
        "createdBy": "createdBy (NVARCHAR) [Person who created / recorded 5M]",
    },
    "abnormal_condition_sheets": {
        "updatedBy": "updatedBy (NVARCHAR) [Person who reported / updated abnormality]",
    },
    "handover_sheets": {
        "createdBy": "createdBy (NVARCHAR) [Shift leader who filled handover sheet]",
    },
    "section_heads": {
        "sectionId": "sectionId (INTEGER) [FK -> sections.id]",
        "name": "name (NVARCHAR) [Section Head Name]",
        "email": "email (NVARCHAR) [Section Head Email Address]",
    },
}


def get_table_schema_context(table_names: List[str]) -> str:
    """
    Given a list of table names, dynamically inspects columns, data types,
    primary keys, and foreign keys directly from MSSQL.
    Filters security/blob noise and annotates critical domain columns.
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
            # 1. Extract Columns & Types (filtering noise)
            columns = inspector.get_columns(table)
            cols_desc = []
            table_ann = COLUMN_ANNOTATIONS.get(table, {})

            for col in columns:
                cname = col["name"]
                if cname.lower() in EXCLUDED_COLUMNS:
                    continue
                if cname in table_ann:
                    cols_desc.append(table_ann[cname])
                else:
                    cols_desc.append(f"{cname} ({str(col['type'])})")

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