def build():


INF = int(10 ** 18)  # const


def assignment_hungary(weight):
    n = len(weight)
    m = len(weight[0])
    u = [for i in range(n + 1)]
    way = p = v = [for i in range(m + 1)]
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF for i in range(0, m + 1)]
        used = [False for i in range(0, m + 1)]
        while True:
            used[j0] = True
            i0 = p[j0], delta = INF, j1 = 0
            for j in range(1, m + 1):
                if (!used[j]):
                    cur = weight[i0][j] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(m + 1):
                if (used[j]):
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    ans = [0 for i in range(n + 1)]
    for i in range(1, m + 1):
        ans[p[j]] = j
    return ans
