def solution(w, h, s):
    class RowSymmetry:
        def __init__(self, permutation_array):
            self.data = permutation_array

    class ColumnSymmetry:
        def __init__(self, permutation_array):
            self.data = permutation_array
            returned_tuple = variable_counter(permutation_array, True)
            self.number_of_variables = returned_tuple[0]
            self.cycles = returned_tuple[1]
            self.cycles_sorted = [sorted(x, key=lambda x: x[0]) for x in self.cycles]

    def create_combination_board(RowObject, ColumnObject):
        board = []
        row_copy = [x for x in RowObject.data]
        for row in range(0, h):
            board.append(row_copy)
            row_copy = [x + w for x in row_copy]
        for cycle in ColumnObject.cycles_sorted:
            helper_dict = {}
            for cycle_node in cycle:
                index_of_node = cycle_node[0]
                helper_dict[index_of_node] = board[index_of_node]
            for cycle_node in cycle:
                board[cycle_node[0]] = helper_dict[cycle_node[1]]
        return board

    class CombinationSymmetry:
        def __init__(self, RowObject, ColumnObject):
            self.board = create_combination_board(RowObject, ColumnObject)
            self.number_of_variables = self.calculate_number_of_variables()
            self.symmetrical_pictures = s ** self.number_of_variables

        def calculate_number_of_variables(self):
            flattened_combined_matrix = []
            for arr in self.board:
                for elem in arr:
                    flattened_combined_matrix.append(elem)
            return variable_counter(flattened_combined_matrix, False)

    def permutations(arr, *args):  # returns an array of arrays containing all permutations of an array of ints
        if not args:
            holder = []
            ans = []
        elif args:
            selected = args[0]
            holder = args[1]
            holder = [x for x in holder]  # create local shallow copy
            arr = [x for x in arr]  # create local shallow copy
            ans = args[2]
            arr.remove(selected)
            holder.append(selected)
            if len(arr) == 0:
                ans.append(holder)
                return
        for selected in arr:
            permutations(arr, selected, holder, ans)  # recursive
        if not args:
            return ans

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

    row_permutations_arr = [x for x in range(0, w)]
    w_permutations = permutations(row_permutations_arr)
    RowSymmetry_arr = []
    for permutation in w_permutations:
        RowSymmetry_arr.append(RowSymmetry(permutation))

    h_arr = [x for x in range(0, h)]
    h_permutations = permutations(h_arr)
    ColumnSymmetry_arr = []
    for permutation in h_permutations:
        ColumnSymmetry_arr.append(ColumnSymmetry(permutation))

    CombinationSymmetry_arr = []
    for RowSymmetryObject in RowSymmetry_arr:
        for ColumnSymmetryObject in ColumnSymmetry_arr:
            CombinationSymmetry_arr.append(CombinationSymmetry(RowSymmetryObject, ColumnSymmetryObject))

    test_arr=[]
    for obj in CombinationSymmetry_arr:
        if obj.board not in test_arr:
            test_arr.append(obj.board)


    summer = 0
    for obj in CombinationSymmetry_arr:
        summer += obj.symmetrical_pictures
    return str((summer // len(CombinationSymmetry_arr)))



