import time
import random
import matplotlib.pyplot as plt


parcels = [
    {"id": "P1", "weight": 5, "value": 60, "deadline": 3},
    {"id": "P2", "weight": 4, "value": 50, "deadline": 1},
    {"id": "P3", "weight": 6, "value": 80, "deadline": 2},
    {"id": "P4", "weight": 3, "value": 40, "deadline": 4},
    {"id": "P5", "weight": 2, "value": 30, "deadline": 1}
]

capacity = 15

graph = {
    "W": {"A": 4, "B": 6, "C": 8},
    "A": {"W": 4, "B": 2, "D": 5},
    "B": {"W": 6, "A": 2, "C": 3},
    "C": {"W": 8, "B": 3, "D": 2},
    "D": {"A": 5, "C": 2}
}

print("Mini-Courier Planner")
print("-------------------")
print("Parcels:")

for parcel in parcels:
    print(parcel)

print("\nDelivery Network:")
for location in graph:
    print(location, ":", graph[location])

def merge_sort(parcels):
    if len(parcels) <= 1:
        return parcels

    mid = len(parcels) // 2

    left = merge_sort(parcels[:mid])
    right = merge_sort(parcels[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i]["deadline"] <= right[j]["deadline"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

def knapsack(parcels, capacity):
    n = len(parcels)

    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = parcels[i - 1]["weight"]
        value = parcels[i - 1]["value"]

        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(value + dp[i - 1][w - weight], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    selected = []
    w = capacity

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(parcels[i - 1])
            w -= parcels[i - 1]["weight"]

    selected.reverse()

    return selected, dp[n][capacity]

import heapq


def dijkstra(graph, start):
    distances = {}

    for location in graph:
        distances[location] = float("inf")

    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_location = heapq.heappop(pq)

        if current_distance > distances[current_location]:
            continue

        for neighbor, weight in graph[current_location].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

def nearest_neighbor(graph, start):
    all_distances = {}

    for location in graph:
        all_distances[location] = dijkstra(graph, location)

    visited = [start]
    current = start
    total_distance = 0

    while len(visited) < len(graph):
        nearest = None
        min_distance = float("inf")

        for location in graph:
            if location not in visited:
                distance = all_distances[current][location]

                if distance < min_distance:
                    min_distance = distance
                    nearest = location

        visited.append(nearest)
        total_distance += min_distance
        current = nearest

    total_distance += all_distances[current][start]
    visited.append(start)

    return visited, total_distance

print("\nVan Capacity:", capacity, "kg")

sorted_parcels = merge_sort(parcels)
selected_parcels, total_value = knapsack(parcels, capacity)

shortest_distances = dijkstra(graph, "W")

print("\nShortest Distances from Warehouse:")
for location, distance in shortest_distances.items():
    print("W to", location, "=", distance, "km")

print("\nSelected Parcels for Packing:")
total_weight = 0

for parcel in selected_parcels:
    print(parcel["id"], "Weight:", parcel["weight"], "Value:", parcel["value"])
    total_weight += parcel["weight"]

print("Total Weight:", total_weight, "kg")
print("Total Value:", total_value)

print("\nParcels Sorted by Deadline:")
for parcel in sorted_parcels:
    print(parcel["id"], "Deadline:", parcel["deadline"])

route, route_distance = nearest_neighbor(graph, "W")

print("\nDelivery Route:")
print(" -> ".join(route))
print("Total Route Distance:", route_distance, "km")

def generate_test_data(size):
    test_parcels = []

    for i in range(size):
        test_parcels.append({
            "id": "P" + str(i + 1),
            "weight": random.randint(1, 10),
            "value": random.randint(10, 100),
            "deadline": random.randint(1, size)
        })

    test_graph = {}

    for i in range(size):
        test_graph[str(i)] = {}

    for i in range(size - 1):
        weight = random.randint(1, 10)
        test_graph[str(i)][str(i + 1)] = weight
        test_graph[str(i + 1)][str(i)] = weight

    for i in range(size):
        for j in range(i + 2, size):
            if random.random() < 0.15:
                weight = random.randint(1, 10)
                test_graph[str(i)][str(j)] = weight
                test_graph[str(j)][str(i)] = weight

    return test_parcels, test_graph


def performance_test():
    sizes = [5, 10, 20, 30]

    merge_times = []
    knapsack_times = []
    dijkstra_times = []
    route_times = []

    for size in sizes:
        test_parcels, test_graph = generate_test_data(size)

        start = time.perf_counter()
        merge_sort(test_parcels)
        merge_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        knapsack(test_parcels, 50)
        knapsack_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        dijkstra(test_graph, "0")
        dijkstra_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        nearest_neighbor(test_graph, "0")
        route_times.append(time.perf_counter() - start)

    print("\nPerformance Results")
    print("-----------------")

    for i in range(len(sizes)):
        print("\nInput Size:", sizes[i])
        print("Merge Sort:", merge_times[i], "seconds")
        print("Knapsack:", knapsack_times[i], "seconds")
        print("Dijkstra:", dijkstra_times[i], "seconds")
        print("Nearest Neighbor:", route_times[i], "seconds")

    plt.plot(sizes, merge_times, marker="o", label="Merge Sort")
    plt.plot(sizes, knapsack_times, marker="o", label="Knapsack")
    plt.plot(sizes, dijkstra_times, marker="o", label="Dijkstra")
    plt.plot(sizes, route_times, marker="o", label="Nearest Neighbor")

    plt.xlabel("Input Size")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Algorithm Performance Comparison")
    plt.legend()
    plt.grid(True)
    plt.savefig("performance_chart.png")
    plt.show()


performance_test()