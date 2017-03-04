'''
Power Hungry
============

Commander Lambda's space station is HUGE. And huge space stations take a LOT of power. Huge space stations with doomsday devices take even more power. To help meet the station's power needs, Commander Lambda has installed solar panels on the station's outer surface. But the station sits in the middle of a quasar quantum flux field, which wreaks havoc on the solar panels. You and your team of henchmen has been assigned to repair the solar panels, but you can't take them all down at once without shutting down the space station (and all those pesky life support systems!). 

You need to figure out which sets of panels in any given array you can take offline to repair while still maintaining the maximum amount of power output per array, and to do THAT, you'll first need to figure out what the maximum output of each array actually is. Write a function answer(xs) that takes a list of integers representing the power output levels of each panel in an array, and returns the maximum product of some non-empty subset of those numbers. So for example, if an array contained panels with power output levels of [2, -3, 1, 0, -5], then the maximum product would be found by taking the subset: xs[0] = 2, xs[1] = -3, xs[4] = -5, giving the product 2*(-3)*(-5) = 30.  So answer([2,-3,1,0,-5]) will be "30".

Each array of solar panels contains at least 1 and no more than 50 panels, and each panel will have a power output level whose absolute value is no greater than 1000 (some panels are malfunctioning so badly that they're draining energy, but you know a trick with the panels' wave stabilizer that lets you combine two negative-output panels to produce the positive output of the multiple of their power values). The final products may be very large, so give the answer as a string representation of the number.

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
(int list) xs = [2, 0, 2, 2, 0]
Output:
(string) "8"

Inputs:
(int list) xs = [-2, -3, 4, -5]
Output:
(string) "60"

Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.
'''

def multiply_list (nums):
    product = 1
    for i in nums:
        product = product * i
    return product

def answer(xs):
    # Separate negatives and positives
    positives = [x for x in xs if x > 0]
    negatives = [x for x in xs if x < 0]

    num_neg_supplied = len(negatives)
    
    # The biggest num to be removed from negatives if even length
    removed = 1

    if len(negatives) % 2 == 0:
        # Even length: multiply all to get a positive #
        # If 0 length, neg_product = 1
        neg_product = multiply_list(negatives)
    else:
        # Remove the biggest number in negatives list
        negatives = sorted(negatives)
        try:
            removed = negatives.pop()
        except IndexError:
            pass
        neg_product = multiply_list(negatives)
    if len(positives) == 0 and len(negatives) == 0:
        # No positive but 1 or 0 negative number
        if num_neg_supplied == 0:
            # No negative
            return "0"
        else:
            # one negative
            if len(xs) >= 2:
                # Besides the neg number, there are 0s in the input. 
                return "0"
            else:
                return str(removed)
    elif len(positives) == 0:
        # No positive but > 1 negative
        return str(max(neg_product))
    else:
        # >= 1 positive and >1 neg.
        # don't include the removed neg
        return str(neg_product * multiply_list(positives))
