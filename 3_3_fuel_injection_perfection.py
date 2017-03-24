'''
Fuel Injection Perfection
=========================

Commander Lambda has asked for your help to refine the automatic quantum antimatter fuel injection system for her LAMBCHOP doomsday device. It's a great chance for you to get a closer look at the LAMBCHOP - and maybe sneak in a bit of sabotage while you're at it - so you took the job gladly. 

Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to figure out the most efficient way to sort and shift the pellets down to a single pellet at a time. 

The fuel control mechanisms have three operations: 

1) Add one fuel pellet
2) Remove one fuel pellet
3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter pellet is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)

Write a function called answer(n) which takes a positive integer as a string and returns the minimum number of operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more pellets than you can express in that many digits.

For example:
answer(4) returns 2: 4 -> 2 -> 1
answer(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1


Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (string) n = "4"
Output:
    (int) 2

Inputs:
    (string) n = "15"
Output:
    (int) 5
'''

'''
We can look at the problem as:
    Given a number, find the fastest way to divide it by 2 until it becomes 1.

An efficient and general way is to look at the number in binary. 
If it ends with a zero (an even number), then we can just divide it (1 bit right-shift). 
If the number ends with a 1 (an odd number), we have to either add or subtract 1.

The question is should we add or subtract?

e.g.

1)
15 -> 16 -> 8 -> 4 -> 2 -> 1 ***
v.s.
15 -> 14 -> 7 -> 6 -> 3 -> 2 -> 1
or
15 -> 14 -> 7 -> 8 -> 4 -> 2 -> 1
We should add first in this case

--------------------------------------

2)
9 -> 8 -> 4 -> 2 -> 1 ***
v.s.
9 -> 10 -> 5 -> 4 -> 2 -> 1
We should subtract first in this case


So the operation really depends on the number itself. Or it doesn't even matter in some cases.


Let's dig into some binaries.

1)
0000-1111  ---> 15
It can become either:
0001-0000  ---> 16     or
0000-1110  ---> 14

From the above example, we see that adding 1 to 15 (becomes 16) is faster. 

---------------------------------------

2)
0000-1001  ---> 9
It can become eiterh:
0000-1000  ---> 8
0000-1010  ---> 10

And subtracting 1 from 9 (becomes 8) is faster in this case.


We can see that the numbers after the first operation both have one common feature: 
    they have more trailing 0's than the other options. i.e. 0000-1000 has more trailing 0's than 0000-1010

So all we really have to do is to find out which way gives us more trailing 0's. 

To find out the number of trailing 0's, there's a very neat algorithm by Sean Anderson
http://graphics.stanford.edu/~seander/bithacks.html#ZerosOnRightLinear

'''

def count_trailing_zeros_in_binary(n):
    # http://graphics.stanford.edu/~seander/bithacks.html#ZerosOnRightLinear
    # Exclusive OR on n and (n-1)
    # To turn trailing 0's into 1's
    # Then shift right by 1 bit
    binary = (n ^ (n-1)) >> 1

    # Now all trailing 0's are 1's
    # Digits before the trailing 0's are canceled to 0's after the XOR operation
    # Keep shifting right until number becomes 0
    counter = 0
    while binary:
        binary >>= 1
        counter += 1

    return counter

def answer(n):
    n = int(n)

    counter = 0
    while n > 3:
        if n % 2 == 0:
            # Even number
            # Right bit shift - divide by 2
            n >>= 1
        else:
            # Odd
            trailing_zero_add = count_trailing_zeros_in_binary(n+1)
            triailing_zero_subtract = count_trailing_zeros_in_binary(n-1)
            if trailing_zero_add > triailing_zero_subtract:
                # n+1 has more trailing 0's 
                # So we prefer n+1 than n-1
                n += 1
            else:
                # n-1 has more trailing 0's
                # Or the same number of trailing 0's as n+1
                # So we can take n-1
                n -= 1
        counter += 1

    if n == 1:
        # Trivial case
        return counter
    elif n == 2:
        # We could've handle n==2 in the while loop
        # But we need to handle the n==3 case
        return counter+1
    else:
        # n==3
        return counter+2
