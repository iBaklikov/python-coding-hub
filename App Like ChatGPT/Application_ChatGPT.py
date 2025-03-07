import sys
import json
import os
import openai
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt

# Constants
APP_TITLE = "LLM Chat"
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".llm_chat_config.json")

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Enter API Key:")
        layout.addWidget(self.label)

        self.api_key_entry = QLineEdit()
        self.api_key_entry.setEchoMode(QLineEdit.Password)  # Hide API key for security
        layout.addWidget(self.api_key_entry)

        self.check_button = QPushButton("Check API Key")
        self.check_button.clicked.connect(self.check_api_key)
        layout.addWidget(self.check_button)

        self.save_button = QPushButton("Save & Proceed")
        self.save_button.setEnabled(False)  # Disabled until API key is valid
        self.save_button.clicked.connect(self.save_and_proceed)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.api_key = self.load_api_key()
        if self.api_key:
            self.api_key_entry.setText(self.api_key)

    def load_api_key(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config.get("api_key", "")
        return ""

    def check_api_key(self):
        api_key = self.api_key_entry.text().strip()
        openai.api_key = api_key

        try:
            openai.Model.list()  # Test the API key with a simple request
            QMessageBox.information(self, "Success", "API key is valid!")
            self.save_button.setEnabled(True)
        except openai.error.AuthenticationError:
            QMessageBox.critical(self, "Error", "Invalid API key!")
            self.save_button.setEnabled(False)

    def save_and_proceed(self):
        api_key = self.api_key_entry.text().strip()
        with open(CONFIG_FILE, "w") as f:
            json.dump({"api_key": api_key}, f)

        QMessageBox.information(self, "Success", "API key saved successfully!")
        self.chat_screen = ChatScreen()  # Open chat screen
        self.chat_screen.show()
        self.close()  # Close login screen


class ChatScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Type your message...")
        layout.addWidget(self.user_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        self.setLayout(layout)
        self.api_key = self.load_api_key()
        if not self.api_key:
            QMessageBox.critical(self, "Error", "No API key found. Please restart and enter an API key.")
            self.close()

    def load_api_key(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config.get("api_key", "")
        return ""

    def send_message(self):
        user_text = self.user_input.text().strip()
        if not user_text:
            return

        self.chat_history.append(f"User: {user_text}")
        self.user_input.clear()

        openai.api_key = self.api_key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}],
            stream=True
        )

        ai_text = "AI: "
        self.chat_history.append(ai_text)

        for chunk in response:
            if "choices" in chunk and chunk["choices"]:
                delta = chunk["choices"][0].get("delta", {})
                if "content" in delta:
                    ai_text += delta["content"]
                    self.chat_history.setPlainText(self.chat_history.toPlainText() + delta["content"])

        self.chat_history.append("\n")  # Add spacing after AI response


if __name__ == "__main__":
    # app = QApplication(sys.argv)
    app = QApplication(D:\Users\u124935\OneDrive - Finance of America Holdings, LLC\Documents\_My Repos\PythonOOP\llm_chat_env\Lib\site-packages\PySide6\plugins\platforms
    if os.path.exists(CONFIG_FILE) and json.load(open(CONFIG_FILE)).get("api_key"):
        chat_screen = ChatScreen()
        chat_screen.show()
    else:
        login_screen = LoginScreen()
        login_screen.show()

    sys.exit(app.exec())
