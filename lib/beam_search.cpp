#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
#include <chrono>
#include <fstream>
#include <random>
#include <unordered_set>
using namespace std;
using namespace std::chrono;

namespace zobrist_hash{
    uint64_t boards[400] = {};
    void init(){
        auto mt = mt19937_64(0);
        for (int i = 0; i < 400; i++) {
            boards[i] = mt();
        }
    }
};

int DX[] = {0, 1, 0, -1};
int DY[] = {1, 0, -1, 0};
char DIR[] = {'R', 'D', 'L', 'U'};

class Action {
    public:
        string action;
        Action() {
            action = "WAIT";
        }
        Action(const string &action) : action(action) {}

    string to_string() const {
        return action;
    }
};

class State {
    private:
        int ref_count = 0;
    public:
        int N;
        int M;
        vector<int> board;
        vector<Action> actions;
        uint64_t hash = 0;
        double score = 0.0;
        double e_score = 0.0;
        bool is_done = false;
        State() {}
        State(const int N, const int M) : N(N), M(M) {
            board = vector<int>(N*N,0);
        }

    vector<Action> legal_actions() {
        vector<Action> actions;
        if (actions.empty()) {
            actions.push_back(Action());
        }
        return actions;
    }

    void advance(Action action) {
    }

    void evaluate_score() {
        e_score = 0;
        if (is_done) return;
    }

    void init() {
        ref_count = 1;
    }

    void release() {
        ref_count--;
        if (ref_count == 0) {
            delete this;
        }
    }

    void retain() {
        ref_count++;
    }

    bool operator<(const State &state) const {
        return score + e_score < state.score + state.e_score;
    }

};

class StatePtr {
    public:
        State *state;

    StatePtr(const State &state) {
        this->state = new State();
        *this->state = state;
        this->state->init();
    }

    StatePtr(const StatePtr &state_ptr) : state(state_ptr.state) {
        state->retain();
    }

    ~StatePtr() {
        state->release();
    }

    void operator=(const StatePtr &state_ptr) {
        if (state != state_ptr.state) {
            state->release();
            state = state_ptr.state;
            state->retain();
        }
    }
};

bool operator<(const StatePtr &state_ptr1, const StatePtr &state_ptr2) {
    return *state_ptr1.state < *state_ptr2.state;
}

vector<Action> beamSearchAction(State &state,int w,int d,double ts) {
    auto current_time = high_resolution_clock::now();
    auto hash_check = unordered_set<uint64_t>();
    priority_queue<StatePtr> now_beam;
    State best_state;
    now_beam.emplace(state);
    for (int t = 0; t < d; ++t){
        auto diff = high_resolution_clock::now() - current_time;
        auto ms = duration_cast<milliseconds>(diff).count();
        if (ms > ts) break;
        priority_queue<StatePtr> next_beam;
        for (int i = 0; i < w; ++i){
            auto diff = high_resolution_clock::now() - current_time;
            auto ms = duration_cast<milliseconds>(diff).count();
            if (ms > ts) break;
            if (now_beam.empty()) break;
            State now_state = *now_beam.top().state;
            now_beam.pop();
            for (auto action : now_state.legal_actions()) {
                State next_state = now_state;
                next_state.advance(action);
                if (hash_check.count(next_state.hash)) continue;
                hash_check.emplace(next_state.hash);
                next_state.evaluate_score();
                next_state.actions.emplace_back(action);
                next_beam.emplace(next_state);
            }
        }
        if (next_beam.empty()) break;
        swap(now_beam,next_beam);
        best_state = *now_beam.top().state;
        if (best_state.is_done) break;
    }
    return best_state.actions;
}

int main() {
    zobrist_hash::init();
    int N, M;
    cin >> N >> M;
    State state = State(N,M);
    vector<Action> actions = beamSearchAction(state, 150, 1600, 2000);
    for (auto action : actions) {
        cout << action.to_string() << endl;
    }
}