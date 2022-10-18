def solution(entrances, exits, path, *args):
    """
    This function uses Dinic's equation to calculate the maximum flow of a system. It takes 3 arguments: a 1D
    array of entrances, a 1D array of exits, and an array of arrays where array[a][b] represents the maximum capacity
    of flow from a to b. The function returns an integer representing the maximum flow of the system.
    """

    def BFS_Level_Classifier():
        """
        This function puts into a dictionary (k,v) where k will be an integer representing the level (1,2,3...) and v
        will contain the indices of the nodes in that level. A node in key "n" says that the shorted possible path from
        an entrance to that node requires n steps. Entrances and exit nodes will not be inside the dictionary.
        """
        levels = {}
        classified_nodes = exits + entrances  # Such nodes will be classified since they will not be part of dictionary.
        # Classified_nodes store all node numbers that have been labelled into a level or are in entrance/exit
        searching_level = 1  # We start off searching for nodes 1 step away from an entrance , hence level 1
        is_first_while_call = True

        while True:
            if is_first_while_call:
                level_1_nodes = []
                for current_node in entrances:
                    for index in range(0, number_of_nodes):
                        current_flow = path[current_node][index]
                        if current_flow != 0 and index not in classified_nodes:  # If we can get there (flow exists)
                            # from current node and new node has not been classified
                            level_1_nodes.append(index)
                            classified_nodes.append(index)
                if not level_1_nodes:  # if no nodes in array, break from while loop (all nodes classified or have no
                    # flow to them)
                    break
                else:  # if nodes in current array/level
                    levels[searching_level] = list(set(level_1_nodes))  # convert to set then list to remove duplicates
                    searching_level = searching_level + 1  # go to next level
                    is_first_while_call = False  # Flip boolean

            else:  # not first_call/not lvl 1
                level_nodes = []
                for current_node in levels[list(levels)[-1]]:
                    # for nodes in previous level, find reachable nodes from previous nodes (have flow in the edge)
                    # and not classified yet
                    for index in range(0, number_of_nodes):
                        if path[current_node][index] != 0 and index not in classified_nodes:
                            level_nodes.append(index)
                            classified_nodes.append(index)
                if not level_nodes:  # if no nodes in array, break from while loop (all nodes classified or have no
                    # flow to them)
                    break
                else:
                    levels[searching_level] = list(set(level_nodes))  # convert to set then list to remove duplicates
                    searching_level = searching_level + 1  # go to next level
        return levels

    def DFS_flow_implementer(l_var_path, *argz):
        """
        This function takes as an argument the 2D path array and will implement part of Dinic's algorithm with the
        current levels dictionary from BFS_Level_Classifier(). It does so using DFS and backtracking. It returns the 2D
        path array after such operations are performed. To implement full Dinic's algorithm, must run
        BFS_Level_Classifier() and DFS_flow_implementer() until path 2d array unchanged after running them
        (reached state of equilibrium).
        """
        if not argz:  # if first call
            current_level = 0
            for node in entrances:  # for each starting node, run DFS_flow_implementer/ Dinic's algorithm
                l_var_path = DFS_flow_implementer(l_var_path, current_level, [node])
            return l_var_path
        else:  # recursive call (argz not empty)
            current_level = argz[0]  # integer representing level of node we are currently in
            current_path = argz[1]  # array representing the nodes we have travelled through
            search_index = 0  # index inside the 1D array (inside l_var_path) of current node we are in
            min_flow_helper = []  # This contains all the edge flows for each consecutive pair of values in current_path
            while True:
                while ((l_var_path[current_path[-1]][search_index] == 0) or (search_index in entrances) or (
                        search_index not in exits and (returned_levels_data.get(current_level + 1) is None or (
                        returned_levels_data.get(current_level + 1) and search_index not in (
                        returned_levels_data.get(current_level + 1)))))):
                    # while search_index pointing to path with no flow, pointing to an entrance or (not pointing to an
                    # exit and and not pointing to a node in next level)
                    if search_index == number_of_nodes - 1:  # if looking at last value inside 1d array of current node
                        # in l_var_path
                        if len(current_path) == 1:
                            return l_var_path

                        else:  # backtracking
                            min_flow_helper.pop()
                            current_level -= 1
                            search_index = current_path.pop() + 1
                            while search_index >= number_of_nodes:
                                try:
                                    min_flow_helper.pop()
                                except:
                                    return l_var_path
                                current_level -= 1
                                search_index = current_path.pop() + 1
                    else:  # go to next index
                        search_index += 1

                # if we got this far, it means (search_index pointing to a node in next level or to an exit) and there
                # is a flow on the edge connecting the nodes
                min_flow_helper.append(
                    l_var_path[current_path[-1]][search_index])  # append flow to targeted node to min_flow_helper
                current_path.append(search_index)  # append
                current_level += 1
                search_index = 0  # reset search_index to 0 for next search

                if current_path[-1] in exits:  # if we reached an exit
                    min_flow = min(min_flow_helper)  # calculate blocking flow/min flow for the path
                    for index in range(0, len(current_path) - 1):
                        # for each edge, we min_flow from the edge and increment it to the backward edge
                        l_var_path[current_path[index]][current_path[index + 1]] -= min_flow
                        l_var_path[current_path[index + 1]][current_path[index]] += min_flow
                    for index in range(0, len(min_flow_helper)):
                        min_flow_helper[
                            index] -= min_flow  # do same for min_flow_helper (keep in sync with l_var_path variables)

                    # backtrack to right before we have a edge of 0 capacity
                    first_zero = min_flow_helper.index(0)
                    search_index = current_path[first_zero + 1] + 1
                    min_flow_helper = min_flow_helper[0:first_zero]
                    current_path = current_path[0:first_zero + 1]
                    current_level = len(current_path) - 1
                    while search_index >= number_of_nodes:  # to cover special cases where we backtrack but the
                        # search_index is greater than or equal to number_of_nodes... keep backtracking
                        search_index = current_path[-1] + 1
                        try:
                            min_flow_helper.pop()
                        except:
                            return l_var_path
                        current_path.pop()
                        current_level = current_level - 1

    def Summer():
        """
        This function returns the sum of all flows that are flowing into the entrances.
        """
        summed = 0
        for entrance in entrances:
            for index in range(0, len(path)):
                summed += path[index][entrance]
        return summed

    if len(entrances) == 0 or len(exits) == 0:
        return 0
    number_of_nodes = len(path)
    outflow_before = Summer()  # to keep track of "outflows" from entrances before Dinic's algorithm

    while True:  # Keep running until path 2D array unchanged after a while loop
        before = [[y for y in x] for x in path]  # deepcopy path variable
        returned_levels_data = BFS_Level_Classifier()  # get dictionary with (k,v), with k being integers
        # representing levels 1,2,3.... and v containing nodes in that level
        path = DFS_flow_implementer(path)  # Run Dinic's algorithm
        if before == path:
            break

    outflow_after = Summer()  # total "outflows" from entrance after Dinic's algorithm
    return outflow_after - outflow_before  # difference represents max flow
