'''
Problem

Tatiana likes to keep things tidy. Her toys are sorted from smallest to largest, her pencils are sorted from shortest to longest and her computers from oldest to newest. One day, when practicing her counting skills, she noticed that some integers, when written in base 10 with no leading zeroes, have their digits sorted in non-decreasing order. Some examples of this are 8, 123, 555, and 224488. She decided to call these numbers tidy. Numbers that do not have this property, like 20, 321, 495 and 999990, are not tidy.

She just finished counting all positive integers in ascending order from 1 to N. What was the last tidy number she counted?

Input

The first line of the input gives the number of test cases, T. T lines follow. Each line describes a test case with a single integer N, the last number counted by Tatiana.

Output

For each test case, output one line containing Case #x: y, where x is the test case number (starting from 1) and y is the last tidy number counted by Tatiana.

Limits

1 ≤ T ≤ 100.
Small dataset

1 ≤ N ≤ 1000.
Large dataset

1 ≤ N ≤ 1018.


Input 
 
4
132
1000
7
111111111111111110

Output 

Case #1: 129
Case #2: 999
Case #3: 7
Case #4: 99999999999999999

Note that the last sample case would not appear in the Small dataset.
'''

def all_9_digit (length):
    return 10**(length) - 1

def last_tidy_num (N):
    if N <= 9:
        return str(N)
    
    N = str(N)

    zero_index = N.find('0')
    if zero_index != -1:
        # Not tidy num for sure
        if zero_index == 1 and N[0] == 1:
            # e.g. 1099 -> 999
            return last_tidy_num(all_9_digit(len(N)-1))
        else:
            # e.g. 2209 -> 2199 -> 1999
            return last_tidy_num(
                    int(N[:zero_index-1] + \
                            str(int(N[zero_index-1]) - 1) + \
                            str(all_9_digit(len(N)-zero_index))))

    # Check if first digit is greater than the 2nd one
    if int(N[0]) > int(N[1]):
        # e.g. 987, 212
        # Subtract the first digit by 1, and change the rest to 9
        # cases like 100, 110 are handled above
            return str(int(N[0])-1) + str(all_9_digit(len(N)-1))
    else:
        # e.g. 123, 121, 110
        return N[0] + str(last_tidy_num(int(N[1:])))

def is_tidy_num(N):
    if int(N) <= 9:
        return True

    N = str(N)
    for i in range(len(N)-1):
        if int(N[i]) > int(N[i+1]):
            return False
    return True

def last_tidy_num_wrapper(N):
    while not is_tidy_num(N):
        N = last_tidy_num(int(N))
    return N
    

rows = int(input())
for i in range(rows):
    print('Case #' + str(i+1) + ': ' + str(last_tidy_num_wrapper(int(input()))))
