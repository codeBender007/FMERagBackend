# Core Folder (`core/`)

Yeh folder pure application ka foundation aur security shield hai. Isme wo settings aur rules hain jo kisi ek route ya table ke liye nahi, balki pure system me globally use hote hain.

---

## Files Overview

### 1. `config.py` (Configuration Manager)
* **Kaam:** `.env` file se saare sensitive variables (Database name, Server IP, Ollama details, JWT secret) load karta hai.
* **Kyun zaroori hai:** Yeh Pydantic ke zariye check karta hai ki har variable ka datatype sahi hai ya nahi. Agar koi setting missing ya galat ho, to server runtime crash hone ke bajay turant error bata deta hai.
* **Fayda:** Pure project me bar-bar `os.getenv()` nahi likhna padta, direct `settings.DB_NAME` use hota hai.

---

### 2. `security.py` (Security Guard & Gatekeeper)
* **Kaam:** Is file ke 2 main kaam hain:
  1. **SQL Guardrail:** LLM jab bhi query banayega, yeh function check karega ki query strictly `SELECT` se shuru ho rahi hai ya nahi. Agar query me `DELETE`, `UPDATE`, `DROP`, ya `INSERT` jaisa koi keyword mila, to yeh usko database tak pahunchne se pehle hi block kar dega.
  2. **JWT Auth:** Admin ke login password ko verify karna aur secure JWT token generate/validate karna.
* **Kyun zaroori hai:** AI ko database ka access dete waqt data delete ya alter hone ka risk zero karne ke liye.

---

### 3. `__init__.py` (Package Marker)
* **Kaam:** Python ko batata hai ki `core` ek module hai.
* **Kyun zaroori hai:** Taaki pure project me clean imports ho sakein (e.g., `from core import settings, sanitize_and_validate_sql`).