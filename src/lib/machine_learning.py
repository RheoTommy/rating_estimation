from typing import List, Tuple
import numpy as np
import random as rd

from src.lib.assembler_graph import Graph, construct_graph_from_assembler


# Weisfeiler Lehman subtree kernel
# ref : https://jmlr.csail.mit.edu/papers/volume12/shervashidze11a/shervashidze11a.pdf
# time complexity : O(Nhm + N^2hn)
def calc_kernel_gram_matrix(n: int, h: int, graphs: List[Graph]) -> np.ndarray:
    N = len(graphs)
    res = np.ndarray(shape=(N, N), dtype=int)
    res.fill(0)
    c = [[[0 for ___ in range(0, n)] for __ in range(0, N)] for _ in range(0, h + 1)]
    for i in range(0, N):
        assert len(graphs[i].label) == n
        c[0][i] = graphs[i].label
    sigma = 2
    for i in range(1, h + 1):
        adj = [[[0 for ___ in range(0, 0)] for __ in range(0, n)] for _ in range(0, N)]
        bucket = [[(0, 0) for __ in range(0, 0)] for _ in range(0, sigma)]
        for j in range(0, N):
            for k in range(0, n):
                adj[j][k].append(c[i - 1][j][k])
                for ak in graphs[j].adj[k]:
                    bucket[c[i - 1][j][ak]].append((j, k))
        for ch in range(0, sigma):
            for j, k in bucket[ch]:
                adj[j][k].append(ch)
        mx_len = 0
        for j in range(0, N):
            for k in range(0, n):
                mx_len = max(mx_len, len(adj[j][k]))
        bucket = [[(0, 0) for __ in range(0, 0)] for _ in range(0, mx_len)]
        for j in range(0, N):
            for k in range(0, n):
                bucket[len(adj[j][k]) - 1].append((j, k))
        ls = []
        idx = [-1 for _ in range(0, sigma)]
        bucket2 = [[(0, 0) for __ in range(0, 0)] for _ in range(0, sigma)]
        for l in range(mx_len - 1, -1, -1):
            it = 0
            hist = []
            for j, k in bucket[l]:
                now = adj[j][k][l]
                if idx[now] == -1:
                    idx[now] = it
                    it += 1
                    hist.append(now)
                bucket2[idx[now]].append((j, k))
            for j, k in ls:
                now = adj[j][k][l]
                if idx[now] == -1:
                    idx[now] = it
                    it += 1
                    hist.append(now)
                bucket2[idx[now]].append((j, k))
            ls.clear()
            for b in range(0, it):
                for j, k in bucket2[b]:
                    ls.append((j, k))
                bucket2[b].clear()
            for ch in hist:
                idx[ch] = -1
        sigma = 0
        phi = [[[] for __ in range(0, 0)] for _ in range(0, N)]
        assert len(ls) == N * n
        for t in range(0, N * n):
            j, k = ls[t]
            if t == 0 or adj[j][k] != adj[ls[t - 1][0]][ls[t - 1][1]]:
                sigma += 1
            c[i][j][k] = sigma - 1
            if len(phi[j]) > 0 and phi[j][-1][0] == sigma - 1:
                phi[j][-1][1] += 1
            else:
                phi[j].append([sigma - 1, 1])
        for j in range(0, N):
            for k in range(j, N):
                cnt = 0
                ji = ki = 0
                while ji < len(phi[j]) and ki < len(phi[k]):
                    if phi[j][ji][0] == phi[k][ki][0]:
                        cnt += phi[j][ji][1] * phi[k][ki][1]
                        ji += 1
                        ki += 1
                    elif phi[j][ji][0] < phi[k][ki][0]:
                        ji += 1
                    else:
                        ki += 1
                res[j][k] += cnt
                if j != k:
                    res[k][j] += cnt

    return res
