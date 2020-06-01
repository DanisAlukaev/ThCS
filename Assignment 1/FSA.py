'''
FSA Validator Implementation
BS19-02 Alukaev Danis
'''


#  FUNCTIONS FOR ERRORS AND WARNINGS NOTIFICATION
def error(id, argument=0):  # id - error code, argument - state or transition that used for notification
    result.write('Error:\n')
    if id == 1:
        result.write("E1: A state '" + argument + "' is not in the set of states\n")
    elif id == 2:
        result.write('E2: Some states are disjoint\n')
    elif id == 3:
        result.write("E3: A transition '" + argument + "' is not represented in the alphabet\n")
    elif id == 4:
        result.write('E4: Initial state is not defined\n')
    elif id == 5:
        result.write('E5: Input file is malformed\n')
    exit(0)


def warning(id):  # id - code of warning
    if not warning_found:  # when FSA has more than one warning to notify
        result.write('Warning:\n')
    if id == 1:
        result.write('W1: Accepting state is not defined\n')
    elif id == 2:
        result.write('W2: Some states are not reachable from the initial state\n')
    elif id == 3:
        result.write('W3: FSA is nondeterministic\n')


#  TOKEN VALIDATOR
def string_validator(token, type=0):
    # token - state or component of alphabet, type - 0 for state and 1 for component of alphabet
    valid = True
    if type == 0:  # state, should consists of letters 'a'-'z', 'A'-'Z', '0'-'9'
        for letter in token:
            if not (
                    letter >= 'a' and letter <= 'z' or letter >= 'A' and letter <= 'Z' or letter >= '0' and letter <= '9') or letter == '':
                valid = False
                break
    elif type == 1:  # component of alphabet, should consists of letters 'a'-'z', 'A'-'Z', '0'-'9', '_'
        for letter in token:
            if not (
                    letter >= 'a' and letter <= 'z' or letter >= 'A' and letter <= 'Z' or letter >= '0' and letter <= '9' or letter == '_'):
                valid = False
                break
    return valid


#  DEPTH FIRST SEARCH
def dfs(graph, current_vertex, visited):
    # used to check whether states of FSA are not reachable from current vertex
    if current_vertex not in visited:
        visited.append(current_vertex)
    for state in states:
        if state not in visited and graph[states.index(current_vertex)][states.index(state)] == 1:
            dfs(graph, state, visited)
    return visited


#  VARIABLE INITIALIZATION
description = open('fsa.txt', 'r')  # input file
result = open('result.txt', 'w+')  # output file
description_lines = description.readlines()  # convert IO strings to list

states = []  # states=[s1,s2,...] // s1 , s2, ... ∈ latin letters, words and numbers
alphabet = []  # alpha=[a1,a2,...] // a1 , a2, ... ∈ latin letters, words, numbers and character '_’(underscore)
initial_state = ''  # init.st=[s] // s ∈ states
final_state = []  # fin.st=[s1,s2,...] // s1, s2 ∈ states
transitions = []  # trans={s1>a>s2,...] // s1,s2,...∈ states; a ∈ alpha

warning_found = False
warning1_found = False
#############################################################################
#                              INPUT + ERROR 5
if len(description_lines) == 5:  # file should consists 5 lines
    for line in description_lines:  # iterates over the lines of input file
        if description_lines.index(line) == 0:  # if current line is first that is list of states
            line = line.replace(' ', '')
            if line[0:8] != 'states=[' or line[-2:] != ']\n':  # check whether it has improper format: states=[...]
                error(5)
            else:
                line = line[8:]  # remove 'states=['
                line = line[:(len(line) - 2)]  # remove ']\n'
                states = line.split(',')  # split line by comma
                for state in states:
                    if not string_validator(state, 0):  # check whether state consists of proper symbols
                        error(5)
                print('states:  ', states)
        elif description_lines.index(line) == 1:  # if current line is second that is alphabet
            line = line.replace(' ', '')
            if line[0:7] != 'alpha=[' or line[-2:] != ']\n':  # check whether it has improper format: alpha=[...]
                error(5)
            else:
                line = line[7:]  # remove 'alpha=['
                line = line[:(len(line) - 2)]  # remove ']\n'
                alphabet = line.split(',')  # split line by comma
                for alpha in alphabet:
                    if not string_validator(alpha, 1):  # check whether alphabet consists of proper symbols
                        error(5)
                print('alphabet: ', alphabet)
        elif description_lines.index(line) == 2:  # if current line is third that is initial state
            line = line.replace(' ', '')
            if line[0:9] != 'init.st=[' or line[-2:] != ']\n':  # check whether it has improper format: init.st=[...]
                error(5)
            else:
                line = line[9:]  # remove 'init.st=['
                line = line[:(len(line) - 2)]  # remove ']\n'
                initial_state = line
                print('initial state: ', initial_state)
        elif description_lines.index(line) == 3:  # if current line is fourth that is list of final states
            line = line.replace(' ', '')
            if line[0:8] != 'fin.st=[' or line[-2:] != ']\n':  # check whether it has improper format: fin.st=[...]
                error(5)
            else:
                line = line[8:]  # remove 'fin.st=['
                line = line[:(len(line) - 2)]  # remove ']\n'
                final_state = line.split(',')  # split line by comma
                print('final states: ', final_state)
                if final_state == ['']:  # check whether FSA has no final states
                    warning1_found = True
        elif description_lines.index(line) == 4:  # if current line is fifth that is list of transitions
            line = line.replace(' ', '')
            if line[0:7] != 'trans=[' or line[-2:] != ']\n' and line[-1:] != ']':
                # check whether it has improper format: trans=[...]
                error(5)
            else:
                line = line[7:]  # remove 'trans=['
                if line[-2:] == ']\n':
                    line = line[:(len(line) - 2)]  # remove ']\n'
                elif line[-1:] == ']':
                    line = line[:(len(line) - 1)]  # remove ']'
                else:
                    error(5)
                temp = line.split(',')  # split line by comma
                for state in temp:
                    elements = state.split('>')  # split line by '>'
                    transitions.append(elements)
                if transitions != [['']]:
                    for transition in transitions:
                        if not (len(transition) == 3 and string_validator(transition[0], 0) and string_validator(
                                transition[1], 1) and string_validator(transition[2], 0)):
                            #  transition should consists of 3 elements that are two states and component of alphabet
                            #  all of them should have proper format
                            error(5)
                print('transitions: ', transitions)
else:  # if it has no 5 lines
    error(5)

#############################################################################
#                              ERROR 4

if initial_state == '':  # initial state is not defined
    error(4)

#############################################################################
#                              ERROR 1

# check whether initial state is in the set of state
if states.count(initial_state) == 0:
    error(1, initial_state)

# check whether final states are in the set of state
if final_state and final_state[0] != '':  # if set of final states is not empty
    for i in final_state:
        if states.count(i) == 0:
            error(1, i)

# check whether states mentioned in transitions are in the set of state
if not transitions == [['']]:
    for transition in transitions:
        for vertex in transition:
            if transition.index(vertex) == 0 or transition.index(vertex) == 2:
                # check elements of transition except component of alphabet
                if states.count(vertex) == 0:
                    error(1, vertex)

#############################################################################
#                              ERROR 3
if not transitions == [['']]:
    for transition in transitions:
        letter_in_alphabet = False
        for letter in alphabet:
            # check whether particular transition is in alphabet
            if transition[1] == letter:
                letter_in_alphabet = True
        if not letter_in_alphabet:
            # if there is no corresponding transitions in alphabet
            error(3, transition[1])

#############################################################################
#                              ERROR 2
visited = []  # list of visited by dfs nodes
graph = []  # list of FSA edges
# preparing positions for connections
if not transitions == [['']]:
    for i in range(len(states)):
        graph.append([])
        for j in range(len(states)):
            graph[i].append(0)
    # fill out the list with connections
    for transition in transitions:
        # mark connectivity from transition[0] to transition[2]
        graph[states.index(transition[0])][states.index(transition[2])] = 1
        # mark connectivity vice versa
        graph[states.index(transition[2])][states.index(transition[0])] = 1
    dfs(graph, initial_state, visited)
    # if some states are not in visited, then some states in FSA are disjoint
    for i in states:
        if i not in visited:
            error(2)
    print('graph to test disjointment: ', graph)

#############################################################################
#                              FSA IS COMPLETE/INCOMPLETE

incoming_edges = []  # list of all incoming transitions
outgoing_edges = []  # list of all outgoing transitions
transition_to_all_states = True
if not transitions == [['']]:
    # preparing positions for edges
    for i in range(len(states)):
        outgoing_edges.append([])
        for j in range(len(alphabet)):
            outgoing_edges[i].append(0)
    # fill out the list with outgoing edges
    for i in range(len(transitions)):
        outgoing_edges[states.index(transitions[i][0])][alphabet.index(transitions[i][1])] += 1
    # check whether there are transitions from all states with different elements of alphabet
    print('outgoing transitions: ', outgoing_edges)
    for i in range(len(states)):
        for j in range(len(alphabet)):
            if outgoing_edges[i][j] == 0:
                # if there are no transition from particular state
                transition_to_all_states = False
# if there are transitions from all states with different elements of alphabet
if transition_to_all_states:
    result.write('FSA is complete\n')
else:
    result.write('FSA is incomplete\n')

#############################################################################
#                              WARNING 1

# during input file parsing we already checked presence of final state
if warning1_found:
    warning(1)
    warning_found = True

#############################################################################
#                              WARNING 2

visited = []  # list of visited by dfs nodes
graph = []  # list of FSA edges
if not transitions == [['']]:
    # preparing positions for edges
    for i in range(len(states)):
        graph.append([])
        for j in range(len(states)):
            graph[i].append(0)
    # fill out the list with edges
    for transition in transitions:
        graph[states.index(transition[0])][states.index(transition[2])] = 1
    dfs(graph, initial_state, visited)
    # if some states are not in visited, then some states in FSA are not reachable from initial state
    for state in states:
        if state not in visited:
            warning(2)
            warning_found = True
    print('graph to test reachability from initial state: ', graph)

#############################################################################
#                              WARNING 3
if not transitions == [['']]:
    for transition_1 in transitions:
        same_transitions = 0
        for transition_2 in transitions:
            if transition_1[:2] == transition_2[:2]:
                # if from state there are several transitions with same element of alphabet
                same_transitions += 1
        if len(states) != 1 and same_transitions > 1:
            # if there at least two transitions with same element of alphabet then FSA is not deterministic
            warning(3)
            break
