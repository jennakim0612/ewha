import sys

graph_simple = {
    'mus': {'baek': 40, 'bon': 180, 'lb': 316, 'dm': 302, 'ygs': 362, 'gym': 467},
    'baek': {'mus': 40, 'bon': 100, 'lb': 236, 'dm': 222, 'ygs': 282, 'gym': 387},
    'bon': {'mus': 180, 'baek': 100, 'lb':136, 'dm': 122, 'ygs': 167, 'gym': 292},
    'lb': {'mus': 316, 'baek': 236, 'bon': 136 , 'dm': 258, 'ygs': 261, 'gym': 156},
    'dm': {'mus': 302, 'baek': 222, 'bon': 122, 'lb': 258, 'ygs': 60, 'gym': 165},
    'ygs': {'mus': 362, 'baek': 282, 'bon': 167, 'lb': 261, 'dm': 60, 'gym': 105},
    'gym': {'mus': 467, 'baek': 387, 'bon': 292, 'lb': 156, 'dm': 165, 'ygs': 105}
}

memo = {}
nodes = list(graph_simple.keys())
nodes_map = {node: i for i, node in enumerate(nodes)}

def tsp_dp(graph, current_node_idx, visited_mask):
    # 종료 조건
    if visited_mask == (1 << len(nodes)) - 1:
        start = nodes[0]
        current = nodes[current_node_idx]
        return graph[current][start]

    # 메모 확인
    if (current_node_idx, visited_mask) in memo:
        return memo[(current_node_idx, visited_mask)]

    min_cost = sys.maxsize

    for next_node_idx in range(len(nodes)):
        if not (visited_mask & (1 << next_node_idx)):
            cost = (
                graph[nodes[current_node_idx]][nodes[next_node_idx]] +
                tsp_dp(graph, next_node_idx, visited_mask | (1 << next_node_idx))
            )
            min_cost = min(min_cost, cost)

    memo[(current_node_idx, visited_mask)] = min_cost
    return min_cost

# 실행
cost_dp = tsp_dp(graph_simple, 0, 1)
print(f"동적 계획법 최단 거리: {cost_dp}")
