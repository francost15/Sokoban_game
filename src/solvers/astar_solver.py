import heapq

class AStarSolver:
    def __init__(self, map_layout, start):
        self.map_layout = map_layout
        self.start = start
        self.goals = self.find_goals()
        self.boxes = self.find_boxes()

    def find_goals(self):
        """Encuentra todas las posiciones de los objetivos (casillas con '.')"""
        goals = []
        for y, row in enumerate(self.map_layout):
            for x, tile in enumerate(row):
                if tile == '.':
                    goals.append((x, y))
        return goals

    def find_boxes(self):
        """Encuentra todas las posiciones de las cajas ('$')"""
        boxes = []
        for y, row in enumerate(self.map_layout):
            for x, tile in enumerate(row):
                if tile == '$':
                    boxes.append((x, y))
        return boxes

    def heuristic(self, boxes):
        """Heurística: suma de las distancias de cada caja a la meta más cercana"""
        total_distance = 0
        for box in boxes:
            min_distance = min(abs(box[0] - goal[0]) + abs(box[1] - goal[1]) for goal in self.goals)
            total_distance += min_distance
        return total_distance

    def is_deadlock(self, boxes):
        """Verifica si el estado actual es un deadlock"""
        for box in boxes:
            if box not in self.goals:
                # Verificar si la caja está en una esquina o contra una pared sin posibilidad de moverse
                x, y = box
                if (self.map_layout[y][x - 1] == '#' or self.map_layout[y][x + 1] == '#') and \
                   (self.map_layout[y - 1][x] == '#' or self.map_layout[y + 1][x] == '#'):
                    return True
                # Verificar si la caja está atrapada entre dos cajas
                if ((x > 0 and self.map_layout[y][x - 1] == '$') or (x < len(self.map_layout[0]) - 1 and self.map_layout[y][x + 1] == '$')) and \
                   ((y > 0 and self.map_layout[y - 1][x] == '$') or (y < len(self.map_layout) - 1 and self.map_layout[y + 1][x] == '$')):
                    return True
        return False

    def solve(self):
        """Resuelve el problema usando el algoritmo A* optimizado"""
        if not self.goals or not self.boxes:
            return None

        open_set = []
        start_state = (self.start, tuple(sorted(self.boxes)))
        heapq.heappush(open_set, (0 + self.heuristic(self.boxes), start_state))
        came_from = {}
        g_score = {start_state: 0}
        closed_set = set()

        while open_set:
            _, (current_pos, current_boxes) = heapq.heappop(open_set)

            if (current_pos, current_boxes) in closed_set:
                continue
            closed_set.add((current_pos, current_boxes))

            # Si todas las cajas están en los objetivos, reconstruimos el camino
            if all(box in self.goals for box in current_boxes):
                return self.reconstruct_path(came_from, (current_pos, current_boxes))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor_pos = (current_pos[0] + dx, current_pos[1] + dy)
                new_boxes = list(current_boxes)

                # Verificar límites del mapa
                if not (0 <= neighbor_pos[0] < len(self.map_layout[0]) and 0 <= neighbor_pos[1] < len(self.map_layout)):
                    continue
                if self.map_layout[neighbor_pos[1]][neighbor_pos[0]] == '#':
                    continue  # Es una pared

                if neighbor_pos in current_boxes:
                    # Intentamos empujar la caja
                    box_move = (neighbor_pos[0] + dx, neighbor_pos[1] + dy)

                    # Verificar límites del mapa para la posición de la caja
                    if not (0 <= box_move[0] < len(self.map_layout[0]) and 0 <= box_move[1] < len(self.map_layout)):
                        continue
                    if self.map_layout[box_move[1]][box_move[0]] == '#' or box_move in current_boxes:
                        continue  # No se puede mover la caja

                    # Mover la caja
                    new_boxes.remove(neighbor_pos)
                    new_boxes.append(box_move)

                neighbor_state = (neighbor_pos, tuple(sorted(new_boxes)))
                tentative_g_score = g_score[(current_pos, current_boxes)] + 1

                if neighbor_state in closed_set or self.is_deadlock(new_boxes):
                    continue

                if neighbor_state not in g_score or tentative_g_score < g_score[neighbor_state]:
                    came_from[neighbor_state] = (current_pos, current_boxes)
                    g_score[neighbor_state] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(new_boxes)
                    heapq.heappush(open_set, (f_score, neighbor_state))

        return None

    def reconstruct_path(self, came_from, current):
        """Reconstruye el camino desde el objetivo hasta el inicio"""
        path = []
        while current in came_from:
            prev = came_from[current]
            dx = current[0][0] - prev[0][0]
            dy = current[0][1] - prev[0][1]
            path.append((dx, dy))
            current = prev
        path.reverse()
        return path