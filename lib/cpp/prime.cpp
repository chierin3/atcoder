#include <bits/stdc++.h>
using namespace std;

namespace prime {
    int M = 1e6;
    vector<int> is_prime(M + 1);
    void init() {
        for (int i = 0; i <= M; i++) {
            is_prime[i] = i;
        }
        int i = 2;
        while (i * i <= M) {
            if (is_prime[i] == i) {
                for (int j = i * i; j <= M; j += i) {
                    if (is_prime[j] == j) {
                        is_prime[j] = i;
                    }
                }
            }
            i++;
        }
    }
}
 
int main() {
    prime::init();
}