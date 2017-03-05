The ai can be run using the command:

    ./testRun <sessionName>

in the /chess-jason_mao/ directory, where <sessionName> is the name of the session that is 
attempting to be joined or created. All possible moves for a designated piece are described in the format:
	   
    <start position> <end position> [<promotion>]

where <start position> and <end position> are locations on the chess board described by (<file>, <rank>) 
and promotion describes what piece a pawn will be promoted into, if applicable. <promotion> may have values:
    
    N = white knight
    n = black knight
    Q = white queen
    q = black queen
    B = white bishop
    b = black bishop
    R = white rook
    r = black rook
