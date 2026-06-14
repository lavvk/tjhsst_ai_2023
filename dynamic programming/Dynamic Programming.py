import sys
sys.setrecursionlimit(50000)

def maxCandies(dollars, memo):
    # if you have $0, no candy
    if dollars == 0:
        return 0
    
    # if the result for this amount of dollars is  calculated return
    if dollars in memo:
        return memo[dollars]
    
    max_candies = 0
    
    # iterate through all the available options for buying candy on day i
    for i in range(1, dollars + 1):
        if i <= len(prices):
            max_candies = max(max_candies, prices[i - 1] + maxCandies(dollars - i, memo))
    
    # sotre in memo
    memo[dollars] = max_candies
    return max_candies


def prob_two(jars, memo):
    ## if valid to even go thru the jars
    
    if not jars:
        return 0
    if len(jars) == 1:
        return max(jars[0], 0)
    if tuple(jars) in memo:
        return memo[tuple(jars)]
    
    # take the first jar individually
    type1 = jars[0] + prob_two(jars[1:], memo)
    
    # first jar and the next jar as a pair
    type2 = jars[0] * jars[1] + prob_two(jars[2:], memo)
    
    # skip the first jar
    type3 = prob_two(jars[1:], memo)

    total = max(type1, type2, type3)
    
    # Store the result in the memo dictionary
    memo[tuple(jars)] = total
    
    return total
## blues
def lcs(s1, s2):
    n, m = len(s1), len(s2)
    memo = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                memo[i][j] = 1 + memo[i - 1][j - 1]
            else:
                memo[i][j] = max(memo[i - 1][j], memo[i][j - 1])

    # Reconstruct the LCS
    i, j = n, m
    lcs_seq = []
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs_seq.append(s1[i - 1])
            i -= 1
            j -= 1
        elif memo[i - 1][j] > memo[i][j - 1]:
            i -= 1
        else:
            j -= 1

    lcs_seq.reverse()
    return lcs_seq

def longest_increasing_subsequence(arr):
    n = len(arr)
    lis_length = [1] * n  # Initialize all LIS lengths to 1

    for i in range(1, n):
        for j in range(0, i):
            if arr[i] > arr[j] and lis_length[i] < lis_length[j] + 1:
                lis_length[i] = lis_length[j] + 1

    max_length = max(lis_length)
    lis = []
    idx = lis_length.index(max_length)  # Find the index of the maximum length

    while max_length > 0 and idx >= 0:
        if lis_length[idx] == max_length:
            lis.insert(0, arr[idx])
            max_length -= 1
        idx -= 1

    return lis

## reds

def prob_five(grp_size, inp_seq):
    seq_len = len(inp_seq)
    
    subseq_lens = [1] * seq_len
    subseqs = [[num] for num in inp_seq]
    assignments = []

    for element_ind in range(seq_len):
        grp_assignment = element_ind // grp_size
        assignments.append(grp_assignment)

    for curr_ind in range(1, seq_len):
        for prev_ind in range(curr_ind):
            curr_element = inp_seq[curr_ind]
            prev_element = inp_seq[prev_ind]
            curr_grp = assignments[curr_ind]
            prev_grp = assignments[prev_ind]
            curr_len = subseq_lens[curr_ind]
            prev_len = subseq_lens[prev_ind]

            met = (curr_element < prev_element and
                             curr_len <= prev_len and
                             curr_grp == prev_grp + 1)

            if met:
                subseq_lens[curr_ind] = prev_len + 1
                subseqs[curr_ind] = subseqs[prev_ind] + [curr_element]
                assignments[curr_ind] = curr_ind // grp_size

    max_len_ind = subseq_lens.index(max(subseq_lens))
    largest_subseq = subseqs[max_len_ind]
    return largest_subseq

def best_parenthesization(numbers):
    n = len(numbers)
    max_dp = [[0] * n for i in range(n)]
    min_dp = [[0] * n for i in range(n)]
    max_operators = [[""] * n for i in range(n)]
    min_operators = [[""] * n for i in range(n)]

    for i in range(n):
        max_dp[i][i] = numbers[i]
        min_dp[i][i] = numbers[i]
        max_operators[i][i] = str(numbers[i])
        min_operators[i][i] = str(numbers[i])

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            max_dp[i][j] = float('-inf')
            min_dp[i][j] = float('inf')

            for k in range(i, j):
                max_kj = max_dp[i][k] * max_dp[k + 1][j]
                max_kj_str = "(" + max_operators[i][k] + " * " + max_operators[k + 1][j] + ")"
                max_kj_plus = max_dp[i][k] + max_dp[k + 1][j]
                max_kj_plus_str = "(" + max_operators[i][k] + " + " + max_operators[k + 1][j] + ")"
                max_kj_min = min_dp[i][k] * max_dp[k + 1][j]
                max_kj_min_str = "(" + min_operators[i][k] + " * " + max_operators[k + 1][j] + ")"
                max_kj_min_plus = min_dp[i][k] + max_dp[k + 1][j]
                max_kj_min_plus_str = "(" + min_operators[i][k] + " + " + max_operators[k + 1][j] + ")"

                min_kj = min_dp[i][k] * min_dp[k + 1][j]
                min_kj_str = "(" + min_operators[i][k] + " * " + min_operators[k + 1][j] + ")"
                min_kj_plus = min_dp[i][k] + min_dp[k + 1][j]
                min_kj_plus_str = "(" + min_operators[i][k] + " + " + min_operators[k + 1][j] + ")"
                min_kj_max = max_dp[i][k] * min_dp[k + 1][j]
                min_kj_max_str = "(" + max_operators[i][k] + " * " + min_operators[k + 1][j] + ")"
                min_kj_max_plus = max_dp[i][k] + min_dp[k + 1][j]
                min_kj_max_plus_str = "(" + max_operators[i][k] + " + " + min_operators[k + 1][j] + ")"

                if max_dp[i][j] < max_kj:
                    max_dp[i][j] = max_kj
                    max_operators[i][j] = max_kj_str
                if max_dp[i][j] < max_kj_plus:
                    max_dp[i][j] = max_kj_plus
                    max_operators[i][j] = max_kj_plus_str
                if max_dp[i][j] < max_kj_min:
                    max_dp[i][j] = max_kj_min
                    max_operators[i][j] = max_kj_min_str
                if max_dp[i][j] < max_kj_min_plus:
                    max_dp[i][j] = max_kj_min_plus
                    max_operators[i][j] = max_kj_min_plus_str

                if min_dp[i][j] > min_kj:
                    min_dp[i][j] = min_kj
                    min_operators[i][j] = min_kj_str
                if min_dp[i][j] > min_kj_plus:
                    min_dp[i][j] = min_kj_plus
                    min_operators[i][j] = min_kj_plus_str
                if min_dp[i][j] > min_kj_max:
                    min_dp[i][j] = min_kj_max
                    min_operators[i][j] = min_kj_max_str
                if min_dp[i][j] > min_kj_max_plus:
                    min_dp[i][j] = min_kj_max_plus
                    min_operators[i][j] = min_kj_max_plus_str

    return max_dp[0][n - 1], max_operators[0][n - 1]



## format to command line args

prob_number = int(sys.argv[1])
filename = sys.argv[2]

if prob_number == 1:
    with open(filename, "r") as file:
        for line in file:
            prices = list(map(int, line.strip().split()))
            max_dollars = len(prices)
            memo = {}
            max_candies = maxCandies(max_dollars, memo)
            print(max_candies, end=" ")

elif prob_number == 2:
    with open(filename, "r") as file:
        for line in file:
            jars = list(map(int, line.strip().split()))
            n = len(jars)
            memo = {}
            candy = prob_two(jars, memo)
            print(candy, end=" ")

elif prob_number == 3:
    def read_sequences(filename):
        sequences = []
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        for line in lines:
            s1, s2 = line.strip().split(' ')
            s1 = list(map(int, s1.split(',')))
            s2 = list(map(int, s2.split(',')))
            sequences.append((s1, s2))
        
        return sequences

    sequences = read_sequences(filename)

    for s1, s2 in sequences:
        lcs_result = lcs(s1, s2)
        print(lcs_result)

elif prob_number == 4:
    def read_sequences(filename):
        sequences = []
        with open(filename, 'r') as file:
            lines = file.readlines()

        for line in lines:
            sequence = list(map(int, line.strip().split()))
            sequences.append(sequence)

        return sequences

    sequences = read_sequences(filename)

    for seq in sequences:
        lis_result = longest_increasing_subsequence(seq)
        print(lis_result)

elif prob_number == 5:
    with open(filename) as file:
        for line in file:
            parts = line.strip().split()
            grp_size = int(parts[0][1:-1])
            sequence = list(map(int, parts[1:]))
            result = prob_five(grp_size, sequence)
            print(str(result))

elif prob_number == 6:
    with open(filename, "r") as file:
        lines = file.readlines()
    for line in lines:
        numbers = list(map(int, line.split()))
        result, expression = best_parenthesization(numbers)
        print(expression + " = " + str(result))

else:
    print("unsolved")