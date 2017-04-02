# This is where you build your AI for the Chess game.

#file containing chess game state and other helper functions
import state as s
import tlabiddlm as mm

from joueur.base_ai import BaseAI
import random


class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    def get_name(self):
        """ This is the name you send to the server so your AI will control the
        player named this string.

        Returns
            str: The name of your Player.
        """

        return "Chess Python Player"  # REPLACE THIS WITH YOUR TEAM NAME

    def start(self):
        """ This is called once the game starts and your AI knows its playerID
        and game. You can initialize your AI here.
        """

        # replace with your start logic

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are
        tracking anything you can update it here.
        """

        # replace with your game updated logic

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and
        dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or
                          lost.
        """

        # replace with your end logic

    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your
                  turn, False means to keep your turn going and re-call this
                  function.
        """

        #self.print_current_board()
        #print(self.game.fen)
        
        if self.player.color == "White":
            playerColor = 'w'
        else:
            playerColor = 'b'

        #construct the history of the current game
        gameHistory = []
        for turn in self.game.moves:
            gameHistory.append(((turn.from_file, turn.from_rank), (turn.to_file, turn.to_rank)))

        #make a move determined by iddl-minimax
        initial = s.state(self.game.fen, history = gameHistory)
        move = mm.tlabiddlm(initial, 4, playerColor).history[-1]
        print("Moving piece located at", move[0], end="")
        for piece in self.player.pieces:
            if (piece.file, piece.rank) == move[0]:
                print("     ", self.player.color, piece.type)
                if len(move) == 2:
                    piece.move(move[1][0], move[1][1])
                else:
                    if move[2] == 'q' or move[2] == 'Q':
                        promote = "Queen"
                    if move[2] == 'r' or move[2] == 'R':
                        promote = "Rook"
                    if move[2] == 'b' or move[2] == 'B':
                        promote = "Bishop"
                    if move[2] == 'n' or move[2] == 'N':
                        promote = "Knight"
                    
                    piece.move(move[1][0], move[1][1], promote)
                break
        
        return True  # to signify we are done with our turn.

    def print_current_board(self):
        """Prints the current board using pretty ASCII art
        Note: you can delete this function if you wish
        """

        # iterate through the range in reverse order
        for r in range(9, -2, -1):
            output = ""
            if r == 9 or r == 0:
                # then the top or bottom of the board
                output = "   +------------------------+"
            elif r == -1:
                # then show the ranks
                output = "     a  b  c  d  e  f  g  h"
            else:  # board
                output = " " + str(r) + " |"
                # fill in all the files with pieces at the current rank
                for file_offset in range(0, 8):
                    # start at a, with with file offset increasing the char
                    f = chr(ord("a") + file_offset)
                    current_piece = None
                    for piece in self.game.pieces:
                        if piece.file == f and piece.rank == r:
                            # then we found the piece at (file, rank)
                            current_piece = piece
                            break

                    code = "."  # default "no piece"
                    if current_piece:
                        # the code will be the first character of their type
                        # e.g. 'Q' for "Queen"
                        code = current_piece.type[0]

                        if current_piece.type == "Knight":
                            # 'K' is for "King", we use 'N' for "Knights"
                            code = "N"

                        if current_piece.owner.id == "1":
                            # the second player (black) is lower case.
                            # Otherwise it's uppercase already
                            code = code.lower()

                    output += " " + code + " "

                output += "|"
            print(output)
