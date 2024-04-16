from ..models.grid import Grid
from ..models.frontier import StackFrontier, QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node: Node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored: dict = {} 
        
        # Add the node to the explored dictionary
        explored[node.state] = True
        
        frontier: QueueFrontier  = QueueFrontier()
        frontier.add(node)
        
        if node.state == grid.end:
            return Solution(node, explored)
        
        while True:
            if frontier.is_empty(): return NoSolution(explored)
            temp_node: Node = frontier.remove()
            
            if temp_node.state in explored.keys() and temp_node.state != node.state: continue
            explored[temp_node.state] = True
            
            actions: dict[str, tuple[int, int]] = grid.get_neighbours(temp_node.state)
            
            for action in actions:
                solution: tuple[int, int] = actions[action]

                if solution not in explored.keys(): 
                    new_node: Node = Node(value="",
                                          state=solution,
                                          cost=temp_node.cost+grid.get_cost(solution),
                                          parent=temp_node,
                                          action=action)
                                 
                    if grid.end == new_node.state: return Solution(new_node, explored)
                    frontier.add(new_node)       
                    
                
        return NoSolution(explored)
