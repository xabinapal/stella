from stella.core.automata import State, Epsilon

def transition_function(state, transitions, )

class NFA(object):
    def __init__(self):
        initial_state = State()
        self.state_count = 1
        self.states = {self.state_count: initial_state}
        self.transitions = {self.state_count: {}}
        self.last_operand
    
    def add_operand(self, value):
        self.last_operand = value

    def add_sub_nfa(self, nfa):
        self.last_operand = nfa

    def modify_last_operand(self, value):
        pass