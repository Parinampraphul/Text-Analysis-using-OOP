import tkinter as tk
from tkinter import messagebox

from .api_client import HuggingFaceClient
from .app import TextAnalysisApp
from .config import load_config
from .database import DatabaseConnectionError, UserRepository


def main() -> None:
    config = load_config()
    root = tk.Tk()
    try:
        users = UserRepository(config.sql_server.connection_string())
    except DatabaseConnectionError as exc:
        messagebox.showerror("Database Connection Error", str(exc))
        root.destroy()
        return

    api_client = HuggingFaceClient(
        token=config.hugging_face.token,
        sentiment_model=config.hugging_face.sentiment_model,
        ner_model=config.hugging_face.ner_model,
        sarcasm_model=config.hugging_face.sarcasm_model,
        abuse_model=config.hugging_face.abuse_model,
    )
    app = TextAnalysisApp(root, users, api_client)
    app.root.mainloop()


if __name__ == "__main__":
    main()
