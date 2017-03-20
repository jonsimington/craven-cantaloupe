import state as s
import random as r
import time

r.seed(time.time())

#iterative deepening depth-limited minimax
#  at the moment, just runs each level of depth limited minimax without using
#  information from previous levels and returns the final levels results
def iddlm(state, depth, maxp):
    result = None
    for i in range(1, depth):
        result = dlm(state, i, maxp)

    return result
#end iddlm


#depth limited minimax
#  takes the initial state of game, depth limit, and max player
#  returns the best move for max (current) player to make
#  depth should be greater than 0, otherwise nothing will be explored
#  the current state will be returned, which doesn't correspond to
#  any valid move
#  maxp shoould be either 'b' or 'w'
def dlm(state, depth, maxp):
    if depth == 0:
        return state
    
    moves = state.getAllMoves()
    
    choices = []
    best = -99999999999
    #for each valid move, try to find the best one by using minimax
    for i, currentState in enumerate(moves):
        value = minv(currentState, depth-1, maxp)
        if value > best:
            best = value
            choices = [i]
        elif value == best:
            choices.append(i)
            
    #return a random move that has best value as determined by minimax
    return moves[choices[r.randint(0, len(choices)-1)]]
#end dlm


#min function for minimax
def minv(state, depth, maxp):
    if depth == 0:
        return s.heuristic(state, maxp)

    moves = state.getAllMoves()
    
    best = 99999999999
    for currentState in moves:
        value = maxv(currentState, depth-1, maxp)
        if value < best:
            best = value

    return best


#max function for minimax
def maxv(state, depth, maxp):
    if depth == 0:
        return s.heuristic(state, maxp)

    moves = state.getAllMoves()

    best = -9999999999
    for currentState in moves:
        value = minv(currentState, depth-1, maxp)
        if value > best:
            best = value

    return best


