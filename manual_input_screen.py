from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QScrollArea
from input_verification import input_parsing

class ManualInputScreen(QWidget):
    def __init__(self, show_welcome_screen_callback, center_on_screen_callback, show_alert_box_callback, show_transition_table_callback):
        super().__init__()
        
        self.show_welcome_screen_callback = show_welcome_screen_callback
        self.center_on_screen_callback = center_on_screen_callback
        self.show_alert_box_callback = show_alert_box_callback
        self.show_transition_table_callback = show_transition_table_callback
        
        self.number_of_states = 0
        self.main_alphabet_size = 0
        self.main_alphabet = set()
        self.main_alphabet_list = []
        self.aux_alphabet_size = 0
        self.aux_alphabet = set()
        self.aux_alphabet_list = []
        self.start_symbol = ''
        self.blank_symbol = ''
        
        ## Master Layout
        self.manual_input_layout = QVBoxLayout()
        self.manual_input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        ## Manual Input Screen Header
        self.manual_input_label = QLabel("<h2>Entrada manual de valores</h2>")
        self.manual_input_label.setMaximumHeight(120)
        self.manual_input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.manual_input_layout.addWidget(self.manual_input_label)
        
        
        ## Number of states input
        self.manual_input_number_of_states_container = QWidget()
        self.manual_input_number_of_states_container.setMaximumHeight(60)
        self.manual_input_number_of_states_layout = QHBoxLayout()
        
        self.number_of_states_label = QLabel("Numero de estados: ")
        self.manual_input_number_of_states_layout.addWidget(self.number_of_states_label)
        
        self.number_of_states_input = QLineEdit()
        self.number_of_states_input.setPlaceholderText(f"Insira um valor inteiro")
        self.manual_input_number_of_states_layout.addWidget(self.number_of_states_input)
        
        self.number_of_states_input_confirm_button = QPushButton("Confirmar")
        self.number_of_states_input_confirm_button.clicked.connect(self.show_main_alphabet_size_input)
        self.manual_input_number_of_states_layout.addWidget(self.number_of_states_input_confirm_button)
        
        self.manual_input_number_of_states_container.setLayout(self.manual_input_number_of_states_layout)
        self.manual_input_layout.addWidget(self.manual_input_number_of_states_container)
        
        
        ## Main alphabet size input
        self.manual_input_main_alphabet_size_container = QWidget()
        self.manual_input_main_alphabet_size_container.setVisible(False)
        self.manual_input_main_alphabet_size_container.setMaximumHeight(60)
        self.manual_input_main_alphabet_size_layout = QHBoxLayout()
        
        self.main_alphabet_size_label = QLabel("Tamanho do alfabeto principal: ")
        self.manual_input_main_alphabet_size_layout.addWidget(self.main_alphabet_size_label)
        
        self.main_alphabet_size_input = QLineEdit()
        self.main_alphabet_size_input.setPlaceholderText(f"Insira um valor inteiro")
        self.manual_input_main_alphabet_size_layout.addWidget(self.main_alphabet_size_input)
        
        self.main_alphabet_size_confirm_button = QPushButton("Confirmar")
        self.main_alphabet_size_confirm_button.clicked.connect(self.show_main_alphabet_values_input)
        self.manual_input_main_alphabet_size_layout.addWidget(self.main_alphabet_size_confirm_button)
        
        self.manual_input_main_alphabet_size_container.setLayout(self.manual_input_main_alphabet_size_layout)
        self.manual_input_layout.addWidget(self.manual_input_main_alphabet_size_container)
        
        
        ## Main alphabet values input
        self.manual_input_main_alphabet_values_container = QWidget()
        self.manual_input_main_alphabet_values_container.setVisible(False)
        self.manual_input_main_alphabet_values_container.setMaximumHeight(80)
        self.manual_input_main_alphabet_values_layout = QHBoxLayout()
        
        self.main_alphabet_values_label = QLabel("Alfabeto principal: ")
        self.manual_input_main_alphabet_values_layout.addWidget(self.main_alphabet_values_label)
        
        self.main_alphabet_values_input_scroll_area = QScrollArea()
        
        self.main_alphabet_values_input_container = QWidget()
        self.main_alphabet_values_input_layout = QHBoxLayout()
        
        ### show_main_alphabet_values_input has the logic for adding QLineEdit widgets
        
        self.main_alphabet_values_input_container.setLayout(self.main_alphabet_values_input_layout)
        
        self.main_alphabet_values_input_scroll_area.setWidget(self.main_alphabet_values_input_container)
        self.main_alphabet_values_input_scroll_area.setWidgetResizable(True)
        self.main_alphabet_values_input_scroll_area.setMaximumHeight(80)
        
        self.manual_input_main_alphabet_values_layout.addWidget(self.main_alphabet_values_input_scroll_area)
        
        self.main_alphabet_values_confirm_button = QPushButton("Confirmar")
        self.main_alphabet_values_confirm_button.clicked.connect(self.show_aux_alphabet_size_input)
        self.manual_input_main_alphabet_values_layout.addWidget(self.main_alphabet_values_confirm_button)
                
        self.manual_input_main_alphabet_values_container.setLayout(self.manual_input_main_alphabet_values_layout)
        self.manual_input_layout.addWidget(self.manual_input_main_alphabet_values_container)
        
        
        ## Aux alphabet size input
        self.manual_input_aux_alphabet_size_container = QWidget()
        self.manual_input_aux_alphabet_size_container.setVisible(False)
        self.manual_input_aux_alphabet_size_container.setMaximumHeight(60)
        self.manual_input_aux_alphabet_size_layout = QHBoxLayout()
        
        self.aux_alphabet_size_label = QLabel("Tamanho do alfabeto auxiliar: ")
        self.manual_input_aux_alphabet_size_layout.addWidget(self.aux_alphabet_size_label)
        
        self.aux_alphabet_size_input = QLineEdit()
        self.aux_alphabet_size_input.setPlaceholderText(f"Insira um valor inteiro")
        self.manual_input_aux_alphabet_size_layout.addWidget(self.aux_alphabet_size_input)
        
        self.aux_alphabet_size_confirm_button = QPushButton("Confirmar")
        self.aux_alphabet_size_confirm_button.clicked.connect(self.show_aux_alphabet_values_input)
        self.manual_input_aux_alphabet_size_layout.addWidget(self.aux_alphabet_size_confirm_button)
        
        self.manual_input_aux_alphabet_size_container.setLayout(self.manual_input_aux_alphabet_size_layout)
        self.manual_input_layout.addWidget(self.manual_input_aux_alphabet_size_container)
        
        
        ## Aux alphabet values input
        self.manual_input_aux_alphabet_values_container = QWidget()
        self.manual_input_aux_alphabet_values_container.setVisible(False)
        self.manual_input_aux_alphabet_values_container.setMaximumHeight(80)
        self.manual_input_aux_alphabet_values_layout = QHBoxLayout()
        
        self.aux_alphabet_values_label = QLabel("Alfabeto auxiliar: ")
        self.manual_input_aux_alphabet_values_layout.addWidget(self.aux_alphabet_values_label)
        
        self.aux_alphabet_values_input_scroll_area = QScrollArea()
        
        self.aux_alphabet_values_input_container = QWidget()
        self.aux_alphabet_values_input_layout = QHBoxLayout()
        
        ### show_aux_alphabet_values_input has the logic for adding QLineEdit widgets
        
        self.aux_alphabet_values_input_container.setLayout(self.aux_alphabet_values_input_layout)
        
        self.aux_alphabet_values_input_scroll_area.setWidget(self.aux_alphabet_values_input_container)
        self.aux_alphabet_values_input_scroll_area.setWidgetResizable(True)
        self.aux_alphabet_values_input_scroll_area.setMaximumHeight(80)
        
        self.manual_input_aux_alphabet_values_layout.addWidget(self.aux_alphabet_values_input_scroll_area)
        
        self.aux_alphabet_values_confirm_button = QPushButton("Confirmar")
        self.aux_alphabet_values_confirm_button.clicked.connect(self.show_start_symbol_input)
        self.manual_input_aux_alphabet_values_layout.addWidget(self.aux_alphabet_values_confirm_button)
                
        self.manual_input_aux_alphabet_values_container.setLayout(self.manual_input_aux_alphabet_values_layout)
        self.manual_input_layout.addWidget(self.manual_input_aux_alphabet_values_container)
        
        
        ## Start symbol input
        self.manual_input_start_symbol_input_container = QWidget()
        self.manual_input_start_symbol_input_container.setVisible(False)
        self.manual_input_start_symbol_input_container.setMaximumHeight(60)
        self.manual_input_start_symbol_input_layout = QHBoxLayout()
        
        self.start_symbol_input_label = QLabel("Simbolo marcador de inicio: ")
        self.manual_input_start_symbol_input_layout.addWidget(self.start_symbol_input_label)
        
        self.start_symbol_input = QLineEdit()
        self.start_symbol_input.setPlaceholderText(f"Insira um simbolo")
        self.start_symbol_input.setMaxLength(1)
        self.manual_input_start_symbol_input_layout.addWidget(self.start_symbol_input)
        
        self.start_symbol_input_confirm_button = QPushButton("Confirmar")
        self.start_symbol_input_confirm_button.clicked.connect(self.show_blank_symbol_input)
        self.manual_input_start_symbol_input_layout.addWidget(self.start_symbol_input_confirm_button)
        
        self.manual_input_start_symbol_input_container.setLayout(self.manual_input_start_symbol_input_layout)
        self.manual_input_layout.addWidget(self.manual_input_start_symbol_input_container)
        
        
        ## Blank symbol input
        self.manual_input_blank_symbol_input_container = QWidget()
        self.manual_input_blank_symbol_input_container.setVisible(False)
        self.manual_input_blank_symbol_input_container.setMaximumHeight(60)
        self.manual_input_blank_symbol_input_layout = QHBoxLayout()
        
        self.blank_symbol_input_label = QLabel("Simbolo marcador de branco: ")
        self.manual_input_blank_symbol_input_layout.addWidget(self.blank_symbol_input_label)
        
        self.blank_symbol_input = QLineEdit()
        self.blank_symbol_input.setPlaceholderText(f"Insira um simbolo")
        self.blank_symbol_input.setMaxLength(1)
        self.manual_input_blank_symbol_input_layout.addWidget(self.blank_symbol_input)
        
        self.blank_symbol_input_confirm_button = QPushButton("Confirmar")
        self.blank_symbol_input_confirm_button.clicked.connect(self.verify_data)
        self.manual_input_blank_symbol_input_layout.addWidget(self.blank_symbol_input_confirm_button)
        
        self.manual_input_blank_symbol_input_container.setLayout(self.manual_input_blank_symbol_input_layout)
        self.manual_input_layout.addWidget(self.manual_input_blank_symbol_input_container)
        
        
        ## Back button
        self.manual_input_back_button = QPushButton("Voltar")
        self.manual_input_back_button.clicked.connect(self.show_welcome_screen_callback)
        self.manual_input_layout.addWidget(self.manual_input_back_button)
        
        self.setLayout(self.manual_input_layout)
        
        if not self.isMaximized:
            QTimer.singleShot(0, self.center_on_screen_callback)
        
    def show_main_alphabet_size_input(self):
        value, type = input_parsing(self.number_of_states_input.text())
        
        if(type == "float"):
            self.show_alert_box_callback("Alerta!", f"Valor inserido '{value}' invalido! Numero deve ser inteiro")
        elif(type == "NaN"):
            self.show_alert_box_callback("Alerta!", f"Valor inserido '{value}' invalido! Entrada deve ser um numero")
        elif(type == "int"):
            self.number_of_states = value
            self.number_of_states_input.setDisabled(True)
            self.number_of_states_input_confirm_button.setVisible(False)
            self.manual_input_main_alphabet_size_container.setVisible(True)
        
    def show_main_alphabet_values_input(self):
        value, type = input_parsing(self.main_alphabet_size_input.text())
        
        if(type == "float"):
            self.show_alert_box_callback("Alerta!", f"Valor inserido '{value}' invalido! Numero deve ser inteiro")
        elif(type == "NaN"):
            self.show_alert_box_callback("Alerta!", f"Valor inserido '{value}' invalido! Entrada deve ser um numero")
        elif(type == "int"):
            self.main_alphabet_size = value
            self.main_alphabet_size_input.setDisabled(True)
            self.main_alphabet_size_confirm_button.setVisible(False)
            
            for i in range(self.main_alphabet_size):
                main_alphabet_values_input = QLineEdit()
                main_alphabet_values_input.setMaxLength(1)
                self.main_alphabet_values_input_layout.addWidget(main_alphabet_values_input)
                
            self.manual_input_main_alphabet_values_container.setVisible(True)
            
    def show_aux_alphabet_size_input(self):
        self.main_alphabet_list.clear()
        self.main_alphabet.clear()
        alphabet_valid = True
        
        for i in range(self.main_alphabet_size):
            widget = self.main_alphabet_values_input_layout.itemAt(i).widget()
            letter = widget.text()
            
            if(self.main_alphabet.__contains__(letter) or letter == ''):
                if self.main_alphabet.__contains__(letter):
                    self.show_alert_box_callback("Alerta!", f"Letra '{letter}' repetida no alfabeto!")
                else:
                    self.show_alert_box_callback("Alerta!", f"Alfabeto contem letra vazia!")
                alphabet_valid = False
                break
            elif(letter.lower() == 'x' or letter.lower() == 'l' or letter.lower() == 'r'):
                self.show_alert_box_callback("Alerta!", f"Alfabeto contem simbolo reservado! ('X', 'L', 'R')")
                alphabet_valid = False
                break
            else:
                self.main_alphabet.add(letter)
                self.main_alphabet_list.append(letter)
                
        if(alphabet_valid):
            for i in range(self.main_alphabet_size):
                self.main_alphabet_values_input_layout.itemAt(i).widget().setDisabled(True)
            self.main_alphabet_values_confirm_button.setVisible(False)
            self.manual_input_aux_alphabet_size_container.setVisible(True)
                
    def show_aux_alphabet_values_input(self):
        value, type = input_parsing(self.aux_alphabet_size_input.text())
        
        if(type == "float"):
            self.show_alert_box_callback("Alerta!", f"Valor inserido '{value}' invalido! Numero deve ser inteiro")
        elif(type == "NaN"):
            self.show_alert_box_callback("Alerta!", f"Valor inserido '{value}' invalido! Entrada deve ser um numero")
        elif(type == "int"):
            self.aux_alphabet_size = value
            self.aux_alphabet_size_input.setDisabled(True)
            self.aux_alphabet_size_confirm_button.setVisible(False)
            
            for i in range(self.aux_alphabet_size):
                aux_alphabet_values_input = QLineEdit()
                aux_alphabet_values_input.setMaxLength(1)
                self.aux_alphabet_values_input_layout.addWidget(aux_alphabet_values_input)
                
            self.manual_input_aux_alphabet_values_container.setVisible(True)
            
    def show_start_symbol_input(self):
        self.aux_alphabet_list.clear()
        alphabet_valid = True
        
        for i in range(self.aux_alphabet_size):
            widget = self.aux_alphabet_values_input_layout.itemAt(i).widget()
            letter = widget.text()
            
            if(self.aux_alphabet.__contains__(letter) or letter == ''):
                if self.aux_alphabet.__contains__(letter):
                    self.show_alert_box_callback("Alerta!", f"Letra '{letter}' repetida no alfabeto!")
                else:
                    self.show_alert_box_callback("Alerta!", f"Alfabeto contem letra vazia!")
                alphabet_valid = False
                self.aux_alphabet.clear()
                break
            elif(letter.lower() == 'x' or letter.lower() == 'l' or letter.lower() == 'r'):
                self.show_alert_box_callback("Alerta!", f"Alfabeto contem simbolo reservado! ('X', 'L', 'R')")
                alphabet_valid = False
                self.aux_alphabet.clear()
                break
            else:
                self.aux_alphabet.add(letter)
                self.aux_alphabet_list.append(letter)
                
        if(alphabet_valid):
            for i in range(self.aux_alphabet_size):
                self.aux_alphabet_values_input_layout.itemAt(i).widget().setDisabled(True)
            self.aux_alphabet_values_confirm_button.setVisible(False)
            self.manual_input_start_symbol_input_container.setVisible(True)
            
    def show_blank_symbol_input(self):
        symbol_valid = True
        
        if(self.start_symbol_input.text() == ''):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{self.start_symbol_input.text()}' vazio!")
        elif(self.main_alphabet.__contains__(self.start_symbol_input.text())):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{self.start_symbol_input.text()}' ja existe no alfabeto principal!")
        elif(self.aux_alphabet.__contains__(self.start_symbol_input.text())):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{self.start_symbol_input.text()}' ja existe no alfabeto auxiliar!")
        elif(self.start_symbol_input.text().lower() == 'x' or self.start_symbol_input.text().lower() == 'l' or self.start_symbol_input.text().lower() == 'r'):
            self.show_alert_box_callback("Alerta!", f"Simbolo de inicio nao pode ser o mesmo que os reservados! ('X', 'L', 'R')")
            symbol_valid = False
        
        if(symbol_valid):
            self.start_symbol = self.start_symbol_input.text()
            self.start_symbol_input.setDisabled(True)
            self.start_symbol_input_confirm_button.setVisible(False)
            self.manual_input_blank_symbol_input_container.setVisible(True)
            
    def verify_data(self):
        symbol_valid = True
        
        if(self.blank_symbol_input.text() == ''):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{self.blank_symbol_input.text()}' vazio!")
        elif(self.blank_symbol_input.text() == self.start_symbol):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{self.blank_symbol_input.text()}' igual ao de inicio!")
        elif(self.main_alphabet.__contains__(self.blank_symbol_input.text())):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{self.blank_symbol_input.text()}' ja existe no alfabeto principal!")
        elif(self.aux_alphabet.__contains__(self.blank_symbol_input.text())):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{self.blank_symbol_input.text()}' ja existe no alfabeto auxiliar!")
        elif(self.blank_symbol_input.text().lower() == 'x' or self.blank_symbol_input.text().lower() == 'l' or self.blank_symbol_input.text().lower() == 'r'):
            self.show_alert_box_callback("Alerta!", f"Simbolo de branco nao pode ser o mesmo que os reservados! ('X', 'L', 'R')")
            symbol_valid = False
        
        if(symbol_valid):
            self.blank_symbol = self.blank_symbol_input.text()
            self.blank_symbol_input.setDisabled(True)
            self.blank_symbol_input_confirm_button.setVisible(False)
            self.show_transition_table_callback()
            
    def send_values(self):
        return self.number_of_states, self.main_alphabet_size, self.main_alphabet, self.main_alphabet_list, self.aux_alphabet_size, self.aux_alphabet, self.aux_alphabet_list, self.start_symbol, self.blank_symbol