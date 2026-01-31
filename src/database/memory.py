from pathlib import Path
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()


def get_project_root() -> Path:
    """
    Returns the root directory of the project.
    memory.py is located at src/database/memory.py
    so parents[2] = project root.
    """
    return Path(__file__).resolve().parents[2]


def get_db_path() -> str:
    """
    Returns the SQLite DB path where memory is saved.
    Ensures /data folder exists.
    """
    root = get_project_root()
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)

    db_path = data_dir / "farmer_ai_memory.sqlite"
    return str(db_path)


def get_checkpointer() -> SqliteSaver:
    """
    Creates and returns LangGraph SqliteSaver checkpointer.
    LangGraph will store conversation state into SQLite automatically.
    """
    db_path = get_db_path()
    return SqliteSaver.from_conn_string(db_path)
