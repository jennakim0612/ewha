#건물
graph_simple = {
    'mus': {'baek': 40, 'bon': 180, 'lb': 316, 'dm': 302, 'ygs': 362, 'gym': 467},
    'baek': {'mus': 40, 'bon': 100, 'lb': 236, 'dm': 222, 'ygs': 282, 'gym': 387},
    'bon': {'mus': 180, 'baek': 100, 'lb':136, 'dm': 122, 'ygs': 167, 'gym': 292},
    'lb': {'mus': 316, 'baek': 236, 'bon': 136 , 'dm': 258, 'ygs': 261, 'gym': 156},
    'dm': {'mus': 302, 'baek': 222, 'bon': 122, 'lb': 258, 'ygs': 60, 'gym': 165},
    'ygs': {'mus': 362, 'baek': 282, 'bon': 167, 'lb': 261, 'dm': 60, 'gym': 105},
    'gym': {'mus': 467, 'baek': 387, 'bon': 292, 'lb': 156, 'dm': 165, 'ygs': 105}
}


import itertools
import sys

def tsp_brute_force(graph, start_node):
    nodes = list(graph.keys())
    nodes.remove(start_node)

    min_path_cost = sys.maxsize
    best_path = []

    # 시작점을 제외한 모든 노드의 순열 생성
    for path_permutation in itertools.permutations(nodes):
        current_path_cost = 0
        current_path = [start_node] + list(path_permutation)

        # 경로 비용 계산
        k = start_node
        for next_node in path_permutation:
            current_path_cost += graph[k][next_node]
            k = next_node

        # 시작 노드로 복귀 비용
        current_path_cost += graph[k][start_node]

        # 최소 비용 경로 갱신
        if current_path_cost < min_path_cost:
            min_path_cost = current_path_cost
            best_path = current_path + [start_node]

    return best_path, min_path_cost


# 실행
path, cost = tsp_brute_force(graph_simple, 'baek') #출발위치
print(f"완전 탐색 최적 경로: {path}")
print(f"완전 탐색 최단 거리: {cost}")
