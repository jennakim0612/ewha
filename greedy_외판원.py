import heapq

# =========================
# 그래프 정의
# =========================
graph_simple = {
    'mus': {'baek': 40, 'bon': 180, 'lb': 316, 'dm': 302, 'ygs': 362, 'gym': 467},
    'baek': {'mus': 40, 'bon': 100, 'lb': 236, 'dm': 222, 'ygs': 282, 'gym': 387},
    'bon': {'mus': 180, 'baek': 100, 'lb':136, 'dm': 122, 'ygs': 167, 'gym': 292},
    'lb': {'mus': 316, 'baek': 236, 'bon': 136 , 'dm': 258, 'ygs': 261, 'gym': 156},
    'dm': {'mus': 302, 'baek': 222, 'bon': 122, 'lb': 258, 'ygs': 60, 'gym': 165},
    'ygs': {'mus': 362, 'baek': 282, 'bon': 167, 'lb': 261, 'dm': 60, 'gym': 105},
    'gym': {'mus': 467, 'baek': 387, 'bon': 292, 'lb': 156, 'dm': 165, 'ygs': 105}
}


# =========================
# 1. Prim 알고리즘으로 MST 생성
# =========================
def prim_mst(graph, start):
    mst = {node: [] for node in graph}
    visited = set([start])
    edges = []

    for to, cost in graph[start].items():
        heapq.heappush(edges, (cost, start, to))

    while edges:
        cost, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst[frm].append(to)
            mst[to].append(frm)

            for next_to, next_cost in graph[to].items():
                if next_to not in visited:
                    heapq.heappush(edges, (next_cost, to, next_to))

    return mst

# =========================
# 2. MST 전위 순회 (DFS)
# =========================
def preorder_traversal(mst, start):
    visited = set()
    order = []

    def dfs(node):
        visited.add(node)
        order.append(node)
        for next_node in mst[node]:
            if next_node not in visited:
                dfs(next_node)

    dfs(start)
    return order

# =========================
# 3. MST 기반 TSP 근사 알고리즘
# =========================
def tsp_mst_approx(graph, start):
    mst = prim_mst(graph, start)
    order = preorder_traversal(mst, start)

    cost = 0
    for i in range(len(order) - 1):
        cost += graph[order[i]][order[i + 1]]

    cost += graph[order[-1]][start]
    order.append(start)

    return order, cost

# =========================
# 실행
# =========================
start_node = 'baek'
path, cost = tsp_mst_approx(graph_simple, start_node)

print("MST 기반 근사 경로:", path)
print("MST 기반 근사 거리:", cost)
