"""
This is the main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))   

'''
The main driver for our code. This will handle user input and updating the graphics.
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs  = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flage variable for when a move is made
    loadImages()# only do this once, before the while loop
    running = True
    sqSelected = () # no square is selected, keep track of the last click of the user (tuple: (row,col))
    playerClicks = [] # keep track of player clicks (two tuples: [(6,4), (4,4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col): #user clicked the same square twice
                    sqSelected = () # deselect
                    playerClicks = [] # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append for both 1 & 2 clicks
                if len(playerClicks) == 2: # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        moveMade = True 
                    # if we're adding an AI later, we will need to check if the move is valid before making it
                    gs.makeMove(move)
                    sqSelected = () # reset user clicks
                    playerClicks = []
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove() 
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
'''
Draw the squares on the board
'''
def drawGameState(screen, gs):
    drawBoard(screen) # add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board)


# top left square is always light
def drawBoard(screen):
    LIGHT_SQ = p.Color(242, 217, 177)   # #F2D9B1
    DARK_SQ  = p.Color(181, 139, 99)    # #B58B63
    colors = [LIGHT_SQ, DARK_SQ]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # logic for alternating colors (0,0) is light, (0,1) is dark, (1,0) is dark, (1,1) is light
            # use (r+c)%2 to determine color
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




# Draw the pieces on the board using the current GameState.board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))





if __name__ == "__main__":
    main()