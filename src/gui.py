import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt
import retriever

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Chatbot")
        self.setGeometry(300, 200, 500, 400)

        layout = QVBoxLayout()
 
        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        layout.addWidget(self.chat_box)

        bottom_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message...")
        self.input_box.returnPressed.connect(self.send_message)
        bottom_layout.addWidget(self.input_box)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        bottom_layout.addWidget(send_button)

        layout.addLayout(bottom_layout)
        self.setLayout(layout)

    def send_message(self):
        user_text = self.input_box.text().strip()
        if not user_text:
            return

        self.chat_box.append(f"<b>You:</b> {user_text}")

        bot_reply = retriever.process_retrieval(user_text)
        self.chat_box.append(bot_reply)

        self.input_box.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())
