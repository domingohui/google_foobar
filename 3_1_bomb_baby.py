'''
Bomb, Baby!
===========

You're so close to destroying the LAMBCHOP doomsday device you can taste it! But in order to do so, you need to deploy special self-replicating bombs designed for you by the brightest scientists on Bunny Planet. There are two types: Mach bombs (M) and Facula bombs (F). The bombs, once released into the LAMBCHOP's inner workings, will automatically deploy to all the strategic points you've identified and destroy them at the same time. 

But there's a few catches. First, the bombs self-replicate via one of two distinct processes: 
Every Mach bomb retrieves a sync unit from a Facula bomb; for every Mach bomb, a Facula bomb is created;
Every Facula bomb spontaneously creates a Mach bomb.

For example, if you had 3 Mach bombs and 2 Facula bombs, they could either produce 3 Mach bombs and 5 Facula bombs, or 5 Mach bombs and 2 Facula bombs. The replication process can be changed each cycle. 

Second, you need to ensure that you have exactly the right number of Mach and Facula bombs to destroy the LAMBCHOP device. Too few, and the device might survive. Too many, and you might overload the mass capacitors and create a singularity at the heart of the space station - not good! 

And finally, you were only able to smuggle one of each type of bomb - one Mach, one Facula - aboard the ship when you arrived, so that's all you have to start with. (Thus it may be impossible to deploy the bombs to destroy the LAMBCHOP, but that's not going to stop you from trying!) 

You need to know how many replication cycles (generations) it will take to generate the correct amount of bombs to destroy the LAMBCHOP. Write a function answer(M, F) where M and F are the number of Mach and Facula bombs needed. Return the fewest number of generations (as a string) that need to pass before you'll have the exact number of bombs necessary to destroy the LAMBCHOP, or the string "impossible" if this can't be done! M and F will be string representations of positive integers no larger than 10^50. For example, if M = "2" and F = "1", one generation would need to pass, so the answer would be "1". However, if M = "2" and F = "4", it would not be possible.

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (string) M = "2"
    (string) F = "1"
Output:
    (string) "1"

Inputs:
    (string) M = "4"
    (string) F = "7"
Output:
    (string) "4"

Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.
'''

'''
The interesting part of the problem is that, either M or F produces exactly one other bomb.
So input of (x,y) or (y,x) should produce the same output.
In other words, we can draw a tree to represent the progression of each generation. 
Each generation is a node on a tree. 
If you start with replicating 1 M, you have 2M1F; start with 1F, you have 1M2F.
At the end, the tree has a symmetry at the root node (1,1).

It produces (m+f) bombs of one kind each generation. So one of them is always strictly greater than the other, 
except for the (0-th) generation at the beginning. 
So we can possibly approach this by backtracking starting from the end result. 
At any generation, the number of the prevailing bomb (the type with a greater number) must be added with 
replication of the other type from the last generation. 
Subtract the smaller number from the bigger number. And we have the numbers from the last generation.
Repeat until both are equal to 1, or one of them is <= 0.

We may also need to optimization here. If the input is 1, 10^50, the it will take 10^50-1 operations. 
This also means no recursion :( 
But we can do some optimization. If floor(big_number/small_number) >= 2, then we can reduce the bigger number
in one step rather than repeating the same process over and over again. 
'''

import math

def answer(M, F):
    # M, F > 0
    m = int(M)
    f = int(F)
    
    counter = 0
    while m != 1 or f != 1:
        # (1,1) is the trivial case
        if m == f or m <= 0 or f <= 0:
            return 'impossible'
        if m > f:
            times = get_times_addition(m,f)
            counter += times
            m = m - f*times
        else:
            times = get_times_addition(f,m)
            counter += times
            f = f - m*times
        
    return str(counter)

def get_times_addition(m,f):
    # Wish I had a better name for this function...
    # Returns the quotient between m and f, rounded down. 
    # m >= f
    t = int(math.floor(m/f))
    if m%f == 0:
        t -= 1
    return t
