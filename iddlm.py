import state as s

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
    
    choice = None
    best = -99999999999
    for i, currentState in enumerate(moves):
        value = minv(currentState, depth-1, maxp)
        if value > best:
            best = value
            choice = i
            
    if choice != None:
        return moves[choice]
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


