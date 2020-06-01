"""
Final Exam: Part 2 (25-05-2020)
Turing Machine Interpreter.
"""

__author__ = "Danis Alukaev"
__email__ = "d.alukaev@innopolis.university"
__copyright__ = "2020, BS19-02"
__version__ = "1.1.0"

import re


class Tape:
    def __init__(self):
        # set the first symbol in tape that is Z_0
        self.tape = ['Z']
        # set the pointer
        self.head = 0

    def write_symbol(self, symbol):
        # write symbol in cell to which head points
        self.tape[self.head] = symbol

    def current_mem_symbol(self):
        # return the symbol to which head points
        return self.tape[self.head]

    def head_right(self):
        # move head to right
        self.head += 1
        self.tape.append('')

    def head_left(self):
        # move head to left
        self.head -= 1

    def head_still(self):
        # stay on the same cell
        pass


class TuringMachine:
    def __init__(self, states, input_language, memory_alphabet, transitions, initial_state, final_states):
        # define the components of TM
        self.states = states
        self.input_alphabet = input_language
        self.memory_alphabet = memory_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        self.tape = Tape()  # create memory tape

    def accept(self, string):
        input = list(string)  # transform string to sequence of symbols (it used instead of input tape)
        input.append('')  # define the end of sequence
        head = 0  # set pointer to input tape
        current_state = self.initial_state  # start with initial state
        while current_state not in final_states:
            # while we didn't reach final state
            symbol = input[head]  # get input symbol
            # print current configuration
            result.write(current_state + ', ' + string[0:head] + '^' + string[head:] + ', ' +
                         ''.join(self.tape.tape[0:self.tape.head]) + '^' + ''.join(
                self.tape.tape[self.tape.head:]) + '\n')
            if symbol == '':
                # replace the empty string by underscore
                symbol = '_'
            if (input[0] == '0' and string.split('#')[0].find('1') != -1) or (
                    string.split('#')[1][0] == '0' and string.split('#')[1].find('1') != -1):
                # if there exist leading zero
                result.write(current_state + ', ' + string[0:head] + '^' + string[head:] + ', ' +
                             ''.join(self.tape.tape[0:self.tape.head]) + '^' + ''.join(
                    self.tape.tape[self.tape.head:]) + '\n')
                result.write('NO')
                exit(0)
            if self.tape.current_mem_symbol() != '':
                # if head in memory tape does not point to empty symbol
                transition = self.transitions.get((current_state, symbol, self.tape.current_mem_symbol()))
            else:
                # else we use underscore as empty symbol
                transition = self.transitions.get((current_state, symbol, '_'))
            if current_state in final_states:
                # we reach final state
                result.write('YES')
                exit(0)
            if transition is None:
                # such transition does not exist
                result.write(current_state + ', ' + string[0:head] + '^' + string[head:] + ', ' +
                             ''.join(self.tape.tape[0:self.tape.head]) + '^' + ''.join(
                    self.tape.tape[self.tape.head:]) + '\n')
                result.write('NO')
                exit(0)
            current_state = transition[0]  # update current state
            if transition[1] != '_':
                # if symbol in memory tape is not empty
                self.tape.write_symbol(transition[1])
            else:
                self.tape.write_symbol('')
            # move the head of input tape accordingly to transition
            if transition[2] == 'R':
                head += 1
            elif transition[2] == 'L':
                head -= 1
            elif transition[2] == 'S':
                pass
            # move the head of memory tape accordingly to transition
            if transition[3] == 'R':
                self.tape.head_right()
            elif transition[3] == 'L':
                self.tape.head_left()
            elif transition[3] == 'S':
                self.tape.head_still()
        # print final configuration
        result.write(current_state + ', ' + string[0:head] + '^' + string[head:] + ', ' +
                     ''.join(self.tape.tape[0:self.tape.head]) + '^' + ''.join(self.tape.tape[self.tape.head:]) + '\n')
        if current_state not in self.final_states:
            # check that TM finish in final state
            result.write('NO')
            exit(0)
        else:
            result.write('YES')
            exit(0)


"""
===========================================================================
                                MAIN
===========================================================================
"""
if __name__ == "__main__":
    file = open('input.txt', 'r')  # an input file
    result = open('output.txt', 'w+')  # an output file
    description = file.readlines()  # convert IO strings to the list
    # define the Turing Machine
    states = ['q0', 'q1', 'q2', 'q3', 'q4']
    input_language = ['0', '1', '#']
    memory_alphabet = ['0', '1']
    transitions = {('q0', '0', 'Z'): ('q0', 'Z', 'S', 'R'), ('q0', '1', 'Z'): ('q0', 'Z', 'S', 'R'),
                   ('q0', '0', '_'): ('q0', '0', 'R', 'R'), ('q0', '1', '_'): ('q0', '1', 'R', 'R'),
                   ('q0', '#', '_'): ('q1', '_', 'R', 'L'),
                   ('q1', '1', '1'): ('q1', '1', 'R', 'L'), ('q1', '0', '0'): ('q1', '0', 'R', 'L'),
                   ('q1', '1', '0'): ('q1', '0', 'R', 'L'), ('q1', '0', '1'): ('q1', '1', 'R', 'L'),
                   ('q1', '_', '1'): ('q4', '1', 'S', 'S'), ('q1', '_', '0'): ('q4', '0', 'S', 'S'),
                   ('q1', '_', 'Z'): ('q2', 'Z', 'L', 'S'),
                   ('q2', '0', 'Z'): ('q2', 'Z', 'L', 'S'), ('q2', '1', 'Z'): ('q2', 'Z', 'L', 'S'),
                   ('q2', '#', 'Z'): ('q3', 'Z', 'R', 'R'),
                   ('q3', '0', '0'): ('q3', '0', 'R', 'R'), ('q3', '1', '1'): ('q3', '1', 'R', 'R'),
                   ('q3', '0', '1'): ('q4', '1', 'S', 'S')}
    initial_states = 'q0'
    final_states = ['q4']
    tm = TuringMachine(states, input_language, memory_alphabet, transitions, initial_states, final_states)

    # check whether input is valid
    if re.search(r'(1[01]*|[0]+)#(1[01]*|[0]+)', description[0]) is None:
        result.write('Invalid input')
    elif len(re.search(r'(1[01]*|[0]+)#(1[01]*|[0]+)', description[0]).group(0)) != len(description[0]):
        result.write('Invalid input')
    else:
        # check the acceptance of string
        tm.accept(description[0])
