/*
   Last year, the Infinite House of Pancakes introduced a new kind of pancake. It has a happy face made of chocolate chips on one side (the "happy side"), and nothing on the other side (the "blank side").

   You are the head cook on duty. The pancakes are cooked in a single row over a hot surface. As part of its infinite efforts to maximize efficiency, the House has recently given you an oversized pancake flipper that flips exactly K consecutive pancakes. That is, in that range of K pancakes, it changes every happy-side pancake to a blank-side pancake, and vice versa; it does not change the left-to-right order of those pancakes.

   You cannot flip fewer than K pancakes at a time with the flipper, even at the ends of the row (since there are raised borders on both sides of the cooking surface). For example, you can flip the first K pancakes, but not the first K - 1 pancakes.

   Your apprentice cook, who is still learning the job, just used the old-fashioned single-pancake flipper to flip some individual pancakes and then ran to the restroom with it, right before the time when customers come to visit the kitchen. You only have the oversized pancake flipper left, and you need to use it quickly to leave all the cooking pancakes happy side up, so that the customers leave feeling happy with their visit.

   Given the current state of the pancakes, calculate the minimum number of uses of the oversized pancake flipper needed to leave all pancakes happy side up, or state that there is no way to do it.

   Input

   The first line of the input gives the number of test cases, T. T test cases follow. Each consists of one line with a string S and an integer K. S represents the row of pancakes: each of its characters is either + (which represents a pancake that is initially happy side up) or - (which represents a pancake that is initially blank side up).

   Output

   For each test case, output one line containing Case #x: y, where x is the test case number (starting from 1) and y is either IMPOSSIBLE if there is no way to get all the pancakes happy side up, or an integer representing the the minimum number of times you will need to use the oversized pancake flipper to do it.

   Limits

   1 ≤ T ≤ 100.
   Every character in S is either + or -.
   2 ≤ K ≤ length of S.
   Small dataset

   2 ≤ length of S ≤ 10.
   Large dataset

   2 ≤ length of S ≤ 1000.
   Sample


   Input 

   Output 

   3
   ---+-++- 3
   +++++ 4
   -+-+- 4

   Case #1: 3
   Case #2: 0
   Case #3: IMPOSSIBLE
   In Case #1, you can get all the pancakes happy side up by first flipping the leftmost 3 pancakes, getting to ++++-++-, then the rightmost 3, getting to ++++---+, and finally the 3 pancakes that remain blank side up. There are other ways to do it with 3 flips or more, but none with fewer than 3 flips.

   In Case #2, all of the pancakes are already happy side up, so there is no need to flip any of them.

   In Case #3, there is no way to make the second and third pancakes from the left have the same side up, because any flip flips them both. Therefore, there is no way to make all of the pancakes happy side up.
   */

/*
 * A general algorithm to do this is to 
 * 1) Check if all pancakes are '+'. If yes, we are done. Otherwise, go to step 2).
 * 2) Locate the first '-' pancake. Then we look at the next K-1 pancakes, flip all of them (incl. the first '-' one)
 * 3) IMPOSSIBLE if a '-' pancake is followed by less than (K-1) pancakes.
 * 4) Repeat step 1)
 * 
 * e.g.
 *
 * If 1 represents '+', and 0 represents '-'
 *
 * Given 00010110, K = 3
 * flip the first 3
 * 11110110
 * we have a 0 at position 4
 * Grab K-1 pancakes after postion 4 -> so we have 011
 * Flip them, we have
 * 11111000
 * 
 * Now we have a 0 at position 5
 * Grab 000
 * Flip them, and get 11111111. Done!
 */

#include<iostream>
#include<vector>

using namespace std;

struct bitset_simple {
    // Should've used boost::dynamic_bitset ......

    private:
        vector<bool> bits;

        // For testing..
        bitset_simple (vector<bool>&& set_to_this) {
            bits = vector<bool>(set_to_this);
        };

    public:

        bitset_simple (string input, char true_char, char false_char) {
            vector<bool> in_bits;
            // Parse input
            for (int i = 0; i < input.length(); i++) {
                if (input[i] == true_char) {
                    in_bits.push_back(true);
                }
                else {
                    in_bits.push_back(false);
                }
            }

            bits = vector<bool>(move(in_bits));
        }

        bool all () {
            for ( int i = 0; i < bits.size(); i++ ) {
                if (!bits[i]) {
                    return false;
                }
            } 
            return true;
        };

        unsigned int size () {
            return bits.size();
        };

        bitset_simple& flip ( size_t pos ) {
            bits[pos] = !bits[pos];
            return *this;
        };

        size_t get_first_false_bit_index () {
            for ( int i = 0; i < bits.size(); i++ ) {
                if ( !bits[i] ) {
                    return i;
                }
            }
            return -1;
        }

        string to_string() {
            string result;
            for (int i = 0; i< bits.size(); i++) {
                if (bits[i]) {
                    result.push_back('1');
                }
                else {
                    result.push_back('0');
                }
            }
            return result;
        }

};

int flip ( bitset_simple& pancakes, const int K ) {
    // Return min number of flips required to have all bits set to true

    //cout << pancakes.to_string() << endl;
    // 1) Check if all bits are set to true already
    if (pancakes.all()) {
        // All bits are set. DONE
        return 0;
    }
    // 2) Find the first '-' pancake
    else {
        int first_false_bit_index = pancakes.get_first_false_bit_index();
        if ( first_false_bit_index == -1 || first_false_bit_index + K > pancakes.size() ) {
            // Not enough pancakes left
            // Impossible
            throw 1;
        }
        // Flip bits
        for ( int i = first_false_bit_index; i < first_false_bit_index + K; i++ ) {
            pancakes.flip(i);
        }
        return 1 + flip(pancakes, K);
    }
}

int main () {
    int rows;
    cin >> rows;

    for ( int i = 1; i <= rows; i++ ) {
        // Get input
        string input;
        int k;
        cin >> input >> k;

        // Get min # of flips
        cout << "Case #" << i << ": ";
        bitset_simple bits = bitset_simple(input, '+', '-');
        int num_flips;
        try {
            num_flips = flip(bits, k);
        }
        catch (int& e ){
            cout << "IMPOSSIBLE" << endl;
            continue;
        }

        cout << num_flips << endl;
    }
}
