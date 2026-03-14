from __future__ import absolute_import, division, print_function
from game import Game
import copy, random, math


MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (state[0], state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        if (len(self.children) == 0):
            return True


# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions: 
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node = None, depth = 0):
        if (depth == 0):
            return

        # Checking if we at MAX_PLAYER
        if (node.player_type == MAX_PLAYER):

            self.simulator.set_state(*node.state)            

            state_right_now = self.simulator.current_state()
            
            for direction in MOVES:
                
                validMove =  self.simulator.move(direction)
                
                if (state_right_now == self.simulator.current_state() and validMove):
                    print("What the hell bruh!")

                #Checking if you can do the move
                if (validMove):

                    #Resulting state due to moving in certain valid direction

                    amended_state = self.simulator.current_state()

                    #Create child Node and inserting it into children list
                    
                    child = Node(amended_state,CHANCE_PLAYER)
                    node.children.append((direction,child))
                    self.build_tree(child,depth-1)
                
                self.simulator.set_state(*state_right_now)
             
            
            
        

        elif (node.player_type == CHANCE_PLAYER):
             
             
             
             #Get unoccupied tiles

             self.simulator.set_state(*node.state)
             

             state_right_now = self.simulator.current_state()
             unoccupied_tiles = self.simulator.get_open_tiles()

             tile_matrix = state_right_now[0]
             score = state_right_now[1]

             

             #Iterate over unoccupied tiles
             for i,j in unoccupied_tiles:
                                               
                amended_tile = copy.deepcopy(tile_matrix)              
                amended_tile[i][j] = 2 

                
                             
                new_state = (amended_tile, score)                
                child = Node(new_state, MAX_PLAYER)                
                node.children.append((None,child))               
                self.build_tree(child, depth - 1)



    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        if (node.is_terminal() == True): #node[1].is_terminal
            return (None,node.state[1])


        elif(node.player_type == MAX_PLAYER):    #node[1].is_terminal
            
            
            max = 0
            max_direction = None

            for (direction,child) in node.children:    #node[1].children
               
                #n, value = self.expectimax((direction,child))
                n, value = self.expectimax(child)
                if (value > max):
                    max = value
                    max_direction = direction
            

            return (max_direction,max)

        elif(node.player_type == CHANCE_PLAYER):   #node[1]

            sum = 0
            
            for (direction,child) in node.children:   #node[1]
                
                _, value = self.expectimax(child)             
                sum += value
                            
            average = sum/len(node.children)     #node[1]
            return (None,average)

    

    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    def compute_decision_ec(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax_ec(self.root)
        return direction
        
    def heuristic_value(self, state):
        """
        Improved heuristic for 2048.
        Rewards:
        - actual score
        - empty cells
        - keeping large values in a corner
        - monotonic decreasing board from that corner
        - merge opportunities
        Penalizes:
        - rough / unsmooth neighboring tiles
        """
        tile_matrix, score = state
        n = len(tile_matrix)
    
        empty_cells = 0
        max_tile = 0
        smoothness = 0
        merge_potential = 0
    
        # Count empties and max tile
        for i in range(n):
            for j in range(n):
                val = tile_matrix[i][j]
                if val == 0:
                    empty_cells += 1
                if val > max_tile:
                    max_tile = val
    
        # Smoothness penalty + merge opportunities
        for i in range(n):
            for j in range(n):
                if tile_matrix[i][j] == 0:
                    continue
    
                curr = math.log(tile_matrix[i][j], 2)
    
                # Compare with right neighbor
                if j + 1 < n and tile_matrix[i][j + 1] != 0:
                    right = math.log(tile_matrix[i][j + 1], 2)
                    smoothness -= abs(curr - right)
                    if tile_matrix[i][j] == tile_matrix[i][j + 1]:
                        merge_potential += 1
    
                # Compare with down neighbor
                if i + 1 < n and tile_matrix[i + 1][j] != 0:
                    down = math.log(tile_matrix[i + 1][j], 2)
                    smoothness -= abs(curr - down)
                    if tile_matrix[i][j] == tile_matrix[i + 1][j]:
                        merge_potential += 1
    
        # Monotonicity score
        monotonicity = 0
    
        for i in range(n):
            for j in range(n - 1):
                a = math.log(tile_matrix[i][j], 2) if tile_matrix[i][j] != 0 else 0
                b = math.log(tile_matrix[i][j + 1], 2) if tile_matrix[i][j + 1] != 0 else 0
                monotonicity -= abs(a - b)
    
        for j in range(n):
            for i in range(n - 1):
                a = math.log(tile_matrix[i][j], 2) if tile_matrix[i][j] != 0 else 0
                b = math.log(tile_matrix[i + 1][j], 2) if tile_matrix[i + 1][j] != 0 else 0
                monotonicity -= abs(a - b)
    
        # Weighted board favoring large tiles in top-left corner
        weights = [
            [65536, 16384, 4096, 1024],
            [256,   1024,  256,   64],
            [16,      64,   16,    4],
            [1,        4,    1,    0]
        ]
    
        weighted_sum = 0
        for i in range(n):
            for j in range(n):
                weighted_sum += tile_matrix[i][j] * weights[i][j]
    
        # Bonus if max tile is in a corner
        corner_bonus = 0
        corners = [
            tile_matrix[0][0],
            tile_matrix[0][n - 1],
            tile_matrix[n - 1][0],
            tile_matrix[n - 1][n - 1]
        ]
        if max_tile in corners:
            corner_bonus = max_tile
    
        value = (
            1.0 * score
            + 300.0 * empty_cells
            + 2.0 * smoothness
            + 80.0 * merge_potential
            + 1.0 * monotonicity
            + 0.1 * weighted_sum
            + 10.0 * corner_bonus
        )
    
        return value


    def expectimax_ec(self, node=None):
        """
        Expectimax using heuristic leaf evaluation instead of raw score.
        """
        if node.is_terminal():
            return (None, self.heuristic_value(node.state))

        elif node.player_type == MAX_PLAYER:
            max_value = float("-inf")
            max_direction = None

            for (direction, child) in node.children:
                _, value = self.expectimax_ec(child)
                if value > max_value:
                    max_value = value
                    max_direction = direction

            return (max_direction, max_value)

        elif node.player_type == CHANCE_PLAYER:
            total = 0

            for (_, child) in node.children:
                _, value = self.expectimax_ec(child)
                total += value

            average = total / len(node.children)
            return (None, average)









