from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

def manhattan_distance(state: tuple[int, int],
                       goal: tuple[int, int]) -> int:
    """
    Calculate the Manhattan distance heuristic between the current state and a fixed goal state.
    """
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution | NoSolution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node: Node = Node("", grid.start, 0)

        frontier: PriorityQueueFrontier = PriorityQueueFrontier()
        
        frontier.add(node, node.cost+manhattan_distance(node.state, grid.end))
        
        # Initialize the explored dictionary to be empty
        explored: dict = {} 
        
        # Add the node to the explored dictionary
        explored[node.state] = node
        
        while True:
            if frontier.is_empty(): return NoSolution

            new_node: Node = frontier.pop()
            
            if grid.end == new_node.state: return Solution(new_node, explored)

            actions: dict[str, tuple[int, int]] = grid.get_neighbours(new_node.state)

            for action in actions:
                child: Node = Node(value="",
                                   state=actions[action],
                                   cost=new_node.cost+grid.get_cost(actions[action]),
                                   parent=new_node,
                                   action=action)
                if child.state not in explored.keys() or child.cost < explored[child.state].cost:
                    explored[child.state] = child
                    frontier.add(child, child.cost+manhattan_distance(child.state,  grid.end))
        
        return NoSolution(explored)
