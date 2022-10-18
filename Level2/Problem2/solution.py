import fractions


def solution(pegs):
    """This function takes in an array of integers representing pegs
    and returns a list of two integers representing the numerator and denominator
    of the first peg > 1 such that the last peg will spin twice as fast
    as the first peg. If no solution exists, it returns [-1,-1]."""

    differences = []
    radii = []

    for i in range(1, len(pegs)):
        if pegs[i] - pegs[i - 1] < 2:  # cannot be less than 2 because each radius is at least 1
            return [-1, -1]
        differences.append(pegs[i] - pegs[i - 1])

    first_peg = 0

    if len(differences) % 2 == 0:
        for index in range(0, len(differences)):
            if index % 2 == 0:
                first_peg = first_peg + differences[index]
            else:
                first_peg = first_peg - differences[index]
        first_peg = first_peg * 2
        radii.append(first_peg)

        for diff in differences:
            radius = diff - radii[-1]
            if radius < 1:  # radius needs to be at least 1, per instructions
                return [-1, -1]
            else:
                radii.append(radius)

        if first_peg < 1:  # radius needs to be at least 1, per instructions
            return [-1, -1]
        elif radii[0] != 2 * radii[-1]:  # check if radius of first circle twice as big as radius of last
            return [-1, -1]
        else:
            first_peg = fractions.Fraction(str(first_peg))
            return [first_peg.numerator, first_peg.denominator]

    else:
        for index in range(0, len(differences)):
            if index % 2 == 0:
                first_peg = first_peg + differences[index]
            else:
                first_peg = first_peg - differences[index]
        first_peg = fractions.Fraction(str(first_peg)) * fractions.Fraction("2/3")
        radii.append(first_peg)

        for diff in differences:
            radius = diff - radii[-1]
            if radius < 1:  # radius needs to be at least 1, per instructions
                return [-1, -1]
            else:
                radii.append(radius)

        if first_peg < 1:  # radius needs to be at least 1, per instructions
            return [-1, -1]
        elif radii[0] != 2 * radii[-1]:  # check if radius of first circle twice as big as radius of last
            return [-1, -1]
        else:
            return [first_peg.numerator, first_peg.denominator]
