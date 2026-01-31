from src.database.memory import get_db_path, get_checkpointer


print("DB Path:", get_db_path())
cp = get_checkpointer()
print("Checkpointer:", type(cp))
print("Memory module is working")