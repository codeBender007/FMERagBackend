# Database Layer (`db/`)

Yeh folder MSSQL database ke sath saare interactions, connection pooling aur table schema inspection ko manage karta hai.

---

## Files Overview

### 1. `connection.py` (Database Engine & Session)
* **Kaam:** SQLAlchemy aur `pyodbc` ke zariye local MSSQL server se connect karta hai.
* **Kyun zaroori hai:** FastAPI routes aur LangGraph nodes ko clean, auto-closing database sessions provide karta hai.

---

### 2. `models.py` (Chat History Tables)
* **Kaam:** Chatbot ke do zaroori tables define karta hai:
  * `AIChatSessions`: Sidebar me dikhne wali chat sessions ki list (Title, Session ID, User ID).
  * `AIChatMessages`: Har chat ke andar user ke sawal, bot ke answers aur execute hui SQL query.
* **Kyun zaroori hai:** User ki previous chat history maintain karne ke liye.

---

### 3. `schema_inspector.py` (Dynamic Schema Extractor)
* **Kaam:** Database ke tables ke columns aur data types ko runtime par read karke text format me badalta hai.
* **Kyun zaroori hai:** Local Ollama model ko batane ke liye ki table me kaun-kaun se columns exist karte hain, taaki query bilkul accurate bane.

---

### 4. `__init__.py` (Package Exporter)
* **Kaam:** Database module se `engine`, `get_db` aur models ko cleanly export karta hai.