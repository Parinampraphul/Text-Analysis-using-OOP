import json
import re
import tkinter as tk
from tkinter import messagebox, scrolledtext
from typing import Callable

from .api_client import TextAnalysisApiError
from .database import User, UserRepository


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class TextAnalysisApp:
    def __init__(self, root: tk.Tk, users: UserRepository, api_client: object) -> None:
        self.root = root
        self.users = users
        self.api_client = api_client
        self.current_user: User | None = None
        self.active_frame: tk.Frame | None = None

        self.root.title("Text Analysis using OOP")
        self.root.geometry("620x560")
        self.root.minsize(560, 500)
        self.root.configure(bg="#eef4f8")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.show_login_page()

    def show_login_page(self) -> None:
        frame = self._new_frame()
        tk.Label(frame, text="Login", font=("Segoe UI", 18, "bold")).pack(pady=(10, 20))

        self.login_email = self._entry(frame, "Email")
        self.login_password = self._entry(frame, "Password", show="*")

        tk.Button(frame, text="Login", width=22, command=self.login).pack(pady=(18, 8))
        tk.Button(frame, text="Create account", width=22, command=self.show_registration_page).pack()

    def show_registration_page(self) -> None:
        frame = self._new_frame()
        tk.Label(frame, text="Create Account", font=("Segoe UI", 18, "bold")).pack(pady=(10, 20))

        self.register_name = self._entry(frame, "Name")
        self.register_email = self._entry(frame, "Email")
        self.register_password = self._entry(frame, "Password", show="*")

        tk.Button(frame, text="Register", width=22, command=self.register).pack(pady=(18, 8))
        tk.Button(frame, text="Back to login", width=22, command=self.show_login_page).pack()

    def show_analysis_page(self) -> None:
        frame = self._new_frame()
        user_name = self.current_user.name if self.current_user else "User"
        tk.Label(frame, text=f"Welcome, {user_name}", font=("Segoe UI", 16, "bold")).pack(pady=(0, 12))

        tk.Label(frame, text="Enter text to analyze").pack(anchor="w")
        self.text_input = scrolledtext.ScrolledText(frame, height=8, wrap=tk.WORD)
        self.text_input.pack(fill=tk.BOTH, expand=False, pady=(4, 12))

        button_frame = tk.Frame(frame)
        button_frame.pack(fill=tk.X)

        actions: list[tuple[str, Callable[[], None]]] = [
            ("Sentiment", self.analyze_sentiment),
            ("NER", self.analyze_entities),
            ("Sarcasm", self.analyze_sarcasm),
            ("Abuse", self.analyze_abuse),
            ("Keywords", self.analyze_keywords),
        ]
        for index, (label, command) in enumerate(actions):
            tk.Button(button_frame, text=label, command=command).grid(
                row=0,
                column=index,
                padx=4,
                sticky="ew",
            )
            button_frame.columnconfigure(index, weight=1)

        tk.Label(frame, text="Result").pack(anchor="w", pady=(14, 4))
        self.result_output = scrolledtext.ScrolledText(frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.result_output.pack(fill=tk.BOTH, expand=True)

        tk.Button(frame, text="Log out", width=16, command=self.logout).pack(pady=(12, 0))

    def register(self) -> None:
        name = self.register_name.get().strip()
        email = self.register_email.get().strip().lower()
        password = self.register_password.get()

        if not name or not email or not password:
            messagebox.showerror("Registration Error", "Please fill in all fields.")
            return
        if not EMAIL_PATTERN.match(email):
            messagebox.showerror("Registration Error", "Please enter a valid email address.")
            return
        if len(password) < 6:
            messagebox.showerror("Registration Error", "Password must be at least 6 characters.")
            return
        if self.users.email_exists(email):
            messagebox.showerror("Registration Error", "This email is already registered.")
            return

        self.users.create_user(name, email, password)
        messagebox.showinfo("Registration Successful", "Account created. You can now log in.")
        self.show_login_page()

    def login(self) -> None:
        email = self.login_email.get().strip().lower()
        password = self.login_password.get()

        if not email or not password:
            messagebox.showerror("Login Error", "Please fill in all fields.")
            return

        user = self.users.authenticate(email, password)
        if user is None:
            messagebox.showerror("Login Error", "Invalid email or password.")
            return

        self.current_user = user
        self.show_analysis_page()

    def analyze_sentiment(self) -> None:
        self._run_analysis("Sentiment", self.api_client.sentiment)

    def analyze_entities(self) -> None:
        self._run_analysis("Named Entity Recognition", self.api_client.named_entities)

    def analyze_sarcasm(self) -> None:
        self._run_analysis("Sarcasm Detection", self.api_client.sarcasm)

    def analyze_abuse(self) -> None:
        self._run_analysis("Abuse Detection", self.api_client.abuse)

    def analyze_keywords(self) -> None:
        self._run_analysis("Keywords", self.api_client.keywords)

    def logout(self) -> None:
        self.current_user = None
        self.show_login_page()

    def close(self) -> None:
        self.users.close()
        self.root.destroy()

    def _run_analysis(self, title: str, analyzer: Callable[[str], dict]) -> None:
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Input Error", "Please enter text to analyze.")
            return

        try:
            result = analyzer(text)
        except TextAnalysisApiError as exc:
            messagebox.showerror("API Error", str(exc))
            return

        self._display_result(title, result)

    def _display_result(self, title: str, result: dict) -> None:
        formatted_result = json.dumps(result, indent=2)
        self.result_output.configure(state=tk.NORMAL)
        self.result_output.delete("1.0", tk.END)
        self.result_output.insert(tk.END, f"{title}\n\n{formatted_result}")
        self.result_output.configure(state=tk.DISABLED)

    def _new_frame(self) -> tk.Frame:
        if self.active_frame is not None:
            self.active_frame.destroy()

        frame = tk.Frame(self.root, bg="#eef4f8", padx=28, pady=24)
        frame.pack(fill=tk.BOTH, expand=True)
        self.active_frame = frame
        return frame

    def _entry(self, parent: tk.Frame, label: str, show: str | None = None) -> tk.Entry:
        tk.Label(parent, text=label, bg="#eef4f8").pack(anchor="w")
        entry = tk.Entry(parent, show=show, width=44)
        entry.pack(fill=tk.X, pady=(4, 12))
        return entry
