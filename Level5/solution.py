def solution(w, h, s):
    def permutations_no_identity_1D(arr, *args):
        if not args:
            holder = []
            ans = []
        elif args:

            selected = args[0]

            holder = args[1]
            holder = [x for x in holder]
            arr = [x for x in arr]
            ans = args[2]
            arr.remove(selected)
            holder.append(selected)

            if len(arr) == 0:
                ans.append(holder)
                return
        for selected in arr:
            permutations_no_identity_1D(arr, selected, holder, ans)

        if not args:
            ans.pop(0)
            return ans

    def permutations_no_identity_2D(w_perm_arr, h_perm_arr):
        # returns each as 1D array
        for w_perm in w_perm_arr:
            for h_perm in h_perm_arr:
                row = [[x for x in w_perm]]
                board = []
                for each_row in h:
                    board.append(row)
                    row = [x + w for x in row]
                pass

    def variable_counter(arr, is_h_array):
        arr_len = len(arr)
        classified = []
        num_of_var = 0
        cycle_storage = []
        for index in range(0, arr_len):
            if index == arr[index]:
                num_of_var += 1
            elif index in classified:
                continue
            else:
                cycle_tracker = []
                cycle_arr = []
                while index not in cycle_tracker:
                    cycle_tracker.append(index)
                    cycle_arr.append([index, arr[index]])
                    index = arr[index]
                num_of_var += 1
                classified += cycle_tracker
                if is_h_array:
                    cycle_storage.append(cycle_arr)
        if not is_h_array:
            return num_of_var
        else:
            return num_of_var, cycle_storage

    # W
    w_arr = [x for x in range(0, w)]
    w_permutations_no_identity_1D = permutations_no_identity_1D(w_arr)
    w_perm_variables_repository = []
    for permutation in w_permutations_no_identity_1D:
        w_perm_variables_repository.append(variable_counter(permutation, False))
    # H
    h_arr = [x for x in range(0, h)]
    h_permutations_no_identity_1D = permutations_no_identity_1D(h_arr)
    h_perm_variables_repository = []
    h_arr_cycles_repository = []
    for permutation in h_permutations_no_identity_1D:
        returned_tuple = variable_counter(permutation,
                                          True)  # tuple first entry is int number of variables, second is cycles
        h_perm_variables_repository.append(returned_tuple[0])
        h_arr_cycles_repository.append(returned_tuple[1])

    h_arr_cycles_repository_sorted = [sorted(x, key=lambda x: x[0]) for x in h_arr_cycles_repository]

    identity_symmetrical_pictures = s ** (w * h)

    # we group em so its easier when doing exponents
    # w_perms dic ... k:v aka variables to [quantity, total variable taking other dimension into account)
    w_perm_dict = {}
    for num in w_perm_variables_repository:
        if w_perm_dict.get(num):
            w_perm_dict[num][0] += 1
        else:
            w_perm_dict[num] = [1, num * h]

    w_switch_only_symmetrical_pictures = 0
    for key in w_perm_dict.keys():
        w_switch_only_symmetrical_pictures += w_perm_dict[key][0] * (s ** w_perm_dict[key][1])

    h_perm_dict = {}
    for num in h_perm_variables_repository:
        if h_perm_dict.get(num):
            h_perm_dict[num][0] += 1
        else:
            h_perm_dict[num] = [1, num * w]
    h_switch_only_symmetrical_pictures = 0
    for key in h_perm_dict.keys():
        h_switch_only_symmetrical_pictures += h_perm_dict[key][0] * (s ** h_perm_dict[key][1])
    counter = 0
    combination_arrays_vars_dict = {}
    for permutation in w_permutations_no_identity_1D:
        permutation_copy = permutation[:]
        temp_2d_arr_only_column_switches = []  # created temp array
        for h_row in range(0, h):
            temp_2d_arr_only_column_switches.append(permutation_copy)
            permutation_copy = [x + w for x in permutation_copy]  # construct 2d array with only w permutations
        for ind in range(0, len(h_permutations_no_identity_1D)):  # for each h perm
            temp_2d_arr_only_column_switches_copy = [arr[:] for arr in temp_2d_arr_only_column_switches]
            obtained_h_cycles = h_arr_cycles_repository[ind]
            for cycle_index in range(0, len(obtained_h_cycles)):  # specific_cycle
                specific_cycle = obtained_h_cycles[cycle_index]
                cycle_helper_dict = {}
                for specific_cycle_node_arr in specific_cycle:
                    cycle_helper_dict[specific_cycle_node_arr[0]] = temp_2d_arr_only_column_switches_copy[
                        specific_cycle_node_arr[0]]
                for specific_cycle_node_arr in specific_cycle:
                    temp_2d_arr_only_column_switches_copy[specific_cycle_node_arr[0]] = cycle_helper_dict[
                        specific_cycle_node_arr[1]]
            flattened_combined_matrix = []
            for arr in temp_2d_arr_only_column_switches_copy:
                for elem in arr:
                    flattened_combined_matrix.append(elem)
            var_counter_func_return = variable_counter(flattened_combined_matrix, False)
            if combination_arrays_vars_dict.get(var_counter_func_return):
                combination_arrays_vars_dict[var_counter_func_return] += 1
                counter += 1
            else:
                combination_arrays_vars_dict[var_counter_func_return] = 1
                counter += 1

    combinations_symmetrical_pictures = 0
    for key in combination_arrays_vars_dict:
        number_of_vars = key
        quantity = combination_arrays_vars_dict[key]
        combinations_symmetrical_pictures += (quantity * (s ** number_of_vars))

    total_symmetrical_pictures = identity_symmetrical_pictures + w_switch_only_symmetrical_pictures + h_switch_only_symmetrical_pictures + combinations_symmetrical_pictures

    number_of_identity_symmetries = 1

    number_of_w_only_symmetries = 0
    for key in w_perm_dict:
        number_of_w_only_symmetries += w_perm_dict[key][0]

    number_of_h_only_symmetries = 0
    for key in h_perm_dict:
        number_of_h_only_symmetries += h_perm_dict[key][0]

    number_of_combination_symmetries = number_of_w_only_symmetries * number_of_h_only_symmetries

    total_number_of_symmetries = number_of_identity_symmetries + number_of_h_only_symmetries + number_of_w_only_symmetries + number_of_combination_symmetries

    return total_symmetrical_pictures // total_number_of_symmetries


print(solution(3, 1, 1))
