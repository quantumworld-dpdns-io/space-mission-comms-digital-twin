from __future__ import annotations

import heapq
from typing import Any, Callable, Dict, List, Optional, Tuple


class RouteOptimizer:
    def __init__(self, graph: Dict[str, Dict[str, float]]):
        self.graph = graph

    def dijkstra_shortest_path(self, source: str, target: str) -> Tuple[Optional[List[str]], float]:
        distances = {node: float('inf') for node in self.graph}
        distances[source] = 0.0
        previous = {node: None for node in self.graph}
        pq = [(0.0, source)]

        while pq:
            current_dist, current = heapq.heappop(pq)
            if current == target:
                path = self._reconstruct_path(previous, target)
                return path, distances[target]
            if current_dist > distances[current]:
                continue
            for neighbor, weight in self.graph.get(current, {}).items():
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))

        return None, float('inf')

    def a_star_search(self, source: str, target: str, heuristic: Callable[[str, str], float]) -> Tuple[Optional[List[str]], float]:
        open_set = {source}
        came_from: Dict[str, Optional[str]] = {}
        g_score = {node: float('inf') for node in self.graph}
        g_score[source] = 0.0
        f_score = {node: float('inf') for node in self.graph}
        f_score[source] = heuristic(source, target)

        while open_set:
            current = min(open_set, key=lambda n: f_score[n])
            if current == target:
                path = self._reconstruct_path(came_from, target)
                return path, g_score[current]

            open_set.remove(current)
            for neighbor, weight in self.graph.get(current, {}).items():
                tentative = g_score[current] + weight
                if tentative < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative
                    f_score[neighbor] = tentative + heuristic(neighbor, target)
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        return None, float('inf')

    def delay_tolerant_routing(self, source: str, target: str, contacts: List[Dict], deadline: float) -> Optional[List[str]]:
        time_graph: Dict[str, List[Tuple[str, float, float]]] = {}
        for contact in contacts:
            src = contact["source"]
            dst = contact["dest"]
            start = contact["start"]
            end = contact["end"]
            if src not in time_graph:
                time_graph[src] = []
            time_graph[src].append((dst, start, end))

        visited = set()
        path = []
        current = source
        current_time = 0.0

        while current != target and current_time < deadline:
            visited.add(current)
            path.append(current)
            best_next = None
            best_arrival = float('inf')
            for neighbor, start, end in time_graph.get(current, []):
                if neighbor in visited:
                    continue
                if current_time <= start and start < best_arrival:
                    best_next = neighbor
                    best_arrival = start
            if best_next is None:
                break
            current = best_next
            current_time = best_arrival

        if current == target:
            path.append(target)
            return path
        return None

    def multi_path_routing(self, source: str, target: str, k: int = 3) -> List[Tuple[List[str], float]]:
        paths: List[Tuple[List[str], float]] = []
        banned_edges: List[Tuple[str, str]] = []

        for _ in range(k):
            temp_graph = {n: dict(edges) for n, edges in self.graph.items()}
            for u, v in banned_edges:
                if u in temp_graph and v in temp_graph[u]:
                    del temp_graph[u][v]

            router = RouteOptimizer(temp_graph)
            path, cost = router.dijkstra_shortest_path(source, target)
            if path is None:
                break

            paths.append((path, cost))
            for i in range(len(path) - 1):
                banned_edges.append((path[i], path[i + 1]))

        return paths

    def load_balancing(self, traffic_matrix: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        link_loads: Dict[str, float] = {}
        for src in traffic_matrix:
            for dst in traffic_matrix[src]:
                path, _ = self.dijkstra_shortest_path(src, dst)
                if path:
                    for i in range(len(path) - 1):
                        link = f"{path[i]}->{path[i + 1]}"
                        link_loads[link] = link_loads.get(link, 0.0) + traffic_matrix[src][dst]
        return link_loads

    def _reconstruct_path(self, previous: Dict[str, Optional[str]], target: str) -> List[str]:
        path = []
        current: Optional[str] = target
        while current is not None:
            path.append(current)
            current = previous[current]
        return list(reversed(path))
