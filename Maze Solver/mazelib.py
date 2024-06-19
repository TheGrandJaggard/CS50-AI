from colorama import init, Fore
init()

# height, width
# row, column
# y, x
# [0], [1]

'''<-Settings->'''

# name = (data, skinny, wide)
passage = (0, " ", "  ")
wall = (1, "█", "██")
start = (2, "@", "<>")
end = (3, "$", "$$")

wide_display = True
random_start_and_end = False
show_path = True
show_explored = True
show_node_stats = True

class MazeObject:
    def __init__(self, maze_array:list[list[int]]):
        self.node_array = maze_array
        self.update_changes()

    @classmethod
    def from_file(cls, file_path:str):
        with open(file_path, "r") as file:
            maze_txt = file.read().splitlines()

        maze:list[list[int]] = []
        for y in range(len(maze_txt)): 
            line:list[int] = []
            for x in range(len(maze_txt[y])):
                line.append(int(maze_txt[y][x]))
            maze.append(line)
        return cls(maze)

    def update_changes(self):
        for row in range(self.get_size()[0]):
            for col in range(self.get_size()[1]):
                if self.node_array[row][col] == start[0]:
                    self.start_node = (row, col)
                if self.node_array[row][col] == end[0]:
                    self.end_node = (row, col)
    # getters
    def get_value_at_coords(self, coords:tuple[int, int]) -> int:
        return self.node_array[coords[0]][coords[1]] # y, x
    
    def get_size(self) -> tuple[int, int]:
        height = len(self.node_array) # height, aka y, aka number of rows
        width = len(self.node_array[0]) # width, aka x, aka number of columns
        return (height, width) # height, width

    def render_maze_pretty(self, overrides:list[tuple[tuple[int, int], str, str]]) -> str:
        # Prints the maze with colors (or not) in an organized and easy to read way.
        array:list[list[str]] = []
        for row in range(0, len(self.node_array)): # for as many lines as there are in the maze
            line:list[str] = []
            for col in range(0, len(self.node_array[0])): # for as many characters as there are in the line
                if self.get_value_at_coords((row, col)) == start[0]:
                    line.append(Fore.MAGENTA + start[1 + wide_display])
                elif self.get_value_at_coords((row, col)) == end[0]:
                    line.append(Fore.MAGENTA + end[1 + wide_display])
                elif self.get_value_at_coords((row, col)) == wall[0]:
                    line.append(Fore.LIGHTBLACK_EX + wall[1 + wide_display])
                elif self.get_value_at_coords((row, col)) == passage[0]:
                    line.append(passage[1 + wide_display])
                else:
                    print("Unexpected value at: row =", row, ", col =", col)
            array.append(line)
        
        for override in overrides:
            if override[0] == self.start_node or override[0] == self.end_node: continue

            display = override[1].rjust(1 + wide_display, " ")[:1 + wide_display]
            array[override[0][0]][override[0][1]] = override[2] + display
        
        result:str = ""
        for line in array:
            result += "\n"
            for char in line:
                result += char
        return result + Fore.RESET

    def render_maze_for_file(self) -> str:
        maze_lines:list[str] = []
        for y in range(len(self.node_array)): 
            line:list[str] = []
            for x in range(len(self.node_array[y])):
                line.append(str(self.node_array[y][x]))
            maze_lines.append("".join(line))
        return "\n".join(maze_lines)

class Node:
    def __init__(self, coordinates:tuple[int, int]) -> None:
        self.coordinates = coordinates
        self.path_cost = 0 # default no path cost
        self.value = 100000 # default infinate value
    
    def find_lineage(self):
        return []

class ChildNode(Node):
    def __init__(self, coordinates:tuple[int, int], parent:Node) -> None:
        self.coordinates = coordinates
        self.parent = parent
        self.path_cost = parent.path_cost + 1

    def find_lineage(self) -> list[Node]:
        result = self.parent.find_lineage()
        result.append(self)
        return result

class SearchAlgorithm:
    def __init__(self) -> None:
        self.nodes:list[Node] = []
    def get_length(self) -> int:
        return len(self.nodes)
    def add_node(self, node) -> None:
        self.nodes.append(node)
    def get_node(self) -> Node:
        raise TypeError("Do not use this class! Please use it's subclasses.")

class BFS(SearchAlgorithm): # Simple breadth first search
    def get_node(self) -> Node:
        return self.nodes.pop(0)

class DFS(SearchAlgorithm): # Simple depth first search
    def get_node(self) -> Node:
        return self.nodes.pop(-1)

class GBFS(SearchAlgorithm): # This is a huristic greedy best-first search
    def get_node(self) -> Node:
        best_node = Node((0, 0)) # creating a blank Node
        best_node.value = 1000000 # 1 million is close enough to infinity

        for node in self.nodes:
            if node.value < best_node.value:
                best_node = node
        
        self.nodes.remove(best_node)
        return best_node

class A_Star(SearchAlgorithm): # Takes into acount path cost
    def get_node(self) -> Node:
        best_node = self.nodes[0] # start with our first node
        for node in self.nodes:
            if (node.value + node.path_cost) < (best_node.value + best_node.path_cost):
                best_node = node
        
        self.nodes.remove(best_node)
        return best_node