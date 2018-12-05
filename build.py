def assignment_hungary(weight0):
    n = len(weight0)
    m = len(weight0[0])
    weight = [[0] * (len(weight0) + 1)] + [[0] + [-x for x in i] for i in weight0]
    u = [0] * (n + 1)
    INF = 10 ** 20
    way = [0] * (m + 1)
    p = [0] * (m + 1)
    v = [0] * (m + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (m + 1)
        used = [False] * (m + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = INF
            j1 = 0
            for j in range(1, m + 1):
                if not used[j]:
                    print(i0, j)
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
    res = [0] * (n + 1)
    for j in range(1, m + 1):
        res[p[j]] = j
    return res
