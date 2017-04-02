import state as s
import random as r
import time
import sys

r.seed(time.time())

#a small buffer when comparing to time limit to allow the heuristic function to run
timeBuffer = 0.015

#time limited, alpha-beta pruning, iterative deepening depth-limited minimax
#  at the moment, just runs each level of depth limited minimax without using
#  information from previous levels and returns the final levels results
def tlabiddlm(state, depth, maxp):
    #allow 15 seconds per turn
    #once 15 seconds has expired, no further depths will be searched
    #turns will take longer than 15 seconds, since the current depth needs to
    #finish.
    timeLimit = 15

    prevTime = 0
    
    result = None
    for i in range(1, depth):
        #if time limit reached, or if the current depth itteration would have
        #less time than the previous itteration
        if timeLimit <= 0 or timeLimit <= prevTime:
            break

        startTime = time.time()
        result = tlabdlm(state, i, maxp, -1*sys.maxsize, sys.maxsize, timeLimit)
        endTime = time.time()
        timeLimit = timeLimit - (endTime - startTime)
        prevTime = endTime - startTime

    print("\tMinimax took {0}s longer than time limit".format(timeLimit*-1))
    return result
#end iddlm


#time limited, alpha-beta pruning, depth limited minimax
#  takes the initial state of game, depth limit, and max player
#  returns the best move for max (current) player to make
#  depth should be greater than 0, otherwise nothing will be explored
#  the current state will be returned, which doesn't correspond to
#  any valid move
#  maxp shoould be either 'b' or 'w'
#  alpha and beta are the alpha and beta values for alpha-beta pruning
def tlabdlm(state, depth, maxp, alpha, beta, timeLimit):
    if depth == 0:
        return state
        
    a = alpha
    b = beta
    startTime = time.time()
    
    moves = state.getAllMoves()
    
    #for each child move, alot time equal to the remaining time
    #divided by the number of children
    timeAlot = timeLimit - (startTime - time.time())
    timeAlot = timeAlot / len(moves)

    choices = []
    best = -99999999999
    #for each valid move, try to find the best one by using minimax
    for i, currentState in enumerate(moves):
        value = minv(currentState, depth-1, maxp, a, b, timeAlot)
        if value > best:
            best = value
            choices = [i]
        elif value == best:
            choices.append(i)
        #check if alpha value updated
        if value > a: a = value
            
    #return a random move that has best value as determined by minimax
    return moves[choices[r.randint(0, len(choices)-1)]]
#end dlm


#min function for minimax
def minv(state, depth, maxp, alpha, beta, timeLimit):

    a = alpha
    b = beta
    startTime = time.time()

    #test for draw
    if state.drawCheck():
        #a draw should only be an objective if the game
        #appears to far lost to be winnable. hence the -4 value
        return -4

    #if time limit or depth limit reached, eval heuristic on the state
    #timeLimit not compared to zero to allow some time for heuristic() to run
    if depth == 0 or timeLimit <= timeBuffer:
        return s.heuristic(state, maxp)

    moves = state.getAllMoves()
    
    #for each child move, alot time equal to the remaining time
    #divided by the number of children
    timeAlot = timeLimit - (startTime - time.time())
    timeAlot = timeAlot / len(moves)

    best = 99999999999
    for currentState in moves:
        value = maxv(currentState, depth-1, maxp, a, b, timeAlot)
        if value < best:
            best = value

        #check for fail low
        if value < a:
            #if fail low, return the current best
            return best

        #check if beta value updated
        if value < b: b = value

    return best


#max function for minimax
def maxv(state, depth, maxp, alpha, beta, timeLimit):

    a = alpha
    b = beta
    startTime = time.time()

    #test for draw
    if state.drawCheck():
        #a draw should only be an objective if the game
        #appears to far lost to be winnable. hence the -4 value
        return -4

    #if time or depth limit reached, return heuristic value
    if depth == 0 or timeLimit <= timeBuffer:
        return s.heuristic(state, maxp)

    moves = state.getAllMoves()

    #for each child move, alot time equal to the remaining time
    #divided by the number of children
    timeAlot = timeLimit - (startTime - time.time())
    timeAlot = timeAlot / len(moves)

    best = -9999999999
    for currentState in moves:
        value = minv(currentState, depth-1, maxp, a, b, timeAlot)
        if value > best:
            best = value

        #check fail high
        if value > b:
            return best

        #check for update to alpha value
        if value > a:
            a = value
        
    return best


