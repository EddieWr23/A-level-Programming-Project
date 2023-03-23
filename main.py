import pieces
import pygame as p
import GUI
import random
import threading
import time

#CHESS VARIABLES
p.init()
WIDTH, HEIGHT = pieces.WIDTH, pieces.HEIGHT #default is 512, 512
DIMENSION = pieces.DIMENSION #chess boards are 8x8
SQ_SIZE = pieces.SQ_SIZE
MAX_FPS = 15 #for animations


redCircle = p.transform.scale(p.image.load("images/red.png"), (SQ_SIZE,SQ_SIZE))
yellowCircle = p.transform.scale(p.image.load("images/yellow.png"), (SQ_SIZE,SQ_SIZE))

playedMoves = []
 
'''
Functions for ranks and files
'''
def rank(num):
    return 8 - num

def file(num): # takes an integer representing a file number and returns the corresponding file letter as used in chess notation (e.g. file 0 is "a", file 7 is "h").
    files = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}
    return files[num]

def RF(position): # takes a tuple representing a chess position (in the form (rank, file)) and returns the corresponding position as a string in chess notation (e.g. (1, 0) becomes "a1").
    return(str(file(position[1])) + str(rank(position[0])))

def undoRF(position): # takes a string representing a chess position (in the form "a1", "b2", etc.) and returns the corresponding position as a tuple (in the form (rank, file)). It "undoes" the RF function by converting the file letter back to a file number and subtracting the rank from 8 to get the rank number.
    position = list(position)
    files = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    filenum = files[position[0]]
    ranknum = 8 - int(position[1])
    return (ranknum , filenum)


'''
The main chess program
'''
def chess():
    screen = p.display.set_mode((WIDTH, HEIGHT)) #WIDTH*1.5 for sidebar
    p.display.set_caption("Eddie's Chess Program") # pygame title
    Icon = p.image.load(r"images/bK.png") # pygame icon
    p.display.set_icon(Icon)
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    global running
    running = True
    global colors
    colors = [p.Color(255,255,255),p.Color("gray")] # default theme
    sqSelected = ()
    playerClicks = []
    possibleMoves = []
    print(GUI.THEME)
    '''
    THEMES
    '''
    if GUI.THEME == ['Black and White']: # Black and White
        colors = [p.Color(255,255,255),p.Color("gray")]
    elif GUI.THEME == ['Green and Beige']: # Green and beige
        colors = [p.Color(215,255,185),p.Color(95, 135, 0)]
    elif GUI.THEME == ['Brown and Beige']: # brown and beige
        colors = [p.Color(215, 255, 185),p.Color(175, 95, 0)]

    while running:
        for e in p.event.get():

            movemade = False

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN: # if the user presses the mouse
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
                        if movePiece(playerClicks[0], playerClicks[1]) == True:
                            movemade = True
                        playerClicks = []
                        sqSelected = ()
                        possibleMoves = []
                    else: # if players first click
                        possibleMoves = []
                        piece = pieces.findPiece(sqSelected)
                        if piece != 0:
                            allLegalMoves = getAllLegalMoves()
                            for move in allLegalMoves:
                                if move[0] == piece.position:
                                    possibleMoves.append(move[1])
                        else: # if the users first press is an empty square
                            possibleMoves = []
                            if len(playerClicks) == 1: 
                                playerClicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_UP:
                    location = p.mouse.get_pos() # x and y position of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    debugSquare((row, col)) # debug square
                elif e.key == p.K_DOWN: #debug game
                    debugGame()
                elif e.key == p.K_RIGHT: # ai make move
                    AI_makeMaterialMove()
                elif e.key == p.K_LEFT: # simulation loop
                    while True:
                        AI_makeMaterialMove()
                        drawGameState(screen,pieces.board,sqSelected,possibleMoves, colors)
                        checkForSufficientMaterial()
                        clock.tick(MAX_FPS)
                        p.display.flip()
                        time.sleep(0.1)
            
            

            drawGameState(screen,pieces.board,sqSelected,possibleMoves, colors) # draws game state
            checkForSufficientMaterial() # checks the board isnt just 2 kings
            clock.tick(MAX_FPS)
            p.display.flip() # update
            if movemade == True:
                AI_makeMaterialMove()
                drawGameState(screen,pieces.board,sqSelected,possibleMoves, colors)
                checkForSufficientMaterial()
                clock.tick(MAX_FPS)
                p.display.flip()


def drawGameState(screen, board, sqSelected,possibleMoves, colors):
    drawBoard(screen,sqSelected,possibleMoves, colors) # draw squares on the board
    drawPieces(screen, board) # draw pieces on the squares

'''
Draws the Squares on the board, The top Left Square is always light. Also draws yellow circles and red squares on square selected and legal moves respectively
'''
def drawBoard(screen,sqSelected,possibleMoves, colors):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row+col)%2]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)) #draws light and dark squares
    if sqSelected != ():
        p.draw.rect(screen, "red", p.Rect(sqSelected[1]*SQ_SIZE, sqSelected[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE)) # draws a red square under the piece
    if possibleMoves != []:
        for move in possibleMoves:
            screen.blit(yellowCircle, p.Rect(move[1]*SQ_SIZE, move[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE)) # draws a yellow circle on legal moves

'''
Draws the Pieces on the board
'''
def drawPieces(screen, board):
    for piece in board: # iterates through the board
        image = piece.image
        row = piece.position[0]
        col = piece.position[1] 
        screen.blit(image, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)) # draws image

'''
Debug Square function, returns
- piece type
- position
- number of pseudolegalmoves
- moves made
- is Square Attacked
- is Square Defended
'''
def debugSquare(position):
    piece = pieces.findPiece(position)
    if piece != 0: #if there is a piece
        rf_moves = []
        moves = piece.get_legal_moves()
        #print(moves)
        for move in (moves):
            rf_moves.append(RF(move))
        print(piece.__class__)
        print("POSITION - " + str(RF(piece.position)) + " / " + str(piece.position))
        print("number of pseudolegal moves - " + str(len(moves)) + ":")
        print("Moves Made - " + str(piece.movesMade))
        print(rf_moves)
    print("Square attacked = " + str(isSquareAttacked(position)))
    print("Square defended = " + str(isSquareDefended(position)))

'''
Provides information about the current gameState
- whos move it is
- no of moves made
- no of moves can be made in this position
- white and black material
- material difference
'''
def debugGame():
    print("-----DEBUGGING GAME-----")
    if pieces.whiteToMove:
        print("WHITE TO MOVE")
    else:
        print("BLACK TO MOVE")
    # moves made in this game
    print("Total Moves Made = " + str(len(playedMoves)) + ":")
    print(playedMoves)
    #all pseudolegal moves in this position
    allLegalMoves = getAllLegalMoves()
    print("Total Number of Legal Moves in this Position = " + str(len(allLegalMoves)))
    whiteMaterial, blackMaterial, materialDifference = calculateMaterial()
    print("White Material = " + str(whiteMaterial))
    print("Black Material = " + str(blackMaterial))
    if materialDifference > 0:
        print("Material Difference = +" + str(materialDifference))
    else:
        print("Material Difference = " + str(materialDifference))
    print("--------------------")

'''
Function for moving a piece, will return true if the move has been sucessfuly made
'''
def movePiece(oldpos, newpos):
    piecetaken = ""
    pieceToMove = pieces.findPiece(oldpos)
    pieceToCapture = pieces.findPiece(newpos)
    allLegalMoves = getAllLegalMoves()
    if ((oldpos, newpos)) in allLegalMoves: # if the move is 'legal'
        if pieceToCapture != 0: # if there is a piece to capture (not an empty square)
            pieces.board.remove(pieceToCapture)
            piecetaken = "x"
            if pieceToCapture.symbol == "K":
                global running
                running = False
                GUI.kingCaptured(pieceToCapture.color)
                return False
        pieceToMove.position = (newpos) # move piece
        print("MOVE MADE - " + str(pieceToMove.symbol + piecetaken + RF(newpos)))
        checkForChecks()
        checkForPromotes()
        playedMoves.append((oldpos, newpos))
        pieces.whiteToMove = not pieces.whiteToMove # changes side to play moves
        pieceToMove.movesMade = pieceToMove.movesMade + 1

        '''
        This additionally moves the rook if the move was the king castling
        '''
        if pieceToMove.symbol == 'K':
            if oldpos == (7,4) and newpos == (7,6):
                rook = pieces.findPiece((7,7))
                rook.position = (7,5)
            elif oldpos == (7,4) and newpos == (7,2):
                rook = pieces.findPiece((7,0))
                rook.position = (7,3)
            elif oldpos == (0,4) and newpos == (0,6):
                rook = pieces.findPiece((0,7))
                rook.position = (0,5)
            elif oldpos == (7,4) and newpos == (7,6):
                rook = pieces.findPiece((0,0))
                rook.position = (7,5)
        return True

'''
Function to return all pseudolegalmoves in a position, excluding checks and pins
'''
def getAllPossibleMoves():
    allPossibleMoves = []
    for piece in pieces.board:
        moves = piece.get_legal_moves()
        for move in moves:
            allPossibleMoves.append(((piece.position),(move)))
    return allPossibleMoves

'''
Returns the King of the color passed in
'''
def findKing(color):
    for piece in pieces.board:
        if piece.symbol == "K" and piece.color == color:
            return piece

'''
Gets all possible moves with getAllPossibleMoves, then checks for legality and returns moves as a list
The function simulates making the move by temporarily making the move, then checking if the King is attacked, which means the piece is pinned or equivalent, and the move is illegal
'''
def getAllLegalMoves():
    allLegalMoves = []
    possibleMoves = getAllPossibleMoves() #get all pseudolegal moves
    if pieces.whiteToMove:
        king = findKing("White")
    else:
        king = findKing("Black")
 
    for move in possibleMoves:
        tempPieceToCapture = pieces.findPiece(move[1])
        tempPieceToMove = pieces.findPiece(move[0])
    
        if tempPieceToCapture != 0:
            pieces.board.remove(tempPieceToCapture)
        tempPieceToMove.position = move[1]

        if isSquareAttacked(king.position) == False: #if the move means your king isnt attacked after, its legal
            allLegalMoves.append(move)
        
        tempPieceToMove.position = move[0]
        if tempPieceToCapture != 0:
            pieces.board.append(tempPieceToCapture)
    
    if len(allLegalMoves) == 0: # if the user has no moves (checkmate or stalemate)
        if isSquareAttacked(king.position): # if its a checkmate
            if pieces.whiteToMove:
                GUI.kingCaptured("White")
            else:
                GUI.kingCaptured("Black")
        else: # if its stalemate
            GUI.draw("stalemate")
        exit()
    return allLegalMoves

'''
Function to return bool value of if a square is attacked
'''
def isSquareAttacked(position):
    piece = pieces.findPiece(position)
    if piece == 0:
        pieces.whiteToMove = not pieces.whiteToMove
        possibleMoves = getAllPossibleMoves()
        for move in possibleMoves:
            if move[1] == position:
                pieces.whiteToMove = not pieces.whiteToMove
                return True
        pieces.whiteToMove = not pieces.whiteToMove
        return False
    else:
        if (piece.color == "White" and pieces.whiteToMove == True) or (piece.color == "Black" and pieces.whiteToMove == False): #same color to move as piece attacked
            pieces.whiteToMove = not pieces.whiteToMove
            possibleMoves = getAllPossibleMoves()
            for move in possibleMoves:
                if move[1] == piece.position:
                    pieces.whiteToMove = not pieces.whiteToMove
                    return True
            pieces.whiteToMove = not pieces.whiteToMove
            return False
        else:
            possibleMoves = getAllPossibleMoves()
            for move in possibleMoves:
                if move[1] == piece.position:
                    return True
            return False

'''
Function to return bool value of if a square is defended
Function swaps piece with one of opposite color, and checks if that piece is now attacked, as pieces cannot take their own pieces, so would always return false
'''
def isSquareDefended(position):
    piece = pieces.findPiece(position)
    flip = False
    if piece == 0: # if the square is empty
        if pieces.whiteToMove == True:
            color = "Black"
        else:
            color = "White"
        pieces.whiteToMove = not pieces.whiteToMove
        temp = pieces.Temp(position, color)
        pieces.board.append(temp)
        allLegalMoves = getAllLegalMoves()
        for move in allLegalMoves:
            if move[1] == position:
                pieces.whiteToMove = not pieces.whiteToMove
                pieces.board.remove(temp)
                return True
        pieces.whiteToMove = not pieces.whiteToMove
        pieces.board.remove(temp)
        return False

    else: # if the square has a piece on it
        if (piece.color == "White" and pieces.whiteToMove == False) or (piece.color == "Black" and pieces.whiteToMove == True):
            flip = True # to allow swap back again
            pieces.whiteToMove = not pieces.whiteToMove
        pieces.board.remove(piece)
        if piece.color == "Black":
            temp = pieces.Temp(piece.position, "White")
        elif piece.color == "White":
            temp = pieces.Temp(piece.position, "Black")
        pieces.board.append(temp)
        allLegalMoves = getAllLegalMoves()
        for move in allLegalMoves:
            if move[1] == piece.position:
                if flip:
                    pieces.whiteToMove = not pieces.whiteToMove
                pieces.board.remove(temp)
                pieces.board.append(piece)
                return True
        if flip:
            pieces.whiteToMove = not pieces.whiteToMove
        pieces.board.remove(temp)
        pieces.board.append(piece)
        return False

'''
Function to print check if the program detects a king being attacked
'''
def checkForChecks():
    if pieces.whiteToMove == True:
        color = "White"
    else:
        color = "Black"
    king = findKing(color)
    if isSquareAttacked(king.position) == True:
        print("Check")

'''
Function to check all pawns to see if they can be promoted, will run a GUI where the user can choose
'''
def checkForPromotes():
    for piece in pieces.board:
        if piece.symbol == "":
            if piece.position[0] == 0 or piece.position[0] == 7:
                chosenPromote = GUI.choosePromote(piece.color)
                pieces.board.remove(piece)
                if chosenPromote == "Queen":
                    pieces.board.append(pieces.Queen(piece.position, piece.color))
                elif chosenPromote == "Rook":
                    pieces.board.append(pieces.Rook(piece.position, piece.color))
                elif chosenPromote == "Bishop":
                    pieces.board.append(pieces.Bishop(piece.position, piece.color))
                elif chosenPromote == "Knight":
                    pieces.board.append(pieces.Knight(piece.position, piece.color))

'''
checks the board has more than just 2 kings on it, to stop the games reaching an endless state of 2 kings
'''
def checkForSufficientMaterial():
    whiteMaterial, blackMaterial, materialDifference = calculateMaterial()
    if whiteMaterial == 0 and blackMaterial == 0:
        GUI.draw("")
        exit()

'''
calculates the material in a position
'''
def calculateMaterial():
    whiteMaterial, blackMaterial = 0, 0
    for piece in pieces.board: # iterates through board
        if piece.color == "Black":
            blackMaterial = blackMaterial + piece.value
        else:
            whiteMaterial = whiteMaterial + piece.value
    materialDifference = whiteMaterial - blackMaterial # material difference
    return (whiteMaterial-100), (blackMaterial-100), materialDifference # subtracts 100 for kings value unaccounted

'''
Function to make the AI make a random move if it doesnt see anything better
'''
def AI_makeRandomMove():
    hangingMoves = []
    nonHangingMoves = []
    allLegalMoves = getAllLegalMoves()
    for move in allLegalMoves:
        if isSquareAttacked(move[1]) == True and isSquareDefended(move[1]) == False:
            hangingMoves.append(move)
        else:
            nonHangingMoves.append(move)
    try:
        moveToMake = random.choice(nonHangingMoves)
    except:
        moveToMake = random.choice(hangingMoves)
    movePiece(moveToMake[0], moveToMake[1])

'''
Function to make AI scan for gaining material lines
'''
def AI_makeMaterialMove():
    allLegalMoves = getAllLegalMoves()
    bestMoveMaterial = -100
    for move in allLegalMoves: # for all possible moves
        pieceToMove = pieces.findPiece(move[0])
        pieceToCapture = pieces.findPiece(move[1])
        if pieceToCapture != 0:
            if isSquareDefended(pieceToCapture.position) == False: # if piece is hanging
                materialExchange = pieceToCapture.value
            else: # if attacked piece is defended
                materialExchange = pieceToCapture.value - pieceToMove.value
            if materialExchange > bestMoveMaterial and materialExchange > 0:
                bestMove, bestMoveMaterial = move, materialExchange
    try:
        movePiece(bestMove[0], bestMove[1])
        print("materialmove")
    except:
        AI_makeRandomMove()
        print("randommove")

'''
Main Loop
'''
if __name__ == '__main__':
    if GUI.GUI() == True: # if user sucessfully logs in
        chess() # runs main loop


    
