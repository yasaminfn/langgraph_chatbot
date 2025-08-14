# AI Q&A Chatbot (FastAPI + LangGraph + Streamlit)

A simple yet robust NLP-powered Q&A chatbot. Backend is built with **FastAPI** and **LangGraph/LangChain** using **OpenAI** models; responses can be **streamed in real time**. The bot can call external tools like **Tavily** web search to enrich answers. All user and assistant messages are stored in **PostgreSQL** in a human-readable table for later analysis; LangGraph’s internal state is checkpointed in Postgres separately.

## Features
-  **Async, streaming responses** via FastAPI (`/stream`)
-  **LangGraph/LangChain agent** with tool-calling (e.g., **TavilySearch**)
-  **Persistent chat history** in PostgreSQL (`chat_history` table, human-readable)
-  **Session management** using `thread_id` to keep conversation context
-  **Extensible tools**: easily add more tools alongside Tavily
-  **Streamlit UI** for a minimal web frontend
-  [![Chatbot.png](https://i.postimg.cc/Rhk4Qvkj/Chatbot.png)](https://postimg.cc/rRNBq2FJ)

## Tech Stack

- **Backend:** FastAPI, LangGraph/LangChain
- **Frontend:** Streamlit
- **Database:** PostgreSQL
- **Environment:** Python 3.11+, dotenv for configuration

## Project Structure
```
project_root/
├─ src/
│  ├─ api/
│  │  ├─ main.py          # FastAPI app entry
│  │  ├─ routes.py        # API routes/endpoints
│  │  └─ schemas.py       # Pydantic models (e.g., Question)
│  │
│  ├─ app/
│  │  └─ app.py           # Streamlit frontend
│  │
│  ├─ db/
│  │  ├─ connection.py    # async Postgres connection
│  │  └─ crud.py          # create_chat_history_table, save_message_to_db
│  │
│  ├─ tools/
│  │  └─ tools.py         # Tavily tool wrapper (@tool safe_tavily)
│  │
│  ├─ logs/
│  │  ├─ app.log          # Agent/app logs
│  │  └─ api.log          # API logs
│  │
│  ├─ graph.py            # LangGraph agent + tool binding
│  └─ __init__.py         # (optional)
│
├─ README.md
├─ requirements.txt
├─ .env (Not Commited)
├─ env.example (Example for .env file)
└─ .gitignore
```
## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL database
- `.env` file with:
```env
  DATABASE_URL=postgresql://username:password@localhost:5432/dbname
  TAVILY_API_KEY=your_api_key_here
  OPENAI_API_KEY=your_openai_key_here
````

### Installation

#### Create virtual environment
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

#### Install dependencies
```bash
pip install -r requirements.txt
```

### Running the Project

#### Backend (FastAPI)

```bash
uvicorn src.api.main:app --reload
```
Endpoints:

**POST /ask → non-streaming JSON response**

**POST /stream → streaming (text/plain)**

#### Frontend (Streamlit)

```bash
streamlit run src/app/app.py
```

### Usage

* Open the Streamlit frontend.
* Type your question in the input box.
* Receive real-time streamed answers.
* All questions and responses are saved in the database.

## Database

The project automatically creates a `chat_history` table in PostgreSQL:

```sql
CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    session_id UUID,
    role VARCHAR(20),
    content TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

* Messages are stored with `role` as either `user` or `assistant`.
* `session_id` links all messages for a single conversation.

## Logging

* Backend logs are saved in `src/logs/api.log`.
* Agent logs are saved in `src/logs/app.log`.


## License

MIT License
