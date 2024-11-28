#include <iostream>
#include <vector>
#include <random>
#include <set>
#include <map>
#include <algorithm>
#include <numeric>
#include <fstream>

using namespace std;

bool isValidMapping(const vector<vector<int>>& G1, const vector<vector<int>>& G2, 
                    const vector<int>& mapping1, const vector<int>& mapping2, int v1, int v2) {

    if (G1[v1].size() != G2[v2].size()) {
        return false;
    }

    for (int i = 0; i < G1.size(); ++i) {
        if (G1[v1][i] == 1 && mapping1[i] != -1) {
            if (G2[v2][mapping1[i]] != 1) {
                return false;
            }
        }
    }
    
    return true;
}

bool vf2Recursive(const vector<vector<int>>& G1, const vector<vector<int>>& G2, 
                  vector<int>& mapping1, vector<int>& mapping2, set<int>& matched1, set<int>& matched2) {

    if (matched1.size() == G1.size()) {
        return true;
    }
    
    for (int v1 = 0; v1 < G1.size(); ++v1) {
        if (matched1.find(v1) == matched1.end()) {
            for (int v2 = 0; v2 < G2.size(); ++v2) {
                if (matched2.find(v2) == matched2.end() && isValidMapping(G1, G2, mapping1, mapping2, v1, v2)) {
                    mapping1[v1] = v2;
                    mapping2[v2] = v1;
                    matched1.insert(v1);
                    matched2.insert(v2);
                    
                    if (vf2Recursive(G1, G2, mapping1, mapping2, matched1, matched2)) {
                        return true;
                    }
                
                    mapping1[v1] = -1;
                    mapping2[v2] = -1;
                    matched1.erase(v1);
                    matched2.erase(v2);
                }
            }
            return false;
        }
    }
    
    return false;
}

bool areIsomorphic(const vector<vector<int>>& G1, const vector<vector<int>>& G2) {
    int n = G1.size();
    if (n != G2.size()) return false;
    
    vector<int> mapping1(n, -1), mapping2(n, -1);
    set<int> matched1, matched2;
    
    return vf2Recursive(G1, G2, mapping1, mapping2, matched1, matched2);
}

pair<vector<vector<int>>, vector<vector<int>>> generate_isomorphic_graphs(int n) {
    vector<vector<int>> A(n, vector<int>(n, 0));
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 1);

    for (int i = 0; i < n; ++i) {
        for (int j = i; j < n; ++j) {
            int edge = dis(gen);
            A[i][j] = edge;
            A[j][i] = edge;
        }
    }

    vector<int> permutation(n);
    iota(permutation.begin(), permutation.end(), 0);
    shuffle(permutation.begin(), permutation.end(), gen);

    vector<vector<int>> B(n, vector<int>(n, 0));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            B[i][j] = A[permutation[i]][permutation[j]];
        }
    }

    return {A, B};
}

void writeMatrixToCSV(const vector<vector<int>>& mat, const string& filename) {
    ofstream file(filename);
    for (int i = 0; i < mat.size(); ++i) {
        for (int j = 0; j < mat[i].size(); ++j) {
            file << mat[i][j];
            if (j < mat[i].size() - 1) {
                file << ", ";
            }
        }
        file << endl;
    }
    file.close();
}

void printMatrix(const vector<vector<int>>& mat) {
    for (int i = 0; i < mat.size(); ++i) {
        for (int j = 0; j < mat[i].size(); ++j) {
            cout << mat[i][j] << " ";
        }
        cout << "\n";
    }
}

int main() {
    int n;
    cout << "Enter the number of vertices (max 100): ";
    cin >> n;

    auto [G1, G2] = generate_isomorphic_graphs(n);

    cout << "Graph 1:\n";
    printMatrix(G1);

    cout << "\nGraph 2:\n";
    printMatrix(G2);

    if (areIsomorphic(G1, G2)) {
        cout << "Isomorphic.\n";
    } else {
        cout << "Not Isomorphic.\n";
    }

    writeMatrixToCSV(G1, "graph1.csv");
    writeMatrixToCSV(G2, "graph2.csv");

    return 0;
}