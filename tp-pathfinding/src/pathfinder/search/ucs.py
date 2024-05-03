from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node
from ..models.frontier import PriorityQueueFrontier

class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node: Node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored: dict = {} 
        
        # Initialize PriorityQueueFrontier
        frontier: PriorityQueueFrontier = PriorityQueueFrontier()

        #Add first node        
        frontier.add(node, node.cost)

        # Add the node to the explored dictionary
        explored[node.state] = node.cost


        while True:
            if frontier.is_empty(): return NoSolution(explored)
            temp_node: Node = frontier.pop()
            #if temp_node.state in explored.keys() and temp_node.state != node.state: continue
            #explored[temp_node.state] = True

            actions: dict[str, tuple[int, int]] = grid.get_neighbours(temp_node.state)
            if grid.end == temp_node.state: return Solution(temp_node, explored)

            for action in actions:
                solution: tuple[int, int] = actions[action]
                cost_aux: int = temp_node.cost+grid.get_cost(solution)

                if solution not in explored.keys() or cost_aux < explored[solution]: 
                    new_node: Node = Node(value="",
                                          state=solution,
                                          cost=cost_aux,
                                          parent=temp_node,
                                          action=action)
                    explored[solution] = new_node.cost
                    frontier.add(new_node, new_node.cost)   

                        
        return NoSolution(explored)
