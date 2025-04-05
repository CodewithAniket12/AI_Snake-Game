import heapq
import random

class AIController:
    def __init__(self, snake_position, fruit_position, snake_body, window_x, window_y):
        self.snake_position = snake_position
        self.fruit_position = fruit_position
        self.snake_body = snake_body
        self.window_x = window_x
        self.window_y = window_y

    def is_safe_move(self, new_position):
        # Check if new position is within bounds
        if (new_position[0] < 0 or new_position[0] >= self.window_x or
            new_position[1] < 0 or new_position[1] >= self.window_y):
            return False
        
        # Check if new position collides with snake body
        return new_position not in self.snake_body[1:]

    def get_direction(self):
        path = self.find_path()
        if path and len(path) > 1:
            next_position = path[1]
            return self.get_direction_from_position(next_position)
        
        # If no path found, move randomly but safely
        safe_moves = self.get_safe_moves()
        return random.choice(safe_moves) if safe_moves else 'UP'  # Default move

    def find_path(self):
        open_list = []
        closed_list = set()
        came_from = {}

        # Starting node
        start = tuple(self.snake_position)
        goal = tuple(self.fruit_position)

        # Priority queue (heap) for A* with (f, node)
        heapq.heappush(open_list, (0 + self.heuristic(start, goal), 0, start))  # (f, g, position)

        # Maps node to cost to reach that node (g)
        g_costs = {start: 0}

        while open_list:
            _, g, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            closed_list.add(current)

            for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                neighbor = self.get_new_position(list(current), direction)
                if not self.is_safe_move(neighbor) or tuple(neighbor) in closed_list:
                    continue

                tentative_g = g + 1
                if tuple(neighbor) not in g_costs or tentative_g < g_costs[tuple(neighbor)]:
                    came_from[tuple(neighbor)] = current
                    g_costs[tuple(neighbor)] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f, tentative_g, tuple(neighbor)))

        return None  # No path found

    def heuristic(self, position, goal):
        # Using Manhattan distance as heuristic
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def get_new_position(self, position, direction):
        if direction == 'UP':
            return [position[0], position[1] - 10]
        elif direction == 'DOWN':
            return [position[0], position[1] + 10]
        elif direction == 'LEFT':
            return [position[0] - 10, position[1]]
        elif direction == 'RIGHT':
            return [position[0] + 10, position[1]]

    def get_safe_moves(self):
        safe_moves = []
        for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            new_pos = self.get_new_position(self.snake_position, direction)
            if self.is_safe_move(new_pos):
                # Count future safe moves
                future_safe_moves = sum(
                    self.is_safe_move(self.get_new_position(new_pos, d)) for d in ['UP', 'DOWN', 'LEFT', 'RIGHT']
                )
                safe_moves.append((direction, future_safe_moves))

        if safe_moves:
            # Prioritize moves with more future safe spaces
            safe_moves.sort(key=lambda x: x[1], reverse=True)
            return [move[0] for move in safe_moves]  # Return sorted directions

        return []

    def get_direction_from_position(self, position):
        if position[0] > self.snake_position[0]:
            return 'RIGHT'
        elif position[0] < self.snake_position[0]:
            return 'LEFT'
        elif position[1] > self.snake_position[1]:
            return 'DOWN'
        elif position[1] < self.snake_position[1]:
            return 'UP'
        return 'RIGHT'  # Default direction
