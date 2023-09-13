from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QCheckBox, QScrollArea
from PyQt6.QtGui import QGuiApplication
from transition import Transition
from input_verification import verify_test_word_input, replacement_letter_valid, direction_letter_valid
from turing_machine_logic import run_turing_machine

class CustomLineEdit(QLineEdit):
    def __init__(self, transition_table, i, j, parent=None):
        super().__init__(parent)
        self.transition_table = transition_table
        self.i = i
        self.j = j

class TransitionTableScreen(QWidget):
    def __init__(self, number_of_states, main_alphabet_size, main_alphabet, main_alphabet_list, aux_alphabet_size, aux_alphabet, aux_alphabet_list, start_symbol, blank_symbol, show_welcome_screen_callback, center_on_screen_callback, show_alert_box_callback):
        super().__init__()
        
        self.show_welcome_screen_callback = show_welcome_screen_callback
        self.center_on_screen_callback = center_on_screen_callback
        self.show_alert_box_callback = show_alert_box_callback
        
        self.number_of_states = number_of_states
        self.main_alphabet_size = main_alphabet_size
        self.main_alphabet = main_alphabet
        self.main_alphabet_list = main_alphabet_list
        self.aux_alphabet_size = aux_alphabet_size
        self.aux_alphabet = aux_alphabet
        self.aux_alphabet_list = aux_alphabet_list
        self.start_symbol = start_symbol
        self.blank_symbol = blank_symbol
        self.transition_array = [[Transition.simplified(False) for _ in range((self.main_alphabet_size + self.aux_alphabet_size + 2))] for _ in range(self.number_of_states)]
        self.transition_inputs = {}
        self.initial_state = None
        
        ## Screen dimensions
        screen = QGuiApplication.primaryScreen()
        screen_size = screen.availableSize()
        
        ## Master Layout
        self.master_layout = QVBoxLayout()
        
        self.transition_table_screen_scroll_area = QScrollArea()
        self.transition_table_screen_scroll_area.setWidgetResizable(True)
        self.transition_table_screen_scroll_area.setMinimumWidth(int(screen_size.width() * 0.70))
        self.transition_table_screen_scroll_area.setMinimumHeight(int(screen_size.height() * 0.70))
        
        self.transition_table_screen_container = QWidget()
        self.transition_table_screen_layout = QVBoxLayout()
        self.transition_table_screen_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        ## Manual Input Screen Header
        self.transition_table_screen_label = QLabel("<h2>Tabela de transicoes</h2>")
        self.transition_table_screen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.transition_table_screen_layout.addWidget(self.transition_table_screen_label)
        
        
        ## Number of states input
        self.transition_table_content_container = QWidget()
        
        ## Setting up the transion table with a grid layout
        self.transition_table_content_layout = QGridLayout()
        self.transition_table_content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ## Setting up the header for the first column with the state names
        transition_table_header = QLabel("Estados")
        self.transition_table_content_layout.addWidget(transition_table_header, 0, 0)
        
        ## Setting up the alphabet headers sequentially (this is why the lists were important)
        count = 1
        for i in range(len(self.main_alphabet_list)):
            transition_table_header = QLabel(self.main_alphabet_list[i])
            transition_table_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.transition_table_content_layout.addWidget(transition_table_header, 0, count)
            count += 1
            
        for i in range(len(self.aux_alphabet_list)):
            transition_table_header = QLabel(self.aux_alphabet_list[i])
            transition_table_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.transition_table_content_layout.addWidget(transition_table_header, 0, count)
            count += 1
        
        ## Setting up the headers for the starting and blank symbols    
        transition_table_header = QLabel(self.start_symbol)
        transition_table_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.transition_table_content_layout.addWidget(transition_table_header, 0, count)
        
        transition_table_header = QLabel(self.blank_symbol)
        transition_table_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.transition_table_content_layout.addWidget(transition_table_header, 0, count+1)
        
        ## Setting up the headers that will allow the user to pick which states are final and the initial state
        transition_table_header = QLabel("Estado Inicial?")
        transition_table_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.transition_table_content_layout.addWidget(transition_table_header, 0, count+2)
        
        transition_table_header = QLabel("Estado Final?")
        transition_table_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.transition_table_content_layout.addWidget(transition_table_header, 0, count+3)
        
        ## Filling the table with input fields where applicable
        for i in range(self.number_of_states):
            for j in range(self.main_alphabet_size + self.aux_alphabet_size + 2):
                transition_table_input = CustomLineEdit(self,i,j)
                transition_table_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
                transition_table_input.setPlaceholderText(f"{i},{j}")
                self.transition_table_content_layout.addWidget(transition_table_input, i+1, j+1)
                self.transition_inputs[(i, j)] = transition_table_input
        
        ## Filling the first column with state name labels and the final two columns with check boxes
        count = 1  
        for i in range(self.number_of_states):
            transition_table_states_label = QLabel(f"S[{count-1}]")
            transition_table_states_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.transition_table_content_layout.addWidget(transition_table_states_label, count, 0)
            
            self.transition_table_content_layout.addWidget(QCheckBox(), count, (self.main_alphabet_size + self.aux_alphabet_size + 3), alignment=Qt.AlignmentFlag.AlignCenter)
            self.transition_table_content_layout.addWidget(QCheckBox(), count, (self.main_alphabet_size + self.aux_alphabet_size + 4), alignment=Qt.AlignmentFlag.AlignCenter)
            count += 1
        
        self.transition_table_content_container.setLayout(self.transition_table_content_layout)
        self.transition_table_screen_layout.addWidget(self.transition_table_content_container)  
                    
        
        ## Confirm button
        self.transition_table_confirm_button = QPushButton("Confirmar")
        self.transition_table_confirm_button.clicked.connect(self.verify_table_integrity)
        self.transition_table_screen_layout.addWidget(self.transition_table_confirm_button)
        
        
        ## Back button
        self.transition_table_back_button = QPushButton("Voltar")
        self.transition_table_back_button.clicked.connect(self.show_welcome_screen_callback)
        self.transition_table_screen_layout.addWidget(self.transition_table_back_button)
        
        
        ## Test word input
        self.test_word_input_container = QWidget()
        self.test_word_input_container.setVisible(False)
        self.test_word_input_layout = QHBoxLayout()
        
        self.test_word_input_label = QLabel("Palavra: ")
        self.test_word_input_layout.addWidget(self.test_word_input_label)
        
        self.test_word_input_input = QLineEdit()
        self.test_word_input_input.setPlaceholderText(f"Insira uma palavra para ser testada")
        self.test_word_input_layout.addWidget(self.test_word_input_input)
        
        self.test_word_input_confirm_button = QPushButton("Confirmar")
        self.test_word_input_confirm_button.clicked.connect(self.check_word_and_run_machine)
        self.test_word_input_layout.addWidget(self.test_word_input_confirm_button)
        
        self.test_word_input_container.setLayout(self.test_word_input_layout)
        self.transition_table_screen_layout.addWidget(self.test_word_input_container)
        
        ## Result scroll area
        self.tape_result_scroll_area = QScrollArea()
        self.tape_result_scroll_area.setVisible(False)
        self.tape_result_scroll_area.setWidgetResizable(True)
        self.tape_result_scroll_area.setMinimumHeight(int(screen_size.height() * 0.50))
        
        self.tape_result_layout_container = QWidget()
        self.tape_result_layout = QVBoxLayout()
        self.tape_result_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ## Test word tape result        
        self.tape_result_label = QLabel("<h3>Resultado da fita</h3>")
        self.tape_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tape_result_layout.addWidget(self.tape_result_label)
        self.tape_result_layout.addSpacing(10)
        
        self.tape_result_value = QLabel()
        self.tape_result_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tape_result_layout.addWidget(self.tape_result_value)
        self.tape_result_layout.addSpacing(20)
        
        
        ## Test word output
        self.test_word_output_label = QLabel("<h3>Transicoes realizadas</h3>")
        self.test_word_output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tape_result_layout.addWidget(self.test_word_output_label)
        self.tape_result_layout.addSpacing(10)
        
        self.test_word_output_value = QLabel()
        self.test_word_output_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tape_result_layout.addWidget(self.test_word_output_value)
        
        
        self.tape_result_layout_container.setLayout(self.tape_result_layout)
        self.tape_result_scroll_area.setWidget(self.tape_result_layout_container)
        self.transition_table_screen_layout.addWidget(self.tape_result_scroll_area)
        
        
        self.transition_table_screen_container.setLayout(self.transition_table_screen_layout)
        self.transition_table_screen_scroll_area.setWidget(self.transition_table_screen_container)
        
        self.master_layout.addWidget(self.transition_table_screen_scroll_area)
        
        self.setLayout(self.master_layout)
        
        if not self.isMaximized:
            QTimer.singleShot(0, self.center_on_screen_callback)
        
    def find_transition_input(self, i, j):
        return self.transition_inputs.get((i, j))
    
    def verify_table_integrity(self):
        encountered_error = False
        starting_state_exists = False
        final_state_exists = False
        
        for i in range(self.number_of_states):
            is_final = False
            
            if((self.transition_table_content_layout.itemAtPosition((i+1), (self.main_alphabet_size + self.aux_alphabet_size + 3))).widget().isChecked()):
                if(not starting_state_exists):
                    starting_state_exists = True
                    self.initial_state = i
                else:
                    self.show_alert_box_callback("Alerta!", f"Apenas um estado inicial e permitido!")
                    encountered_error = True
                    self.initial_state = None
                    break
            
            if((self.transition_table_content_layout.itemAtPosition((i+1), (self.main_alphabet_size + self.aux_alphabet_size + 4))).widget().isChecked()):
                final_state_exists = True
                is_final = True
            
            for j in range(self.main_alphabet_size + self.aux_alphabet_size + 2):
                if(self.find_transition_input(i, j).text() == ''):
                    self.show_alert_box_callback("Alerta!", f"Transicao '{i,j}' nao foi preenchida!")
                    encountered_error = True
                    break
                elif(self.find_transition_input(i, j).text().lower() == 'x'):
                    self.transition_array[i][j] = Transition.simplified(is_final)
                else:
                    parameters = []
                    for parameter in self.find_transition_input(i, j).text():
                        parameters.append(parameter)
                    
                    if(len(parameters)<3):
                        self.show_alert_box_callback("Alerta!", f"Transicao '{i,j}' nao foi preenchida corretamente, faltando parametros!")
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
                        self.show_alert_box_callback("Alerta!", f"Notacao invalida na transicao '{i,j}'. O primeiro valor deve ser o estado futuro.")
                        encountered_error = True
                        break
                    
                    next_state = int(number_string)
                    
                    if(next_state>(self.number_of_states-1)):
                        self.show_alert_box_callback("Alerta!", f"Estado futuro invalido na transicao '{i,j}'! Uma transicao deve apontar para um estado existente.")
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
                        self.show_alert_box_callback("Alerta!", f"Notacao invalida na transicao '{i,j}'! Apenas 3 parametros sao aceitos, [NUMERO][TROCA][DIRECAO].")
                        encountered_error = True
                        break
                    
                    current_state = i
                    current_letter = (self.transition_table_content_layout.itemAtPosition(0, (j+1))).widget().text()
                    
                    self.transition_array[i][j] = Transition(current_state, next_state, current_letter, replacement_letter, direction, is_final)
            
            if(encountered_error):
                break
        
        if(not encountered_error):
            if(not starting_state_exists):
                self.show_alert_box_callback("Alerta!", f"Tabela de transicao sem estado inicial!")
                encountered_error = True
                
            if(not final_state_exists):
                self.show_alert_box_callback("Alerta!", f"Tabela de transicao sem estado final!")
                encountered_error = True
            
            if(not encountered_error):
                self.transition_table_confirm_button.setVisible(False)
                for i in range(self.number_of_states):
                    self.transition_table_content_layout.itemAtPosition((i+1), (self.main_alphabet_size + self.aux_alphabet_size + 3)).widget().setDisabled(True)
                    self.transition_table_content_layout.itemAtPosition((i+1), (self.main_alphabet_size + self.aux_alphabet_size + 4)).widget().setDisabled(True)
                    for j in range(self.main_alphabet_size + self.aux_alphabet_size + 2):
                        self.find_transition_input(i, j).setDisabled(True)
                        
                self.test_word_input_container.setVisible(True)
    
    def check_word_and_run_machine(self):
        self.tape = verify_test_word_input(self.test_word_input_input.text(), self.main_alphabet, self.aux_alphabet, self.start_symbol, self.blank_symbol)
        
        if(self.tape is not None):
            result_tape, result_text, transition_log = run_turing_machine(self.transition_array, self.tape, self.initial_state, self.main_alphabet_size, self.aux_alphabet_size)
            self.tape_result_scroll_area.setVisible(True)
            self.tape_result_value.setText(''.join(result_tape) + "\n\n" + result_text)
            self.test_word_output_value.setText(''.join(transition_log))
        else:
            self.show_alert_box_callback("Alerta!", f"Palavra invalida! Simbolos inseridos que nao estao nos alfabetos!")