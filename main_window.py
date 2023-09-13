import os
import sys
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedLayout, QMessageBox
from PyQt6.QtGui import QGuiApplication, QIcon
from manual_input_screen import ManualInputScreen
from file_input_screen import FileInputScreen
from transition_table_screen import TransitionTableScreen

## PyInstaller file path handler
if getattr(sys, 'frozen', False):
    # Running as a PyInstaller executable
    base_path = sys._MEIPASS
else:
    # Running as a script
    base_path = os.path.abspath(".")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.input_widget = None
        self.transition_table_widget = None

        self.setWindowTitle("Simulador Maquina de Turing")
        self.setWindowIcon(QIcon(os.path.join(base_path, 'resources', 'logo-unespar.jpg')))
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        ## User screen's dimenions
        self.screen = QGuiApplication.primaryScreen()
        self.screen_size = self.screen.availableSize()

        ## Master Layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 


        ## Application Header
        title_label = QLabel("<h1>Simulador Maquina de Turing</h1>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        
        ## Stacked Layout
        self.stacked_layout_container = QWidget()
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        ## First stacked view: Welcome Screen
        self.welcome_layout_container = QWidget()
        self.welcome_layout_container.setMinimumWidth(int(self.screen_size.width() * 0.70))
        self.welcome_layout_container.setMinimumHeight(int(self.screen_size.height() * 0.70))
        
        self.welcome_layout = QVBoxLayout()
        self.welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        welcome_label = QLabel("<h2>Bem vindo!</h2>")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_layout.addWidget(welcome_label)
        
        self.welcome_buttons_container = QWidget()
        self.welcome_buttons_layout = QHBoxLayout()
        
        self.button_script_manual = QPushButton("Manual")
        self.button_script_manual.clicked.connect(self.show_manual_input_screen)
        self.welcome_buttons_layout.addWidget(self.button_script_manual)
        self.button_script_arquivo = QPushButton("Arquivo")
        self.button_script_arquivo.clicked.connect(self.show_file_input_screen)
        self.welcome_buttons_layout.addWidget(self.button_script_arquivo)
        
        self.welcome_buttons_container.setLayout(self.welcome_buttons_layout)
        self.welcome_layout.addWidget(self.welcome_buttons_container)
        
        self.welcome_layout_container.setLayout(self.welcome_layout)
        
        
        ## Finalizing the stacked layout
        self.stacked_layout.addWidget(self.welcome_layout_container)
        
        self.stacked_layout_container.setLayout(self.stacked_layout)
        
        self.main_layout.addWidget(self.stacked_layout_container)
        
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        
        self.showMaximized()
    
    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            if self.windowState() & Qt.WindowState.WindowMaximized:
                self.isMaximized = True
            else:
                if self.isMaximized:
                    # The window was previously maximized, and now it's not
                    self.center_on_screen()
                self.isMaximized = False
            
    def center_on_screen(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        
        center_x = int((screen_geometry.width() - self.width()) / 2)
        center_y = int((screen_geometry.height() - self.height()) / 2.5)
        
        self.move(center_x, center_y)
        
    def show_alert_box(self, title, text):
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Icon.Information)
        alert.setWindowIcon(QIcon(os.path.join(base_path, 'resources', 'logo-unespar.jpg')))
        alert.setWindowTitle(title)
        alert.setText(text)
        alert.setStandardButtons(QMessageBox.StandardButton.Ok)
        alert.exec()
        
    def show_welcome_screen(self):
        self.stacked_layout.setCurrentWidget(self.welcome_layout_container)
        if not self.isMaximized:
            self.center_on_screen()
        self.destroy_input_widget()
        self.destroy_transition_table_widget()
        
    def show_manual_input_screen(self):
        self.input_widget = ManualInputScreen(self.show_welcome_screen, self.center_on_screen, self.show_alert_box, self.show_transition_table_screen)
        self.stacked_layout.addWidget(self.input_widget)
        self.stacked_layout.setCurrentWidget(self.input_widget)
        
    def show_file_input_screen(self):
        self.input_widget = FileInputScreen(self.show_welcome_screen, self.center_on_screen, self.show_alert_box)
        self.stacked_layout.addWidget(self.input_widget)
        self.stacked_layout.setCurrentWidget(self.input_widget)
        
    def show_transition_table_screen(self):
        number_of_states, main_alphabet_size, main_alphabet, main_alphabet_list, aux_alphabet_size, aux_alphabet, aux_alphabet_list, start_symbol, blank_symbol = self.input_widget.send_values()
        
        self.transition_table_widget = TransitionTableScreen(number_of_states, main_alphabet_size, main_alphabet, main_alphabet_list, aux_alphabet_size, aux_alphabet, aux_alphabet_list, start_symbol, blank_symbol, self.show_welcome_screen, self.center_on_screen, self.show_alert_box)
        self.stacked_layout.addWidget(self.transition_table_widget)
        self.stacked_layout.setCurrentWidget(self.transition_table_widget)
        
    def destroy_input_widget(self):
        if self.input_widget:
            self.input_widget.deleteLater()
            self.stacked_layout.removeWidget(self.input_widget)
            self.input_widget.deleteLater()
            self.input_widget = None
            
    def destroy_transition_table_widget(self):  
        if self.transition_table_widget:
            self.transition_table_widget.deleteLater()
            self.stacked_layout.removeWidget(self.transition_table_widget)
            self.transition_table_widget.deleteLater()
            self.transition_table_widget = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())