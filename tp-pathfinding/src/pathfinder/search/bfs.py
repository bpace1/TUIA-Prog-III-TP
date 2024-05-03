from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node: Node = Node("", grid.start, 0)

        #check test
        if node.state == grid.end:
            return Solution(node, explored)
        
        # Initialize the explored dictionary to be empty
        explored: dict = {} 
        
        # Initialize QueueFrontier
        frontier: QueueFrontier = QueueFrontier()

        #Add first node
        frontier.add(node)

        # Add the node to the explored dictionary
        explored[node.state] = True


        while True:
            if frontier.is_empty(): return NoSolution(explored)
            temp_node: Node = frontier.remove()
            #tamo bien
            #if temp_node.state in explored.keys() and temp_node.state != node.state: continue
            #explored[temp_node.state] = True
            
            actions: dict[str, tuple[int, int]] = grid.get_neighbours(temp_node.state)
            actions_as_list: list = list(actions)
            actions_as_list.sort(key=lambda x: x != "down")
            
            for action in actions_as_list:
                solution: tuple[int, int] = actions[action]

                if solution not in explored.keys(): 
                    new_node: Node = Node(value="",
                                          state=solution,
                                          cost=temp_node.cost+grid.get_cost(solution),
                                          parent=temp_node,
                                          action=action)
                                 
                    if grid.end == new_node.state: return Solution(new_node, explored)
                    explored[new_node.state] = True
                    frontier.add(new_node)   

        return NoSolution(explored)
