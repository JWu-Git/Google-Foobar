def solution(x, y):
    for elem in set(x).symmetric_difference(set(y)):
        return int(elem)

if __name__=='__main__':
	solution.solution([14, 27, 1, 4, 2, 50, 3, 1], [2, 4, -4, 3, 1, 1, 14, 27, 50])
