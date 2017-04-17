import state as s
import random as r
import time
import sys

r.seed(time.time())

#a small buffer when comparing to time limit to allow the heuristic function to run
timeBuffer = 0.001

#history-table, quicent, time limited, alpha-beta pruning,
# iterative deepening depth-limited minimax
def htqtlabiddlm(state, depth, maxp):
    #allow 15 seconds per turn
    #once 15 seconds has expired, no further depths will be searched
    #turns will take longer than 15 seconds, since the current depth needs to
    #finish.
    timeLimit = 12

    prevTime = 0
    
    result = None

    historyTable = {}

    for i in range(1, depth):
        #if time limit reached, or if the current depth itteration would have
        #less time than the previous itteration
        if timeLimit <= 0 or timeLimit <= prevTime:
            break

        startTime = time.time()
        result = minimax(state, i, 2, maxp, -1*sys.maxsize, sys.maxsize, timeLimit, historyTable)
        endTime = time.time()
        timeLimit = timeLimit - (endTime - startTime)
        prevTime = endTime - startTime

    print("\tMinimax took {0}s longer than time limit".format(timeLimit*-1))
    return result
#end iddlm


#history table, quiecent, time limited, alpha-beta pruning, depth limited minimax
#  takes the initial state of game, depth limit, and max player
#  returns the best move for max (current) player to make
#  depth should be greater than 0, otherwise nothing will be explored
#  the current state will be returned, which doesn't correspond to
#  any valid move
#  quiecentDepth is the allowed quiecent search depth
#  maxp shoould be either 'b' or 'w'
#  alpha and beta are the alpha and beta values for alpha-beta pruning
def minimax(state, depth, quiecentDepth, maxp, alpha, beta, timeLimit, historyTable):
    if depth == 0:
        return state
        
    a = alpha
    b = beta
    startTime = time.time()
    
    moves = state.getAllMoves()
    moves.sort(key = lambda a: compare(a, historyTable), reverse = True)
    
    heurVal = s.heuristic(state, maxp)

    #for each child move, alot time equal to the remaining time
    #divided by the number of children
    timeAlot = timeLimit - (startTime - time.time())
    timeAlot = timeAlot / len(moves)

    choices = []
    best = -99999999999
    #for each valid move, try to find the best one by using minimax
    for i, currentState in enumerate(moves):
        quiecentFlag = True
        value = minv(currentState, depth-1, quiecentDepth, maxp, a, b, timeAlot, heurVal, historyTable)
        if value > best:
            best = value
            choices = [i]
        elif value == best:
            choices.append(i)
        #check if alpha value updated
        if value > a: a = value
            
    #return a random move that has best value as determined by minimax
    #also update history table
    finalMove = r.randint(0, len(choices)-1)
    moveID = moves[choices[finalMove]].getID()
    tableVal = compare(moveID, historyTable)
    historyTable[moveID] = tableVal+1
    return moves[choices[finalMove]]
#end dlm


#min function for minimax
#  quiecentDepth is quiecent search depth
#  preVal is the heuristic value of the parent of the current state,
#    used to test  for quiecence
def minv(state, depth, quiecentDepth, maxp, alpha, beta, timeLimit, preVal, historyTable):

    a = alpha
    b = beta
    d = depth
    q = quiecentDepth
    startTime = time.time()

    #test for draw
    if state.drawCheck():
        #a draw should only be an objective if the game
        #appears to far lost to be winnable. hence the -4 value
        return -4

    heurVal = s.heuristic(state, maxp)

    #if the depth limit is reached, check for quiecence
    if d <= 0:
        if abs(heurVal - preVal)>0 and q >0:
            #non-quiecent state with quiecent depth > 0, then continue search
            q = q-1
            d = d+1
        else:
            return heurVal

    moves = state.getAllMoves()
    moves.sort(key = lambda a: compare(a, historyTable), reverse = True)

    #if the opponent has no moves, and is in check, then checkmate has been reached
    if len(moves) == 0: return -9999999999
    
    #for each child move, alot time equal to the remaining time
    #divided by the number of children
    timeAlot = timeLimit + (startTime - time.time())
    timeAlot = timeAlot / len(moves)

    #if the time alotment for remaining moves is too small, stop the search
    if timeAlot <= timeBuffer:
        return heurVal

    best = 99999999999
    for i, currentState in enumerate(moves):
        value = maxv(currentState, d-1, q, maxp, a, b, timeAlot, heurVal, historyTable)
        if value < best:
            best = value
            bestID = currentState.getID()

        #check for fail low
        if value < a:
            #if fail low, return the current best
            return best

        #check if beta value updated
        if value < b: b = value

        #recalculate time alotment
        timeAlot = timeLimit + (startTime - time.time())
        timeAlot = timeAlot / (len(moves)-i)

        #if the time alotment for remaining moves is too small, stop the search
        if timeAlot <= timeBuffer:
            break

    #return best move, update history table
    tableVal = compare(bestID, historyTable)
    historyTable[bestID] = tableVal + 1
    return best


#max function for minimax
def maxv(state, depth, quiecentDepth, maxp, alpha, beta, timeLimit, preVal, historyTable):

    a = alpha
    b = beta
    d = depth
    q = quiecentDepth
    startTime = time.time()

    #test for draw
    if state.drawCheck():
        #a draw should only be an objective if the game
        #appears to far lost to be winnable. hence the -4 value
        return -4

    heurVal = s.heuristic(state, maxp)

    #if depth limit reached, check for quiecence
    if d <= 0:
        if abs(heurVal - preVal)>0 and q>0:
            #non-quiecent state with quiecent depth > 0, then continue search
            q = q-1
            d = d+1
        else:
            return heurVal


    moves = state.getAllMoves()
    moves.sort(key = lambda a: compare(a, historyTable), reverse = True)
    
    #if the opponent has no moves, and is in check, then checkmate has been reached
    if len(moves) == 0: return 9999999999

    #for each child move, alot time equal to the remaining time
    #divided by the number of children
    timeAlot = timeLimit + (startTime - time.time())
    timeAlot = timeAlot / len(moves)

    best = -9999999999
    for i,currentState in enumerate(moves):
        value = minv(currentState, d-1, q, maxp, a, b, timeAlot, heurVal, historyTable)
        if value > best:
            best = value
            bestID = currentState.getID()

        #check fail high
        if value > b:
            return best

        #check for update to alpha value
        if value > a:
            a = value

        #recalculate time alotment
        timeAlot = timeLimit + (startTime - time.time())
        timeAlot = timeAlot / (len(moves)-i)

        #if the time alotment for remaining moves is too small, stop the search
        if timeAlot <= timeBuffer:
            break
        
    #return the best moves, update history table
    tableVal = compare(bestID, historyTable)
    historyTable[bestID] = tableVal + 1
    return best




#function which, given a key and a dict, returns the value of the map
# for the key if it exists and 0 otherwise. Used as key to sort history table
def compare(keyVal, dictionary):
    if keyVal in dictionary:
        return dictionary[keyVal]
    return 0
