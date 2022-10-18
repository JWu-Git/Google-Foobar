def solution(banana_list, *args):
    """
    This function takes in a list of integers representing the number of bananas each player has, and returns an
    integer representing the number of unpaired players after the maximum number of players have been paired into
    infinite loops. An infinite loop is defined as a game between a pair of players that goes on forever, given that
    the player with fewer bananas bets all their bananas and the player with more bananas matches such bet,
    and that the player with fewer bananas always wins, getting his opponent's bet. A game in which two players
    somehow end in a state where they have the same number of bananas does not end in infinite loop.
    """

    def ok(x, y, x_index, y_index, memo):  # This checks whether such pairing of players is acceptable
        if memo[x_index][y_index] != -1:  # If memo entry is populated, return value from memo
            return memo[x_index][y_index]
        if x == y:  # Two players with same bananas never end in infinite loop
            memo[x_index][y_index] = 0
            return False
        elif x == 1 or y == 1:
            # If one of players has 1 banana, it will not end in infinite loop if sum of bananas is power of 2. If
            # one of players has 1 banana and if sum not power of 2, it will always end in infinite loop.
            if x + y in powers_table:
                memo[x_index][y_index] = 0
                return False
            else:
                memo[x_index][y_index] = 1
                return True
        elif (x % 2 == 0 and y % 2 == 1) or (
                y % 2 == 0 and x % 2 == 1):  # If banana pairing different parity, it will always end in infinite loop
            memo[x_index][y_index] = 1
            return True
        else:  # Else, play a round and recursively call ok function on pairing
            min_val = min(x, y)
            max_val = max(x, y)
            return ok(min_val, (max_val - min_val) / 2, x_index, y_index, memo)

    def backtrack(array1, index1):
        index1 -= 1
        while array1[index1] < 0 or array1[index1] == index1:  # If current player taken or paired by someone else,
            # keep backtracking
            index1 -= 1
        return index1

    def incrementEntry(array1, odds1, index1):
        if array1[array1[index1]] == -99:
            array1[array1[index1]] = array1[
                index1]  # If current player matched to someone, release the matched player before incrementing

        array1[index1] += 1  # Increment

        if array1[index1] >= len(
                array1):  # If index entry after incrementing is past last index of array (e.g. player
            # matched to someone past last player), reset entry
            array1[index1] = index1
            return

        while array1[index1] in array1[0:index1] or not ok(odds1[index1], odds1[array1[index1]], index1, array1[index1],
                                                           memo_helper):
            # While someone else (earlier in array) matched with same player or NOT okay(does not end in infinite loop)
            array1[index1] += 1
            if array1[index1] >= len(
                    array1):  # If we match to someone beyond last available person e.g. went past too far
                array1[index1] = index1
                return

        array1[array1[index1]] = -99  # set matched person to -99 (representing matched/taken)

    evens = []
    odds = []

    for elem in banana_list:
        if elem % 2 == 0:
            evens.append(elem)
        else:
            odds.append(elem)

    memo_helper = [[-1 for x in range(0, len(odds))] for x in
                   range(0, len(odds))]  # This will help us memoize who can match with who

    evens_length = len(evens)
    odds_length = len(odds)

    if not args:  # First call
        if len(banana_list) % 2 == 0:
            max_possible_matches = len(banana_list)
            leftover = 0
        else:
            max_possible_matches = len(banana_list) - 1
            leftover = 1  # Will always be 1 person leftover minimum if we pair odd number of players

        # Powers table will help us figure out if we in infinite loop given one player has 1 banana.
        # It will end in infinite loop if sum of their bananas is not power of 2. Will not if power of 2.
        powers_table = [1]
        for a in range(0, 30):
            powers_table.append(powers_table[-1] * 2)

    else:  # Recursive calls
        max_possible_matches = args[0]
        powers_table = args[1]
        leftover = args[2]

    odd_even_matches = 2 * min(evens_length,
                               odds_length)  # Odd-even pairs always end in infinite loop, so make note of them
    matches_to_find = max_possible_matches - odd_even_matches

    if matches_to_find == 0:  # If we don't need to match anymore, return leftover
        return leftover

    if odds_length == evens_length:  # If #odd = #even, and since odd/even pair always end in infinite loop,
        # return leftover which is 0 (since sum is even)
        return 0

    if evens_length > odds_length:  # If more evens than odds, divide each even by 2, and recursive call solution()
        # on them. We also pass into solution() leftovers and matches_to_find
        for index in range(0, len(evens)):
            evens[index] = evens[index] // 2
        return solution(evens, matches_to_find, powers_table, leftover)

    else:  # More odds than evens
        arr = [x for x in range(0, odds_length)]  # We initialize each person matched to itself(meaning not matched
        # to anyone)
        current_index = 0
        max_matched = 0

        while max_matched < matches_to_find and current_index >= 0:  # So long as we matched fewer than
            # matched_to_find or we are not at index -1 (Which would mean we backtracked too far)
            if current_index >= len(
                    arr):  # If we past last index of array, we have a solution. count number of players matched. If
                # its more than max_matched, this is new max_matched. Backtrack.
                max_matched_holder = 0
                for num in range(0, len(odds)):
                    if arr[num] > num:
                        max_matched_holder += 2
                if max_matched_holder > max_matched:
                    max_matched = max_matched_holder
                current_index = backtrack(arr, current_index)
                continue

            elif arr[current_index] == -99:  # If current player taken by someone else, go to next player
                current_index += 1

            elif arr[current_index] >= len(arr):  # If current player matched to someone beyond last person in list
                arr[current_index] = current_index  # Match current player to himself (i.e. matched to no one)
                current_index = backtrack(arr, current_index)  # Backtrack
                continue

            else:
                # We check to see if its possible to get a higher max_matched given number of previous players before
                # current player who matches with no one(i.e. they are exhausted)
                counter = 0
                for index in range(0, current_index):
                    if arr[index] == index:
                        counter += 1
                if len(arr) - counter < max_matched:  # If impossible to get higher max_matched, break
                    break

                incrementEntry(arr, odds, current_index)  # Else, increment entry
                current_index += 1
                continue

        remainder = matches_to_find - max_matched

        if remainder <= 0:
            return 0 + leftover
        else:
            return remainder + leftover
