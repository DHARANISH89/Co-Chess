"""
This classmis respomsible for storing all the info
"""
class GameState():
    def __init__(self):
        # board is an 8x8 2d list, each element of the list has 2 characters.
        # The first character represents the color of the piece, 'b' or 'w'.
        # The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N', or 'p'.
        # "--" represents an empty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []

    '''
    Takes a move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
    idk what are these things right now!!! 
    ''' 
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--" # empty the start square
        self.board[move.endRow][move.endCol] = move.pieceMoved # move the piece to the end square
        self.moveLog.append(move) # log the move and undo the later
        self.whiteToMove = not self.whiteToMove # swap players

    
    '''
    Undo the last move 
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: # make sure that there is a move to undo  AND O(1)
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # to swap players back

    '''
    All move considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() # for now not to worry about checks

    '''
    All move without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # number of rows
            for c in range(len(self.board[r])): # number of columns in a given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawaMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
        return moves
                    
    '''
    get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawaMoves(self, r, c, moves):
        '''
        white pawns start on row 6 and black pawns start on row 1
        white pawns move up the board (decreasing row number) and black pawns move down the board (increasing row number)
        '''
        pass

    '''
    get all the pawn moves for the rook located at row, col and add these moves to the list
    '''
    def getRockMoves(self, r, c, moves):
        pass


    

# we can also have nested class
class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol # unique ID for the move
        print(self.moveID)


    '''
    Overriding the equals method
    '''
    def __eq__(self, other): # comparing the object to another object
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        #can also add make it feel real chess notation meaning adding more graphics
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol )


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]    