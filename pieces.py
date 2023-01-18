import pygame as p

# define the superclass "Piece"
class Piece:
  def __init__(self, position, color):
    self.position = position
    self.color = color
  
  # method to get the legal moves for a piece
  def get_legal_moves(self):
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
      moves.append((y - 1, x))
      if y == 6:  # allow pawns to move two squares on their first move
        moves.append((y - 2, x))
    
    # black pawns can only move backward
    elif self.color == 'Black':
      moves.append((y + 1, x))
      if y == 1:  # allow pawns to move two squares on their first move
        moves.append((y + 2, x))
    
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
    temp = []
    moves = []
    
    # add all possible moves along the row and column
    for i in range(8):
      temp.append((x, i))
      temp.append((i, y))

    for move in temp:
      if move != self.position:
        moves.append(move)
    
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
    temp = []
    moves = []
    
    # add all possible "L" shaped moves
    temp.append((x + 2, y + 1))
    temp.append((x + 2, y - 1))
    temp.append((x - 2, y + 1))
    temp.append((x - 2, y - 1))
    temp.append((x + 1, y + 2))
    temp.append((x + 1, y - 2))
    temp.append((x - 1, y + 2))
    temp.append((x - 1, y - 2))
    
    for move in temp: #check if they are on the board and append them
      if move[0] < 8 and move[0] > -1 and move[1] < 8 and move[1] > -1:
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
    temp = []
    moves = []

    # add all possible moves along the diagonals
    i = x
    j = y
    while i < 8 and j < 8:  # move along top right diagonal
        temp.append((i, j))
        i += 1
        j += 1
    i = x
    j = y
    while i < 8 and j > -1: # down and right diagonal
        temp.append((i, j))
        i += 1
        j -= 1
    i = x
    j = y
    while i > -1 and j < 8: # up and left diagonal
        temp.append((i, j))
        i -= 1
        j += 1
    i = x
    j = y
    while i > -1 and j > -1: #down and left diagonal
        temp.append((i, j))
        i -= 1
        j -= 1

    for move in temp:
      if move != self.position:
        moves.append(move)
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
    temp = []
    moves = []

    # add all possible moves along the row and column
    for i in range(8):
      temp.append((x, i))
      temp.append((i, y))

    # add all possible moves along the diagonals
    i = x
    j = y
    while i < 8 and j < 8:  # move along top right diagonal
        temp.append((i, j))
        i += 1
        j += 1
    i = x
    j = y
    while i < 8 and j > -1: # down and right diagonal
        temp.append((i, j))
        i += 1
        j -= 1
    i = x
    j = y
    while i > -1 and j < 8: # up and left diagonal
        temp.append((i, j))
        i -= 1
        j += 1
    i = x
    j = y
    while i > -1 and j > -1: #down and left diagonal
        temp.append((i, j))
        i -= 1
        j -= 1

    for move in temp:
      if move != self.position:
        moves.append(move)
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
    temp = []
    moves = []
    
    # add all possible "L" shaped moves
    temp.append((x - 1, y - 1))
    temp.append((x + 1, y - 1))
    temp.append((x - 1, y + 1))
    temp.append((x + 1, y + 1))
    temp.append((x, y + 1))
    temp.append((x, y - 1))
    temp.append((x + 1, y))
    temp.append((x - 1, y))

    for move in temp: #check if they are on the board and append them
        if move[0] < 8 and move[0] > -1 and move[1] < 8 and move[1] > -1:
            moves.append(move)

    return moves

'''
BOARD ####################################################################################################################
'''
board = [Rook((7,0),"White"),Knight((7,1),"White"),Bishop((7,2),"White"),Queen((7,3),"White"),King((7,4),"White"),Bishop((7,5),"White"),Knight((7,6),"White"),Rook((7,7),"White"),
        Pawn((6,0),"White"),Pawn((6,1),"White"),Pawn((6,2),"White"),Pawn((6,3),"White"),Pawn((6,4),"White"),Pawn((6,5),"White"),Pawn((6,6),"White"),Pawn((6,7),"White"),
        Rook((0,0),"Black"),Knight((0,1),"Black"),Bishop((0,2),"Black"),Queen((0,3),"Black"),King((0,4),"Black"),Bishop((0,5),"Black"),Knight((0,6),"Black"),Rook((0,7),"Black"),
        Pawn((1,0),"Black"),Pawn((1,1),"Black"),Pawn((1,2),"Black"),Pawn((1,3),"Black"),Pawn((1,4),"Black"),Pawn((1,5),"Black"),Pawn((1,6),"Black"),Pawn((1,7),"Black")]

whiteToMove = True

def findPiece(position):
    for piece in board:
        if piece.position == position:
            return piece
    return 0