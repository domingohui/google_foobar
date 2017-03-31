'''
Queue To Do
===========

You're almost ready to make your move to destroy the LAMBCHOP doomsday device, but the security checkpoints that guard the underlying systems of the LAMBCHOP are going to be a problem. You were able to take one down without tripping any alarms, which is great! Except that as Commander Lambda's assistant, you've learned that the checkpoints are about to come under automated review, which means that your sabotage will be discovered and your cover blown - unless you can trick the automated review system.

To trick the system, you'll need to write a program to return the same security checksum that the guards would have after they would have checked all the workers through. Fortunately, Commander Lambda's desire for efficiency won't allow for hours-long lines, so the checkpoint guards have found ways to quicken the pass-through rate. Instead of checking each and every worker coming through, the guards instead go over everyone in line while noting their security IDs, then allow the line to fill back up. Once they've done that they go over the line again, this time leaving off the last worker. They continue doing this, leaving off one more worker from the line each time but recording the security IDs of those they do check, until they skip the entire line, at which point they XOR the IDs of all the workers they noted into a checksum and then take off for lunch. Fortunately, the workers' orderly nature causes them to always line up in numerical order without any gaps.

For example, if the first worker in line has ID 0 and the security checkpoint line holds three workers, the process would look like this:
0 1 2 /
3 4 / 5
6 / 7 8
where the guards' XOR (^) checksum is 0^1^2^3^4^6 == 2.

Likewise, if the first worker has ID 17 and the checkpoint holds four workers, the process would look like:
17 18 19 20 /
21 22 23 / 24
25 26 / 27 28
29 / 30 31 32
which produces the checksum 17^18^19^20^21^22^23^25^26^29 == 14.

All worker IDs (including the first worker) are between 0 and 2000000000 inclusive, and the checkpoint line will always be at least 1 worker long.

With this information, write a function answer(start, length) that will cover for the missing security checkpoint by outputting the same checksum the guards would normally submit before lunch. You have just enough time to find out the ID of the first worker to be checked (start) and the length of the line (length) before the automatic review occurs, so your program must generate the proper checksum with just those two values.

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (int) start = 0
    (int) length = 3
Output:
    (int) 2

Inputs:
    (int) start = 17
    (int) length = 4
Output:
    (int) 14
'''

'''
If the line is n people long,
we grab the first n people
grab the frist n-1 people
...
grab the first 1 person

XOR everone's id

First id of each row always increases by n

But a naive approach like the one below is going to cause memory error since we could be dealing with billions of int in a list...
'''

from functools import reduce
import operator

"""
# Naive brute force; store ranges
# But iterating through 2 bln int's could be a problem
def answer(start, length):
    checksum = 0

    for line_row_num in range(0, length):
        checksum ^= reduce(operator.xor, range(start, start + (length - line_row_num)), 0 )
        start += length # Increment first id of each row

    return checksum
"""

# Better approach
'''
even^odd XOR == 1 where even < odd 
Because the last digit of an even # in binary is 0, odd has 1 as the last digit
So XOR gives 0 in all positions except for the last one, which becomes 1

1 XOR 1 == 0

and

0 XOR anything == 0 since 0 is the identity element in XOR

So we just need to find out:
    - If a row starts with an even number, 
        - and it has even pairs of elements, we can ignore it since 1^1^1^1 == 0;
        - and it has odd pairs of elements, we can add 1 to the list for XOR later since 1^1^1 == 1;
        - then add the last element of the row if it exists
    - Or if a row starts with an odd number, 
        - and it has even # of elements, excluding first and last element, we add [first, last]
        - and it has odd # of elements, excluding first and last element, we add [first, 1, last]
        - ( if last exists after pairing numbers after the first num )
'''

# Smarter approach?
def answer(start, length):
    ids = []
    
    for row_num in range(0, length):
        # Each row, we take the first (length-row_num) id's
        num_of_elements_to_take = length-row_num
        num_pairs = (num_of_elements_to_take)/2
        if start % 2 != 0:
            # First element is odd
            if num_of_elements_to_take % 2 != 0 and num_pairs % 2 != 0:
                # Odd # of elements and odd pairs
                # e.g. 11^(12^13)^(14^15)^(16^17) = 11^1^1^1 = 11^0^1 = 11^1
                ids.extend([start,1])
            elif num_of_elements_to_take % 2 != 0 and num_pairs % 2 == 0:
                # Odd # of elements and even pairs
                # e.g. 11^(12^13)^(14^15) = 11^1^1 = 11^0 = 11
                ids.append(start)
            elif num_of_elements_to_take % 2 == 0 and num_pairs > 1 and (num_pairs-1) % 2 != 0:
                # Even # and odd pairs (excl. first and last id)
                # Works since num_of_elements_to_take >=1
                # 11^12^13^14^15^16^17^18 = 11^(12^13)^(14^15)^(16^17)^18 = 11^1^1^1^18 = 11^1^18
                # So we take [first, 1, last]
                ids.extend([start,1,(start+num_of_elements_to_take-1)])
            elif num_of_elements_to_take % 2 == 0 and num_pairs == 1:
                ids.extend([start,(start+num_of_elements_to_take-1)])
            else:
                # Even # and even pairs (excl. first and last id)
                # 11^12^13^14^15^16^17^18 = 11^(12^13)^(14^15)^16 = 11^1^1^16 = 11^16
                # So we can take [first, last]
                ids.extend([start,(start+num_of_elements_to_take-1)])
        else:
            # First element is even
            if num_of_elements_to_take % 2 != 0 and num_pairs % 2 != 0:
                # Odd # of elements and odd pairs
                # e.g. (12^13)^(14^15)^(16^17)^18 = 1^1^1^18 = 0^1^18 = 1^18
                # So we can do 1^last
                ids.extend([1,(start+num_of_elements_to_take-1)])
            elif num_of_elements_to_take % 2 != 0 and num_pairs % 2 == 0:
                # Odd # of elements and even pairs
                # e.g. (12^13)^(14^15)^16 = 1^1^16 = 0^16 = 16
                # Just take the last one
                ids.append(start+num_of_elements_to_take-1)
            elif num_of_elements_to_take % 2 == 0 and num_pairs % 2 != 0:
                # Even # and odd pairs
                # 12^13^14^15^16^17 = (12^13)^(14^15)^(16^17) = 1^1^1 = 0^1 = 1
                ids.append(1)
            else:
                # Even # and even pairs
                # 12^13^14^15^16^17^18^19 = (12^13)^(14^15)^(16^17)^(18^19) = 1^1^1^1 = 0^0
                ids.append(0)
        start += length

    return reduce(operator.xor, ids, 0)
