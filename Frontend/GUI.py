# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from dotenv import dotenv_values
# import sys
# import os

# env_vars = dotenv_values(".env")
# Assistantname = env_vars.get("AssistantName", "Jarvis") # Added default just in case
# current_dir = os.getcwd()
# old_chat_message = ""
# TempDirPath = rf"{current_dir}\Frontend\Files"
# GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

# def AnswerModifier(Answer):
#     lines = Answer.split("\n")
#     non_empty_lines = [line for line in lines if line.strip()]
#     modified_answer = '\n'.join(non_empty_lines)
#     return modified_answer

# def QueryModifier(Query):
#     new_query = Query.lower().strip()
#     query_words = new_query.strip()
#     question_words = [
#         "how", "what", "why", "where", "which", "who",
#         "how's", "what's", "whom's", "may", "whose",
#         "could", "whom", "can you", "who's", "Is"
#     ]

#     if any(word + "" in new_query for word in question_words):
#         if query_words[-1][-1] in [".", "?", "!"]:
#             new_query = new_query[:-1] + "?"
#         else:
#             new_query += "?"
#     else:
#         if query_words[-1][-1] in [".", "?", "!"]:
#             new_query = new_query[:-1] + "."
#         else:
#             new_query += "."

#     return new_query.capitalize()

# def SetMicrophoneStatus(Command):
#     with open(rf"{TempDirPath}\Mic.data", "w", encoding="utf-8") as file:
#         file.write(Command)

# def GetMicrophoneStatus():
#     with open(rf"{TempDirPath}\Mic.data", "r", encoding="utf-8") as file:
#         Status = file.read()
#     return Status

# def SetAssistantStatus(Status):
#     with open(rf"{TempDirPath}\Status.data", "w", encoding="utf-8") as file:
#         file.write(Status)

# # Ensure directory exists before writing initial status
# if not os.path.exists(TempDirPath):
#     os.makedirs(TempDirPath)

# SetAssistantStatus("Speaking...")

# def GetAssistantStatus():
#     with open(rf"{TempDirPath}\Status.data", "r", encoding="utf-8") as file:
#         Status = file.read()
#     return Status

# def MicButtonInitialed():
#     SetMicrophoneStatus("False")

# def MicButtonClosed():
#     SetMicrophoneStatus("True")

# def GraphicsDirectoryPath(FileName):
#     Path = rf"{GraphicsDirPath}\{FileName}"
#     return Path

# def TempDirectoryPath(FileName):
#     Path = rf"{TempDirPath}\{FileName}"
#     return Path

# def ShowTextToScreen(Text):
#     with open(rf"{TempDirPath}\Responses.data", "w", encoding="utf-8") as file:
#         file.write(Text)

# class ChatSection(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.toggled = False
#         self.icon_label = QLabel(self)
#         layout = QVBoxLayout()
#         layout.setContentsMargins(-10, 40, 40, 100)
#         layout.setSpacing(-10)
        
#         self.chat_text_edit = QTextEdit()
#         self.chat_text_edit.setReadOnly(True)
#         self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
#         self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        
#         layout.addWidget(self.chat_text_edit)
        
#         self.setStyleSheet("background-color:grey;")
#         layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
#         layout.setStretch(1, 1)
#         self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        
#         text_color = QColor(Qt.blue)
#         text_color_text = QTextCharFormat()
#         text_color_text.setForeground(text_color)
#         self.chat_text_edit.setCurrentCharFormat(text_color_text)
        
#         self.gif_label = QLabel()
#         self.gif_label.setStyleSheet("border:none;")
#         movie = QMovie(GraphicsDirectoryPath('Jarvis.gif')) # Ensure this is a .gif if you want it to move, or .png is static
#         max_gif_size_W = 100
#         max_gif_size_H = 250
#         movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
#         self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
#         self.gif_label.setMovie(movie)
#         movie.start()
        
#         layout.addWidget(self.gif_label) # Added once here
        
#         self.label = QLabel("")
#         self.label.setStyleSheet("color:white; font-size:16px; margin-right:195px; border:none; margin-top:-30px")
#         self.label.setAlignment(Qt.AlignRight)
        
#         layout.addWidget(self.label)
#         layout.setSpacing(-10)
        
#         # --- FIX: REMOVED THE DUPLICATE GIF_LABEL ADDITION HERE ---
        
#         layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
#         self.setLayout(layout) # Ensure layout is set
        
#         self.load_icon(GraphicsDirectoryPath('Mic_off.png'))
#         self.icon_label.mousePressEvent = self.toggle_icon

#         font = QFont()
#         font.setPointSize(13)
#         self.chat_text_edit.setFont(font)
        
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(lambda: self.loadMessages())
#         self.timer.timeout.connect(self.SpeechRecogText)
#         self.timer.start(5)
        
#         self.setStyleSheet("""
#             QScrollBar:vertical{
#             border:none;
#             background: black;
#             width:10px;
#             margin 0px 0px 0px 0px;
#             }
#             QScrollBar::handle:vertical{
#             background:white;
#             min-height:20px;
#             }
#             QScrollBar::add-line:vertical{
#             background:black;
#             subcontrol-position:bottom;
#             subcontrol-origin:margin;
#             height:10px;
#             }
#             QScrollBar::sub-line:vertical{
#             background:black;
#             subcontrol-position:bottom;
#             subcontrol-origin:margin;
#             height:10px;
#             }
#             QScrollBar::up-arrow:vertical,QScrollBar::down-arrow:vertical{
#             border:none;
#             background:none;
#             color:none;
#             }
#             QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{
#             background:none;
#             }
#         """)

#     def loadMessages(self):
#         global old_chat_message
#         try:
#             with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
#                 messages = file.read()
            
#             if messages is None:
#                 pass
#             elif len(messages) <= 1:
#                 pass
#             elif str(old_chat_message) == str(messages):
#                 pass
#             else:
#                 self.addMessage(message=messages, color="White")
#                 old_chat_message = messages
#         except FileNotFoundError:
#             pass

#     def SpeechRecogText(self):
#         try:
#             with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
#                 messages = file.read()
#                 self.label.setText(messages)
#         except FileNotFoundError:
#             pass

#     def load_icon(self, path, width=60, height=60):
#         pixmap = QPixmap(path)
#         new_pixmap = pixmap.scaled(width, height)
#         self.icon_label.setPixmap(new_pixmap)

#     def toggle_icon(self, event=None):
#         if self.toggled:
#             self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
#             MicButtonInitialed()
#         else:
#             self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
#             MicButtonClosed()
#         self.toggled = not self.toggled

#     def addMessage(self, message, color):
#         cursor = self.chat_text_edit.textCursor()
#         format = QTextCharFormat()
#         formatm = QTextBlockFormat()
#         formatm.setTopMargin(10)
#         formatm.setLeftMargin(10)
#         format.setForeground(QColor(color))
#         cursor.setCharFormat(format)
#         cursor.setBlockFormat(formatm)
#         cursor.insertText(message + "\n")
#         self.chat_text_edit.setTextCursor(cursor)

# class InitialScreen(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         desktop = QApplication.desktop()
#         screen_width = desktop.screenGeometry().width()
#         screen_height = desktop.screenGeometry().height()
        
#         # --- FIX: Main Layout ---
#         content_layout = QVBoxLayout()
#         content_layout.setContentsMargins(0, 0, 0, 20) # Small bottom margin
#         content_layout.setAlignment(Qt.AlignCenter)
        
#         # --- GIF SETUP ---
#         gif_label = QLabel()
#         movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
#         gif_label.setMovie(movie)
        
#         # FIX: Make GIF smaller than screen (e.g., 85% width) to leave room for Mic
#         # The previous code made it 100% height, pushing mic off screen.
#         gif_width = int(screen_width * 0.45) 
#         gif_height = int(gif_width / 16 * 9)
        
#         movie.setScaledSize(QSize(gif_width, gif_height))
#         gif_label.setAlignment(Qt.AlignCenter)
#         movie.start()
        
#         # --- MIC SETUP ---
#         self.icon_label = QLabel()
#         self.icon_label.setFixedSize(100, 100) # Slightly larger for Home screen
#         self.icon_label.setAlignment(Qt.AlignCenter)
#         self.icon_label.setCursor(Qt.PointingHandCursor)
#         self.toggled = True
#         self.toggle_icon()
#         self.icon_label.mousePressEvent = self.toggle_icon
        
#         # --- LABEL SETUP ---
#         self.label = QLabel("")
#         self.label.setStyleSheet("color:White; font-size: 20px; font-weight: bold; margin-bottom: 10px;")
#         self.label.setAlignment(Qt.AlignCenter)

#         # --- ADDING TO LAYOUT ---
#         # Add Stretch at top to push everything to center
#         content_layout.addStretch()
#         content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
#         content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
#         content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
#         # Add Stretch at bottom
#         content_layout.addStretch()
        
#         self.setLayout(content_layout)
#         self.setFixedHeight(screen_height)
#         self.setFixedWidth(screen_width)
#         self.setStyleSheet("background-color:black;")
        
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.SpeechRecogText)
#         self.timer.start(5)

#     def SpeechRecogText(self):
#         try:
#             with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
#                 messages = file.read()
#                 self.label.setText(messages)
#         except FileNotFoundError:
#             pass

#     def load_icon(self, path, width=60, height=60):
#         pixmap = QPixmap(path)
#         new_pixmap = pixmap.scaled(width, height)
#         self.icon_label.setPixmap(new_pixmap)

#     def toggle_icon(self, event=None):
#         if self.toggled:
#             self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
#             MicButtonInitialed()
#         else:
#             self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
#             MicButtonClosed()
#         self.toggled = not self.toggled

# class MessageScreen(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         desktop = QApplication.desktop()
#         screen = QApplication.primaryScreen()
#         rect = screen.availableGeometry()
#         screen_width = rect.width()
#         screen_height = rect.height()
#         layout = QVBoxLayout()
#         label = QLabel("")
#         layout.addWidget(label)
#         chat_section = ChatSection()
#         layout.addWidget(chat_section)
#         self.setLayout(layout)
#         self.setStyleSheet("background-color:black;")
#         self.setFixedHeight(screen_height)
#         self.setFixedWidth(screen_width)

# class CustomTopBar(QWidget):
#     def __init__(self, parent, stacked_widget):
#         super().__init__(parent)
#         self.initUI()
#         self.current_screen = None
#         self.stacked_widget = stacked_widget

#     def initUI(self):
#         self.setFixedHeight(50)
#         layout = QHBoxLayout(self)
#         layout.setAlignment(Qt.AlignRight)
        
#         home_button = QPushButton()
#         home_icon = QIcon(GraphicsDirectoryPath('Home.png'))
#         home_button.setIcon(home_icon)
#         home_button.setText("Home")
#         home_button.setStyleSheet("height:40px;line_height:40px;background-color:white;color:black")
        
#         message_button = QPushButton()
#         message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
#         message_button.setIcon(message_icon)
#         message_button.setText("Chat")
#         message_button.setStyleSheet("background-color:white")
        
#         minimize_button = QPushButton()
#         minimize_icon = QIcon(GraphicsDirectoryPath('Minimize.png'))
#         minimize_button.setIcon(minimize_icon)
#         minimize_button.setStyleSheet("background-color:white")
#         minimize_button.clicked.connect(self.minimizeWindow)
        
#         self.maximize_button = QPushButton()
#         self.maximum_icon = QIcon(GraphicsDirectoryPath("Maximize.png"))
#         self.restore_icon = QIcon(GraphicsDirectoryPath("Minimize.png"))
#         self.maximize_button.setIcon(self.maximum_icon)
#         self.maximize_button.setFlat(True)
#         self.maximize_button.setStyleSheet("background-color:white")
#         self.maximize_button.clicked.connect(self.maximizeWindow)
        
#         self.close_button = QPushButton()
#         close_icon = QIcon(GraphicsDirectoryPath('Close.png'))
#         self.close_button.setIcon(close_icon)
#         self.close_button.setStyleSheet("background-color:white")
#         self.close_button.clicked.connect(self.closeWindow)
        
#         line_frame = QFrame()
#         line_frame.setFixedHeight(1)
#         line_frame.setFrameShape(QFrame.HLine)
#         line_frame.setFrameShadow(QFrame.Sunken)
#         line_frame.setStyleSheet("border-color:black;")
        
#         title_label = QLabel(f"{str(Assistantname).capitalize()} AI")
#         title_label.setStyleSheet("color:black;font-size:18px;background-color:white;")
        
#         home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
#         message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
#         layout.addWidget(title_label)
#         layout.addStretch(1)
#         layout.addWidget(home_button)
#         layout.addWidget(message_button)
#         layout.addStretch(1)
#         layout.addWidget(minimize_button)
#         layout.addWidget(self.maximize_button)
#         layout.addWidget(self.close_button)
#         layout.addWidget(line_frame)
        
#         self.draggable = True
#         self.offset = None

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.fillRect(self.rect(), Qt.white)
#         super().paintEvent(event)

#     def minimizeWindow(self):
#         self.parent().showMinimized()

#     def maximizeWindow(self):
#         if self.parent().isMaximized():
#             self.parent().showNormal()
#             self.maximize_button.setIcon(self.maximum_icon)
#         else:
#             self.parent().showMaximized()
#             self.maximize_button.setIcon(self.restore_icon)

#     def closeWindow(self):
#         self.parent().close()

#     def mousePressEvent(self, event):
#         if self.draggable:
#             self.offset = event.pos()

#     def mouseMoveEvent(self, event):
#         if self.draggable and self.offset:
#             new_pos = event.globalPos() - self.offset
#             self.parent().move(new_pos)

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.initUI()

#     def initUI(self):
#         desktop = QApplication.desktop()
#         screen = QApplication.primaryScreen()
#         rect = screen.availableGeometry()
#         screen_width = rect.width()
#         screen_height = rect.height()
        
#         stacked_widget = QStackedWidget(self)
#         initial_screen = InitialScreen()
#         message_screen = MessageScreen()
#         stacked_widget.addWidget(initial_screen)
#         stacked_widget.addWidget(message_screen)
        
#         # --- FIX: CHANGED GEOMETRY TO ALLOW RESTORE TO WORK ---
#         # Instead of 0,0,screen_width,screen_height (which is effectively maximized)
#         self.setGeometry(100, 100, screen_width - 200, screen_height - 200)
        
#         self.setStyleSheet("background-color:black;")
#         top_bar = CustomTopBar(self, stacked_widget)
#         self.setMenuWidget(top_bar)
#         self.setCentralWidget(stacked_widget)

# def GraphicalUserInterface():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     GraphicalUserInterface()
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("AssistantName", "Jarvis")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.strip()
    question_words = [
        "how", "what", "why", "where", "which", "who",
        "how's", "what's", "whom's", "may", "whose",
        "could", "whom", "can you", "who's", "Is"
    ]

    if any(word + "" in new_query for word in question_words):
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(rf"{TempDirPath}\Mic.data", "w", encoding="utf-8") as file:
        file.write(Command)

def GetMicrophoneStatus():
    with open(rf"{TempDirPath}\Mic.data", "r", encoding="utf-8") as file:
        Status = file.read()
    return Status

def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}\Status.data", "w", encoding="utf-8") as file:
        file.write(Status)

if not os.path.exists(TempDirPath):
    os.makedirs(TempDirPath)

SetAssistantStatus("Speaking...")

def GetAssistantStatus():
    with open(rf"{TempDirPath}\Status.data", "r", encoding="utf-8") as file:
        Status = file.read()
    return Status

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def GraphicsDirectoryPath(FileName):
    Path = rf"{GraphicsDirPath}\{FileName}"
    return Path

def TempDirectoryPath(FileName):
    Path = rf"{TempDirPath}\{FileName}"
    return Path

def ShowTextToScreen(Text):
    with open(rf"{TempDirPath}\Responses.data", "w", encoding="utf-8") as file:
        file.write(Text)

class ChatSection(QWidget):
    def __init__(self):
        super().__init__()
        self.toggled = False
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)
        
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        self.chat_text_edit.setStyleSheet("background-color: transparent; font-size: 13pt; color: blue;")
        
        self.bottom_widget = QWidget()
        self.bottom_layout = QVBoxLayout()
        self.bottom_layout.setContentsMargins(0,0,0,0)
        self.bottom_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border:none;")
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif')) 
        if not movie.isValid():
            movie = QMovie(GraphicsDirectoryPath('Jarvis.png'))
            
        max_gif_size_W = 200 
        max_gif_size_H = 200
        movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
        self.gif_label.setMovie(movie)
        movie.start()
        
        self.label = QLabel("")
        self.label.setStyleSheet("color:white; font-size:16px; border:none; margin-bottom: 5px;")
        self.label.setAlignment(Qt.AlignRight)
        
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(60, 60)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setCursor(Qt.PointingHandCursor)
        
        self.bottom_layout.addWidget(self.gif_label, alignment=Qt.AlignRight)
        self.bottom_layout.addWidget(self.label, alignment=Qt.AlignRight)
        self.bottom_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        
        self.bottom_widget.setLayout(self.bottom_layout)

        layout.addWidget(self.chat_text_edit)
        layout.addWidget(self.bottom_widget)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color:grey;")
        
        self.load_icon(GraphicsDirectoryPath('Mic_off.png'))
        self.icon_label.mousePressEvent = self.toggle_icon

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.loadMessages())
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(10)
        
        self.setStyleSheet(self.styleSheet() + """
            QScrollBar:vertical{
                border:none; background: black; width:10px;
            }
            QScrollBar::handle:vertical{
                background:white; min-height:20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical{
                height:0px;
            }
        """)

    def loadMessages(self):
        global old_chat_message
        try:
            with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
                messages = file.read()
            if messages and len(messages) > 1 and str(old_chat_message) != str(messages):
                self.addMessage(message=messages, color="White")
                old_chat_message = messages
        except FileNotFoundError:
            pass

    def SpeechRecogText(self):
        try:
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                self.label.setText(messages)
        except FileNotFoundError:
            pass

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            self.icon_label.setStyleSheet("background-color: red; border-radius: 30px;")
            self.icon_label.setText("MIC")
        else:
            new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon_label.setPixmap(new_pixmap)
            self.icon_label.setStyleSheet("border: none;")

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
            MicButtonClosed()
        self.toggled = not self.toggled

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)
        self.chat_text_edit.ensureCursorVisible()

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setAlignment(Qt.AlignCenter)
        
        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        if not movie.isValid():
             movie = QMovie(GraphicsDirectoryPath('Jarvis.png'))

        gif_label.setMovie(movie)
        
        # --- CRITICAL FIX: Base size on HEIGHT, not Width ---
        # This forces the GIF to take only 60% of the screen height,
        # guaranteeing 40% of room for the Mic and Text below it.
        gif_height = int(screen_height * 0.6) 
        gif_width = int(gif_height * (16/9))
        
        movie.setScaledSize(QSize(gif_width, gif_height))
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(100, 100)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setCursor(Qt.PointingHandCursor)
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon
        
        self.label = QLabel("")
        self.label.setStyleSheet("color:White; font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        self.label.setAlignment(Qt.AlignCenter)

        content_layout.addStretch()
        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.addStretch()
        
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color:black;")
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def SpeechRecogText(self):
        try:
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                self.label.setText(messages)
        except FileNotFoundError:
            pass

    def load_icon(self, path, width=100, height=100):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            self.icon_label.setStyleSheet("background-color: blue; border-radius: 50px; border: 2px solid white;")
            self.icon_label.setText("MIC")
        else:
            new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon_label.setPixmap(new_pixmap)
            self.icon_label.setStyleSheet("border: none;")

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 100, 100)
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 100, 100)
            MicButtonClosed()
        self.toggled = not self.toggled

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        screen_width = rect.width()
        screen_height = rect.height()
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color:black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.initUI()
        self.current_screen = None
        self.stacked_widget = stacked_widget

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        
        home_button = QPushButton()
        home_icon = QIcon(GraphicsDirectoryPath('Home.png'))
        home_button.setIcon(home_icon)
        home_button.setText("Home")
        home_button.setStyleSheet("height:40px;line_height:40px;background-color:white;color:black")
        
        message_button = QPushButton()
        message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText("Chat")
        message_button.setStyleSheet("background-color:white")
        
        minimize_button = QPushButton()
        minimize_icon = QIcon(GraphicsDirectoryPath('Minimize.png'))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("background-color:white")
        minimize_button.clicked.connect(self.minimizeWindow)
        
        self.maximize_button = QPushButton()
        self.maximum_icon = QIcon(GraphicsDirectoryPath("Maximize.png"))
        self.restore_icon = QIcon(GraphicsDirectoryPath("Minimize.png"))
        self.maximize_button.setIcon(self.maximum_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("background-color:white")
        self.maximize_button.clicked.connect(self.maximizeWindow)
        
        self.close_button = QPushButton()
        close_icon = QIcon(GraphicsDirectoryPath('Close.png'))
        self.close_button.setIcon(close_icon)
        self.close_button.setStyleSheet("background-color:white")
        self.close_button.clicked.connect(self.closeWindow)
        
        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color:black;")
        
        title_label = QLabel(f"{str(Assistantname).capitalize()} AI")
        title_label.setStyleSheet("color:black;font-size:18px;background-color:white;")
        
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)
        layout.addWidget(line_frame)
        
        self.draggable = True
        self.offset = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximum_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        desktop = QApplication.desktop()
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        screen_width = rect.width()
        screen_height = rect.height()
        
        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        
        self.setGeometry(100, 100, screen_width - 200, screen_height - 200)
        self.setStyleSheet("background-color:black;")
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()