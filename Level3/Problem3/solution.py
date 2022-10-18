def solution(transition_matrix, *args):
    """
    This function takes in a 2D list of non-negative integers, where each sublist represents a different state (call it
    state #(index of sublist) and each integer inside a sublist represents the number of times state #(index of sublist)
    has transitioned into state #(index of integer). The function returns an array of integers representing the
    probabilities of ending up in the terminal states, given that each non-terminal state will always lead to a terminal
    state. The array will contain the numerators of the probabilities in order of their terminal state number number and
    the last integer in the array will be the shared denominator of the numerators.
    """

    class Fraction:
        def __init__(self, n, d):
            self.numerator = n
            self.denominator = d

        def __add__(self, other):  # overload addition operator
            return Fraction(self.numerator * other.denominator + other.numerator * self.denominator,
                            self.denominator * other.denominator)

        def __iadd__(self, other):  # overload in-place addition operator
            return self.__add__(other)

        def __sub__(self, other):  # overload subtraction operator
            return Fraction(self.numerator * other.denominator - other.numerator * self.denominator,
                            self.denominator * other.denominator)

        def __isub__(self, other):  # overload in-place subtraction operator
            return self.__sub__(other)

        def __mul__(self, other):  # overload multiplication operator
            return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

        def __imul__(self, other):  # overload in-place multiplication operator
            return self.__mul__(other)

        def __div__(self, other):  # overload division operator
            return self * Fraction(other.denominator, other.numerator)

        def __idiv__(self, other):  # overload in-place division operator
            return self.__div__(other)

        def __nonzero__(self):  # This is Python 2's version of __bool__, which is called when we say "if Fraction"
            if self.numerator == 0:
                return False
            else:
                return True

        def __repr__(self):  # This will determine how the Fraction is displayed when we print the Fraction
            return '(' + str(self.numerator) + '/' + str(self.denominator) + ')'

        def reduce(self):
            # This Fraction will use Euclid's algorithm to find greatest common divisor and reduce fraction to most
            # simplified form
            if self.numerator == 0:
                return Fraction(0, 1)
            elif self.numerator == 1 or self.denominator == 1:
                # if 1 in numerator or denominator, it is in most simplified form already
                return self
            else:
                # Euclid's algorithm to find gcd of numerator and denimonator
                bigger = max(self.numerator, self.denominator)
                smaller = min(self.numerator, self.denominator)
                if bigger % smaller == 0:
                    return Fraction(self.numerator // smaller, self.denominator // smaller)
                while not smaller == 0 or smaller == 1:
                    bigger = bigger % smaller
                    temp = bigger
                    bigger = smaller
                    smaller = temp
                gcd = bigger
                # divide numerator and denominator by gcd to get fraction in most simplified form
                return Fraction(self.numerator // gcd, self.denominator // gcd)

    number_of_states = len(transition_matrix)

    if not args:
        terminals = []  # used to store terminal states

        for index in range(0, number_of_states):
            transition_matrix[index][index] = 0  # set diagonals to 0 b/c it will transition to another state
            # eventually since it is not terminal state
            single_state_transitions = transition_matrix[index]
            if set(single_state_transitions) == {0}:  # if it transitions nowhere, it is a terminal state
                terminals.append(index)  # append the index of terminal state to terminals list

        if len(terminals) == 1:
            return [1, 1]  # if only 1 terminal state, 100% chance it ends up in that state

        # convert each transition into a fraction representing the chance the current state will transition into that
        # state the next step
        for row in range(0, number_of_states):
            row_sum = sum(transition_matrix[row])
            for col in range(0, number_of_states):
                transition_matrix[row][col] = Fraction(transition_matrix[row][col], row_sum)  # convert to Fraction

        state_history = [0]
        # state history captures all states ore was in and state it is currently in. currently in state 0 so append 0

        current_state_INITIAL_prob = Fraction(1, 1)
        # there is 100% probability we are in this state since we begin in state 0.

    else:
        # if in recursive call, args will be populated. store args elements into respective variable
        current_state_INITIAL_prob = args[0]
        state_history = args[1]
        terminals = args[2]

    current_state = state_history[-1]
    # current state always last element in list because we append the state when doing recursive call

    state_values = [Fraction(0, 1) for x in range(0, number_of_states)]
    # used to store Fraction for each state, initialized to Fraction(0,1) for each state

    recursive_states_db = []  # used to store recursive function return data

    for index in range(0, number_of_states):
        next_state_probability = transition_matrix[current_state][index]
        if not next_state_probability:  # if probability of going to this state is 0, continue.
            continue
        elif next_state_probability and (index in terminals or index in state_history):
            state_values[index] += next_state_probability * current_state_INITIAL_prob
            # if going to terminal state or traversed state, multiply probability of current state and
            # probability of going to next state, and add to respective place in state_values
        else:
            recursive_states_db.append(solution(transition_matrix, next_state_probability * current_state_INITIAL_prob,
                                                state_history + [index], terminals))
            # if next state is not terminal or traversed state, do a recursive call and append returned data into
            # recursive_states_db

    combined_returns = [Fraction(0, 1) for x in range(0, number_of_states)]
    # used to store the sum of all returned data

    # loop through combined_returns and add to each element of combined_returns the
    # respective elements in recursive_states_db_index
    for state_index in range(0, number_of_states):
        for recursive_states_db_index in range(0, len(recursive_states_db)):
            combined_returns[state_index] += recursive_states_db[recursive_states_db_index][state_index]

    # add combined_returns to state_values
    for state in range(0, number_of_states):
        state_values[state] += combined_returns[state]

    if not state_values[current_state]:
        pass
    else:
        # if we get further states coming back to current state(looping back), it will transform again into another
        # state, and some of those will loop back. This is a geometric ratio. q+qr+qr^2... = q/(1-r),
        # where q represents the probability of a state that is not current_state
        current_state_prob = state_values[current_state]
        geometric_ratio = current_state_prob / current_state_INITIAL_prob
        one_minus_geometric_ratio = Fraction(1, 1) - geometric_ratio

        for state in range(0, number_of_states):  # apply geometric ratio to each state_value
            state_values[state] /= one_minus_geometric_ratio
        state_values[current_state] = Fraction(0, 1)

    if args:  # i.e. if recursive call
        return state_values

    else:  # if not recursive call
        terminal_values = []
        for num in range(number_of_states):
            state_values[num] = state_values[num].reduce()  # reduce each fraction to least simplified form
            if num in terminals:
                terminal_values.append(state_values[num])  # only append to terminal list Fractions for terminal values

        common_denominator = terminal_values[0].denominator  # this is initial least common denominator

        # This method uses Euclid's algorithm to find least common multiple/denominator of n fractions.
        # Assuming LCD_preceding is current least common denominator of preceding n-1 fractions, LCD of n fractions is
        # (LCD_preceding)*(denominator of new fraction)//(gcd). GCD can be found by Euclid's algorithm.
        for num in range(1, len(terminal_values)):
            bigger2 = max(common_denominator, terminal_values[num].denominator)
            smaller2 = min(common_denominator, terminal_values[num].denominator)
            if bigger2 % smaller2 == 0:
                gcd2 = smaller2
            else:  # Euclid's algorithm
                while not smaller2 == 0 or smaller2 == 1:
                    bigger2 = bigger2 % smaller2
                    temp2 = bigger2
                    bigger2 = smaller2
                    smaller2 = temp2
                gcd2 = bigger2
            common_denominator *= terminal_values[num].denominator // gcd2

        for num in range(0, len(terminal_values)):
            # converting each fraction to equivalent fraction with common denominator
            if terminal_values[num].denominator != common_denominator:
                ratio = common_denominator // terminal_values[num].denominator
                terminal_values[num] = Fraction(terminal_values[num].numerator * ratio,
                                                terminal_values[num].denominator * ratio)
            else:
                pass

        # format the fractions in terminal_values so that only numerators show and common denominator is last element
        # in the list
        formatted_terminal_values = []
        for val in terminal_values:
            formatted_terminal_values.append(val.numerator)
        formatted_terminal_values.append(terminal_values[0].denominator)

        return formatted_terminal_values
