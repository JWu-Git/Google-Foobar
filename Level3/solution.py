def solution(n):
    """This function takes in an integer >2 representing the total number of bricks and returns an integer
    representing the total choices of staircases you can build using all bricks, given that
    each step is lower than the previous one and each step has at least one brick."""

    # DYNAMIC PROGRAMMING

    helper = [0]  # this array will tell us the MINimum number of bricks needed to build stairs with index number of steps
    for index in range(1, 22):
        helper.append(helper[-1] + index)

    chart = [[], []]  # we append two empty lists inside this list to make it more intuitive to access elements
    # column represents number of bricks, from 0 to n.
    # row represents number of steps, starting from 0
    row_index_2 = []  # this list is for 2 steps. every element inside is number of ways to build 2 step stairs for index number of bricks.
    for column in range(0, n + 1):
        node = [1 for i in range(1, int((column - 1) / 2) + 1)]
        row_index_2.append(node)
    chart.append(row_index_2)

    last_row_index = -1
    for num in range(0, len(helper)):  # calculate how many rows we need to fill in chart using helper array
        if n >= helper[num]:
            last_row_index = num

    for row in range(3, last_row_index+1):
        r = []
        for col in range(0, n + 1):
            c = []
            if col < helper[row]:  # if this returns true, that means we cannot build stairs with such number of steps and bricks
                c.append(0)
                r.append(c)
                continue  # go onto next col
            else:
                keep_backing = True
                cycle = 1  # we start at cycle 1, meaning we prepend a step of 1(cycle) brick in front of a smaller stair that is made of cycle fewer number of bricks.
                while keep_backing:
                    grabbed_value = sum(chart[row - 1][col - cycle][cycle:])  # we add up all number of stairs that is has cycle fewer number of bricks and that is built with 1 fewer step.
                    c.append(grabbed_value)
                    if grabbed_value < 1:  # if grabbed value is 0, it means there adding cycles won't yield anymore results.
                        keep_backing = False  # exit while loop
                    else:
                        cycle = cycle + 1  # go onto next cycle
            r.append(c)
        chart.append(r)

    # add up column to get total combinations of stairs for all number of steps
    ans = 0
    for i in range(2, last_row_index + 1):
        ans = ans + sum(chart[i][n])
    return ans
