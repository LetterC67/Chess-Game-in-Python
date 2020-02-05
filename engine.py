
#Author: Le Tuan Hoang
#Email: hoangdeptoong@gmail.com


#This project is a very simple chess engine which requires only basic knowledge about Python(list, function, class, ...)
#There are 2 mode, computer vs human an human vs human
#AI chess from here: https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/
#This uses Minimax algorithm, find out here: https://en.wikipedia.org/wiki/Minimax

#Chess engine v1.1.2

#import built-in modules
import random,time,copy,os

#evaluate board for AI chess
from evaluate import evaluate


#position
class state():
  def __init__(self):
    # necessary variables
    self.board = []
    self.bKMoved = 0
    self.wKMoved = 0
    self.bQueenSideCastle = 0
    self.bKingSideCastle = 0
    self.wQueenSideCastle = 0
    self.wKingSideCastle = 0
    self.enPassant = 0
    self.enPassantCol = 0
    self.countDown = 0
    
  def set(self,board,value):
    #set value after a move
    self.board = copy.deepcopy(board)
    self.bKMoved,self.wKMoved,self.bQueenSideCastle,self.bKingSideCastle,self.wQueenSideCastle,self.wKingSideCastle,self.enPassant,self.enPassantCol,self.countDown = value

  def get(self):
    #get the value when undo
    return [self.board,[self.bKMoved,self.wKMoved,self.bQueenSideCastle,self.bKingSideCastle,self.wQueenSideCastle,self.wKingSideCastle,self.enPassant,self.enPassantCol,self.countDown]]


class chess():
  def __init__(self):
    #Pieces W for white, B for black
    self.WKING=9
    self.WQUEEN=11
    self.WROCK=3
    self.WBISHOP=1
    self.WKNIGHT=5
    self.WPAWN=7
    self.BKING=8
    self.BQUEEN=10
    self.BROCK=2
    self.BBISHOP=0
    self.BKNIGHT=4
    self.BPAWN=6

    #some necessary variables
    self.evaluated = 0
    self.canmove = []
    self.maxDepth = 3
    self._isEndGame = 'nothing'
    self.currentTurn = 0
    self.checkMate,self.comPlayer = False,False
    self.bQueenSideCastle,self.bKingSideCastle,self.wQueenSideCastle,self.wKingSideCastle = True,True,True,True #castling ability
    self.enPassant,self.enPassantCol = False,0 #en passsant
    self.wKMoved,self.bKMoved = False,False #white king moved, black king moved (for castling)
    self.choice,self.match,self.specMove = [],[],[]
    self.match.append(state())
    self.countDown = 50 #50 moves rule
    self.num = -1
    self.c,self.r,self.rc,self.cc,self.rk,self.ck = 0,0,0,0,0,0

    self.BLACK = 1
    self.WHITE = 0

    #board is 9x9 2D array(8x8 is for pieces)
    self.originalBoard = [ 
        [' ','a','b','c','d','e','f','g','h'],
        ['8',self.BROCK,self.BKNIGHT,self.BBISHOP,self.BQUEEN,self.BKING,self.BBISHOP,self.BKNIGHT,self.BROCK],
        ['7',self.BPAWN,self.BPAWN,self.BPAWN,self.BPAWN,self.BPAWN,self.BPAWN,self.BPAWN,self.BPAWN],
        ['6',' ',' ',' ',' ',' ',' ',' ',' '],
        ['5',' ',' ',' ',' ',' ',' ',' ',' '],
        ['4',' ',' ',' ',' ',' ',' ',' ',' '],
        ['3',' ',' ',' ',' ',' ',' ',' ',' '],
        ['2',self.WPAWN,self.WPAWN,self.WPAWN,self.WPAWN,self.WPAWN,self.WPAWN,self.WPAWN,self.WPAWN],
        ['1',self.WROCK,self.WKNIGHT,self.WBISHOP,self.WQUEEN,self.WKING,self.WBISHOP,self.WKNIGHT,self.WROCK],
      ]

    #use this board
    self.board =  []

    #save first position
    self.match[0].set(self.originalBoard,[self.wKMoved,self.bKMoved,self.bKingSideCastle,self.bQueenSideCastle,self.wKingSideCastle,self.wQueenSideCastle,self.enPassant,self.enPassantCol,self.countDown])

    #squares which king cannot move to
    #1 means cannot move to
    self.danger = [] 
    for i in range(9):
      self.danger.append([])
      for j in range(9):
        self.danger[i].append(0)

    #way to the opponent's king
    self.checkWay = []

    #init
    self.initBoard()
    
  def BW(self,x): #black, white or nothing
    if str(x) == ' ':
      return 2
    if x%2:
      return self.BLACK
    else:
      return self.WHITE

  def canMoveTo(self,row,col,color): #can move to this square row,col are coordinations
    if self.board[row][col] == ' ' or self.BW(self.board[row][col]) == color:
      return 1
    else:
      return 0
    
  def pawnMove(self,row,col,color): #row,col are destinations, x is piece's color
    if self.BW(self.board[row][col]) == color: self.choice[self.num].append([row,col])

  def knightMove(self,move,color): # move is list which  consists of 8 elements. This will remove illegal moves
    return [x for x in move if 0<x[0]<=8 and 0<x[1]<=8 and self.canMoveTo(x[0],x[1],color)]

  def kingMove(self,move,color): # move is list which  consists of 8 elements. This will remove illegal moves
    return [x for x in move if 0<x[0]<=8 and 0<x[1]<=8 and self.canMoveTo(x[0],x[1],color) and not self.danger[x[0]][x[1]]]

  def queenRockMove(self,color,king): # king is white king or black king
    move = self.queenRockRule()
    for i in move:
      self.choice[self.num].extend(self.valid(i,color))

  def valid(self,move,color):#legal move, z is color
    for i in range(len(move)):
      if self.BW(self.board[move[i][0]][move[i][1]]) == color^1: # if there is a piece which has the same color block the way, return
        return move[:i]
      elif self.BW(self.board[move[i][0]][move[i][1]]) == color: # if there is a piece which has different color, block the way (can capture that piece), return
        return move[:i+1]
    return move # no piece block its way, all moves are legal

  def queenBishopRule(self):# move diagonally, z is color
    x,y = self.row,self.col
    move1 = [[x+i,y+i] for i in range(1,8) if 1<=x+i<9 and 1<=y+i<9]
    move2 = [[x-i,y+i] for i in range(1,8) if 1<=x-i<9 and 1<=y+i<9]
    move3 = [[x+i,y-i] for i in range(1,8) if 1<=x+i<9 and 1<=y-i<9]
    move4 = [[x-i,y-i] for i in range(1,8) if 1<=x-i<9 and 1<=y-i<9]
    return [move1,move2,move3,move4]

  def queenRockRule(self):# move horizontally, vertically
    x,y = self.row,self.col
    move1 = [[x+i,y] for i in range(1,8) if 1<=x+i<9 and 1<=y<9]
    move2 = [[x,y+i] for i in range(1,8) if 1<=x<9 and 1<=y+i<9]
    move3 = [[x-i,y] for i in range(1,8) if 1<=x-i<9 and 1<=y<9]
    move4 = [[x,y-i] for i in range(1,8) if 1<=x<9 and 1<=y-i<9]
    return [move1,move2,move3,move4]

  def queenBishopMove(self,color,king): #add legal move
    move = self.queenBishopRule()
    for i in move:
      self.choice[self.num].extend(self.valid(i,color))

  def findPos(self,row,col): # find legal move from 'choice' list
    num = 0
    for i in self.choice:
      if [row,col] in i:
        break
      num+=1
    return num

  def checkMateRock(self):#find the way from rock or queen to the opponent's king
    r,c,rc,cc  = self.r,self.c,self.rc,self.cc
    if self.rc > self.r and self.cc == self.c:
      self.checkWay[-1].extend([[self.r+1+i,self.c] for i in range(0,8) if self.r+1+i<self.rc])
    elif self.rc < self.r and self.cc == self.c:
      self.checkWay[-1].extend([[self.r-1-i,self.c] for i in range(0,8) if r-1-i>rc])
    elif self.cc > self.c and self.rc == self.r:
      self.checkWay[-1].extend([[self.r,self.c+1+i] for i in range(0,8) if c+1+i<cc])
    elif self.cc < self.c and self.rc == self.r:
      self.checkWay[-1].extend([[self.r,self.c-1-i] for i in range(0,8) if c-1-i>cc])

  def checkMateBishop(self):#find the way from bishop or queen to the opponent's king
    r,c,rc,cc  = self.r,self.c,self.rc,self.cc
    if self.rc > self.r and self.cc > self.c:
      self.checkWay[-1].extend([[r+1+i,c+1+i] for i in range(0,8) if r+1+i<rc and c+1+i<cc])
    elif self.rc < self.r and self.cc < self.c:
      self.checkWay[-1].extend([[r-1-i,c-1-i] for i in range(0,8) if r-1-i>rc and c-1-i>cc])
    elif self.cc > self.c and self.rc < self.r:
      self.checkWay[-1].extend([[r-1-i,c+1+i] for i in range(0,8) if r-1-i>rc and c+1+i<cc])
    elif self.cc < self.c and self.rc > self.r:
      self.checkWay[-1].extend([[r+1+i,c-1-i] for i in range(0,8) if r+1+i<rc and c-1-i>cc])

  def funcBishop(self,color,king): #piece has special move because if this piece is moved, its king will be affected
    self.specMove.append([])
    count = 0
    addX,addY  = -1,-1 # each time this piece move, row changes by addX, col changes by addY
    if self.rk > self.r: addX = 1
    if self.ck > self.c: addY = 1
    x,y = self.r,self.c
    while x != self.rk and y!=self.ck:
      if self.canMoveTo(x,y,color) and self.board[x][y] != ' ':
        if count: # if there is 2 (or more) pieces block the opponent's bishop(queen)'s way to the king, these pieces can move normally
          self.specMove.pop() 
          return 0 #stop

        #insert coordinations to the first
        self.specMove[-1].insert(0,[x,y])

        #count pieces which block the way to the king
        count+=1 

      elif not self.canMoveTo(x,y,color) and (x!=self.r or y!=self.c):
        self.specMove.pop()
        return 0
      
      # append special move
      self.specMove[-1].append([x,y])

      # change position
      x+=addX
      y+=addY
    # if there is no piece(checkmate), delete it
    if not count:
      self.specMove.pop()
      return 0
    
  def funcRock(self,z,king): #similar to funcBishop
    self.specMove.append([])
    count = 0
    addX,addY = 0,0
    
    if self.rk > self.r: addX = 1
    elif self.rk < self.r: addX = -1
    elif self.ck > self.c: addY = 1
    else: addY = -1
    
    x,y = self.r,self.c

    while (x!=self.rk and addX) or (y!=self.ck and addY):
      if self.canMoveTo(x,y,z) and self.board[x][y] != ' ':

        if count:
          self.specMove.pop()
          return 0

        self.specMove[-1].insert(0,[x,y])
        count+=1

      elif not self.canMoveTo(x,y,z) and (x!=self.r or y!=self.c):
        self.specMove.pop()
        return 0

      self.specMove[-1].append([x,y])

      x += addX
      y += addY

    if not count:
      self.specMove.pop()
      return 0
    
  def pawnDanger(self,row,col,color): # dangerous square for opponent's king
    if self.canMoveTo(row,col,color^1) or self.board[row][col] == ' ': self.danger[row][col] = 1
      
  def knightDanger(self,dg): # dangerous square for opponent's king
    for i in dg:
      if 0<i[0]<=8 and 0<i[1]<=8: self.danger[i[0]][i[1]] = 1     

  def kingDanger(self,dg): # dangerous square for opponent's king
    for i in dg:
      if 0<i[0]<=8 and 0<i[1]<=8: self.danger[i[0]][i[1]] = 1

  def validDanger(self,danList,color,king,addX,addY):# similar to 'valid' function
    for i in range(len(danList)):
      if self.BW(self.board[danList[i][0]][danList[i][1]]) == color:
        if self.find(king) == danList[i]:
          try:
            self.danger[danList[i][0] + addX][danList[i][1] + addY] = 1
          except:
            pass
        return
      elif self.BW(self.board[danList[i][0]][danList[i][1]]) == color ^ 1:
        self.danger[danList[i][0]][danList[i][1]] = 1
        return
      self.danger[danList[i][0]][danList[i][1]] = 1
      
  def queenRockDanger(self,z,king): # dangerous square for opponent's king
    x,y = self.row,self.col
    move1,move2,move3,move4 = self.queenRockRule()
    self.validDanger(move1,z,king,1,0)
    self.validDanger(move2,z,king,0,1)
    self.validDanger(move3,z,king,-1,0)
    self.validDanger(move4,z,king,0,-1)
    
  def queenBishopDanger(self,z,king):# dangerous square for opponent's king
    x,y = self.row,self.col
    move1,move2,move3,move4 = self.queenBishopRule()
    self.validDanger(move1,z,king,1,1)
    self.validDanger(move2,z,king,-1,1)
    self.validDanger(move3,z,king,1,-1)
    self.validDanger(move4,z,king,-1,-1)

  def inCheckWay(self,x):# a piece, whose king is being checked, must has the ablity to move to a square which is in checkmate way to move
    for check in self.checkWay:
      if x in check:
        return True
    return False

  def canNotMove(self): #check if all pieces on the board cannot move anymore (draw)
    for choice in self.choice:
      if len(choice) != 1:
        return False
    return True

  def inSpecMove(self,row,col): #check if the piece at row,col has special moves
    for i in range(len(self.specMove)):
      if [row,col] == self.specMove[i][0]:
        return i+1
    return 0

  def draw(self):#check draw
    count = 0
    for i in range(1,9):
      for j in range(1,9):
        if self.board[i][j] not in [self.WKING,self.BKING,self.WKNIGHT,self.WBISHOP,self.BKNIGHT,self.BBISHOP,' ']: #1 side can win if it has any piece not in this list
          return False
        if self.board[i][j] != ' ': #count pieces
          count += 1
    return count < 4 # if there is only 2 or 3 piece left (include 2 kings), game draw

  def choiceGen(self,no):
    #generate legal moves
    self.num,self.choice = -1,[]
    for self.row in range(1,9):
      for self.col in range(1,9):
        val = self.board[self.row][self.col]
        if val == [self.WPAWN,self.BPAWN][no]: 
          self.num+=1
          self.choice.append([[self.row,self.col]])
          
          #move forward 1 square
          if self.row+[-1,1][no] in range(1,9) and self.board[self.row+[-1,1][no]][self.col] == ' ':
            self.choice[self.num].append([self.row+[-1,1][no],self.col])
            
            #move forward 2 squares
            if self.row == [7,2][no]:
              if self.board[self.row+[-2,2][no]][self.col] == ' ':
                self.choice[self.num].append([self.row+[-2,2][no],self.col])
                
          # check if can capture
          if self.col > 1 and [self.row<8,self.row>1][no^1]:
            self.pawnMove(self.row+[-1,1][no],self.col-1,no)
          if self.col < 8 and [self.row<8,self.row>1][no^1]:
            self.pawnMove(self.row+[-1,1][no],self.col+1,no)
            
          # en passant move
          if self.row == [4,5][no] and self.enPassant and abs(self.enPassantCol - self.col) == 1:
            self.choice[self.num].append([[3,6][no],self.enPassantCol])
        elif val == [self.WKNIGHT,self.BKNIGHT][no]:
          self.num+=1
          self.choice.append([[self.row,self.col]])
          self.choice[self.num].extend(self.knightMove([[self.row+1,self.col+2],[self.row-1,self.col+2],[self.row+1,self.col-2],[self.row-1,self.col-2],[self.row-2,self.col-1],[self.row+2,self.col-1],[self.row-2,self.col+1],[self.row+2,self.col+1]],no))
        elif val == [self.WROCK,self.BROCK][no]:
          self.num+=1
          self.choice.append([[self.row,self.col]])
          self.queenRockMove(no,[self.BKING,self.WKING][no])
        elif val == [self.WBISHOP,self.BBISHOP][no]:
          self.num+=1
          self.choice.append([[self.row,self.col]])
          self.queenBishopMove(no,[self.BKING,self.WKING][no])
        elif val == [self.WQUEEN,self.BQUEEN][no]:
          self.num+=1
          self.choice.append([[self.row,self.col]])
          self.queenRockMove(no,[self.BKING,self.WKING][no])
          self.queenBishopMove(no,[self.BKING,self.WKING][no])
        elif val == [self.WKING,self.BKING][no]:
          self.num+=1
          self.choice.append([[self.row,self.col]])

          #castling
          if not self.checkMate and not [self.wKMoved,self.bKMoved][no]:
            #if king side rock was not moved and king was not moved too, player can make the castle move
            if [self.wKingSideCastle,self.bKingSideCastle][no] and self.danger[[8,1][no]][6] == 0 and self.danger[[8,1][no]][7] == 0 and self.board[[8,1][no]][6] == ' ' and self.board[[8,1][no]][7] == ' ' and self.board[[8,1][no]][8] == [self.WROCK,self.BROCK][no]:
              self.choice[self.num].append([[8,1][no],7])

            #if queen side rock was not moved and king was not moved too, player can make the castle move
            if [self.wQueenSideCastle,self.bQueenSideCastle][no] and self.danger[[8,1][no]][4] == 0 and self.danger[[8,1][no]][3] == 0 and self.board[[8,1][no]][4] == ' ' and self.board[[8,1][no]][3] == ' ' and self.board[[8,1][no]][1] == [self.WROCK,self.BROCK][no]:
              self.choice[self.num].append([[8,1][no],3])
          i,j = self.row,self.col
          self.choice[self.num].extend(self.kingMove([[i+1,j],[i-1,j],[i+1,j+1],[i-1,j+1],[i+1,j-1],[i-1,j-1],[i,j+1],[i,j-1]],no))
          
        #special moves
        if self.inSpecMove(self.row,self.col) and self.canMoveTo(self.row,self.col,[1,0][no]) and self.board[self.row][self.col] != ' ':
          templist = []
          for i in self.choice[self.num]:
            if i in self.specMove[self.inSpecMove(self.row,self.col) - 1]:
              templist.append(i)
          self.choice[self.num] = templist.copy()
          
    #remove illegal moves
    for c in range(len(self.choice)):
      length = len(self.choice[c])
      k = 1
      while k < length:
        if (self.checkMate and not self.inCheckWay([self.choice[c][k][0],self.choice[c][k][1]]) and self.board[self.choice[c][0][0]][self.choice[c][0][1]] != [self.WKING,self.BKING][no]):
          del self.choice[c][k]
          k-=1
        length = len(self.choice[c])
        k+=1

  def find(self,piece):#return the position of a piece
    for i in range(1,9):
      for j in range(1,9):
        if self.board[i][j] == piece:
          return [i,j]
  evaluated = 0

  def maxi(self,depth):#for computer, minimax algorithm
    if depth == 0:
      return evaluate(self.board)
    bestVal = 99999
    checkRes = self.generateMoves()

    if checkRes == 'win':
      print('hoho')
      return 99999
    elif checkRes == 'draw':
      return 0
    #temporary
    t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14 = self.bKMoved,self.wKMoved,self.bQueenSideCastle,self.bKingSideCastle,self.wQueenSideCastle,self.wKingSideCastle,copy.deepcopy(self.choice),self.enPassantCol,self.enPassant,copy.deepcopy(self.board),self.wC,self.checkMate,self.countDown,copy.deepcopy(self.checkWay)
    for i in t7:
      for j in range(1,len(i)):
        row,col,rowt,colt = i[0][0],i[0][1],i[j][0],i[j][1]
        self.evaluated += 1
        self.makeAMove(row,col,rowt,colt,False)
        point = self.mini(depth-1)
        if point == 99999:
          print(row,col,rowt,colt,bestVal)
        if point == bestVal:
          if depth == self.maxDepth:
            self.canmove.append([row,col,rowt,colt])
        elif point < bestVal:
          bestVal = point
          if depth == self.maxDepth:
            self.canmove = [[row,col,rowt,colt]]
        self.currentTurn ^= 1
        #restore
        self.bKMoved,self.wKMoved,self.bQueenSideCastle,self.bKingSideCastle,self.wQueenSideCastle,self.wKingSideCastle,self.choice,self.enPassantCol,self.enPassant,self.board,self.wC,self.checkMate,self.countDown,self.checkWay = t1,t2,t3,t4,t5,t6,copy.deepcopy(t7),t8,t9,copy.deepcopy(t10),t11,t12,t13,copy.deepcopy(t14)
    return bestVal
  
  def mini(self,depth):#for computer, minimax algorithm
    if depth == 0:
      return evaluate(self.board)
    bestVal = -99999
    checkRes = self.generateMoves()
    if checkRes =='win':
      self.displayBoard()
      print('HO ho')
      return -99999
    elif checkRes == 'draw':
      return 0
    t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14 = self.bKMoved,self.wKMoved,self.bQueenSideCastle,self.bKingSideCastle,self.wQueenSideCastle,self.wKingSideCastle,copy.deepcopy(self.choice),self.enPassantCol,self.enPassant,copy.deepcopy(self.board),self.wC,self.checkMate,self.countDown,copy.deepcopy(self.checkWay)
    for i in t7:
      for j in range(1,len(i)):
        row,col,rowt,colt = i[0][0],i[0][1],i[j][0],i[j][1]
        self.evaluated += 1
        self.makeAMove(row,col,rowt,colt,False)
        point = self.maxi(depth-1)
        if point == bestVal:
          if depth == self.maxDepth:
            self.canmove.append([row,col,rowt,colt])
        elif point > bestVal:
          bestVal = point
          if depth == self.maxDepth:
            self.canmove = [[row,col,rowt,colt]]
        self.currentTurn ^= 1
        self.bKMoved,self.wKMoved,self.bQueenSideCastle,self.bKingSideCastle,self.wQueenSideCastle,self.wKingSideCastle,self.choice,self.enPassantCol,self.enPassant,self.board,self.wC,self.checkMate,self.countDown,self.checkWay = t1,t2,t3,t4,t5,t6,copy.deepcopy(t7),t8,t9,copy.deepcopy(t10),t11,t12,t13,copy.deepcopy(t14)
    return bestVal

  def dangerGen(self,no):#this will generate list of squares which king cannot move to
    for i in range(1,9):
      for j in range(1,9):
        self.danger[i][j] = 0
    for self.row in range(1,9):
      for self.col in range(1,9):
        val = self.board[self.row][self.col]
        row,col = self.row,self.col
        if val == [self.WKING,self.BKING][no]:
          #8 squares around the king
          self.kingDanger([[row+1,col+1],[row-1,col+1],[row+1,col-1],[row-1,col-1],[row-1,col],[row+1,col],[row,col+1],[row,col-1]])
        elif val == [self.WPAWN,self.BPAWN][no]:
          if col > 1 and [row>1,row<8][no]:
            self.pawnDanger(row+[-1,1][no],col-1,no)
          if col < 8 and [row>1,row<8][no]: 
            self.pawnDanger(row+[-1,1][no],col+1,no)
        elif val == [self.WKNIGHT,self.BKNIGHT][no]:
          #8 squares around the knight
          self.knightDanger([[row+1,col-2],[row-1,col-2],[row+1,col+2],[row-1,col+2],[row+2,col+1],[row-2,col+1],[row+2,col-1],[row-2,col-1]])
        elif val == [self.WROCK,self.BROCK][no]:
          self.queenRockDanger(no,[self.WKING,self.BKING][no^1])
        elif val == [self.WBISHOP,self.BBISHOP][no]:
          self.queenBishopDanger(no,[self.WKING,self.BKING][no^1])
        elif val == [self.WQUEEN,self.BQUEEN][no]:
          self.queenRockDanger(no,[self.WKING,self.BKING][no^1])
          self.queenBishopDanger(no,[self.WKING,self.BKING][no^1])
          
  def checkMateCheck(self,no):#check if the king is being checked
    self.checkWay = []
    for i in self.choice:
      for j in range(1,len(i)):
        #piece can move to i[j][0],i[j][1]
        self.rc,self.cc = i[j][0],i[j][1]

        #check if an opponent's piece is checking the king
        if self.board[self.rc][self.cc] == [self.BKING,self.WKING][no]:
          #position of the piece which is checking the king
          self.r,self.c = i[0][0],i[0][1]

          #val is that piece
          val = self.board[self.r][self.c]
          
          self.checkMate = True
          self.checkWay.append([[self.r,self.c]])

          if val == [self.WROCK,self.BROCK][no]:
            self.checkMateRock()
          elif val == [self.WBISHOP,self.BBISHOP][no]:
            self.checkMateBishop()
          elif val == [self.WQUEEN,self.BQUEEN][no]:
            self.checkMateRock()
            self.checkMateBishop()
            
  def specMoveGen(self,no,king):#special move
    #find position of the king
    self.rk,self.ck  = self.find(king)
    self.specMove = []
    
    for i in range(1,9):
      for j in range(1,9):
        if self.board[i][j] == [self.WBISHOP,self.BBISHOP][no]:
          if abs(i-self.rk) == abs(j-self.ck):
            self.r,self.c = i,j
            self.funcBishop(no,king)
        elif self.board[i][j] ==[self.WROCK,self.BROCK][no]:
          if i == self.rk or self.ck == j:
            self.r,self.c = i,j
            self.funcRock(no,king)
        elif self.board[i][j] == [self.WQUEEN,self.BQUEEN][no]:
          if abs(i-self.rk) == abs(j-self.ck):
            self.r,self.c = i,j
            self.funcBishop(no,king)
          if i == self.rk or self.ck == j:
            self.r,self.c = i,j
            self.funcRock(no,king)
            
  def generateMoves(self): # generate moves and do everything else
      self.dangerGen(self.currentTurn)
      self.specMoveGen(self.currentTurn,[self.BKING,self.WKING][self.currentTurn])
      self.choiceGen(self.currentTurn ^ 1)
      self.checkMateCheck(self.currentTurn ^ 1)
      self.dangerGen(self.currentTurn ^ 1)
      self.specMoveGen(self.currentTurn ^ 1,[self.BKING,self.WKING][self.currentTurn^1])
      self.choiceGen(self.currentTurn)
      checkRes = self.checkState(self.currentTurn ^ 1)
      if checkRes != None:
        return checkRes
      return self.choice
      
  def checkState(self,no):#check if draw,win,...
      # return 'draw','win' and 'checkmate'
      canMove = []
      if self.checkMate:
          for i in self.choice:
              for j in i:
                  length = len(self.checkWay)
                  k = 0
                  while k < length:
                      if j in self.checkWay[k] and self.board[i[0][0]][i[0][1]] != [self.BKING,self.WKING][no]:
                          canMove.append([i[0][0],i[0][1]])
                          break
                      elif self.board[i[0][0]][i[0][1]] == [self.BKING,self.WKING][no]:
                          if len(i) != 1:
                              canMove.append([i[0][0],i[0][1]]) 
                          break
                      k+=1
      if len(canMove) != 0 and not len(self.checkWay) >= 2:
        self.checkMate = False
        return 'checkmate'
      if len(self.checkWay) >= 2 and self.checkMate:
          for i in range(1,9):
              for j in range(1,9):
                  if self.board[i][j] == [self.BKING,self.WKING][no]:
                    if len(self.choice[self.findPos(i,j)]) == 1:
                      break

                    #only king can move
                    choice = self.choice[self.findPos(i,j)]
                    self.choice = [[]]
                    for i in choice:
                      self.choice[0].append(i)
                    
                    self.checkMate = False
                    return 'checkmate'
      if self.checkMate:
          return 'win'
      elif self.canNotMove() or not self.countDown or self.draw():
          return 'draw'

  def makeAMove(self,row=0,col=0,rowt=0,colt=0,saveToHistory = True):#move
    '''
    if type(row) == str:
      if row not in self._moves:
        print('Illegal Move! Please try again')
        return
      row,col,rowt,colt = self.toNumber(row)
    else:
      if self.toNotation(row,col,rowt,colt) not in self._moves:
        print('Illegal Move! Please try again')
        return
    '''
    no = 0
    if self.currentTurn == self.WHITE:
        no = 1
        
    #en passant move
    if self.board[row][col] == [self.BPAWN,self.WPAWN][no] and rowt == [6,3][no] and colt == self.enPassantCol and self.enPassant:
        self.board[[5,4][no]][self.enPassantCol] = ' '
        
    #castle
    if self.board[row][col] == [self.BKING,self.WKING][no] and abs(colt-col) == 2:
        self.board[[1,8][no]][1+(colt>col)*7] = ' '
        self.board[[1,8][no]][4+(colt>col)*2] = [self.BROCK,self.WROCK][no]

    #reset en passant
    self.enPassant = False

    #for castling
    if self.board[row][col] == [self.BROCK,self.WROCK][no]:
        if row == [1,8][no] and col == 8:
            #king side rock is moved
            if not no:
                self.bKingSideCastle = False
            else:
                self.wKingSideCastle = False
        elif row == [1,8][no] and col == 1:
            #queen side rock is moved
            if not no:
                self.bQueenSideCastle = False
            else:
                wQueenSideCastle = False
    elif self.board[row][col] == [self.BKING,self.WKING][no]:
        #king is moved
        if not no:
            self.bKMoved = True
        else:
            self.wKMoved = True
    elif self.board[row][col] == [self.BPAWN,self.WPAWN][no] and row == [2,7][no] and rowt == [4,5][no]:
        #en passant
        self.enPassant = True
        self.enPassantCol = col
        
    #50 moves rule
    if self.board[rowt][colt] == ' ' and self.board[row][col] != [self.WPAWN,self.BPAWN][no]:
        self.countDown -= 1
    else:
        self.countDown = 50
        
    #move from row,col to rowt,colt
    self.board[rowt][colt] = self.board[row][col]
    self.board[row][col] = ' '

    #temporarily promote pawn
    if rowt == [8,1][no] and self.board[rowt][colt] == [self.BPAWN,self.WPAWN][no]:
        self.board[rowt][colt] == [self.BQUEEN,self.WQUEEN][no]
        
    #save position for the future purpose
    if saveToHistory:
      self.match.append(state())
      self.match[-1].set(copy.deepcopy(self.board),[self.wKMoved,self.bKMoved,self.bKingSideCastle,self.bQueenSideCastle,self.wKingSideCastle,self.wQueenSideCastle,self.enPassant,self.enPassantCol,self.countDown])
      count = 0

      #3 fold repetition check
      for i in range(1,len(self.match)-2):
        if self.match[i].get()[0] == self.board and self.match[i].get()[1][2:8] == [self.bKingSideCastle,self.bQueenSideCastle,self.wKingSideCastle,self.wQueenSideCastle,self.enPassant,self.enPassantCol]:
          count+=1
          if count == 2:
            return 'draw'

    #change turn
    self.currentTurn ^= 1
    
  def initBoard(self,Board = None): #init board
    if Board:
      self.board = copy.deepcopy(Board)
    else:
      self.board = copy.deepcopy(self.originalBoard)
    self.match.clear()
    self.match.append(state())
    self.match[0].set(self.board,[self.wKMoved,self.bKMoved,self.bKingSideCastle,self.bQueenSideCastle,self.wKingSideCastle,self.wQueenSideCastle,self.enPassant,self.enPassantCol,self.countDown])

  def undo(self):
    if len(self.match) != 1:
      #change turn first
      self.currentTurn = not self.currentTurn

      #delete the lastest position
      self.match.pop()

      #undo
      self.wKMoved,self.bKMoved,self.bKingSideCastle,self.bQueenSideCastle,self.wKingSideCastle,self.wQueenSideCastle,self.enPassant,self.enPassantCol,self.countDown = self.match[-1].get()[1]
      self.board = copy.deepcopy(self.match[-1].get()[0])
    #generate new moves for the new position
    self.generateMoves()
    
  def restore(self):
    #restore to play again
    self.checkMate = False
    self.bQueenSideCastle,self.bKingSideCastle,self.wQueenSideCastle,self.wKingSideCastle = True,True,True,True
    self.enPassant,self.enPassantCol = False,0
    self.wKMoved,self.bKMoved = False,False
    self.choice,self.cantMove,self.specMove,self.match = [],[],[],[]
    self.match.append(state())
    self.countDown = 50
    self.num = -1
    self.rowt,self.colt,self.row,self.col,self.c,self.r,self.rc,self.cc,self.rk,self.ck = 0,0,0,0,0,0,0,0,0,0
    self.board = copy.deepcopy(self.originalBoard)
    self.match[0].set(self.board,[self.wKMoved,self.bKMoved,self.bKingSideCastle,self.bQueenSideCastle,self.wKingSideCastle,self.wQueenSideCastle,self.enPassant,self.enPassantCol,self.countDown])

  def displayBoard(self):
    #print characters board
    pieces = ['b','B','r','R','n','N','p','P','k','K','q','Q']
    for i in range (9):
      for j in range(9):
        if type(self.board[i][j]) == int:
          print(pieces[self.board[i][j]],end = ' ')
        else:
          if self.board[i][j] == ' ':
            print('_',end = ' ')
            continue
          print(self.board[i][j],end = ' ')
      print()

  def toNotation(self,a,b,c,d):
    return chr(b+96)+chr(9-a+48)+chr(d+96)+chr(9-c+48)

  def toNumber(self,notation):
    return [-ord(notation[1])+48+9,ord(notation[0])-96,-ord(notation[3])+48+9,ord(notation[2])-96]
  
  def legalMoves(self):
    temp = self.generateMoves()
    if type(temp) != list:
      self._isEndGame = temp
      return temp
    moves = []
    for move in self.choice:
      for i in range(1,len(move)):
        moves.append(self.toNotation(move[0][0],move[0][1],move[i][0],move[i][1]))
    self._moves = copy.deepcopy(moves)
    return moves

  def gameState(self):
    return self._isEndGame
  
  def computerMove(self,depth = 3):
    self.wC = 0
    self.maxDepth = depth
    self.legalMoves()
    if self.currentTurn:
      self.maxi(depth)
    else:
      self.mini(depth)
    return self.canmove
