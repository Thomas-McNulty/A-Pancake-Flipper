from queue import PriorityQueue
from copy import copy
import random

#node class represents a potential representation of the
#pancake stack
class node():


    #nodes are initialized with a current stack, parent node, and goal stack
    def __init__(self, stack, parent, goal_stack):
        self.stack = stack
        self.parent = parent

        #int representation of the stack
        self.name = self.stack_to_int()
        self.goal = goal_stack

        #know if node is in the frontier
        self.frontier = True


        #initial state has no parent
        if self.parent == None:
            self.g = 0
        else:
            self.g = parent.g + self.cost_function()

        self.h = self.heuristic_function()
        self.f = self.g + self.h


    #heuristic function evaluates how close the stack is to the goal
    #by seeing how far by checking the distance between neighboring pancakes
    def heuristic_function(self):
        score = 0
        if self.stack == self.goal:
            return score
        for i in range(len(self.stack) - 1):
            if abs(self.stack[i] - self.stack[i + 1]) > 1:
                score += 1
        return score + 1


    #cost function evaluates how far from the initial state the current stack
    #is. It is the sum of the parents initial state and how many pancakes are
    #misplaced from the parent in the child.
    def cost_function(self):
        score = 0
        parent = self.parent.stack
        for i in range(len(self.stack)):
            if self.stack[i] != parent[i]:
                score+=1
        return score



    #stack_to_int converts a stack list into an integer representation simply
    #by concatenating the numbers
    def stack_to_int(self):
        name = [str(i) for i in self.stack]
        return int("".join(name)) 

#flip_stack flips the list values after an index, essentially flipping
#the stack. The index must be greater than or equal to 0
def flip_stack(stack, index):
    assert(index >= 0)
    stack = copy(stack)
    stack[index:] = stack[index:][::-1]
    return stack

#find_children finds all the possible children that can be made by flipping
#the stack
def find_children(stack):
    children = []
    for i in range(len(stack) - 1):
        child = flip_stack(stack, i)
        children.append(child)
    return children



#A star search for pancake stack solution. This function searches for
#a stack of pancakes which is in the ideal_stack order starting from
#the start_stack order. It does this by exploring potential nodes,
#and evaluating their forward/backward costs. 
def A_star_pancake(ideal_stack, start_stack):

    #Create a starting node using the initial state with no parents
    start = node(start_stack, None, ideal_stack)

    #initialize frontier with starting node
    frontier = PriorityQueue()
    frontier.put((0, start.name))

    #add starting node to visited nodes
    visited = {start.name: start}

    path = None

    while not frontier.empty():

        node_pair = frontier.get()
        curr_node = visited[node_pair[1]]

        if node_pair[0] > curr_node.f:
            pass

        #mark it as no longer in the frontier since it is being explored
        visited[curr_node.name].frontier = False

        #goal test
        if curr_node.stack == ideal_stack:

            #traverse to first parent and record stacks
            path = []
            while curr_node is not None:
                path.append(curr_node.stack)
                curr_node = curr_node.parent
            break


        children = find_children(curr_node.stack)

        for child in children:

            #create a potential node to be added to the frontier
            child_node = node(child, curr_node, ideal_stack)

            #Once a node is added to the frontier it is marked as visited,
            #so any node either in the frontier or visited is in visited
            if child_node.name not in visited:

                #places child into frontier at total cost priority
                frontier.put((child_node.f, child_node.name))
                visited[child_node.name] = child_node

            #place child in frontier if it is currently in the frontier and has a higher cost
            elif visited[child_node.name].frontier == True and visited[child_node.name].f > child_node.f:
                
                frontier.put((child_node.f, child_node.name))


    #prints path in reversed order since path was recorded from goal state
    if path == None:
        print("No path found")
    else:
        for i in reversed(path):
            print(i)

    
#main function takes the current stack and 
def main(start_stack, ideal_stack):

    if start_stack == "random":
        start_stack = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        cycles = int(input("How many stacks?: "))
        for i in range(cycles):
            random.shuffle(start_stack)
            start = ""
            for i in start_stack:
                start = start + " " + str(i)
            print("STARTING POINT IS: " + start)
            A_star_pancake(ideal_stack, start_stack)
    else:
        start_stack = start_stack.split(" ")
        start_stack = [int(i) for i in start_stack]
        assert(len(start_stack) == 10)

        A_star_pancake(ideal_stack, start_stack)


if __name__ == "__main__":
    start_stack = input("What is the current stack? (separated by spaces): ").rstrip()
    ideal_stack = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    main(start_stack, ideal_stack)