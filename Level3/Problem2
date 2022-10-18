def solution(n, *args):
    """
    This function takes in an int n >0 representing number of pellets and returns an int representing minimum number of
    moves needed to get n to 1, with constraint that a move consists of adding 1, subtracting 1, or
    dividing by two (only when n is even).
    """

    # RECURSIVE DYNAMIC PROGRAMMING

    n = int(n)
    recorded_n = n  # captures n before it is manipulated
    sol = 0

    if not args:
        memo = {}  # if this no args, this is base function so need to create memo
    else:
        memo = args[0]  # if recursive call, args[0] will contain memo

    if n in memo:
        # if n in memo, that means we in recursive call. return memo[n] for
        # least number of steps to get to 1 from n and return memo
        return memo[n], memo
    else:
        pass

    while n % 2 == 0:
        if n in memo:
            sol = sol + memo[n]
            if not args:
                return sol
            else:
                memo[recorded_n] = sol
                return sol, memo
        else:
            n = n // 2  # if n is even, divide n by 2 and increment sol. // is used to get int after division
            sol = sol + 1

    if n == 1:  # reached base case, return sol
        memo[recorded_n] = sol
        if not args:
            return sol
        else:
            return sol, memo
    else:
        pass

    helper = []  # helper is used to record powers of 2
    helper.append(2 ** 0)
    while helper[-1] < n:
        helper.append(helper[-1] * 2)
    helper.append(helper[-1] * 2)  # record 1 more power of 2 in case adding 1 to n gives you power of 2

    if n - 1 in helper:  # if subtracting 1 gives you power of 2, take that path. dividing by 2 is most efficient
        sol = helper.index(n - 1) + sol + 1  # the +1 is for the step of subtracting 1
        if args:
            memo[recorded_n] = sol
            return sol, memo
        else:
            return sol
    elif n + 1 in helper:  # if adding 1 gives you power of 2, take that path. dividing by 2 is most efficient
        sol = helper.index(n + 1) + 1 + sol  # the +1 is for the step of adding 1
        if args:
            memo[recorded_n] = sol
            return sol, memo
        else:
            return sol
    else:
        pass

    n_min_1_tuple = solution(n - 1, memo)  # recursive func returns 2 arguments as a tuple.
    memo = n_min_1_tuple[1]  # index 1 in tuple is memo

    n_plus_1_tuple = solution(n + 1, memo)  # recursive func returns 2 arguments as a tuple.
    memo = n_plus_1_tuple[1]  # index 1 in tuple is memo

    n_min_1_sol = n_min_1_tuple[0]  # index 0 in tuple is sol
    n_plus_1_sol = n_plus_1_tuple[0]  # index 0 in tuple is sol

    if n_min_1_sol >= n_plus_1_sol:  # if n-1 is better path or equal, take that path
        sol = sol + 1 + n_plus_1_sol
    else:
        sol = sol + 1 + n_min_1_sol  # else take n+1 path

    if not args:
        return sol
    else:
        memo[recorded_n] = sol
        return sol, memo
