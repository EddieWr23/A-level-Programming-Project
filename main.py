from pieces import *
import pygame as p
import GUI

#CHESS VARIABLES
p.init()
WIDTH, HEIGHT = 512, 512       #default is 512, 512
DIMENSION = 8 #chess boards are 8x8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15 #for animations later on
board = [Rook((7,0),"White"),Knight((7,1),"White"),Bishop((7,2),"White"),Queen((7,3),"White"),King((7,4),"White"),Bishop((7,5),"White"),Knight((7,6),"White"),Rook((7,7),"White"),
        Pawn((6,0),"White"),Pawn((6,1),"White"),Pawn((6,2),"White"),Pawn((6,3),"White"),Pawn((6,4),"White"),Pawn((6,5),"White"),Pawn((6,6),"White"),Pawn((6,7),"White"),
        Rook((0,0),"Black"),Knight((0,1),"Black"),Bishop((0,2),"Black"),Queen((0,3),"Black"),King((0,4),"Black"),Bishop((0,5),"Black"),Knight((0,6),"Black"),Rook((0,7),"Black"),
        Pawn((1,0),"Black"),Pawn((1,1),"Black"),Pawn((1,2),"Black"),Pawn((1,3),"Black"),Pawn((1,4),"Black"),Pawn((1,5),"Black"),Pawn((1,6),"Black"),Pawn((1,7),"Black")]

redCircle = p.transform.scale(p.image.load("images/red.png"), (64,64))
yellowCircle = p.transform.scale(p.image.load("images/yellow.png"), (64,64))

'''
Functions for ranks and files
'''
def rank(num):
    return 8 - num

def file(num):
    files = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}
    return files[num]

def RF(position):
    return(str(file(position[1])) + str(rank(position[0])))

'''
The main chess program
'''
def chess():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Eddie's Chess Program")
    Icon = p.image.load(r"images/bK.png")
    p.display.set_icon(Icon)
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    running = True
    WhiteToMove = True
    sqSelected = ()
    playerClicks = []
    possibleMoves = []
    while running:
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # x and y position of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): # user clicked the same square twice
                    sqSelected = () # deselect
                    playerClicks = []
                    possibleMoves = []
                else:
                    sqSelected = (row, col)
                    print(RF((row,col)))
                    playerClicks.append(sqSelected) # append for both first and second clicks
                    piece = findPiece(sqSelected)
                    if piece != 0:
                        possibleMoves = piece.get_legal_moves()
                    else:
                        possibleMoves = []
                        if len(playerClicks) == 1: # if the users first press is an empty square
                            playerClicks = []

                if len(playerClicks) == 2:
                    if movePiece(playerClicks[0], playerClicks[1]) == True:
                        WhiteToMove = not WhiteToMove
                    playerClicks = []
                    sqSelected = ()
                    possibleMoves = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_UP:
                    location = p.mouse.get_pos() # x and y position of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    debugSquare((row, col))

            drawGameState(screen,board,sqSelected,possibleMoves)
            clock.tick(MAX_FPS)
            p.display.flip()

def drawGameState(screen, board, sqSelected,possibleMoves):
    drawBoard(screen,sqSelected,possibleMoves) # draw squares on the board
    drawPieces(screen, board) # draw pieces on the squares

'''
Draws the Squares on the board, The top Left Square is always light. Also draws yellow and red squares
'''
def drawBoard(screen,sqSelected,possibleMoves):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row+col)%2]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if sqSelected != ():
        #screen.blit(redCircle, p.Rect(sqSelected[1]*SQ_SIZE, sqSelected[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE)) # draws a red circle on selected square
        p.draw.rect(screen, "red", p.Rect(sqSelected[1]*SQ_SIZE, sqSelected[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE)) # draws a red square under the piece
    if possibleMoves != []:
        for move in possibleMoves:
            screen.blit(yellowCircle, p.Rect(move[1]*SQ_SIZE, move[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE)) # draws a red circle on selected square
            #p.draw.rect(screen, "yellow", p.Rect(move[1]*SQ_SIZE, move[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE)) # draws a red square under the piece

'''
Draws the Pieces on the board, The top Left Square is always light
'''
def drawPieces(screen, board):
    for piece in board:
        image = piece.image
        row = piece.position[0]
        col = piece.position[1]
        screen.blit(image, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def getAllLegalMoves(board):
    moves = []
    for piece in board:
        moves.append[piece.get_legal_moves]

def debugSquare(position):
    piece = findPiece(position)
    if piece != 0:
        rf_moves = []
        moves = piece.get_legal_moves()
        print(moves)
        for move in (moves):
            rf_moves.append(RF(move))
        print(rf_moves)
        print(piece.__class__)
        print("POSITION - " + str(RF(piece.position)))
        print("number of pseudolegal moves - " + str(len(moves)))

def findPiece(position):
    for piece in board:
        if piece.position == position:
            return piece
    return 0

def movePiece(oldpos, newpos):
    piecetoCapture = findPiece(newpos)
    piece = findPiece(oldpos)
    piecetaken = ""
    if piecetoCapture != 0: #if there is a piece to capture
        if piece.color != piecetoCapture.color:
            board.remove(piecetoCapture) #capture piece
            piecetaken = "x"
            piece.position = newpos #move piece
            print("MOVE MADE - " + str(piece.symbol + piecetaken + RF(newpos)))
    else:
        piece.position = newpos #move piece
        print("MOVE MADE - " + str(piece.symbol + piecetaken + RF(newpos)))

'''
def movePiece(oldpos, newpos, legalMoves):
    if (oldpos, newpos) in legalMoves:
        pieceToCapture = findPiece(newpos)
        if pieceToCapture != 0:
            board.remove(pieceToCapture)
        pieceToMove = findPiece(oldpos)
        pieceToMove.position = (newpos)
'''


if __name__ == '__main__':
    #if GUI.GUI() == True:
    chess()
