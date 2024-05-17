from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        # Inicializa un nodo con la posición inicial
        node: Node = Node("", grid.start, 0)

        # Comprueba si el nodo inicial es el objetivo
        if node.state == grid.end:
            # Retorna una solución con el nodo inicial si es el objetivo
            return Solution(node, explored)
        
        # Inicializa el diccionario de nodos explorados como vacío
        explored: dict = {} 
        
        # Inicializa la frontera de búsqueda como una cola
        frontier: QueueFrontier = QueueFrontier()

        # Añade el nodo inicial a la frontera
        frontier.add(node)

        # Añade el nodo inicial al diccionario de nodos explorados
        explored[node.state] = True

        # Bucle principal del algoritmo BFS
        while True:
            # Si la frontera está vacía, no hay solución
            if frontier.is_empty(): 
                # Retorna un objeto NoSolution con el diccionario de nodos explorados
                return NoSolution(explored)
            
            # Obtiene el nodo de la frontera
            temp_node: Node = frontier.remove()
            
            # Obtiene las acciones posibles desde el nodo actual y las ordena para mantener un orden predecible
            actions: dict[str, tuple[int, int]] = grid.get_neighbours(temp_node.state)
            actions_as_list: list = list(actions)
            actions_as_list.sort(key=lambda x: x != "down")
            
            # Explora los nodos vecinos del nodo actual
            for action in actions_as_list:
                # Obtiene la solución para una acción específica
                solution: tuple[int, int] = actions[action]

                # Si la solución no ha sido explorada, crea un nuevo nodo hijo
                if solution not in explored.keys(): 
                    new_node: Node = Node(value="",
                                          state=solution,
                                          cost=temp_node.cost + grid.get_cost(solution),
                                          parent=temp_node,
                                          action=action)
                    
                    # Si el nodo hijo es el objetivo, retorna la solución
                    if grid.end == new_node.state:
                        return Solution(new_node, explored)
                    
                    # Marca el nodo hijo como explorado y lo añade a la frontera
                    explored[new_node.state] = True
                    frontier.add(new_node)   

        # Si no se encuentra solución, retorna un objeto NoSolution con el diccionario de nodos explorados
        return NoSolution(explored)
