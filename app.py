from flask import Flask, request, jsonify

app = Flask(__name__)

# Define your data structures to store cab details, pricing, and booking information
cabs = {
    'Cab1': {'price_per_minute': 2.5},
    'Cab2': {'price_per_minute': 3.0},
    'Cab3': {'price_per_minute': 3.5},
    'Cab4': {'price_per_minute': 4.0},
    'Cab5': {'price_per_minute': 4.5}
}

# Define a graph to represent destinations and their distances
destinations = {
    'A': {'B': 5, 'C': 7},
    'B': {'A': 5, 'D': 15, 'E':20},
    'C': {'A': 7, 'D': 5, 'E': 35},
    'D': {'B': 15, 'C': 5, 'F': 20},
    'E': {'B': 20, 'C': 35, 'F': 10},
    'F': {'D': 20, 'E': 10}
}

booked_trips = {}  # Dictionary to simulate booked trips

def dijkstra(graph, start, end):
    # Implementation of Dijkstra's algorithm to find the shortest path
    shortest_path = {}
    predecessors = {}
    unvisited_nodes = graph

    for node in unvisited_nodes:
        shortest_path[node] = float('inf')
    shortest_path[start] = 0

    while unvisited_nodes:
        min_node = None
        for node in unvisited_nodes:
            if min_node is None:
                min_node = node
            elif shortest_path[node] < shortest_path[min_node]:
                min_node = node

        for neighbor, weight in graph[min_node].items():
            if weight + shortest_path[min_node] < shortest_path[neighbor]:
                shortest_path[neighbor] = weight + shortest_path[min_node]
                predecessors[neighbor] = min_node
        unvisited_nodes.pop(min_node)

    node = end
    path = []
    while node in predecessors:
        path.insert(0, node)
        node = predecessors[node]
    path.insert(0, start)
    return path, shortest_path[end]

# Define an endpoint to book a cab
@app.route('/book', methods=['POST'])
def book_cab():
    data = request.get_json()
    email = data['email']
    source = data['source']
    destination = data['destination']
    cab_choice = data['cab_choice']

    if source not in destinations or destination not in destinations:
        return jsonify({'message': 'Invalid source or destination'})

    if email not in booked_trips:
        booked_trips[email] = []

    # Calculate the shortest route and estimated cost
    shortest_path, shortest_time = dijkstra(destinations, source, destination)
    price_per_minute = cabs[cab_choice]['price_per_minute']
    estimated_cost = shortest_time * price_per_minute

    # Simulate the booking by adding it to the user's booked trips
    booked_trips[email].append({
        'source': source,
        'destination': destination,
        'cab_choice': cab_choice,
        'shortest_path': shortest_path,
        'estimated_cost': estimated_cost
    })

    return jsonify({'message': 'Cab booked successfully', 'shortest_path': shortest_path, 'estimated_cost': estimated_cost})

if __name__ == '__main__':
    app.run(debug=True)

