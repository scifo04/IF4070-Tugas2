import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QFrame
)
from PyQt5.QtCore import Qt, QPoint
import retriever

class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setFixedHeight(40)
        self.setStyleSheet("background-color: #000000; border-top-left-radius:15px; border-top-right-radius:15px;")

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)

        self.title = QLabel("STEI Course Chatbot")
        self.title.setStyleSheet("color: white; font-size: 16px; font-family: 'Segoe UI';")
        layout.addWidget(self.title)

        layout.addStretch()

        # Minimize button
        self.min_btn = QLabel("—")
        self.min_btn.setStyleSheet("color: white; font-size: 20px; padding: 5px;")
        self.min_btn.mousePressEvent = self.minimize
        layout.addWidget(self.min_btn)

        # Close button
        self.close_btn = QLabel("×")
        self.close_btn.setStyleSheet("color: white; font-size: 20px; padding: 5px;")
        self.close_btn.mousePressEvent = self.close_window
        layout.addWidget(self.close_btn)

        self.setLayout(layout)
        self.old_pos = None

    def minimize(self, event):
        self.parent.showMinimized()

    def close_window(self, event):
        self.parent.close()

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
            self.old_pos = event.globalPos()


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Remove native title bar → custom title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        # White rounded border around entire window
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border: 3px solid white;
                border-radius: 15px;
                font-family: 'Segoe UI';
                color: white;
            }
            QTextEdit {
                background-color: #121212;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #2a2a2a;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3a3a3a;
                border-radius: 10px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)

        # Fullscreen
        self.showFullScreen()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Custom black title bar
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Content frame
        content = QFrame()
        content.setStyleSheet("background-color: #1e1e1e; border-radius: 0px;")
        content_layout = QVBoxLayout()

        # Chat box
        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        content_layout.addWidget(self.chat_box)

        # Input row
        bottom_layout = QHBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message...")
        self.input_box.returnPressed.connect(self.send_message)
        bottom_layout.addWidget(self.input_box)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        bottom_layout.addWidget(send_button)

        content_layout.addLayout(bottom_layout)
        content.setLayout(content_layout)

        main_layout.addWidget(content)
        self.setLayout(main_layout)

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
