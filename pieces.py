import pygame as p

# define the superclass "Piece"
class Piece:
  def __init__(self, position, color):
    self.position = position
    self.color = color
  
  # method to get the legal moves for a piece
  def checkForSelfChecks(moves):
    if whiteToMove == True:
      pass
  
  def move_piece(self):
    pass
'''
PAWN ##########################################################################################
'''
# define the subclass "Pawn"
class Pawn(Piece):
  def __init__(self, position, color):
    super().__init__(position, color)
    self.symbol = ""
    if color == "White":
      self.image = p.transform.scale(p.image.load("images/wp.png"), (64,64))
    else:
      self.image = p.transform.scale(p.image.load("images/bp.png"), (64,64))
  
  def get_legal_moves(self):
    if self.color == "White" and whiteToMove == False or self.color == "Black" and whiteToMove == True:
      return []
    y, x = self.position
    moves = []
    
    # white pawns can only move forward
    if self.color == 'White':
      if findPiece(((y-1), x)) == 0: # if the square in front is not occupied
        moves.append((y - 1, x))
      if y == 6 and findPiece(((y-2), x)) == 0:  # allow pawns to move two squares on their first move provided it is empty
        moves.append((y - 2, x))
      piece = findPiece(((y-1), x+1))
      if piece != 0: #if there is a piece diagonally
        if piece.color == "Black":
          moves.append(piece.position)
      piece = findPiece(((y-1), x-1))
      if piece != 0: #if there is a piece diagonally
        if piece.color == "Black":
          moves.append(piece.position)
    
    # black pawns can only move backward
    elif self.color == 'Black':
      if findPiece(((y+1), x)) == 0: # if the square in front is not occupied
        moves.append((y+1, x))
      if y == 1 and findPiece(((y+2), x)) == 0:  # allow pawns to move two squares on their first move provided it is empty
        moves.append((y+2, x))
      piece = findPiece(((y+1), x+1))
      if piece != 0: #if there is a piece diagonally
        if piece.color == "White":
          moves.append(piece.position)
      piece = findPiece(((y+1), x-1))
      if piece != 0: #if there is a piece diagonally
        if piece.color == "White":
          moves.append(piece.position)

    
    
    return moves
'''
ROOK ##########################################################################################
'''
# define the subclass "Rook"
class Rook(Piece):
  def __init__(self, position, color):
    super().__init__(position, color)
    self.symbol = "R"
    if color == "White":
      self.image = p.transform.scale(p.image.load("images/wR.png"), (64,64))
    else:
      self.image = p.transform.scale(p.image.load("images/bR.png"), (64,64))
  
  def get_legal_moves(self):
    if self.color == "White" and whiteToMove == False or self.color == "Black" and whiteToMove == True:
      return []
    x, y = self.position
    moves = []

    i = 1 # RIGHT
    while (i + x) < 8:
      piece = findPiece(((x+i), y))
      if piece == 0: #if square is empty
        moves.append(((x+i), y))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append(((x+i), y))
          break
      i = i+1

    i = 1 # LEFT
    while (x - i) >= 0:
      piece = findPiece(((x-i), y))
      if piece == 0: #if square is empty
        moves.append(((x-i), y))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append(((x-i), y))
          break
      i = i+1

    i = 1 # DOWN
    while (y + i) < 8:
      piece = findPiece((x, (y+i)))
      if piece == 0: #if square is empty
        moves.append((x, (y+i)))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append((x, (y+i)))
          break
      i = i+1

    i = 1 # UP
    while (y - i) >= 0:
      piece = findPiece((x, (y-i)))
      if piece == 0: #if square is empty
        moves.append((x, (y-i)))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append((x, (y-i)))
          break
      i = i+1
    
    return moves
'''
KNIGHT ##########################################################################################
'''
# define the subclass "Knight"
class Knight(Piece):
  def __init__(self, position, color):
    super().__init__(position, color)
    self.symbol = "N"
    if color == "White":
      self.image = p.transform.scale(p.image.load("images/wN.png"), (64,64))
    else:
      self.image = p.transform.scale(p.image.load("images/bN.png"), (64,64))
  
  def get_legal_moves(self):
    if self.color == "White" and whiteToMove == False or self.color == "Black" and whiteToMove == True:
      return []
    x, y = self.position
    knightDirections = [(x + 2, y + 1),(x + 2, y - 1),(x - 2, y + 1),(x - 2, y - 1),(x + 1, y + 2),(x + 1, y - 2),(x - 1, y + 2),(x - 1, y - 2)]
    moves = []
    
    for move in knightDirections: #check if they are on the board and append them
      if move[0] < 8 and move[0] > -1 and move[1] < 8 and move[1] > -1:
        piece = findPiece(move)
        if piece == 0: # if square is empty
          moves.append(move)
        else: #if square has a piece on it
          if piece.color != self.color:
            moves.append(move)


    return moves
'''
BISHOP ##########################################################################################
'''
# define the subclass "Bishop"
class Bishop(Piece):
  def __init__(self, position, color):
    super().__init__(position, color)
    self.symbol = "B"
    if color == "White":
      self.image = p.transform.scale(p.image.load("images/wB.png"), (64,64))
    else:
      self.image = p.transform.scale(p.image.load("images/bB.png"), (64,64))
  
  def get_legal_moves(self):
    if self.color == "White" and whiteToMove == False or self.color == "Black" and whiteToMove == True:
      return []
    x, y = self.position
    moves = []

    i = 1
    while (x + i) < 8 and  (y + i) < 8: #DOWN AND RIGHT
      piece = findPiece(((x+i), (y+i)))
      if piece == 0: #if square is empty
        moves.append(((x+i), (y+i)))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append(((x+i), (y+i)))
          break
      i = i+1

    i = 1 
    while (x - i) >= 0 and (y + i) < 8: #UP AND RIGHT
      piece = findPiece(((x-i), (y+i)))
      if piece == 0: #if square is empty
        moves.append(((x-i), (y+i)))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append(((x-i), (y+i)))
          break
      i = i+1

    i = 1 
    while (x + i) < 8 and (y - i) >= 0: # DOWN AND LEFT
      piece = findPiece(((x+i), (y-i)))
      if piece == 0: #if square is empty
        moves.append(((x+i), (y-i)))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append(((x+i), (y-i)))
          break
      i = i+1

    i = 1 
    while (x - i) >= 0 and (y - i) >= 0: # UP AND LEFT
      piece = findPiece(((x-i), (y-i)))
      if piece == 0: #if square is empty
        moves.append(((x-i), (y-i)))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append(((x-i), (y-i)))
          break
      i = i+1
    
    return moves
'''
QUEEN ##########################################################################################
'''
# define the subclass "Queen"
class Queen(Piece):
  def __init__(self, position, color):
    super().__init__(position, color)
    self.symbol = "Q"
    if color == "White":
      self.image = p.transform.scale(p.image.load("images/wQ.png"), (64,64))
    else:
      self.image = p.transform.scale(p.image.load("images/bQ.png"), (64,64))
  
  def get_legal_moves(self):
    if self.color == "White" and whiteToMove == False or self.color == "Black" and whiteToMove == True:
      return []
    x, y = self.position
    moves = []
    i = 1 # RIGHT
    while (i + x) < 8:
      piece = findPiece(((x+i), y))
      if piece == 0: #if square is empty
        moves.append(((x+i), y))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append(((x+i), y))
          break
      i = i+1

    i = 1 # LEFT
    while (x - i) >= 0:
      piece = findPiece(((x-i), y))
      if piece == 0: #if square is empty
        moves.append(((x-i), y))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append(((x-i), y))
          break
      i = i+1

    i = 1 # DOWN
    while (y + i) < 8:
      piece = findPiece((x, (y+i)))
      if piece == 0: #if square is empty
        moves.append((x, (y+i)))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append((x, (y+i)))
          break
      i = i+1

    i = 1 # UP
    while (y - i) >= 0:
      piece = findPiece((x, (y-i)))
      if piece == 0: #if square is empty
        moves.append((x, (y-i)))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append((x, (y-i)))
          break
      i = i+1
    
    i = 1
    while (x + i) < 8 and  (y + i) < 8: #DOWN AND RIGHT
      piece = findPiece(((x+i), (y+i)))
      if piece == 0: #if square is empty
        moves.append(((x+i), (y+i)))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append(((x+i), (y+i)))
          break
      i = i+1

    i = 1 
    while (x - i) >= 0 and (y + i) < 8: #UP AND RIGHT
      piece = findPiece(((x-i), (y+i)))
      if piece == 0: #if square is empty
        moves.append(((x-i), (y+i)))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append(((x-i), (y+i)))
          break
      i = i+1

    i = 1 
    while (x + i) < 8 and (y - i) >= 0: # DOWN AND LEFT
      piece = findPiece(((x+i), (y-i)))
      if piece == 0: #if square is empty
        moves.append(((x+i), (y-i)))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append(((x+i), (y-i)))
          break
      i = i+1

    i = 1 
    while (x - i) >= 0 and (y - i) >= 0: # UP AND LEFT
      piece = findPiece(((x-i), (y-i)))
      if piece == 0: #if square is empty
        moves.append(((x-i), (y-i)))
      else: #if the square is empty
        if piece.color == self.color:
          break
        else:
          moves.append(((x-i), (y-i)))
          break
      i = i+1
    
    return moves

'''
KING ##########################################################################################
'''
# define the subclass "King"
class King(Piece):
  def __init__(self, position, color):
    super().__init__(position, color)
    self.symbol = "K"
    if color == "White":
      self.image = p.transform.scale(p.image.load("images/wK.png"), (64,64))
    else:
      self.image = p.transform.scale(p.image.load("images/bK.png"), (64,64))
  
  def get_legal_moves(self):
    if self.color == "White" and whiteToMove == False or self.color == "Black" and whiteToMove == True:
      return []
    x, y = self.position
    kingDirections = [(x - 1, y - 1),(x + 1, y - 1),(x - 1, y + 1),(x + 1, y + 1),(x, y + 1),(x, y - 1),(x + 1, y),(x - 1, y)]
    moves = []

    for move in kingDirections: #check if they are on the board and append them
      if move[0] < 8 and move[0] > -1 and move[1] < 8 and move[1] > -1:
        piece = findPiece(move)
        if piece == 0: # if square is empty
          moves.append(move)
        else: #if square has a piece on it
          if piece.color != self.color:
            moves.append(move)

    return moves

'''
BOARD ####################################################################################################################
'''
#board = [Rook((7,0),"White"),Knight((7,1),"White"),Bishop((7,2),"White"),Queen((7,3),"White"),King((7,4),"White"),Bishop((7,5),"White"),Knight((7,6),"White"),Rook((7,7),"White"),
#        Pawn((6,0),"White"),Pawn((6,1),"White"),Pawn((6,2),"White"),Pawn((6,3),"White"),Pawn((6,4),"White"),Pawn((6,5),"White"),Pawn((6,6),"White"),Pawn((6,7),"White"),
#        Rook((0,0),"Black"),Knight((0,1),"Black"),Bishop((0,2),"Black"),Queen((0,3),"Black"),King((0,4),"Black"),Bishop((0,5),"Black"),Knight((0,6),"Black"),Rook((0,7),"Black"),
#        Pawn((1,0),"Black"),Pawn((1,1),"Black"),Pawn((1,2),"Black"),Pawn((1,3),"Black"),Pawn((1,4),"Black"),Pawn((1,5),"Black"),Pawn((1,6),"Black"),Pawn((1,7),"Black")]

board = [Pawn((6,0),"Black"), Pawn((1,7), "White")]

whiteToMove = True

def findPiece(position):
    for piece in board:
        if piece.position == position:
            return piece
    return 0