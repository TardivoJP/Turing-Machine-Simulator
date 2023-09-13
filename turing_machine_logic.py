def run_turing_machine(transition_array, tape, initial_state, main_alphabet_size, aux_alphabet_size):
    tape_pointer = 1
    current_state = initial_state
    transition_log = []
    result_text = None
    
    while True:
        is_stuck = True
        is_current_state_final = False
        out_of_bounds_error = False
        
        if(transition_array[current_state][0].is_final):
            is_current_state_final = True
        
        for j in range(main_alphabet_size + aux_alphabet_size + 2):
            if(transition_array[current_state][j].current_state != -1):
                if(tape[tape_pointer]==transition_array[current_state][j].current_letter):
                    transition_log.append("Trocou '"+tape[tape_pointer]+"' com '"+transition_array[current_state][j].current_letter+"'. Agora movendo-se '"+(transition_array[current_state][j].direction.upper())+"' para o estado '"+str(transition_array[current_state][j].next_state)+"'\n")
                    tape[tape_pointer]=transition_array[current_state][j].replacement_letter
                    
                    if(transition_array[current_state][j].direction.lower() == 'l'):
                        if((tape_pointer - 1) < 0):
                            out_of_bounds_error = True
                            break
                        else:
                            tape_pointer -= 1
                    else:
                        if((tape_pointer + 1) >= len(tape)):
                            out_of_bounds_error = True
                            break
                        else:
                            tape_pointer += 1
                    
                    current_state = transition_array[current_state][j].next_state
                    is_stuck = False
                    break
        
        if(out_of_bounds_error):
            result_text = "Palavra nao aceita! Ponteiro fora do escopo da fita!"
            break
        elif(is_stuck and is_current_state_final and tape_pointer == 1):
            result_text = "Palavra aceita!"
            break
        elif(is_stuck and is_current_state_final):
            result_text = "Palavra nao aceita! Ponteiro nao esta na posicao inicial!"
            break
        elif(is_stuck):
            result_text = "Palavra nao aceita! Estado sem saida!"
            break
    
    return tape, result_text, transition_log