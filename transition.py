class Transition:
    def __init__(self, current_state, next_state, current_letter, replacement_letter, direction, is_final):
        self.current_state = current_state
        self.next_state = next_state
        self.current_letter = current_letter
        self.replacement_letter = replacement_letter
        self.direction = direction
        self.is_final = is_final
    
    @classmethod
    def simplified(cls, is_final):
        return cls(-1, None, None, None, None, is_final)