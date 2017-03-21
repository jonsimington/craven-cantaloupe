#file containing the game state class for chess ai and some accompanying functions

#rank directions for each color of player
#these are used to modify the rank on the chess board, not to
#index the board in state. To modify index, multiply by -1
rankDir = {'b': -1,
           'w': 1 }

#piece names for each color of player
#used to easily determine if a piece is an ally or an enemy
pieceNames = { 'b': ['p', 'q', 'k', 'n', 'b', 'r'],
               'w': ['P', 'Q', 'K', 'N', 'B', 'R'] }

#diagonal and horizontal/vertical (straight) directional movements
#for bishops, rooks, queens, and kings
diagMods = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
straightMods = [ (-1, 0), (1, 0), (0, 1), (0, -1) ]

#checks the movement of the piece along diagonals
#  takes as agruments the position of the piece being moved
#  the enemy color of the piece 
#  the current chess board
#  optional argument limited specifies if the piece can move 
#  any number of spaces (False) or only one (True)
def diagMoves(piece, enemy, board, limited = False):
    x, y = convertXY(piece)
    moves = []
    for diag in diagMods:
        if limited:
            #explore one space
            destx, desty = (x+diag[0], y+diag[1])
            if inBounds(convertRF(destx, desty)):
                obj = board[desty][destx]
            else:
                obj = None
            if obj == "" or obj in pieceNames[enemy]:
                moves.append((piece, convertRF(destx, desty)))
        else:
            #explore direction until non-empty space is found
            destx, desty = (x+diag[0], y+diag[1])
            if inBounds(convertRF(destx, desty)):
                obj = board[desty][destx]
            else:
                obj = None
            while obj == "":
                moves.append((piece, convertRF(destx, desty)))
                destx = destx + diag[0]
                desty = desty + diag[1]
                if inBounds(convertRF(destx, desty)):
                    obj = board[desty][destx]
                else:
                    obj = None
            #check one further for an enemy piece to capture
            if obj in pieceNames[enemy]:
                moves.append((piece, convertRF(destx, desty)))
    
    return moves
#end diag mods
    
#checks the movement of the piece along straight paths
#  takes as agruments the position of the piece being moved
#  the enemy color of the piece 
#  the current chess board
#  optional argument limited specifies if the piece can move 
#  any number of spaces (False) or only one (True)
def straightMoves(piece, enemy, board, limited = False):
    x, y = convertXY(piece)
    moves = []
    for straight in straightMods:
        if limited:
            #explore one space
            destx, desty = (x+straight[0], y+straight[1])
            if inBounds(convertRF(destx, desty)):
                obj = board[desty][destx]
            else:
                obj = None
            if obj == "" or obj in pieceNames[enemy]:
              moves.append((piece, convertRF(destx, desty)))
        else:
            #explore direction until non-empty space is found
            destx, desty = (x+straight[0], y+straight[1])
            if inBounds(convertRF(destx, desty)):
                obj = board[desty][destx]
            else:
                obj = None
            while obj == "":
                moves.append((piece, convertRF(destx, desty)))
                destx = destx + straight[0]
                desty = desty + straight[1]
                if inBounds(convertRF(destx, desty)):
                    obj = board[desty][destx]
                else:
                    obj = None
    
            #check one further for an enemy piece to capture
            if obj in pieceNames[enemy]:
                moves.append((piece, convertRF(destx, desty)))
    return moves
#end straight moves

#changed file by an input amount. for example, fileMod("a", 3) gives "d" 
def fileMod(File, mod):
    return chr(ord(File)+mod)

#takes a tuple of (file, rank) and if the 
#location is in bounds, returns true
def inBounds(coords):
    if coords[1] <= 8 and coords[1] >= 1 and ord(coords[0]) <= ord('h') and ord(coords[0]) >= ord('a'):
        return True
    return False

#converts (x, y) index values for accessing the board to (file, rank)
#x corresponds to which column (file) while y corresponds to which row (rank)
def convertRF(x, y):
    return (chr(x+ord('a')), 8-y)

#converts (file, rank) into an x and y value for indexing board[y][x]
#the indexing is backwards on board[][] because of how I chose to print the board
def convertXY(coords):
    return (ord(coords[0])-ord('a'), 8-coords[1])








#chess game state
class state:
    #initialize a state based on a Forsyth Edwards notation string
    def __init__(self, fenString, inCheck=None, history = None):
        #board containing peices, capitals are white lower case if black.
        #p is pawn, r is rook, q is queen, k is king, b is bishop, n is knight
        self.board = [["" for i in range(0, 8)] for j in range(0, 8)]
    
        #flag for en passant, is False if none is allowed, contains the 
        #coordinates of the suqare behind the captureable pawn if allowed
        self.enPass = False;

        self.history = history
        if self.history == None:
            self.history = []

        #flags for castling
        #note that these flags don't tell if castling is allowed, but only
        #if the king and appropriate rook have made no moves
        self.castle = {"blackQueen" : False,
                       "blackKing": False,
                       "whiteQueen": False,
                       "whiteKing":False}

        #flag for active player, takes values {b, w}
        self.active = "w"

        #dictionary to hold the locations of pieces
        self.pawns = {'b':[], 'w':[]}
        self.knights = {'b':[], 'w':[]}
        self.bishops = {'b':[], 'w':[]}
        self.rooks = {'b':[], 'w':[]}
        self.queens = {'b':[], 'w':[]}
        self.kings = {'b':[], 'w':[]}

        #parse the fenString to create game state
        pieces, self.active, castleString, self.enPass, halfMove, fullMove = fenString.split(" ")
        
        #populate the pieces onto board
        for k, row in enumerate(pieces.split("/")):
            i=0
            for piece in row:
                #test if it is a number of empty spaces
                if piece.isdigit():
                    i += int(piece)
                else:
                    self.board[k][i] = piece
                    if piece == 'p':
                        self.pawns['b'].append(convertRF(i, k))
                    if piece == "P":
                        self.pawns['w'].append(convertRF(i, k))
                    if piece == "r":
                        self.rooks['b'].append(convertRF(i, k))
                    if piece == "R":
                        self.rooks['w'].append(convertRF(i, k))
                    if piece == "b":
                        self.bishops['b'].append(convertRF(i, k))
                    if piece == "B":
                        self.bishops['w'].append(convertRF(i, k))
                    if piece == "n":
                        self.knights['b'].append(convertRF(i, k))
                    if piece == "N":
                        self.knights['w'].append(convertRF(i, k))
                    if piece == "q":
                        self.queens['b'].append(convertRF(i, k))
                    if piece == "Q":
                        self.queens['w'].append(convertRF(i, k))
                    if piece == "k":
                        self.kings['b'].append(convertRF(i, k))
                    if piece == "K":
                        self.kings['w'].append(convertRF(i, k))

                    i += 1

        #set the flags for castling
        for castleFlag in castleString:
            if castleFlag == "K":
                self.castle["whiteKing"] = True
            if castleFlag == "k":
                self.castle["blackKing"] = True
            if castleFlag == "Q":
                self.castle["whiteQueen"] = True
            if castleFlag == "q":
                self.castle["blackQueen"] = True

        #set enPass flag
        if self.enPass == "-":
            self.enPass = False
        else:
            en, Pass = tuple(self.enPass)
            self.enPass = (en, int(Pass))

        
        #checks if active player is in check
        if inCheck == None:
            self.check = self.inCheck(self.active)
        else:
            self.check = inCheck
    #end state generation from FEN string

    #prints the board
    def printBoard(self):
        print("  a b c d e f g h")
        for i, row in enumerate(self.board):
            print(8-i, end="")
            for tile in row:
                print("|{:1}".format(tile), end="")
            print("|")
    #end board printing
    
    #retrieves what is on the board at the input (file, rank) in coords
    def getObj(self, coords):
        if not inBounds(coords):
            return "-1"
        return self.board[8-coords[1]][ord(coords[0])-ord('a')]
    #end obj retrieval


    #generates a new state by using the input move
    def genState(self, move):
        newState = self.stateCopy()
        
        obj = newState.getObj(move[0])
        
        #check if the moving piece is a pawn moving two spaces
        if obj == 'p' or obj == 'P':
            x, y = convertXY(move[1])
            y += rankDir[newState.active]
            newState.enPass = convertRF(x, y)
        else:
            newState.enPass = None

        #check if any castling flags were broken
        if obj == 'k':
            newState.castle["blackKing"] = False
            newState.castle["blackQueen"] = False
        if obj == 'K':
            newState.castle["whiteKing"] = False
            newState.castle["whiteQueen"] = False
        if move[0] == ('a', 8):
            newState.castle["blackQueen"] = False
        if move[0] == ('a', 1):
            newState.castle["whiteQueen"] = False
        if move[0] == ('h', 8):
            newState.castle["blackKing"] = False
        if move[0] == ('h', 1):
            newState.castle["blackKing"] = False

        #move the piece
        y0, x0 = convertXY(move[0])
        y1, x1 = convertXY(move[1])
        newState.board[x1][y1] = newState.board[x0][y0]
        newState.board[x0][y0] = ""
        #check for pawn promotion
        if len(move) == 3:
            newState.board[x1][y1] = move[2]
        #check for castling
        if obj == 'k' or obj == 'K':
            if abs(y0-y1) == 2:
                #white king side
                if move[1] == ('g', 1):
                    newState.board[7][5] = newState.board[7][7]
                    newState.board[7][7] = ""
                #white queen side
                if move[1] == ('c', 1):
                    newState.board[7][3] = newState.board[7][0]
                    newState.board[7][0] = ""
                #black king side
                if move[1] == ('g', 8):
                    newState.board[0][5] = newState.board[0][7]
                    newState.board[0][7] = ""
                #black queen side
                if move[1] == ('c', 8):
                    newState.board[0][3] = newState.board[0][0]
                    newState.board[0][0] = ""


        newState.pawns = {'b':[], 'w':[]}
        newState.knights = {'b':[], 'w':[]}
        newState.bishops = {'b':[], 'w':[]}
        newState.rooks = {'b':[], 'w':[]}
        newState.queens = {'b':[], 'w':[]}
        newState.kings = {'b':[], 'w':[]}
        
        #repopulate the dicts of pieces
        for k in range(0, 8):
            for i in range(0, 8):
                piece = newState.board[k][i]
                if piece == 'p':
                    newState.pawns['b'].append(convertRF(i, k))
                if piece == "P":
                    newState.pawns['w'].append(convertRF(i, k))
                if piece == "r":
                    newState.rooks['b'].append(convertRF(i, k))
                if piece == "R":
                    newState.rooks['w'].append(convertRF(i, k))
                if piece == "b":
                    newState.bishops['b'].append(convertRF(i, k))
                if piece == "B":
                    newState.bishops['w'].append(convertRF(i, k))
                if piece == "n":
                    newState.knights['b'].append(convertRF(i, k))
                if piece == "N":
                    newState.knights['w'].append(convertRF(i, k))
                if piece == "q":
                    newState.queens['b'].append(convertRF(i, k))
                if piece == "Q":
                    newState.queens['w'].append(convertRF(i, k))
                if piece == "k":
                    newState.kings['b'].append(convertRF(i, k))
                if piece == "K":
                    newState.kings['w'].append(convertRF(i, k))

        #set check flag. This is from the new active players perspective, 
        #is it tells if the move puts the player who just moved into check
        #(which isnt an allowed move)
        newState.check = newState.inCheck

        #pass the turn to other player and return the state
        if newState.active == 'b':
            newState.active = 'w'
        else:
            newState.active = 'b'
        return newState
    #end child state generation

    #generates all pawn moves for active player
    def pawnMoves(self):
        player = self.active
        if player == 'b':
            enemy = 'w'
        else:
            enemy = 'b'

        moves = []
        promotes = {'w':['Q', 'R', 'B', 'N'],
                    'b':['q', 'r', 'b', 'n']}


        #for every pawn owned by the active player
        target = 'p'
        if player == 'w':
            target = 'P'

        for location in self.pawns[player]:
            x, y = convertXY(location)
            #look if the tile immediately ahead is empty
            if self.getObj(convertRF(x, y-rankDir[player]))=="":
                #space is empty, add that move to the possible moves
                #but check for promotion
                if (y-rankDir[player]) == 0 or (y-rankDir[player]) == 7:
                    for promote in promotes[player]:
                        moves.append((location, convertRF(x, y-rankDir[player]), promote))
                else:
                    moves.append((location, convertRF(x, y-rankDir[player])))
            #check if the pawn is in the initial position and can move 2 spaces
            if (player=='w' and location[1]==2) or (player=='b' and location[1]==7):
                if self.getObj(convertRF(x, y-rankDir[player]))=="" and self.getObj(convertRF(x, y-(rankDir[player]*2)))=="":
                    moves.append((location, convertRF(x, y-(2*rankDir[player]))))
            #check for killing an enemy piece
            diags = [convertRF(x+i, y-rankDir[player]) for i in [-1, 1]]
            for diag in diags:
                if self.getObj(diag) in pieceNames[enemy] or diag == self.enPass:
                    #can take an enemy piece
                    #but check for promotion
                    if diag[1] == 1 or diag[1] == 8:
                        for promote in promotes[player]:
                            moves.append((location, diag, promote))
                    else:
                        moves.append((location, diag))
                    
        return moves
    #end pawn moves


    #gets the moves for the knight
    def knightMoves(self):
        player = self.active
        if player == 'b':
            enemy = 'w'
        else: 
            enemy = 'b'

        moves = []

        #list of ways the knight can move
        knightMods = [(2, 1), (2, -1), (1, 2), (1, -2), (-2, 1), (-1, 2), (-2, -1), (-1, -2)]

        #for every knight
        for knight in self.knights[player]:
            x, y = convertXY(knight)
            for mod in knightMods:
                #see what is at the destination
                dest = self.getObj(convertRF(x+mod[0], y+mod[1]))
                if dest == "" or dest in pieceNames[enemy]:
                    moves.append((knight, convertRF(x+mod[0], y+mod[1])))

        return moves
    #end knight moves

    
    #gets the bishops moves
    def bishopMoves(self):
        player = self.active
        if player == 'b':
            enemy = 'w'
        else: 
            enemy = 'b'

        moves = []

        for bishop in self.bishops[player]:
            moves.extend(diagMoves(bishop, enemy, self.board))

        return moves
    #end bishop moves

    #gets rook moves
    def rookMoves(self):
        player = self.active
        if player == 'b':
            enemy = 'w'
        else: 
            enemy = 'b'

        moves = []

        for rook in self.rooks[player]:
            moves.extend(straightMoves(rook, enemy, self.board))

        return moves

    #gets the queens moves:
    def queenMoves(self):
        player = self.active
        if player == 'b':
            enemy = 'w'
        else: 
            enemy = 'b'

        moves = []

        for queen in self.queens[player]:
            moves.extend(diagMoves(queen, enemy, self.board))
            moves.extend(straightMoves(queen, enemy, self.board))

        return moves
    #end queen moves

    #gets the king's moves
    def kingMoves(self):
        player = self.active
        if player == 'b':
            enemy = 'w'
        else: 
            enemy = 'b'
            
        moves = []
            
        king = self.kings[player][0]
        moves.extend(diagMoves(king, enemy, self.board, limited=True))
        moves.extend(straightMoves(king, enemy, self.board, limited=True))


        #checks for castling
        if player == 'w' and not self.check:
            if self.castle["whiteKing"]:
                test = True
                inter = [('f', 1), ('g', 1)]
                for move in inter:
                    interState = self.genState((king, move))
                    #check if the king moves throught check or an occupied space
                    if interState.inCheck(player) or self.getObj(move) !="":
                        test = False
                if test: 
                     moves.append((king, ('g',1)))
            if self.castle["whiteQueen"]:
                test = True
                inter = [('d', 1), ('c', 1)]
                for move in inter:
                    interState = self.genState((king, move))
                    #check if the king moves throught check or an occupied space
                    if interState.inCheck(player) or self.getObj(move) !="":
                        test = False
                if test and self.getObj(('b', 1))=="":
                     moves.append((king, ('c',1)))
        if player == 'b' and not self.check:
            if self.castle["blackKing"]:
                test = True
                inter = [('f', 8), ('g', 8)]
                for move in inter:
                    interState = self.genState((king, move))
                    #check if the king moves throught check or an ocucpied space
                    if interState.inCheck(player) or self.getObj(move) !="":
                        test = False
                if test:
                     moves.append((king, ('g',8)))
            if self.castle["blackQueen"]:
                test = True
                inter = [('d', 8), ('c', 8)]
                for move in inter:
                    interState = self.genState((king, move))
                    #check if the king moves throught check or an occupied space
                    if interState.inCheck(player) or self.getObj(move) !="":
                        test = False
                if test and self.getObj(('b', 8))=="":
                     moves.append((king, ('c', 8)))


        return moves
    #end king moves
    
    #checks if the current state results in a draw
    def drawCheck(self):
        #check if the opponent has no legal moves and is not in check
        if state.inCheck == False and len(state.getAllMoves()) == 0:
            return True

        #check if checkmate is impossible
        if len(self.queens['b']) == 0 and len(self.queens['w']) == 0 and \
           len(self.rooks['b']) == 0 and len(self.rooks['w']) == 0 and \
           len(self.pawns['b']) == 0 and len(self.pawns['w']) == 0:
            #king vs king
            if len(self.knights['b']) == 0 and len(self.knights['b']) == 0 and \
               len(self.bishops['b']) == 0 and len(self.bishops['w']) == 0:
                return True
            #king vs king and knight
            if len(self.bishops['b']) == 0 and len(self.bishops['w']) == 0:
                if (len(self.knights['b']) == 0 and len(self.knights['w']) == 1) or \
                   (len(self.knights['w']) == 0 and len(self.knights['b']) == 1):
                    return True
            #king vs king with any number of bishops that are all on the same color
            #  bishops may be any color, as long as they are on the same colored tile
            if len(self.knights['b'])==0 and len(self.knights['w'])==0:
                allBishops = []
                allBishops.extend(self.bishops['b'])
                allBishops.extend(self.bishops['w'])
                if len(allBishops) > 0:
                    x0, y0 = convertXY(allBishops[0])
                    color = (x0+y0)%2

                    bishopFlag = True
                    #two bishops on the same color if the sum of their x, y board coords
                    # are both even or both odd
                    for bishop in allBishops:
                        x, y = convertXY(bishop)
                        if color != ((x+y)%2):
                            bishopFlag = False
                            break
                    if bishopFlag:
                        return True

        #simple three turn repetition rule
        if len(self.history) >= 8:
            firstTurns = self.history[-8:-4]
            secondTurns = self.history[-4:]
            repeatFlag = True
            #check that each turn in the first four match those in the second four
            for i in range(0, 4):
                if firstTurns[i] != secondTurns[i] or len(firstTurns[i]) != 2:
                    repeatFlag = False
                    break
            if repeatFlag:
                return True

        return False
    #end draw check

    #checks if the passed player is in check
    def inCheck(self, enemy):
        if enemy == 'b':
            player = 'w'
        else: 
            player = 'b'
            
        diagPieces = {'b': ['q', 'b'],
                      'w': ['Q', 'B']}
        straightPieces = {'b': ['r', 'q'],
                          'w': ['R', 'Q']}

        #list of ways the knight can move
        knightMods = [(2, 1), (2, -1), (1, 2), (1, -2), (-2, 1), (-1, 2), (-2, -1), (-1, -2)]

        #starting at the enemy king
        for king in self.kings[enemy]:
            x, y = convertXY(king)
            #explore diagonals
            for diag in diagMods:
                #explore a direction until a non-empty space is found
                dest = (x+diag[0], y+diag[1])
                obj = self.getObj(convertRF(*dest))
                while obj=="":
                    dest = (dest[0]+diag[0], dest[1]+diag[1])
                    obj = self.getObj(convertRF(*dest))
                #after looking at all the blank spaces, look at the space immediately 
                #after to see if it is a piece that can attack the king
                if obj in diagPieces[player]:
                    #print(obj, " able to take king")
                    return True
            #explore straight directions
            for straight in straightMods:
                #explore a direction until a non-empty space is found
                dest = (x+straight[0], y+straight[1])
                obj = self.getObj(convertRF(*dest))
                while obj=="":
                    dest = (dest[0]+straight[0], dest[1]+straight[1])
                    obj = self.getObj(convertRF(*dest))
                #after looking at all the blank spaces, look at the space immediately 
                #after to see if it is an enemy
                if obj in straightPieces[player]:
                    #print(obj, "able to take player")
                    return True

            #check pawns that can attack the king
            for diag in [(x+i, y-rankDir[enemy]) for i in [-1, 1]]:
                playerPawn = 'p'
                if player == 'w':
                    playerPawn = 'P'
                if self.getObj(convertRF(*diag))==playerPawn:
                    #print("pawn able to take player")
                    return True
            #check if player king can attack enemy king
            bkingx, bkingy = convertXY(self.kings['b'][0])
            wkingx, wkingy = convertXY(self.kings['w'][0])
            if abs(bkingx-wkingx) <=1 and abs(bkingy-wkingy) <= 1:
                #print("kings too close")
                return True

            #check if a knight can take the king
            playerKnight = 'n'
            if player == 'w':
                playerKnight = 'N'
            for mod in knightMods:
                dest = (x+mod[0], y+mod[1])
                if self.getObj(convertRF(*dest)) == playerKnight:
                    #print(playerKnight, " able to take king at", convertRF(*dest))
                    return True

        return False
    #end inCheck

    #makes a deep copy of the current state
    def stateCopy(self):
        newState = state("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", inCheck = False)
        #copy board
        for x in range(0, 8):
            for y in range(0, 8):
                newState.board[x][y] = self.board[x][y]
        
        #copy castling flags
        for flag in ['blackKing', 'blackQueen', 'whiteKing', 'whiteQueen']:
            newState.castle[flag] = self.castle[flag]
        
        #copy enPass
        newState.enPass = self.enPass
        
        #copy pieces
        newState.pawns = {'b':[], 'w':[]}
        newState.knights = {'b':[], 'w':[]}
        newState.bishops = {'b':[], 'w':[]}
        newState.rooks = {'b':[], 'w':[]}
        newState.queens = {'b':[], 'w':[]}
        newState.kings = {'b':[], 'w':[]}
        for player in ['b', 'w']:
            newState.pawns[player].extend(self.pawns[player])
            newState.rooks[player].extend(self.rooks[player])
            newState.bishops[player].extend(self.bishops[player])
            newState.queens[player].extend(self.queens[player])
            newState.kings[player].extend(self.kings[player])
            newState.knights[player].extend(self.knights[player])
            
        #copy check flag
        newState.check = self.check
        
        #copy actived player
        newState.active = self.active

        #copy history
        newState.history = []
        newState.history.extend(self.history)
        
        return newState
    #end state copying

    #gets ALL legal moves for the game state and returns them
    def getAllMoves(self):
        moves = []
        validStates = []
        moves.extend(self.pawnMoves())
        moves.extend(self.bishopMoves())
        moves.extend(self.kingMoves())
        moves.extend(self.queenMoves())
        moves.extend(self.rookMoves())
        moves.extend(self.knightMoves())
        
        player = self.active

        for move in moves:
            #check if the moves places the current player in check
            newState = self.genState(move)
            if not newState.inCheck(player):
                #add the move to the state's history and add it to 
                #the valid children states
                newState.history.append(move)
                validStates.append(newState)

        return validStates
    #end getting allmoves



#heuristic function for minimax
#  takes a state to be evaluated and a max player
#  maxp should be either 'b' or 'w'
def heuristic(state, maxp):
    #if the current player has no moves to make and is in check (checkmate) 
    #  and the current player is NOT the max player, then the
    #  state is really good, so return a high value
    moves = state.getAllMoves()
    if len(moves) == 0 and maxp != state.active and state.inCheck(maxp): 
        return 9001
    elif len(moves) == 0 and maxp == state.active and state.inCheck(maxp):
        #conversely, if the active player is the max player, the state is really bad
        return -9001

    #each piece has a value which contributes to a player's score
    #  pawns:1
    #  knight:3
    #  bishop:3
    #  rook:5
    #  queens:9 
    blackVal = len(state.pawns['b']) + (3*len(state.knights['b'])) + (3*len(state.bishops['b']))
    blackVal += (5*len(state.rooks['b'])) + (9*len(state.queens['b']))
                                                                    
    whiteVal = len(state.pawns['w']) + (3*len(state.knights['w'])) + (3*len(state.bishops['w']))
    whiteVal += (5*len(state.rooks['w'])) + (9*len(state.queens['w']))

    #the value of the heuristic is the difference between the blackVal and whiteVal
    heuristicVal = blackVal - whiteVal
    
    #if maxp is black, return heuristic val calculated above
    if maxp == 'b':
        return heuristicVal
    else:
        #if maxp is white, return -1*the heuristicVal
        return -1*heuristicVal
    

