import math


def solution(w, h, s):
    def cycle_counter_2d_subsystem(nodes, rings):
        """counts how many times it wraps around the subsystem"""
        gcd = find_gcd(nodes, rings)
        total_covered_1_ring = nodes // gcd
        number_of_cycles = (nodes // total_covered_1_ring)
        return number_of_cycles

    def find_combinations(n, r):
        return math.factorial(n) // (math.factorial(n - r) * math.factorial(r))

    def find_permutations(n, r):
        return math.factorial(n) // math.factorial(n - r)

    def find_lcm(n, m):
        gcd = find_gcd(n, m)
        return n * m // gcd

    def find_gcd(n, m):
        if n == 0:
            return m

        return find_gcd(m % n, n)

    def cycles_1D_increasing_size(n, arr, *args):
        """
        [[1,2],[3]] no identity
        """
        if not args:  # first call
            storage = []
            min_bound = 1
            max_bound = n + 1
        if args:

            storage = args[0]
            min_bound = storage[-1]
            max_bound = n - sum(storage) + 1
            if sum(storage) == n:
                arr.append(storage)
                return
            elif sum(storage) > n:
                return

        if not args:
            for num in range(min_bound, max_bound):
                cycles_1D_increasing_size(n, arr, [x for x in storage] + [num])
            arr.pop(0)
        elif args:
            for num in range(min_bound, max_bound):
                cycles_1D_increasing_size(n, arr, [x for x in storage] + [num])

    def combinations_counter_for_1D_cycle_array(cycle_array_input):
        """[list of ints]"""
        entries = sum(cycle_array_input[0])
        return_array = []
        for subarray in cycle_array_input:
            entries_copy = entries
            combinations = 1
            for elem in subarray:
                if elem == 1:
                    continue
                elif elem != 1:
                    combinations = combinations * find_combinations(entries_copy, elem)
                    entries_copy = entries_copy - elem
            duplicate_cycles_counter_dict = dict((i, subarray.count(i)) for i in subarray if i != 1)
            for dict_quantity in list(duplicate_cycles_counter_dict.values()):
                combinations = combinations // math.factorial(dict_quantity)
            return_array = return_array + [combinations]
        return return_array

    def solve_for_1d(n, other, w_or_h_cycles_1D_increasing_size):
        """input 1 number, get tuple, first is symmetrical pictures, second is symmetries"""
        w_combination_quantities_per_1d_cycle_array = combinations_counter_for_1D_cycle_array(
            w_or_h_cycles_1D_increasing_size)

        number_of_cycles_per_cycle_config = []
        for subarr in w_or_h_cycles_1D_increasing_size:
            number_of_cycles_per_cycle_config.append(len(subarr))

        pics_per_combination = []
        for num in number_of_cycles_per_cycle_config:
            pics_per_combination.append(s ** (num * other))

        symmetrical_pictures_for_respective = 0
        for item in range(0, len(pics_per_combination)):
            symmetrical_pictures_for_respective += w_combination_quantities_per_1d_cycle_array[item] * \
                                                   pics_per_combination[item]

        symmetries_for_respective = sum(w_combination_quantities_per_1d_cycle_array)
        return symmetrical_pictures_for_respective, symmetries_for_respective

    def diff_state_combinations(states, quantity, *args):
        if not args:
            ans_array = []
        for num in range(0, states + 1):
            diff_state_combinations(states, quantity, num)

    def number_of_combinations_2d(cycle_length, nodes_per_ring):
        helper_arr = []
        div = nodes_per_ring // cycle_length
        leftover = nodes_per_ring % cycle_length
        for diff_slice in range(0, cycle_length):
            helper_arr.append(div)
        current_index = 0
        while leftover > 0:
            helper_arr[current_index] += 1
            current_index += 1
        helper_arr[0] -= 1
        ans = 1
        nodes_per_ring_1_less = nodes_per_ring - 1
        for repeats_of_certain_slice in helper_arr:
            ans *= find_combinations(nodes_per_ring_1_less, repeats_of_certain_slice)
            nodes_per_ring_1_less -= repeats_of_certain_slice
        return ans

    def states_foo(quantity, states, *args):
        arr = []
        cycles_1D_increasing_size(quantity, arr, *args)
        arr.append([1 for x in range(0, quantity)])
        return arr

    def possible_permutations(perspective_subarray, other_subarray, states_per_cycle):
        count_dict = {}
        for num in range(0, len(states_per_cycle)):
            if perspective_subarray[num] == 1 or states_per_cycle[num] == 1:
                continue
            else:
                if count_dict.get(perspective_subarray[num]):
                    count_dict[perspective_subarray[num]] += 1
                else:
                    count_dict[perspective_subarray[num]] = 1
        with_multiple = []
        if count_dict:
            for key in count_dict.keys():
                if count_dict[key] > 1:
                    with_multiple.append(key)
        states_dict = {}
        if with_multiple:
            for cycle in with_multiple:
                states_dict[cycle] = (
                    states_foo(perspective_subarray.count(cycle), states_per_cycle[perspective_subarray.index(cycle)]))
        return states_dict

    def combinations_counter_for_2d(cycle_array_input):
        entries = sum(cycle_array_input)
        combinations = 1
        for elem in cycle_array_input:
            if elem == 1:
                continue
            else:
                combinations = combinations * find_combinations(entries, elem)
                entries = entries - elem
        duplicate_cycles_counter_dict = dict((i, cycle_array_input.count(i)) for i in cycle_array_input if i != 1)
        for dict_quantity in list(duplicate_cycles_counter_dict.values()):
            combinations = combinations // math.factorial(dict_quantity)
        return combinations

    def combinations_2d_(subarray, perspective_subarray, key):
        perspective_subarray = [x for x in perspective_subarray]
        total = sum(perspective_subarray)
        ans = 1
        arr = []
        popped = []
        for num in range(0, len(perspective_subarray)):
            if perspective_subarray[num] == key:
                arr.append(num)
        for num1 in range(0, len(perspective_subarray)):
            if num1 not in arr:
                ans *= find_combinations(total, num1)
                total = total - num1
                popped.append(perspective_subarray.pop(num1))
            else:
                ans *= find_combinations(total, num1)
                total = total - num1
        for dict_quantity in perspective_subarray:
            ans = ans // math.factorial(dict_quantity)
        for num in subarray:
            ans = ans // math.factorial(num)
        return ans

    def break_into_smaller_problem(perspective_subarray, other_subarray, *args):
        if args:
            prod = args[0]
        states_per_cycle = []
        var_per_cycle = []
        for perspective_subarray_specific_cycle_length in perspective_subarray:
            var = 0
            if perspective_subarray_specific_cycle_length == 1:
                states_per_cycle.append(1)
                var_per_cycle.append(len(other_subarray))
                continue
            else:
                current_2d_cycle_length = 1
                for elem2 in other_subarray:
                    if elem2 == 1:
                        var += 1
                        continue
                    else:
                        identified_cycle = cycle_counter_2d_subsystem(perspective_subarray_specific_cycle_length, elem2)
                        current_2d_cycle_length = find_lcm(identified_cycle, current_2d_cycle_length)
                        var += identified_cycle
                # now we append to states_per_cycle

            if perspective_subarray_specific_cycle_length <= current_2d_cycle_length + 1:
                states_per_cycle.append(math.factorial(perspective_subarray_specific_cycle_length - 1))
            else:
                ans = number_of_combinations_2d(current_2d_cycle_length,
                                                perspective_subarray_specific_cycle_length)
                states_per_cycle.append(ans)
            var_per_cycle.append(var)
        returned = possible_permutations(perspective_subarray, other_subarray, states_per_cycle)

        if not args:
            if not returned:
                prod = 1
                for num in states_per_cycle:
                    prod *= num
                number = combinations_counter_for_2d(perspective_subarray)
                prod *= number
                ans = break_into_smaller_problem(other_subarray, other_subarray, prod)
                return ans
            else:
                prod = 1
                for num in states_per_cycle:
                    if num not in returned:
                        prod *= num
                for subarray in returned[list(returned.keys())[0]]:
                    subarray = subarray
                    local_prod = prod
                    diff = len(subarray)
                    n = states_per_cycle[perspective_subarray.index(list(returned.keys())[0])]
                    r = diff
                    if n < r:
                        continue
                    local_prod *= find_combinations(n, r)
                    combinations = combinations_2d_(subarray, perspective_subarray, list(returned.keys())[0])
                    local_prod = local_prod * combinations
                    ans = break_into_smaller_problem(other_subarray, perspective_subarray, local_prod)
                    return ans
        if args:
            if not returned:
                prod = args[0]
                for num in states_per_cycle:
                    prod *= num
                number = combinations_counter_for_2d(perspective_subarray)
                prod *= number
                symmetries = prod
                total_pictures = symmetries * s ** sum(var_per_cycle)
                return symmetries, total_pictures

            else:
                prod = args[0]
                for num in states_per_cycle:
                    if num not in returned:
                        prod *= num
                for subarray in returned[list(returned.keys())[0]]:
                    subarray = subarray
                    local_prod = prod
                    diff = len(subarray)
                    n = states_per_cycle[perspective_subarray.index(list(returned.keys())[0])]
                    r = diff
                    if n < r:
                        continue
                    local_prod *= find_combinations(n, r)
                    combinations = combinations_2d_(subarray, perspective_subarray, list(returned.keys())[0])
                    local_prod = local_prod * combinations
                    symmetries = local_prod
                    total_pictures = symmetries * s ** sum(var_per_cycle)
                    return symmetries, total_pictures

    def solve_2d_master(h_w_cycles_1D_increasing_size, other):
        repo = []
        for perspective_subarray in h_w_cycles_1D_increasing_size:
            for other_subarray in other:
                repo.append(break_into_smaller_problem(perspective_subarray, other_subarray))
        return repo

    # identity
    identity_symmetries = 1
    identity_symmetrical_pictures = s ** (w * h)

    # W only
    w_cycles_1D_increasing_size = []
    cycles_1D_increasing_size(w, w_cycles_1D_increasing_size)

    w_returned_tuple = solve_for_1d(w, h, w_cycles_1D_increasing_size)
    w_switch_only_symmetrical_pictures = w_returned_tuple[0]
    w_switch_only_symmetries = w_returned_tuple[1]

    # H only
    h_cycles_1D_increasing_size = []
    cycles_1D_increasing_size(h, h_cycles_1D_increasing_size)

    h_returned_tuple = solve_for_1d(h, w, h_cycles_1D_increasing_size)
    h_switch_only_symmetrical_pictures = h_returned_tuple[0]
    h_switch_only_symmetries = h_returned_tuple[1]

    combination_symmetrical_pictures = 0
    combination_symmetries = 0

    ans = solve_2d_master(h_cycles_1D_increasing_size, w_cycles_1D_increasing_size)
    for tup in ans:
        combination_symmetries += tup[0]
        combination_symmetrical_pictures += tup[1]

    total_symmetrical_pictures = identity_symmetrical_pictures + w_switch_only_symmetrical_pictures + h_switch_only_symmetrical_pictures + combination_symmetrical_pictures
    total_symmetries = identity_symmetries + w_switch_only_symmetries + h_switch_only_symmetries + combination_symmetries
    return str(int(total_symmetrical_pictures // total_symmetries))


