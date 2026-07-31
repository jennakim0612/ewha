#건물
graph_simple = {
    'mus': {'baek': 10, 'bon': 15, 'lb': 20, 'dm': 25, 'ygs': 30, 'gym': 35},
    'baek': {'mus': 10, 'bon': 35, 'lb': 25, 'dm': 30, 'ygs': 20, 'gym': 40},
    'bon': {'mus': 15, 'baek': 35, 'lb': 30, 'dm': 20, 'ygs': 25, 'gym': 30},
    'lb': {'mus': 20, 'baek': 25, 'bon': 30, 'dm': 10, 'ygs': 15, 'gym': 20},
    'dm': {'mus': 25, 'baek': 30, 'bon': 20, 'lb': 10, 'ygs': 35, 'gym': 15},
    'ygs': {'mus': 30, 'baek': 20, 'bon': 25, 'lb': 15, 'dm': 35, 'gym': 10},
    'gym': {'mus': 35, 'baek': 40, 'bon': 30, 'lb': 20, 'dm': 15, 'ygs': 10}
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
path, cost = tsp_brute_force(graph_simple, 'mus')
print(f"완전 탐색 최적 경로: {path}")
print(f"완전 탐색 최단 거리: {cost}")
