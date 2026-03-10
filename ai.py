from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

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
        return random.randint(0, 3)

