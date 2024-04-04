from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


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
        node = Node("", grid.start, 0)

        frontier = PriorityQueueFrontier()
        frontier.add(node, 0)

        # Initialize the explored dictionary to be empty
        explored = {} 
        
        # Add the node to the explored dictionary
        explored[node.state] = 0
        
        while True:
             #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)
            
            node = frontier.pop()
            successors = grid.get_neighbours(node.state)

            if node.state == grid.end:
                return Solution(node, explored)
            
            for movimiento in successors:
                new_state = successors[movimiento]
                new_cost = node.cost + grid.get_cost(new_state)

                if (new_state not in explored) or (new_cost < explored[new_state]):
                    new_node = Node("", new_state, new_cost,
                                     parent=node, action=movimiento)
                    
                    explored[new_state] = new_cost #guardamos el costo porque necesitamos compararlo con el anterior
            
                    frontier.add(new_node, new_cost)

        return NoSolution(explored)
