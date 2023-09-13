def input_parsing(value):
    try:
        parsed_value = float(value)
        if parsed_value.is_integer():
            return int(parsed_value), "int"
        else:
            return parsed_value, "float"
    except ValueError:
        return value, "NaN"

def verify_test_word_input(word, main_alphabet, aux_alphabet, start_symbol, blank_symbol):
    is_word_valid = True
    
    word = start_symbol + word
    while(len(word)<50):
        word = word + blank_symbol
    
    tape = []
    for letter in word:
        if(replacement_letter_valid(letter, main_alphabet, aux_alphabet, start_symbol, blank_symbol)):
            tape.append(letter)
        else:
            is_word_valid = False
            break
        
    if(is_word_valid):
        return tape
    else:
        return None
        
def replacement_letter_valid(letter, main_alphabet, aux_alphabet, start_symbol, blank_symbol):
    if(main_alphabet.__contains__(letter) or aux_alphabet.__contains__(letter) or letter == start_symbol or letter == blank_symbol):
        return True
    else:
        return False

def direction_letter_valid(letter):
    if(letter.lower() == 'l' or letter.lower() == 'r'):
        return True
    else:
        return False