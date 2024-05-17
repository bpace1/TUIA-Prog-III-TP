from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution | NoSolution:
        """
        Encuentra un camino entre dos puntos en un grid utilizando búsqueda en profundidad.

        Args:
            grid (Grid): Grid de puntos
            
        Returns:
            Solution: Solución encontrada
        """
        # Inicializa un nodo con la posición inicial
        node: Node = Node("", grid.start, 0)

        # Inicializa el diccionario de nodos explorados como vacío
        explored: dict = {} 
        
        # Añade el nodo inicial al diccionario de nodos explorados
        explored[node.state] = True
        
        # Inicializa la frontera de búsqueda como una pila
        frontier: StackFrontier  = StackFrontier()
        frontier.add(node)
        
        # Verifica si el nodo inicial es el objetivo
        if node.state == grid.end:
            return Solution(node, explored)
        
        # Bucle principal del algoritmo de búsqueda en profundidad
        while True:
            # Si la frontera está vacía, no hay solución
            if frontier.is_empty(): 
                return NoSolution(explored)
            
            # Extrae un nodo de la frontera
            temp_node: Node = frontier.remove()
            
            # Si el nodo actual ya ha sido explorado, pasa al siguiente nodo
            if temp_node.state in explored.keys() and temp_node.state != node.state:
                continue
            
            # Marca el nodo actual como explorado
            explored[temp_node.state] = True
            
            # Obtiene las acciones posibles desde el nodo actual
            actions: dict[str, tuple[int, int]] = grid.get_neighbours(temp_node.state)
            
            # Ordena las acciones para que se explore en un orden específico
            actions_as_list: list = list(actions)
            actions_as_list.sort(key=lambda x: x != "down")
            
            # Explora las acciones posibles desde el nodo actual
            for action in actions_as_list:
                solution: tuple[int, int] = actions[action]

                # Si la solución no ha sido explorada, crea un nuevo nodo y lo añade a la frontera
                if solution not in explored.keys(): 
                    new_node: Node = Node(value="",
                                          state=solution,
                                          cost=temp_node.cost + grid.get_cost(solution),
                                          parent=temp_node,
                                          action=action)
                                 
                    # Si se encuentra la solución, retorna la solución encontrada
                    if grid.end == new_node.state: 
                        return Solution(new_node, explored)
                    
                    # Añade el nuevo nodo a la frontera
                    frontier.add(new_node)       

        # Si no se encuentra solución, retorna un objeto NoSolution con el diccionario de nodos explorados
        return NoSolution(explored)
