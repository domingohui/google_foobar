'''
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function answer(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (int) m = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
Output:
    (int list) [7, 6, 8, 21]

Inputs:
    (int) m = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
Output:
    (int list) [0, 3, 2, 9, 14]

Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.
'''


'''
After doing some research, this turns out to be an Absorbing Markov Chain problem :D
I found this video a great resource to learn about the Markov Chain (and AMC) -> https://www.youtube.com/watch?v=BsOkOaB8SFk

In an AMC, the basic idea is that there are two types of states, transient states and absorbing states. 
A transient state can transform to another state (transient or absorbing).
This repeats until it reaches an absorbing state. Then, it never changes.
We can think of it having 0 probability of transforming into any other differnt states.
An AMC guarantees that a transient state can reach an absorbing state in a finite number of steps. 
So we are in business!

In simple terms, we need to find the probabilities of reaching different individual absorbing states given a specific transient state to begin with. 
To do that, we need to find the 'fundamental matrix', F. 
Then, multiply it with a matrix of probabilities of going from a transient state to any one of absorbing state(s).
Let's call it R. So R(T,A) is the probability of state T becoming state A.
So F*R is what we need at the end. 

F tells us the expected number of times transforming into a transient state from another transient state (could be the same one). 
So F(A,B) is the probability of state A becoming state B.
However, that is not very helpful in this case. 
But if we also have the probabilities of a transient state becoming a absorbing state (which is R), 
then we know the probabilities of a transient state going into an absorbing state. 

To set up the matrix, we also need to group all transient states and absorbing states together.
If the input is [ transient, absorbing, transient ], we need to reorder the rows and columns so that the matrix becomes [ transient, transient, absorbing ].
'''

from fractions import Fraction, gcd
from functools import reduce

def organize (m):
    to_return = []

    # Absorbing and transient states #:
    absorbing_index = []
    transient_index = []
    dim = len(m)

    # Get absorbing_index and transient_index
    for r in range(dim):
        if sum(m[r]) == 0:
            absorbing_index.append(r)
        else:
            transient_index.append(r)

    # Reorder arrays so that transient_states come before absorbing_states
    for row_index in transient_index+absorbing_index:
        if row_index in absorbing_index:
            # This row is an absorbing state
            # We just assign a row of 0s
            to_return.append([Fraction(0)] * dim)
        else:
            # Row of a transient state
            row = []
            s = sum(m[row_index]) # To normalize probabilities
            # Select all transient states first
            row += [ Fraction(m[row_index][i], s) for i in transient_index]
            # Then absorbing states
            row += [ Fraction(m[row_index][i], s) for i in absorbing_index]
            to_return.append(row)

    return to_return

def inverse (m):
    dim = len(m)

    augmented = []
    
    # 1) Augment the matrix
    for row_index in range(dim):
        augmented.append(m[row_index] + 
                [Fraction(0)] * row_index + 
                [Fraction(1)] + 
                [Fraction(0)] * (dim - row_index - 1))

    # 2) Elimination - Clear a column 
    # to turn rows into reduced row-echelon form.
    # https://people.richland.edu/james/lecture/m116/matrices/pivot.html
    for r in range(dim):
        for c in range(dim):
            # Clear each column
            if r != c:
                # Pivot element
                ratio = augmented[c][r]/augmented[r][r]
                for k in range(dim*2):
                    augmented[c][k] = augmented[c][k] - ratio * augmented[r][k]

    # 3) Apply ratios(multiples) in diagonal entries
    # to reduce entries in rhs of the augmented matrix to simplest form
    for r in range(dim):
        multiple = augmented[r][r]
        for c in range(dim*2):
            augmented[r][c] /= multiple
    
    to_return = [ [element for element in row[dim:]] for row in augmented]

    return to_return


def get_fundamental_matrix (Q):
    # Do I - Q
    N_Q = []
    dim = len(Q)
    for r in range(dim):
        row = []
        for c in range(dim):
            # Identity matrix minus Q
            if r == c:
                row.append(Fraction(1)-Q[r][c])
            else:
                row.append(Fraction(-1)*Q[r][c])
        N_Q.append(row)

    # Get its inverse
    return inverse(N_Q)

def lcm (a,b):
    '''
    Find the lowest common multiple of a and b
    '''
    return int(a * b / gcd(a,b))

def lcmm (*args):
    '''
    Find lcm of more than 2 numbers
    '''
    return reduce(lcm, args)

def answer(m):
    # 1) Reorder, and normalize matrix entries, 
    # so that all transient states are above the absorbing states.
    # From the input, an absorbing state has a 0-filled row.
    # Also, use Fraction to keep track of numerators and denominators
    matrix = organize(m)

    transient_states = 0
    absorbing_states = 0
    # 2) Count # of transient states 
    for row in matrix:
        for col in row:
            if col.numerator != 0:
                transient_states += 1
                break
    absorbing_states = len(matrix) - transient_states

    # 3) Get fundamental matrix
    # = inverse(I - the matrix of probabilities of transient to transient)

    # Q matrix = the matrix of probabilities of transient to transient
    # Take the first t elements of number of row_count rows
    # t = number of transient states
    Q = [ row[:transient_states] for row in matrix[:transient_states]]

    # This is the fundamental matrix
    F = get_fundamental_matrix(Q)

    # If no fundamental matrix, the ore always stays in state #0
    if len(F) == 0:
        return [1] + [0]* (absorbing_states-1) + [1]

    # 4) Get the R matrix
    # Instead of starting from column 0, we start with column transient_states
    R = [ row[transient_states:] for row in matrix[:transient_states]]

    # 5) Multiply F by R
    # We only need row 0, since we always start with state 0
    F0 = F[0]
    prob = []
    for col in range(absorbing_states):
        # For each absorbing state
        # We multiply the fundamental matrix with each column representing each state
        result = 0
        for t in range(transient_states):
            result += F0[t] * R[t][col]
        prob.append(result)

    # 6) Separate numerators and the denomenator
    # Get lcm of all denominators
    denominators = [ p.denominator for p in prob ]
    lowest_common_multiple = lcmm(*denominators)
    # Scale numerators if necessary
    result = [ int(p.numerator * (lowest_common_multiple / p.denominator)) for p in prob ]
    result.append(int(lowest_common_multiple))
    return result

'''
#Testing
dim = int(input())
M = []
while(len(M) < dim):
    row = []
    for i in range(dim):
        row.append(int(input()))
    M.append(row)
print(answer(M))
'''
