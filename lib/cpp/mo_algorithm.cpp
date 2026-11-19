#include <bits/stdc++.h>
using namespace std;

vector<int> D;

void add(int x, int& count) {
    D[x]++;
    if (D[x] == 1) {
        count++;
    }
}

void remove(int x, int& count) {
    D[x]--;
    if (D[x] == 0) {
        count--;
    }
}
 
int main() {
    int N, Q;
    cin >> N >> Q;
    vector<int> A(N);
    vector<int> ans(Q);
    for (int i = 0; i < N; i++) {
        cin >> A[i];
    }
    D = vector<int>(*max_element(A.begin(), A.end()) + 1);
    int width = max(1, (int)(N / sqrt(Q)));
    vector<vector<tuple<int, int, int>>> qs = vector<vector<tuple<int, int, int>>>(N / width + 1);
    for (int i = 0; i < Q; i++) {
        int l, r;
        cin >> l >> r;
        l--;
        r--;
        qs[l / width].push_back(make_tuple(r, l, i));
    }
    int x = 0;
    int y = -1;
    int count = 0;
    for (int i = 0; i < qs.size(); i++) {
        sort(qs[i].begin(), qs[i].end(), [i](const tuple<int, int, int>& a, const tuple<int, int, int>& b) {
            return (i & 1) ? get<0>(a) > get<0>(b) : get<0>(a) < get<0>(b);
        });
        for (auto [r, l, j] : qs[i]) {
            while (x > l) {
                x--;
                add(A[x], count);
            }
            while (y < r) {
                y++;
                add(A[y], count);
            }
            while (x < l) {
                remove(A[x], count);
                x++;
            }
            while (y > r) {
                remove(A[y], count);
                y--;
            }
            ans[j] = count;
        }
    }
    for (int a : ans) {
        cout << a << endl;
    }
    return 0;
}