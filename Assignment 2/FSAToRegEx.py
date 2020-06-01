""" FSA to RegExp Translator.

For a given in the <fsa.txt> FSA description the program outputs the <result.txt> that contains an error
description or a regular expression that corresponds to the given FSA. The regular expression built
according to the Kleene’s algorithm.
"""

__author__ = "Danis Alukaev"
__email__ = "d.alukaev@innopolis.university"
__copyright__ = "2020, BS19-02"
__version__ = "1.1.0"
__status__ = "Submitted"


def error(id, argument=""):
    """
    The function generates and outputs an error description.

    :param id: an error code.
    :param argument: a state or a transition, which caused the error.
    """

    result.write("Error:\n")
    if id == 1:
        result.write("E1: A state '" + argument + "' is not in the set of states\n")
    elif id == 2:
        result.write("E2: Some states are disjoint\n")
    elif id == 3:
        result.write("E3: A transition '" + argument + "' is not represented in the alphabet\n")
    elif id == 4:
        result.write("E4: Initial state is not defined\n")
    elif id == 5:
        result.write("E5: Input file is malformed\n")
    elif id == 6:
        result.write("E6: FSA is nondeterministic\n")
    exit(0)


def string_validator(string, type=0):
    """
    The function checks whether the string tokens are valid.

    :param string: a string to be considered.
    :param type: a variable that specifies domain of verification (type - 0 for state titles, 1 - for a component
                 of an alphabet).
    :return: True if the string consists of characters that belong to the domain defined below, False - otherwise.
    """

    valid = True
    if type == 0:
        # received string is the state title
        # should consists of tokens 'a'-'z', 'A'-'Z', '0'-'9'
        for letter in string:
            if not (letter >= "a" and letter <= "z" or
                    letter >= "A" and letter <= "Z" or
                    letter >= "0" and letter <= "9") or \
                    letter == "":
                valid = False
                break
    elif type == 1:
        # received string is the component of an alphabet
        # should consists of tokens 'a'-'z', 'A'-'Z', '0'-'9', '_'
        for letter in string:
            if not (letter >= "a" and letter <= "z" or
                    letter >= "A" and letter <= "Z" or
                    letter >= "0" and letter <= "9" or
                    letter == "_"):
                valid = False
                break
    return valid


def dfs(graph, current_vertex, visited):
    """
    The Depth First Search implementation - used to check whether states of FSA are not reachable from a current state.

    :param graph: a graph to be traversed.
    :param current_vertex: a starting vertex to define the reachability of the rest of the vertexes.
    :param visited: a list of discovered vertexes.
    :return: an updated list of discovered vertexes.
    """

    if current_vertex not in visited:
        visited.append(current_vertex)
    for state in states:
        if state not in visited and graph[states.index(current_vertex)][states.index(state)] == 1:
            dfs(graph, state, visited)
    return visited


def compute_regex(i, j, k):
    """
    The function generates a RegEx on the k-th step using the Kleene's algorithm recurrence
    relation defined as:
                R^{k}_{ij} = (R^{k-1}_{ik})(R^{k-1}_{kk})*(R^{k-1}_{kj})|(R_{k-1}_{ij}).

    :param i: an index of the first state.
    :param j: an index of the second state.
    :param k: a current step.
    :return: a string with the following structure:
                '('R^{k-1}_{ik}')('R^{k-1}_{kk}')*('R^{k-1}_{kj}')|('R_{k-1}_{ij}')'.
    """

    return "(" + str(intermediate_results[i][k]) + ")(" + str(intermediate_results[k][k]) + ")*(" + str(
        intermediate_results[k][j]) + ")|(" + str(intermediate_results[i][j]) + ")"


"""
===========================================================================
                        VARIABLE INITIALIZATION
===========================================================================
"""

description = open('fsa.txt', 'r')  # an input file
result = open('result.txt', 'w+')  # an output file
description_lines = description.readlines()  # convert IO strings to the list

states = []  # states=[s1,s2,...] // s1 , s2, ... ∈ latin letters, words and numbers
alphabet = []  # alpha=[a1,a2,...] // a1 , a2, ... ∈ latin letters, words, numbers and character '_’(underscore)
initial_state = ''  # init.st=[s] // s ∈ states
final_states = []  # fin.st=[s1,s2,...] // s1, s2 ∈ states
transitions = []  # trans={s1>a>s2,...] // s1,s2,...∈ states; a ∈ alpha
intermediate_results = []  # stores intermediate regular expressions

"""
===========================================================================
                            INPUT + ERROR 5
===========================================================================
"""

if len(description_lines) == 5:  # the file should consists 5 lines
    for line in description_lines:  # iterates over the lines of an input file
        if description_lines.index(line) == 0:
            # the first line denotes a list of states
            line = line.replace(" ", "")
            if line[0:8] != "states=[" or line[-2:] != "]\n":
                # check whether the line has an improper format: states=[...]
                error(5)
            else:
                line = line[8:]  # remove 'states=['
                line = line[:(len(line) - 2)]  # remove ']\n'
                states = line.split(",")  # split line by a comma
                for state in states:
                    if not string_validator(state, 0):
                        # check whether the state consists of valid symbols
                        error(5)
                print("states:  ", states)
        elif description_lines.index(line) == 1:
            # the second line denotes an alphabet
            line = line.replace(" ", "")
            if line[0:7] != "alpha=[" or line[-2:] != "]\n":
                # check whether the line has an improper format: alpha=[...]
                error(5)
            else:
                line = line[7:]  # remove 'alpha=['
                line = line[:(len(line) - 2)]  # remove ']\n'
                alphabet = line.split(",")  # split line by a comma
                for alpha in alphabet:
                    if not string_validator(alpha, 1):
                        # check whether an alphabet consists of valid symbols
                        error(5)
                print("alphabet: ", alphabet)
        elif description_lines.index(line) == 2:
            # the third line denotes the initial state
            line = line.replace(" ", "")
            if line[0:9] != "init.st=[" or line[-2:] != "]\n":
                # check whether the line has an improper format: init.st=[...]
                error(5)
            else:
                line = line[9:]  # remove 'init.st=['
                line = line[:(len(line) - 2)]  # remove ']\n'
                initial_state = line
                print("initial state: ", initial_state)
        elif description_lines.index(line) == 3:
            # the fourth line denotes final states
            line = line.replace(" ", "")
            if line[0:8] != "fin.st=[" or line[-2:] != "]\n":
                # check whether the line has an improper format: fin.st=[...]
                error(5)
            else:
                line = line[8:]  # remove 'fin.st=['
                line = line[:(len(line) - 2)]  # remove ']\n'
                final_states = line.split(",")  # split line by a comma
                print("final states: ", final_states)
        elif description_lines.index(line) == 4:
            # the fifth line denotes the list of transitions
            line = line.replace(" ", "")
            if line[0:7] != "trans=[" or line[-2:] != "]\n" and line[-1:] != "]":
                # check whether the line has an improper format: trans=[...]
                error(5)
            else:
                line = line[7:]  # remove 'trans=['
                if line[-2:] == "]\n":
                    line = line[:(len(line) - 2)]  # remove ']\n'
                elif line[-1:] == "]":
                    line = line[:(len(line) - 1)]  # remove ']'
                else:
                    error(5)
                temp = line.split(",")  # split line by a comma
                for state in temp:
                    elements = state.split(">")  # split the line by '>'
                    transitions.append(elements)
                if transitions != [[""]]:
                    for transition in transitions:
                        if not (len(transition) == 3 and string_validator(transition[0], 0) and string_validator(
                                transition[1], 1) and string_validator(transition[2], 0)):
                            #  a transition should consists of 3 elements, which are two states and component
                            #  of an alphabet; all of them should have proper format
                            error(5)
                print("transitions: ", transitions)
else:
    # an input file has more or less than 5 lines
    error(5)

"""
===========================================================================
                                  ERROR 4
===========================================================================
"""

if initial_state == "":
    # an initial state is not defined
    error(4)

"""
===========================================================================
                                  ERROR 1
===========================================================================
"""

if initial_state not in states:
    # an initial state is in the set of states
    error(1, initial_state)

# check whether final states are in the set of states
if final_states and final_states[0] != "":
    # if a set of final states is non-empty
    for state in final_states:
        if state not in states:
            error(1, state)

# check whether states mentioned in transitions are in the set of states
if not transitions == [[""]]:
    # there is at least one transition
    for transition in transitions:
        # check whether states q0, q1 of a current transition δ(q0,input)=q1 belong to a set of states
        if transition[0] not in states:
            # q0 not in the set of states
            error(1, transition[0])
        elif transition[2] not in states:
            # q1 not in the set of states
            error(1, transition[2])

"""
===========================================================================
                                  ERROR 3
===========================================================================
"""

if not transitions == [[""]]:
    # there is at least one transition
    for transition in transitions:
        if transition[1] not in alphabet:
            # if there is no such an input in alphabet
            error(3, transition[1])

"""
===========================================================================
                                  ERROR 2
===========================================================================
"""

visited = []  # the list of visited by dfs nodes
graph = []  # the list of FSA edges
if not transitions == [[""]]:
    # there is at least one transition

    # preparing positions for state connections
    for i in range(len(states)):
        graph.append([])
        for state in states:
            graph[i].append(0)
    # fill out the list of FSA edges with state connections
    for transition in transitions:
        # mark a connectivity from the state q0 to the q1 of a current transition δ(q0,input)=q1
        graph[states.index(transition[0])][states.index(transition[2])] = 1
        # mark a connectivity from the state q1 to the q0 of a current transition δ(q0,input)=q1
        graph[states.index(transition[2])][states.index(transition[0])] = 1
    visited = dfs(graph, initial_state, visited)
    for state in states:
        # if the state is not in visited, then states of FSA are disjoint
        if state not in visited:
            error(2)
    print("graph to test disjointment: ", graph)

"""
===========================================================================
                                  ERROR 6
===========================================================================
"""

if not transitions == [[""]]:
    # there is at least one transition
    for transition_1 in transitions:
        same_transitions = 0
        for transition_2 in transitions:
            if transition_1[:2] == transition_2[:2]:
                # if from the state there is transition with the same input
                same_transitions += 1
        if len(states) != 1 and same_transitions > 1:
            # if there are at least two transitions with the same element of an alphabet, then FSA is non-deterministic
            error(6)
            break

"""
===========================================================================
                            PRODUCING REGEXs
===========================================================================
"""
# check whether the FSA has no final states
if final_states == [""]:
    # the corresponding RegEx is ∅
    result.write("{}")
    exit(0)

# preparing positions for intermediate results
for i, state in enumerate(states):
    intermediate_results.append([])
    for j in states:
        # mark a position as undefined (use symbols "<", ">", which are not allowed in alphabet and states titles,
        # to avoid collisions)
        intermediate_results[i].append("<undefined>")

# perform the step with k = -1 (base case)
for transition in transitions:
    # let δ is the transition function: δ:S×Σ→S, i.e δ(q0,input)=q1 for some states q0 and q1
    source = states.index(transition[0])  # store the state q0
    target = states.index(transition[2])  # stare the state q1
    if (intermediate_results[source][target]) == "<undefined>":
        # found the first transition input for q0; add it to a preliminary RegEx
        intermediate_results[source][target] = str(transition[1])
    if (intermediate_results[source][target]) != "<undefined>":
        if str(transition[1]) not in intermediate_results[source][target]:
            # found an another transition input for q0; add it to a preliminary RegEx
            intermediate_results[source][target] = str(intermediate_results[source][target]) + "|" + str(transition[1])
        if transition[0] == transition[2]:
            # found the reflexive transition, i.e. δ(q0,input)=q0
            if "|eps" in intermediate_results[source][target]:
                # if epsilon already included - erase it
                intermediate_results[source][target] = intermediate_results[source][target].replace("|eps", "")
            # and place "eps" on the rightmost position
            intermediate_results[source][target] += "|eps"
# undefined element (with tag "<undefined>") can be either empty set or epsilon
epsilons = []  # list to store positions of elements that should be an epsilon
empty_sets = []  # list to store positions of elements that should be an empty set
for i, intermediate_result in enumerate(intermediate_results):
    for j, regex in enumerate(intermediate_result):
        if regex == "<undefined>":
            # found undefined element
            if i == j:
                # state should have the reflexive transition,
                # i.e. the transition δ(q0,epsilon)=q0 always exists
                epsilons.append([i, j])
            else:
                # the i-th state has no transitions to the j-th state
                empty_sets.append([i, j])
for epsilon in epsilons:
    # set the necessary element to an epsilon
    intermediate_results[epsilon[0]][epsilon[1]] = "eps"
for empty_set in empty_sets:
    # set the necessary element to an empty set
    intermediate_results[empty_set[0]][empty_set[1]] = "{}"
print(str(intermediate_results))

#  perform the steps with k ∈ [0,n-1], where n is the number of states
for k, state in enumerate(states):
    # create the list to store generated on the current step RegExs
    # buffer used to avoid data hazards, specifically the Write After Read (WAR) issue
    buffer = []
    for i, intermediate_result_i in enumerate(intermediate_results):
        for j, intermediate_result_j in enumerate(intermediate_results):
            # produce a RegEx for the state with indexes i, j on the current step k
            buffer.append(compute_regex(i, j, k))
    index = -1  # variable used to treat elements of the buffer container
    for i, intermediate_result_i in enumerate(intermediate_results):
        for j, intermediate_result_j in enumerate(intermediate_results):
            index += 1
            # copy the RegEx obtained on the current step k in list with intermediate results
            intermediate_results[i][j] = buffer[index]

for i, state in enumerate(final_states):
    # print the RegExs, which represent a language accepted by the FSA
    if i + 1 != len(final_states):
        # separate RegExs for each final state with '|' symbol
        result.write(intermediate_results[0][states.index(state)] + "|")
    else:
        # print the RegEx for the last final state
        result.write(intermediate_results[0][states.index(state)])
