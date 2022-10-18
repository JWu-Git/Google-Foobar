def solution(xs):
    """Please consult README.md for problem/motivation."""
    xs.sort()  # sorting the array
    product = 0

    # We have this variable (neg_num) to store a negative number.
    # If we find a second negative number, we multiply the negative numbers to get a positive number
    neg_num = 0

    # We keep track of whether a zero is in the list in case the only entry in list is a negative number.
    # If so, we change product variable from 0 to the only number (negative) in the list.
    zero_found = False

    # we loop through the entries in the sorted array
    for index in range(0, len(xs)):
        if xs[index] > 0:
            if product == 0:
                product = product + xs[index]
            else:
                product = product * xs[index]
        elif xs[index] == 0:
            zero_found = True
        else:
            if neg_num == 0:
                neg_num = xs[index]
            else:
                if product == 0:
                    product = product + neg_num * xs[index]
                    neg_num = 0  # reset neg_num since it's been used
                else:
                    product = product * neg_num * xs[index]
                    neg_num = 0  # reset neg_num since it's been used

    # if only one entry in list and it's a negative number, change product to the negative number entry
    if (zero_found is False) and (product == 0):
        product = xs[0]

    return str(product)

if __name__=='__main__':
	print(solution.solution([2,-3,1,0,-5]))
