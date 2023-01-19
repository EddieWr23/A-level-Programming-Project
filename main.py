import pieces
import pygame as p
import GUI

#CHESS VARIABLES
p.init()
WIDTH, HEIGHT = 768, 512 #default is 512, 512
DIMENSION = 8 #chess boards are 8x8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15 #for animations later on

redCircle = p.transform.scale(p.image.load("images/red.png"), (64,64))
yellowCircle = p.transform.scale(p.image.load("images/yellow.png"), (64,64))

playedMoves = []

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
                else: # if the square selected isnt already selected (first or second)
                    sqSelected = (row, col)
                    #print(RF((row,col))) # prints the official chess notation for the square to ghelp with debbugging
                    playerClicks.append(sqSelected) # append for both first and second clicks
                    if len(playerClicks) == 2: # if it was the second click
                        if movePiece(playerClicks[0], playerClicks[1], possibleMoves) == True:
                            WhiteToMove = not WhiteToMove
                        playerClicks = []
                        sqSelected = ()
                        possibleMoves = []
                    else:
                        piece = pieces.findPiece(sqSelected)
                        if piece != 0:
                            possibleMoves = piece.get_legal_moves()
                        else: # if the users first press is an empty square
                            possibleMoves = []
                            if len(playerClicks) == 1: 
                                playerClicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_UP:
                    location = p.mouse.get_pos() # x and y position of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    debugSquare((row, col))
                if e.key == p.K_DOWN:
                    debugGame()

            drawGameState(screen,pieces.board,sqSelected,possibleMoves)
            clock.tick(MAX_FPS)
            p.display.flip()

def drawGameState(screen, board, sqSelected,possibleMoves):
    drawBoard(screen,sqSelected,possibleMoves) # draw squares on the board
    drawPieces(screen, board) # draw pieces on the squares

'''
Draws the Squares on the board, The top Left Square is always light. Also draws yellow circles and red squares on square selected and legal moves respectively
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
    piece = pieces.findPiece(position)
    if piece != 0:
        rf_moves = []
        moves = piece.get_legal_moves()
        #print(moves)
        for move in (moves):
            rf_moves.append(RF(move))
        print(piece.__class__)
        print("POSITION - " + str(RF(piece.position)))
        print("number of pseudolegal moves - " + str(len(moves)) + ":")
        print(rf_moves)

def debugGame():
    print("-----DEBUGGING GAME-----")
    # moves made in this game
    print("Total Moves Made = " + len(playedMoves) + ":")
    print(playedMoves)
    #all pseudolegal moves in this position
    allLegalMoves = []
    for piece in pieces.board:
        moves = piece.get_legal_moves()
        for move in moves:
            allLegalMoves.append(move)
    print("Total Number of Legal Moves in this Position = " + len(allLegalMoves))
    print("--------------------")


def movePiece(oldpos, newpos, legalMoves):
    piecetaken = ""
    if (newpos) in legalMoves:
        pieceToCapture = pieces.findPiece(newpos)
        if pieceToCapture != 0:
            pieces.board.remove(pieceToCapture)
            piecetaken = "x"
        pieceToMove = pieces.findPiece(oldpos)
        pieceToMove.position = (newpos)
        print("MOVE MADE - " + str(pieceToMove.symbol + piecetaken + RF(newpos)))
        playedMoves.append((oldpos, newpos))
        pieces.whiteToMove = not pieces.whiteToMove # changes side to play moves
        


if __name__ == '__main__':
    #if GUI.GUI() == True:
    chess()
