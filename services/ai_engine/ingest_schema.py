# services/ai_engine/ingest_schema.py
import re
import os
import shutil
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from services.ai_engine.catalog import TABLE_CATALOG, TABLE_METADATA, TABLE_NAMES
from core.config import settings

PERSIST_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "chroma_db"))

def parse_catalog_to_documents(catalog_text: str) -> list[Document]:
    """
    Parses physical schema catalog and combines it with 100% English semantic metadata
    (purpose, business synonyms/topics, key columns, join intents, and DDL) for each table.
    """
    blocks = re.split(r"={10,}\s*\nTABLE:\s*", catalog_text)
    ddl_by_table: dict[str, str] = {}

    for block in blocks:
        block = block.strip()
        if not block or block.startswith("FME / Furukawa"):
            continue

        lines = block.splitlines()
        table_name = lines[0].strip()
        ddl_by_table[table_name] = block

    documents = []
    # Saari tables ka union lein (Metadata + Whitelist + DDL)
    all_tables = sorted(set(TABLE_METADATA.keys()) | set(TABLE_NAMES) | set(ddl_by_table.keys()))

    for table_name in all_tables:
        meta = TABLE_METADATA.get(table_name, {})
        purpose = meta.get("purpose", f"Physical database table storing operational records for {table_name}.")
        synonyms = meta.get("synonyms", table_name.replace("_", " "))
        key_cols = meta.get("key_columns", "")
        raw_ddl = ddl_by_table.get(table_name, "")

        # YAHI ASLI FIX HAI:
        # Technical DDL ke sath high-density English context embed ho raha hai
        doc_text = (
            f"TABLE NAME: {table_name}\n"
            f"OPERATIONAL BUSINESS PURPOSE & JOIN INTENT: {purpose}\n"
            f"BUSINESS TOPICS & SEARCH QUERIES: {synonyms}\n"
            f"PRIMARY AND FOREIGN KEY COLUMNS: {key_cols}\n"
            f"PHYSICAL DDL SCHEMA:\n{raw_ddl}"
        )

        doc = Document(
            page_content=doc_text,
            metadata={
                "table_name": table_name,
                "purpose": purpose,
                "synonyms": synonyms,
            }
        )
        documents.append(doc)

    return documents

def build_vector_store():
    # 1. Purani biased ya corrupted ChromaDB directory ko delete karein
    if os.path.exists(PERSIST_DIRECTORY):
        print(f"Purani vector database clean ho rahi hai: '{PERSIST_DIRECTORY}'...")
        try:
            shutil.rmtree(PERSIST_DIRECTORY)
            print("Purani ChromaDB directory successfully delete ho gayi.")
        except Exception as e:
            print(f"Warning: Purani directory delete nahi ho saki: {e}")

    # 2. Semantic documents banayein
    print("TABLE_CATALOG aur TABLE_METADATA ko rich English semantic chunks mein parse kiya ja raha hai...")
    docs = parse_catalog_to_documents(TABLE_CATALOG)
    print(f"Total {len(docs)} tables successfully prepare hui embedding ke liye.")

    # 3. Ollama nomic-embed-text initialize karein
    embeddings = OllamaEmbeddings(
        base_url=settings.OLLAMA_BASE_URL,
        model="nomic-embed-text"
    )

    # 4. Fresh vector store persist karein
    print(f"Fresh ChromaDB banai ja rahi hai '{PERSIST_DIRECTORY}' mein...")
    vector_db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name="fme_schema_catalog"
    )
    print("SUCCESS: Vector database 100% English semantic metadata ke sath successfully build aur persist ho chuki hai!")

if __name__ == "__main__":
    build_vector_store()