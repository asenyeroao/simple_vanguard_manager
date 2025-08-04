import sys
import os
import subprocess
import ctypes
import winreg
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QComboBox, QFrame, QSpacerItem, QSizePolicy, QDialog, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPalette, QColor, QFont, QPainter, QLinearGradient, QBrush


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("設定 / Settings")
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setModal(True)
        self.setFixedSize(300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("設定 / Settings")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        lang_layout = QHBoxLayout()
        lang_label = QLabel("語言:")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["中文", "English"])
        self.lang_combo.setCurrentIndex(0 if self.parent_window.language == "zh" else 1)
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)

        theme_layout = QHBoxLayout()
        theme_label = QLabel("主題:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["深色主題", "淺色主題", "Vanguard 主題"])
        self.theme_combo.setCurrentIndex(self.parent_window.theme_combo.currentIndex())
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        close_btn = QPushButton("關閉 / Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def change_language(self):
        self.parent_window.language = "zh" if self.lang_combo.currentIndex() == 0 else "en"
        self.parent_window.update_ui()

    def change_theme(self):
        self.parent_window.theme_combo.setCurrentIndex(self.theme_combo.currentIndex())
        self.parent_window.switch_theme()


class VanguardManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vanguard Manager")
        self.setFixedSize(480, 320)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        self.language = "zh"
        self.translations = {
            "status": {"zh": "Vanguard 狀態：", "en": "Vanguard Status:"},
            "running": {"zh": "運行中", "en": "Running"},
            "not_running": {"zh": "未運行", "en": "Not Running"},
            "toggle": {"zh": "啟用/停用 Vanguard", "en": "Enable/Disable Vanguard"},
            "autostart": {"zh": "切換開機自啟", "en": "Toggle Autostart"},
            "title": {"zh": "Vanguard 管理工具", "en": "Vanguard Manager"}
        }

        self.init_ui()
        self.init_timer()
        self.update_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 25, 25, 25)

        header_layout = QHBoxLayout()
        self.title_label = QLabel(self.translations["title"][self.language])
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        header_layout.addWidget(self.title_label)
        header_layout.addItem(spacer)

        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setFixedSize(35, 35)
        settings_font = QFont()
        settings_font.setPointSize(16)
        self.settings_btn.setFont(settings_font)
        self.settings_btn.clicked.connect(self.show_settings)
        header_layout.addWidget(self.settings_btn)

        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(35, 35)
        close_font = QFont()
        close_font.setPointSize(18)
        close_font.setBold(True)
        self.close_btn.setFont(close_font)
        self.close_btn.clicked.connect(self.close)
        header_layout.addWidget(self.close_btn)

        main_layout.addLayout(header_layout)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        status_font = QFont()
        status_font.setPointSize(14)
        status_font.setBold(True)
        self.status_label.setFont(status_font)
        self.status_label.setMinimumHeight(50)
        main_layout.addWidget(self.status_label)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)

        self.toggle_button = QPushButton()
        self.toggle_button.setMinimumHeight(45)
        button_font = QFont()
        button_font.setPointSize(11)
        button_font.setBold(True)
        self.toggle_button.setFont(button_font)
        
        self.autostart_button = QPushButton()
        self.autostart_button.setMinimumHeight(45)
        self.autostart_button.setFont(button_font)

        button_layout.addWidget(self.toggle_button)
        button_layout.addWidget(self.autostart_button)
        main_layout.addLayout(button_layout)

        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_bottom)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["深色主題", "淺色主題", "Vanguard 主題"])
        self.theme_combo.currentIndexChanged.connect(self.switch_theme)
        self.theme_combo.hide()

        self.setLayout(main_layout)

        self.toggle_button.clicked.connect(self.toggle_vanguard)
        self.autostart_button.clicked.connect(self.toggle_autostart)

    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(3000)

    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

    def get_vanguard_status(self):
        try:
            output = subprocess.getoutput("sc query vgc")
            return "RUNNING" in output
        except:
            return False

    def toggle_vanguard(self):
        try:
            if self.get_vanguard_status():
                subprocess.run(["sc", "stop", "vgc"], shell=True, check=True)
                subprocess.run(["sc", "stop", "vgk"], shell=True, check=True)
            else:
                subprocess.run(["sc", "start", "vgk"], shell=True, check=True)
                subprocess.run(["sc", "start", "vgc"], shell=True, check=True)
        except subprocess.CalledProcessError:
            self.status_label.setText("操作失敗，請檢查權限 / Operation failed, check permissions")
        self.update_ui()

    def toggle_autostart(self):
        key_path = r"SYSTEM\CurrentControlSet\Services\vgc"
        try:
            reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            key = winreg.OpenKey(reg, key_path, 0, winreg.KEY_ALL_ACCESS)
            start_value = winreg.QueryValueEx(key, "Start")[0]
            new_value = 2 if start_value != 2 else 4
            winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, new_value)
            winreg.CloseKey(key)
        except PermissionError:
            self.status_label.setText("需要管理員權限 / Administrator rights required")
        except Exception as e:
            self.status_label.setText(f"設定失敗 / Settings failed: {str(e)}")

    def update_ui(self):
        status = self.get_vanguard_status()
        status_text = self.translations["status"][self.language]
        status_text += self.translations["running" if status else "not_running"][self.language]
        self.status_label.setText(status_text)

        self.toggle_button.setText(self.translations["toggle"][self.language])
        self.autostart_button.setText(self.translations["autostart"][self.language])
        self.title_label.setText(self.translations["title"][self.language])

    def switch_language(self):
        self.language = "zh" if self.lang_combo.currentIndex() == 0 else "en"
        self.update_ui()

    def switch_theme(self):
        theme_index = self.theme_combo.currentIndex()
        palette = QPalette()
        
        if theme_index == 0:
            self.apply_dark_theme(palette)
        elif theme_index == 1:
            self.apply_light_theme(palette)
        else:
            self.apply_vanguard_theme(palette)
        
        self.setPalette(palette)
        self.update()

    def apply_dark_theme(self, palette):
        palette.setColor(QPalette.Window, QColor(35, 35, 35))
        palette.setColor(QPalette.WindowText, QColor(240, 240, 240))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.Text, QColor(240, 240, 240))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(240, 240, 240))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    def apply_light_theme(self, palette):
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    def apply_vanguard_theme(self, palette):
        palette.setColor(QPalette.Window, QColor(15, 15, 15))
        palette.setColor(QPalette.WindowText, QColor(255, 85, 85))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
        palette.setColor(QPalette.Text, QColor(255, 85, 85))
        palette.setColor(QPalette.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ButtonText, QColor(255, 85, 85))
        palette.setColor(QPalette.Highlight, QColor(200, 50, 50))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        theme_index = self.theme_combo.currentIndex()
        
        if theme_index == 0:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor(50, 50, 50))
            gradient.setColorAt(0.5, QColor(35, 35, 35))
            gradient.setColorAt(1, QColor(20, 20, 20))
        elif theme_index == 1:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor(255, 255, 255))
            gradient.setColorAt(0.5, QColor(245, 245, 245))
            gradient.setColorAt(1, QColor(235, 235, 235))
        else:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor(30, 30, 30))
            gradient.setColorAt(0.3, QColor(20, 20, 20))
            gradient.setColorAt(0.7, QColor(15, 15, 15))
            gradient.setColorAt(1, QColor(10, 10, 10))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(QColor(100, 100, 100))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 15, 15)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_start_position') and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_position)


if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin():
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        window = VanguardManager()
        window.show()
        sys.exit(app.exec_())
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
