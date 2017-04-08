/*
   Problem

   A certain bathroom has N + 2 stalls in a single row; the stalls on the left and right ends are permanently occupied by the bathroom guards. The other N stalls are for users.

   Whenever someone enters the bathroom, they try to choose a stall that is as far from other people as possible. To avoid confusion, they follow deterministic rules: For each empty stall S, they compute two values LS and RS, each of which is the number of empty stalls between S and the closest occupied stall to the left or right, respectively. Then they consider the set of stalls with the farthest closest neighbor, that is, those S for which min(LS, RS) is maximal. If there is only one such stall, they choose it; otherwise, they choose the one among those where max(LS, RS) is maximal. If there are still multiple tied stalls, they choose the leftmost stall among those.

   K people are about to enter the bathroom; each one will choose their stall before the next arrives. Nobody will ever leave.

   When the last person chooses their stall S, what will the values of max(LS, RS) and min(LS, RS) be?

   Solving this problem

   This problem has 2 Small datasets and 1 Large dataset. You must solve the first Small dataset before you can attempt the second Small dataset. You will be able to retry either of the Small datasets (with a time penalty). You will be able to make a single attempt at the Large, as usual, only after solving both Small datasets.

   Input

   The first line of the input gives the number of test cases, T. T lines follow. Each line describes a test case with two integers N and K, as described above.

   Output

   For each test case, output one line containing Case #x: y z, where x is the test case number (starting from 1), y is max(LS, RS), and z is min(LS, RS) as calculated by the last person to enter the bathroom for their chosen stall S.

   Limits

   1 ≤ T ≤ 100.
   1 ≤ K ≤ N.
   Small dataset 1

   1 ≤ N ≤ 1000.
   Small dataset 2

   1 ≤ N ≤ 106.
   Large dataset

   1 ≤ N ≤ 1018.

   Sample

   Input 

   5
   4 2
   5 2
   6 2
   1000 1000
   1000 1


   Output 

   Case #1: 1 0
   Case #2: 1 0
   Case #3: 1 1
   Case #4: 0 0
   Case #5: 500 499

   In Case #1, the first person occupies the leftmost of the middle two stalls, leaving the following configuration (O stands for an occupied stall and . for an empty one): O.O..O. Then, the second and last person occupies the stall immediately to the right, leaving 1 empty stall on one side and none on the other.

   In Case #2, the first person occupies the middle stall, getting to O..O..O. Then, the second and last person occupies the leftmost stall.

   In Case #3, the first person occupies the leftmost of the two middle stalls, leaving O..O...O. The second person then occupies the middle of the three consecutive empty stalls.

   In Case #4, every stall is occupied at the end, no matter what the stall choices are.

   In Case #5, the first and only person chooses the leftmost middle stall.
   */

#include<iostream>

using namespace std;

struct empty_stalls {
    long long min {0};
    long long max {0};
};

long long get_even_smaller (long long n) {
    return (n%2 == 0)? n/2 - 1 : n/2;
}

empty_stalls assign_stalls (long long stalls, long long ppl) {
    empty_stalls to_return;
    if ( ppl == 1 ) {
        // Assign the person in the middle
        to_return.max = stalls/2;
        to_return.min = get_even_smaller(stalls);
        return to_return;
    }
    else if ( ppl == 0 ) {
        return to_return;
    }
    else if ( ppl >= stalls ) {
        // (0,0)
        return to_return;
    }
    else {
        // Assign and split
        if ( stalls % 2 == 0 && ppl % 2 == 0 ) {
            // 2nd half is preferred
            return assign_stalls(stalls/2, ppl/2);
        }
        else if ( stalls % 2 == 0 && ppl % 2 != 0 ) {
            // first half is preferred
            // 6,3
            // O......O will eventually become:
            // O..O.O.O so we want spot #1
            return assign_stalls(get_even_smaller(stalls), get_even_smaller(ppl));
        }
        else if ( stalls % 2 != 0 && ppl % 2 != 0 ) {
            // Doesn't matter in this case
            // 2nd half is preferred
            // 5,3
            // O.....O will eventually become:
            // OO.OO..O so we want spot #5
            return assign_stalls(stalls/2, get_even_smaller(ppl));
        }
        else {
            // first half is preferred
            // 7,4
            // O.......O
            // O.O.O.O.O
            // spot #1 is preferred
            return assign_stalls(get_even_smaller(stalls), ppl/2);
        }
    }
}

int main () {
    int rows;
    cin >> rows;

    for ( int i = 1; i <= rows; i++ ) {
        long long N, K; // # of stalls, # of people
        cin >> N >> K;
        empty_stalls a = assign_stalls(N, K);

        // ( Max # of empty stalls, Min # of empty stalls )
        cout << "Case #" << i << ": " << a.max << " " << a.min << endl;
    }
}