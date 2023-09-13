from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QScrollArea, QFileDialog
from PyQt6.QtGui import QColor, QGuiApplication
from transition import Transition
from input_verification import verify_test_word_input, replacement_letter_valid, direction_letter_valid
from turing_machine_logic import run_turing_machine

class FileInputScreen(QWidget):
    def __init__(self, show_welcome_screen_callback, center_on_screen_callback, show_alert_box_callback):
        super().__init__()
        
        self.show_welcome_screen_callback = show_welcome_screen_callback
        self.center_on_screen_callback = center_on_screen_callback
        self.show_alert_box_callback = show_alert_box_callback
        
        self.number_of_states = 0
        self.main_alphabet_size = 0
        self.main_alphabet = set()
        self.main_alphabet_list = []
        self.aux_alphabet_size = 0
        self.aux_alphabet = set()
        self.aux_alphabet_list = []
        self.start_symbol = ''
        self.blank_symbol = ''
        self.initial_state = None
        self.tape = []
        
        ## Screen dimensions
        screen = QGuiApplication.primaryScreen()
        screen_size = screen.availableSize()
        
        
        ## Master Layout
        self.master_layout = QVBoxLayout()
        
        self.file_input_scroll_area = QScrollArea()
        self.file_input_scroll_area.setWidgetResizable(True)
        self.file_input_scroll_area.setMinimumWidth(int(screen_size.width() * 0.70))
        self.file_input_scroll_area.setMinimumHeight(int(screen_size.height() * 0.70))
        
        self.file_input_container = QWidget()
        self.file_input_layout = QVBoxLayout()
        self.file_input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        ## Manual Input Screen Header
        self.file_input_label = QLabel("<h2>Entrada de valores por arquivo</h2>")
        self.file_input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_input_layout.addWidget(self.file_input_label)
        
        
        ## Text box input
        self.file_input_text_box = QTextEdit()
        self.file_input_text_box.setPlaceholderText(f"Cole o texto da tabela de transicao aqui...")
        self.file_input_text_box.setMinimumHeight(int(screen_size.height() * 0.50))
        self.file_input_layout.addWidget(self.file_input_text_box)
        
        
        ## Confirm button
        self.file_input_confirm_button = QPushButton("Confirmar")
        self.file_input_confirm_button.clicked.connect(self.get_data)
        self.file_input_layout.addWidget(self.file_input_confirm_button)
        
        ## Open file button
        self.file_input_open_file_button = QPushButton("Abrir arquivo")
        self.file_input_open_file_button.clicked.connect(self.open_file_button)
        self.file_input_layout.addWidget(self.file_input_open_file_button)
        
        ## Back button
        self.file_input_back_button = QPushButton("Voltar")
        self.file_input_back_button.clicked.connect(lambda: self.show_welcome_screen_callback())
        
        self.file_input_layout.addWidget(self.file_input_back_button)
                
        
        ## Result scroll area
        self.tape_result_scroll_area = QScrollArea()
        self.tape_result_scroll_area.setVisible(False)
        self.tape_result_scroll_area.setWidgetResizable(True)
        self.tape_result_scroll_area.setMinimumHeight(int(screen_size.height() * 0.50))
        
        self.tape_result_layout_container = QWidget()
        self.tape_result_layout = QVBoxLayout()
        self.tape_result_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ## Test word tape result
        self.tape_result_label = QLabel("<h2>Resultado da fita</h2>")
        self.tape_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tape_result_layout.addWidget(self.tape_result_label)
        self.tape_result_layout.addSpacing(10)
        
        self.tape_result_value = QLabel()
        self.tape_result_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tape_result_layout.addWidget(self.tape_result_value)
        self.tape_result_layout.addSpacing(20)
        
        
        ## Test word output
        self.test_word_output_label = QLabel("<h2>Transicoes realizadas</h2>")
        self.test_word_output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tape_result_layout.addWidget(self.test_word_output_label)
        self.tape_result_layout.addSpacing(10)
        
        self.test_word_output_value = QLabel()
        self.test_word_output_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tape_result_layout.addWidget(self.test_word_output_value)
        
        
        self.tape_result_layout_container.setLayout(self.tape_result_layout)
        self.tape_result_scroll_area.setWidget(self.tape_result_layout_container)
        self.file_input_layout.addWidget(self.tape_result_scroll_area)
        
        
        self.file_input_container.setLayout(self.file_input_layout)
        self.file_input_scroll_area.setWidget(self.file_input_container)
        
        self.master_layout.addWidget(self.file_input_scroll_area)
        
        self.setLayout(self.master_layout)
        
        if not self.isMaximized:
            QTimer.singleShot(0, self.center_on_screen_callback)
        
    def open_file_button(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Tabelas de transicao (*.txt)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            
            with open(selected_file, "r") as file:
                raw_text = file.read()
                
            self.file_input_text_box.setText(raw_text)
                
            lines = raw_text.split('\n')
            self.verify_state_number_input(lines)
    
    def input_parsing(self, value):
        try:
            parsed_value = float(value)
            if parsed_value.is_integer():
                return int(parsed_value), "int"
            else:
                return parsed_value, "float"
        except ValueError:
            return value, "NaN"
        
    def get_data(self):
        raw_text = self.file_input_text_box.toPlainText()
        lines = raw_text.split('\n')
        
        self.verify_state_number_input(lines)
        
    def verify_state_number_input(self, lines):
        value, type = self.input_parsing(lines[0])
        
        if(type == "float"):
            self.show_alert_box_callback("Alerta!", f"Valor inserido '{value}' invalido! Numero deve ser inteiro")
        elif(type == "NaN"):
            self.show_alert_box_callback("Alerta!", f"Valor inserido '{value}' invalido! Entrada deve ser um numero")
        elif(type == "int"):
            self.number_of_states = value
            self.verify_main_alphabet_input(lines)
            
    def verify_main_alphabet_input(self, lines):
        self.main_alphabet.clear()
        self.main_alphabet_list.clear()
        alphabet_valid = True
        
        symbols = lines[1].split(',')
        self.main_alphabet_size = len(symbols)
        
        for i in range(self.main_alphabet_size):
            letter = symbols[i]
            
            if(len(letter)>1):
                self.show_alert_box_callback("Alerta!", f"Cada letra do alfabeto principal deve ser apenas um unico simbolo!")
                alphabet_valid = False
                self.main_alphabet.clear()
                break
            elif(self.main_alphabet.__contains__(letter) or letter == ''):
                if self.main_alphabet.__contains__(letter):
                    self.show_alert_box_callback("Alerta!", f"Letra '{letter}' repetida no alfabeto!")
                else:
                    self.show_alert_box_callback("Alerta!", f"Alfabeto contem letra vazia!")
                alphabet_valid = False
                self.main_alphabet.clear()
                break
            elif(letter.lower() == 'x' or letter.lower() == 'l' or letter.lower() == 'r'):
                self.show_alert_box_callback("Alerta!", f"Alfabeto contem simbolo reservado! ('X', 'L', 'R')")
                alphabet_valid = False
                self.main_alphabet.clear()
                break
            else:
                self.main_alphabet.add(letter)
                self.main_alphabet_list.append(letter)
                
        if(alphabet_valid):
            self.verify_aux_alphabet_input(lines)
            
    def verify_aux_alphabet_input(self, lines):
        self.aux_alphabet.clear()
        self.aux_alphabet_list.clear()
        alphabet_valid = True
        
        symbols = lines[2].split(',')
        self.aux_alphabet_size = len(symbols)
        
        for i in range(self.aux_alphabet_size):
            letter = symbols[i]
            
            if(len(letter)>1):
                self.show_alert_box_callback("Alerta!", f"Cada letra do alfabeto auxiliar deve ser apenas um unico simbolo!")
                alphabet_valid = False
                self.aux_alphabet.clear()
                break
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
            self.verify_start_symbol_input(lines)
            
    def verify_start_symbol_input(self, lines):
        symbol_valid = True
        symbol_input = lines[3]
        
        if(len(symbol_input)>1):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{symbol_input}' deve ser apenas um caractere!")
        elif(symbol_input == ''):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{symbol_input}' vazio!")
        elif(self.main_alphabet.__contains__(symbol_input)):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{symbol_input}' ja existe no alfabeto principal!")
        elif(self.aux_alphabet.__contains__(symbol_input)):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{symbol_input}' ja existe no alfabeto auxiliar!")
        elif(symbol_input.lower() == 'x' or symbol_input.lower() == 'l' or symbol_input.lower() == 'r'):
            self.show_alert_box_callback("Alerta!", f"Simbolo de inicio nao pode ser o mesmo que os reservados! ('X', 'L', 'R')")
            symbol_valid = False
        
        if(symbol_valid):
            self.start_symbol = symbol_input
            self.verify_blank_symbol_input(lines)
            
    def verify_blank_symbol_input(self, lines):
        symbol_valid = True
        symbol_input = lines[4]
        
        if(len(symbol_input)>1):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{symbol_input}' deve ser apenas um caractere!")
        elif(symbol_input == ''):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{symbol_input}' vazio!")
        elif(symbol_input == self.start_symbol):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{symbol_input}' igual ao de inicio!")
        elif(self.main_alphabet.__contains__(symbol_input)):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{symbol_input}' ja existe no alfabeto principal!")
        elif(self.aux_alphabet.__contains__(symbol_input)):
            symbol_valid = False
            self.show_alert_box_callback("Alerta!", f"Simbolo '{symbol_input}' ja existe no alfabeto auxiliar!")
        elif(symbol_input.lower() == 'x' or symbol_input.lower() == 'l' or symbol_input.lower() == 'r'):
            self.show_alert_box_callback("Alerta!", f"Simbolo de inicio nao pode ser o mesmo que os reservados! ('X', 'L', 'R')")
            symbol_valid = False
        
        if(symbol_valid):
            self.blank_symbol = symbol_input
            self.verify_initial_state_number_input(lines)
            
    def verify_initial_state_number_input(self, lines):
        value, type = self.input_parsing(lines[5])
        
        if(type == "float"):
            self.show_alert_box_callback("Alerta!", f"Valor inserido '{value}' invalido! Numero deve ser inteiro")
        elif(type == "NaN"):
            self.show_alert_box_callback("Alerta!", f"Valor inserido '{value}' invalido! Entrada deve ser um numero")
        elif(type == "int"):
            self.initial_state = value
            self.tape = verify_test_word_input(lines[6], self.main_alphabet, self.aux_alphabet, self.start_symbol, self.blank_symbol)
            if(self.tape is not None):
                self.verify_transition_table_input(lines)
            else:
                self.show_alert_box_callback("Alerta!", f"Palavra invalida! Simbolos inseridos que nao estao nos alfabetos!")
            
    def verify_transition_table_input(self, lines):
        self.transition_array = [[Transition.simplified(False) for _ in range((self.main_alphabet_size + self.aux_alphabet_size + 2))] for _ in range(self.number_of_states)]
        
        table_header = self.main_alphabet_list + self.aux_alphabet_list
        table_header.append(self.start_symbol)
        table_header.append(self.blank_symbol)
        
        encountered_error = False
        
        if(len(lines)>(7+self.number_of_states)):
            self.show_alert_box_callback("Alerta!", f"Tabela de transicao invalida! Existem mais estados do que previamente definido!")
            encountered_error = True
        elif(len(lines)<(7+self.number_of_states)):
            self.show_alert_box_callback("Alerta!", f"Tabela de transicao invalida! Existem estados indefinidos!")
            encountered_error = True
        
        if(not encountered_error):
            final_state_exists = False
            
            for i in range(self.number_of_states):
                encountered_error = False
                
                row = lines[7+i].split(',')
                
                if(len(row)<(self.main_alphabet_size + self.aux_alphabet_size + 3)):
                    self.show_alert_box_callback("Alerta!", f"Tabela de transicao invalida! Estado 'S[{i}]' nao tem todas suas regras de transicoes definidas!")
                    encountered_error = True
                    break
                
                is_final = False
                if(row[0].lower() != 't' and row[0].lower() != 'f'):
                    self.show_alert_box_callback("Alerta!", f"Tabela de transicao invalida! O primeiro valor de cada linha deve ser T ou F declarando se o estado é final ou não!")
                    encountered_error = True
                    break
                elif(row[0].lower() == 't'):
                    final_state_exists = True
                    is_final = True
                
                for j in range(1, self.main_alphabet_size + self.aux_alphabet_size + 3):
                    if(row[j] == ''):
                        self.show_alert_box_callback("Alerta!", f"Transicao '{i,(j-1)}' nao foi preenchida!")
                        encountered_error = True
                        break
                    elif(row[j].lower() == 'x'):
                        self.transition_array[i][j-1] = Transition.simplified(is_final)
                    else:
                        parameters = []
                        for parameter in row[j]:
                            parameters.append(parameter)
                        
                        if(len(parameters)<3):
                            self.show_alert_box_callback("Alerta!", f"Transicao '{i,(j-1)}' nao foi preenchida corretamente, faltando parametros!")
                            encountered_error = True
                            break
                        
                        number_digits = 0
                        number_string = ""
                        for char in parameters:
                            if char.isdigit():
                                number_digits += 1
                                number_string += char
                            else:
                                break
                        
                        if(number_digits==0):
                            self.show_alert_box_callback("Alerta!", f"Notacao invalida na transicao '{i,(j-1)}'. O primeiro valor deve ser o estado futuro.")
                            encountered_error = True
                            break
                        
                        next_state = int(number_string)
                        
                        if(next_state>(self.number_of_states-1)):
                            self.show_alert_box_callback("Alerta!", f"Estado futuro invalido na transicao '{i,(j-1)}'! Uma transicao deve apontar para um estado existente.")
                            encountered_error = True
                            break
                        
                        if(replacement_letter_valid(parameters[number_digits], self.main_alphabet, self.aux_alphabet, self.start_symbol, self.blank_symbol)):
                            replacement_letter = parameters[number_digits]
                        else:
                            self.show_alert_box_callback("Alerta!", f"Notacao invalida na transicao '{i,j}'. O segundo valor nao esta contido nos alfabetos estabelecidos anteriormente.")
                            encountered_error = True
                            break
                        
                        if(direction_letter_valid(parameters[number_digits+1])):
                            direction = parameters[number_digits+1]
                        else:
                            self.show_alert_box_callback("Alerta!", f"Notacao invalida na transicao '{i,j}'. O terceiro valor deve ser 'L' ou 'R' para a direcao.")
                            encountered_error = True
                            break
                        
                        if(len(parameters)>number_digits+2):
                            self.show_alert_box_callback("Alerta!", f"Notacao invalida na transicao '{i,(j-1)}'! Apenas 3 parametros sao aceitos, [NUMERO][TROCA][DIRECAO].")
                            encountered_error = True
                            break
                        
                        current_state = i
                        current_letter = table_header[j-1]
                        
                        self.transition_array[i][j-1] = Transition(current_state, next_state, current_letter, replacement_letter, direction, is_final)
                
                if(encountered_error):
                    break
            
        if(not encountered_error):   
            if(not final_state_exists):
                self.show_alert_box_callback("Alerta!", f"Tabela de transicao sem estado final!")
                encountered_error = True
            
            if(not encountered_error):
                result_tape, result_text, transition_log = run_turing_machine(self.transition_array, self.tape, self.initial_state, self.main_alphabet_size, self.aux_alphabet_size)
                
                self.tape_result_scroll_area.setVisible(True)
                self.tape_result_value.setText(''.join(result_tape) + "\n\n" + result_text)
                self.test_word_output_value.setText(''.join(transition_log))