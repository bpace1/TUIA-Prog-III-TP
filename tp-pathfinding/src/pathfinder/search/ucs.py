from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Encuentra un camino entre dos puntos en un grid utilizando búsqueda de costo uniforme.

        Args:
            grid (Grid): Grid de puntos
            
        Returns:
            Solution: Solución encontrada
        """
        # Inicializa un nodo con la posición inicial
        node: Node = Node("", grid.start, 0)

        # Inicializa el diccionario de nodos explorados como vacío
        explored: dict = {} 
        
        # Inicializa la frontera de búsqueda como una cola de prioridad
        frontier: PriorityQueueFrontier = PriorityQueueFrontier()

        # Añade el primer nodo a la frontera con un costo de cero
        frontier.add(node, node.cost)

        # Añade el nodo inicial al diccionario de nodos explorados con un costo de cero
        explored[node.state] = node.cost

        # Bucle principal del algoritmo de búsqueda de costo uniforme
        while True:
            # Si la frontera está vacía, no hay solución
            if frontier.is_empty(): 
                return NoSolution(explored)

            # Extrae un nodo de la frontera con el menor costo
            temp_node: Node = frontier.pop()

            # Obtiene las acciones posibles desde el nodo actual
            actions: dict[str, tuple[int, int]] = grid.get_neighbours(temp_node.state)

            # Si el nodo actual es el objetivo, se ha encontrado la solución
            if grid.end == temp_node.state: 
                return Solution(temp_node, explored)

            # Explora las acciones posibles desde el nodo actual
            for action in actions:
                solution: tuple[int, int] = actions[action]
                # Calcula el costo del nuevo nodo hijo
                cost_aux: int = temp_node.cost + grid.get_cost(solution)

                # Si la solución no ha sido explorada o tiene un costo menor, crea un nuevo nodo y lo añade a la frontera
                if solution not in explored.keys() or cost_aux < explored[solution]: 
                    new_node: Node = Node(value="",
                                          state=solution,
                                          cost=cost_aux,
                                          parent=temp_node,
                                          action=action)
                    # Añade el nuevo nodo a los nodos explorados y a la frontera
                    explored[solution] = new_node.cost
                    frontier.add(new_node, new_node.cost)   

        # Si no se encuentra solución, retorna un objeto NoSolution con el diccionario de nodos explorados
        return NoSolution(explored)
