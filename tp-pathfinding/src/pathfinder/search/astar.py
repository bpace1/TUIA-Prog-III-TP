from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

def manhattan_distance(state: tuple[int, int], goal: tuple[int, int]) -> int:
    # Calcula la distancia de Manhattan entre dos puntos en el grid
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution | NoSolution:
        # Inicializa un nodo con la posición inicial
        node: Node = Node("", grid.start, 0)

        # Inicializa la frontera de búsqueda con una cola de prioridad
        frontier: PriorityQueueFrontier = PriorityQueueFrontier()
        
        # Añade el nodo inicial a la frontera, con una prioridad basada en el costo y la heurística
        frontier.add(node, node.cost + manhattan_distance(node.state, grid.end))
        
        # Inicializa el diccionario de nodos explorados como vacío
        explored: dict = {} 
        
        # Añade el nodo inicial al diccionario de nodos explorados
        explored[node.state] = node
        
        # Bucle principal del algoritmo A*
        while True:
            # Si la frontera está vacía, no hay solución
            if frontier.is_empty(): 
                return NoSolution

            # Obtiene el nodo con la prioridad más alta de la frontera
            new_node: Node = frontier.pop()
            
            # Si el nodo actual es el objetivo, se ha encontrado la solución
            if grid.end == new_node.state: 
                return Solution(new_node, explored)

            # Obtiene las acciones posibles desde el nodo actual
            actions: dict[str, tuple[int, int]] = grid.get_neighbours(new_node.state)

            # Expande el nodo actual y añade sus hijos a la frontera
            for action in actions:
                # Crea un nuevo nodo hijo
                child: Node = Node(value="",
                                   state=actions[action],
                                   cost=new_node.cost + grid.get_cost(actions[action]),
                                   parent=new_node,
                                   action=action)
                # Si el hijo no ha sido explorado o tiene un costo menor, lo añade a la frontera
                if child.state not in explored.keys() or child.cost < explored[child.state].cost:
                    explored[child.state] = child
                    # Calcula la prioridad del hijo basada en el costo y la heurística y lo añade a la frontera
                    frontier.add(child, child.cost + manhattan_distance(child.state,  grid.end))
        
        # Si no se encuentra solución, retorna un objeto NoSolution con el diccionario de nodos explorados
        return NoSolution(explored)
