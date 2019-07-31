#GUI for chess

#Author: Le Tuan Hoang
#Email: hoangdeptoong@gmail.com


#import
import engine,copy,time,os,random
from tkinter import *
from math import floor,ceil
from functools import partial
from datetime import datetime
try:
    from PIL import ImageTk,Image
except:
    os.system('pip install pillow')

#Initialize window
root = Tk()
root.title('Chess Game')
canvas = Canvas(root)
canvas.pack()

#canvas.create_image(0,0,image = ImageTk.PhotoImage(Image.open('Image\\BackGround.png')))
frame = Frame()
frame.pack()

#Small square
class square():
    def __init__(self):
        self.row = 0
        self.col = 0
        self.FILE = 0
        self.obj = 0

    def setRowCol(self,row,col):
        #set coordinations
        self.row = row
        self.col = col

        #image file
        self.FILE = ImageTk.PhotoImage(Image.open(self.obj.listFile[abs(row%2-col%2)^1]).resize((self.obj.squareSize,self.obj.squareSize),Image.ANTIALIAS))

        #create image
        self.Image()

    def Image(self):
        canvas.create_image(self.obj.squareSize*self.col,self.obj.squareSize*self.row, image = self.FILE,activeimage = self.obj.AFile)
        if self.obj.game.board[self.row][self.col] != ' ':
            canvas.create_image(self.obj.squareSize*self.col,self.obj.squareSize*self.row,image = self.obj.PiecesFile[self.obj.game.board[self.row][self.col]],activeimage = self.obj.APieces[self.obj.game.board[self.row][self.col]])

    def setObject(self,obj):
        self.obj = obj

class chessGame():
    def __init__(self):
        self.game = engine.chess()
        self.Board = []
        self.window = 0

        #Images
        self.listFile = ['Image\\SquareGrey.gif','Image\\SquareWhite.gif']
        self.AFile = ImageTk.PhotoImage(Image.open('Image\\SquareActive.gif'))
        self.PiecesFileName = ['BishopBlack','BishopWhite','RockBlack','RockWhite','KnightBlack','KnightWhite','PawnBlack','PawnWhite','KingBlack','KingWhite','QueenBlack','QueenWhite']
        self.PiecesFile = [ImageTk.PhotoImage(Image.open('Image\\' +  i+'.gif')) for i in self.PiecesFileName] 
        self.APieces = [ImageTk.PhotoImage(Image.open('Image\\'+ i+'Act.gif')) for i in self.PiecesFileName]
        
        self.last = []
        self.result = [0,0]
        
        self.promoted = True
        self.isEndGame = False
        self.comPlayer = False
        self.screenState = False
        
        self.lastClickedRow,lastClickedCol = -1,-1
        self.checkedRow,self.checkedCol = 0,0

        self.filename = 0
        self.savedName = ''
        self.saved = True
        self.puzzle = False
        
        self.scrollbar = Scrollbar(root)
        self.scrollbar.pack(side = RIGHT,fill = Y)

        self.squareSize = 91

        self.backGroundImage = ImageTk.PhotoImage(Image.open('Image\\BackGround.png').resize((root.winfo_screenwidth(),root.winfo_screenheight()),Image.ANTIALIAS))

        root.state('zoomed')
        root.bind('<F11>',partial(self.toggleFullScreen,root))

        self.menu()
        self.autoResizeSquare()
        
    def toggleFullScreen(self,root,event):
        self.screenState = not self.screenState
        root.attributes('-fullscreen',self.screenState)

    def backGround(self):
        Label(root,image = self.backGroundImage).place(x = 0,y = 0,relwidth=1,relheight = 1)

    def menu(self):
        global frame,canvas
        root.protocol('WM_DELETE_WINDOW',root.destroy)
        #clear everything
        self.clear()

        #initialize background
        self.backGround()

        #initialize canvas
        canvas = Canvas()
        canvas.pack()
        canvas.config(height = 0)

        IMAGE = ImageTk.PhotoImage(Image.open('Image\\ChessWord2.png'))
        chess = Label(root,image = IMAGE)
        chess.image = IMAGE
        chess.pack()

        img = ImageTk.PhotoImage(Image.open('Image\\chessGameIcon.jpg'))
        label = Label(root,image = img)
        label.image = img
        label.pack()

        img2 = ImageTk.PhotoImage(Image.open('Image\\NewGameButton.png'))
        img3 = ImageTk.PhotoImage(Image.open('Image\\LoadGameButton.png'))
        img4 = ImageTk.PhotoImage(Image.open('Image\\PuzzlesButton.png'))
        img5 = ImageTk.PhotoImage(Image.open('Image\\HowToPlayButton.png'))

        b1 = Button(root,image = img2,command = self.newGame,bd=0,highlightthickness=0)
        b1.image = img2
        b1.pack(pady=10)

        b2 = Button(root,image = img3,command = self.loadGame,bd = 0,highlightthickness = 0)
        b2.image = img3
        b2.pack()

        b3 = Button(root,image = img4,command = self.loadPuzzle,bd = 0,highlightthickness = 0)
        b3.image = img4
        b3.pack(pady=10)

        b4 = Button(root,image = img5,command = self._howToPlay,bd = 0,highlightthickness = 0)
        b4.image = img5
        b4.pack(pady=10)
        
    def _howToPlay(self):
        #new window to show 'How to play'
        root = Toplevel(height = 600,width = 800)

        #full screen
        root.state('zoomed')

        #press F11 -> full screen
        root.bind('<F11>',partial(self.toggleFullScreen,root))

        #number of pages
        num = len(os.listdir('data\\howtoplay'))
        
        self.howToPlay(1,root,num)
        
    def valid(self,no,num):
        #page validator, if page < 1, go to last page
        if no<1:
            return num
        elif no>num:
            return 1
        return no
    
    def howToPlay(self,page,root,num):
        #clear all
        for widget in root.winfo_children():
            widget.destroy()

        #2 buttons
        lButton = ImageTk.PhotoImage(Image.open('Image\\LeftButton.png'))
        rButton = ImageTk.PhotoImage(Image.open('Image\\RightButton.png'))
        
        lB = Button(root,image = lButton,command = partial(self.howToPlay,self.valid(page-1,num),root,num))
        lB.image = lButton
        lB.place(x=0,y=0)
        
        rB = Button(root,image = rButton,command = partial(self.howToPlay,self.valid(page+1,num),root,num))
        rB.image = rButton
        rB.place(x=root.winfo_screenwidth()-34,y=0)

        #open file
        file = open('data\\howtoplay\\page'+str(page)+'.txt')

        #current page
        Label(root,text = str(page)+'/'+str(num),font = ('Comic Sans MS',17,'bold')).pack()
        text = file.readline()
        frame = 0

        #start read
        while text != 'END' and text != 'END\n':
            #dat list may contain format, text, path to image
            dat = text.split(';')

            #if this is image
            if dat[0] == 'IMAGE':
                img = ImageTk.PhotoImage(Image.open(dat[1][0:len(dat[1])-1]))
                lb  = 0
                if len(dat) == 3:
                    #frame
                    lb = Label(frame,image = img)
                else:
                    #root
                    lb = Label(root,image = img)

                lb.image = img
                
                if len(dat) != 3:
                    lb.pack()
                else:
                    #pack label
                    if dat[2] == 'FRAME_LEFT':
                        lb.pack(side = LEFT)
                    else:
                        lb.pack(side = RIGHT)
            elif dat[0] == 'INIT_FRAME\n':
                #create frame
                frame = Frame(root)
                frame.pack()
            elif dat[0] == 'ENDL\n':
                #end line
                self.createLabel(12,'normal',W,'',root)
            else:
                #normal text
                self.createLabel(int(dat[0]),dat[1],dat[2],dat[3][0:len(dat[3])-1],root)
            text = file.readline()
        file.close()
        self.centre(root)
        
    def createLabel(self,Size,Type,Anchor,Text,Root):
        Label(Root,text = '   '+Text,font = ('Comic Sans MS',Size,Type),wraplength = Root.winfo_screenwidth()).pack(anchor = Anchor)
        
    def newGame(self):
        global canvas
        global frame

        #clear and init background
        self.clear()
        self.backGround()

        #choose mode
        Label(root,text = 'Choose your mode!',font = ('Comic Sans MS',20,'normal')).pack(side= TOP)
        img2 = ImageTk.PhotoImage(Image.open('Image\\HumanVSHuman.png'))
        img3 = ImageTk.PhotoImage(Image.open('Image\\HumanVSComputer.png'))
        b1 = Button(root,image = img2,command = self.humanMode)
        b1.image = img2
        b1.pack(pady=20)
        b2 = Button(root,image = img3,command = self.computerMode)
        b2.image = img3
        b2.pack()

        #home button to return to menu
        img = ImageTk.PhotoImage(Image.open('Image\\HomeButton.png'))
        bt = Button(root,image = img,command = self._menu)
        bt.image = img
        bt.place(x = 0,y = 0)

    def clear(self):
        # clear all widgets
        for widget in root.winfo_children():
            widget.destroy()

    def humanMode(self):
        self.comPlayer = False
        self.startGame()

    def computerMode(self):
        self.comPlayer = True
        self.startGame()
        
    def startGame(self,res = True,reset = True):
        global canvas
        #set variables
        self.checkedCol,self.checkRow = 0,0
        self.isEndGame = False
        self.saved = True
        self.Retry = False
        self.last = []
        self.result = [0,0]
        
        if reset:
            #new game
            self.game.currentTurn = self.game.WHITE
        if self.savedName == '' and res:
            self.puzzle = False
            self.game.restore()
        else:
            self.puzzle = True

        #ask to save game when close 
        root.protocol('WM_DELETE_WINDOW',partial(self.exitGame,True))

        #clear all and init background
        self.clear()
        self.backGround()

        #resize to fit the screen
        self.autoResizeSquare()
        
        #canvas
        canvas = Canvas(height = self.squareSize * 9,width = self.squareSize * 9)
        canvas.pack()
        canvas.delete('all')
        canvas.config(height=root.winfo_screenheight(),width=root.winfo_screenheight(),bg = 'green')
        canvas.bind('<Button-1>',self.clicked)

        #new game
        if reset:
            self.game.initBoard()
        self.game.generateMoves()

        #display board
        self.display()

        #some button
        frame = Frame()
        img = ImageTk.PhotoImage(Image.open('Image\\HomeButton.png'))
        img2 = ImageTk.PhotoImage(Image.open('Image\\UndoButton.png'))
        img3 = ImageTk.PhotoImage(Image.open('Image\\SettingsButton.png'))
        
        bt = Button(root,image = img,command = self._menu)
        bt.image = img
        bt.place(x = 0,y = 0)
        
        bt = Button(root,image = img2,command = self.undo)
        bt.image = img2
        bt.place(x = 0,y = 100)
        
        bt = Button(root,image = img3,command = self.settings)
        bt.image = img3
        bt.place(x = 0,y = 200)

        # choose difficulty
        if self.comPlayer:
            ROOT = Toplevel(height = 120,width = 200)
            ROOT.protocol('WM_DELETE_WINDOW',self.nothing)
            self.centre(ROOT)
            
            Label(ROOT,text = 'Choose your difficulty!').pack()
            Button(ROOT,text = 'EASY',command = partial(self.setDif,1,ROOT)).pack()
            Button(ROOT,text = 'MEDIUM',command = partial(self.setDif,2,ROOT)).pack(pady=5)
            Button(ROOT,text = 'HARD',command = partial(self.setDif,3,ROOT)).pack()
            
            ROOT.grab_set()
            
    def settings(self):
        #new window
        ROOT = Toplevel(height = 260,width = 400)

        #move to centre
        self.centre(ROOT)

        #size setting
        Label(ROOT,text = 'SETTINGS',font = ('Comic Sans MS',20,'normal')).pack()
        Label(ROOT,text = 'SIZE',font = ('Comic Sans MS',15,'normal')).pack(anchor = NW,padx = 10)

        #checkbox 1, auto resize squares
        var1 = IntVar()
        checkbox1 = Checkbutton(ROOT,text = ' Auto',font = ('Comic Sans MS',15,'normal'),variable = var1)
        checkbox1.pack(anchor = NW,padx = 20)
        checkbox1.select()

        #checkbox 2, customize size
        var = IntVar()
        checkbox = Checkbutton(ROOT,text = ' Customise',font = ('Comic Sans MS',15,'normal'),variable = var)
        checkbox.pack(anchor = NW,padx = 20)

        frame = Frame(ROOT)
        frame.pack(anchor = NW,padx = 40)

        entry = Entry(frame)
        entry.pack(padx = 5,side = LEFT,pady = 5)
        entry.config(state = 'disabled')

        checkbox1.config(command = partial(self.toggle,checkbox,var1,entry))
        checkbox.config(command = partial(self.modifyEntry,var,checkbox1,entry))

        Label(frame,text = 'px',font = ('Comic Sans MS',10,'normal')).pack(side = LEFT)
        err = Label(ROOT,text = '')
        Button(ROOT,text = 'SAVE',font = ('Comic Sans MS',10,'normal'),command = partial(self.getSize,ROOT,entry,var1,err)).pack(pady = 5)
        err.pack()

    def modifyEntry(self,var,auto,entry):
        #enable or disable entry
        State = lambda x:['disabled','normal'][x]
        entry.config(state = State(var.get()))

        #modify auto checkbox
        if var.get():
            auto.deselect()
        else:
            auto.select()

    def getSize(self,ROOT,entry,var,err):
        size = 0
        self.lastClickedCol = -1
        if var.get():
            #auto
            ROOT.destroy()
            self.autoResizeSquare()
            canvas.config(width = self.squareSize * 9,height = self.squareSize * 9)
            canvas.delete('all')
            self.display()
            return

        #check if user's input is integer or not
        try:
            print(entry.get())
            size = int(entry.get())
        except ValueError:
            err.config(text = 'Must be an integer')
            return

        #A number which is smaller than 0 is not accepted            
        if type(size) != int or size <= 0:
            err.config(text = 'Must be an integer and bigger than 0!')
            return
        
        #customize size
        self.squareSize = size
        canvas.config(width = size*9,height = size*9)
        canvas.delete('all')
        self.resizeImage()
        self.display()
        ROOT.destroy()
        
    def toggle(self,customize,var,entry):
        if var.get():
            #user chose auto so deselect customize checkbox
            customize.deselect()
            #disable entry
            entry.config(state = 'disabled')
        else:
            #user chose deselect auto so select customize checkbox
            customize.select()
            #enable entry
            entry.config(state = 'normal')
        
    def undo(self):
        self.lastClickedCol,self.lastClickedRow = -1,-1
        self.game.undo()

        if self.comPlayer:
            # 2 times
            self.game.checkMate,self.game.checkWay = False,[]
            self.game.undo()

        #display board
        self.display()

    def setDif(self,dif,root):
        self.game.maxDepth = dif
        root.destroy()

    def _menu(self):
        self.exitGame(False)

    def exitGame(self,end):
        if self.saved:
            #if file is saved
            self.exit(end,False)
            return

        #if not, ask user
        self.window = Toplevel(height = 80,width = 500)
        self.window.title('Save?')
        self.centre(self.window)

        Label(self.window,text = 'Save game? (Unsaved data will be lost!)',font = ('Comic Sans MS',15,'normal')).pack()
        
        frame = Frame(self.window)
        frame.pack()
        
        Button(frame,text = 'Yes',command = partial(self.saveGame,end),width = 10,font = ('Comic Sans MS',10,'normal')).pack(side = LEFT,padx = 5)
        Button(frame,text = 'No',command = partial(self.exit,end),width = 10,font = ('Comic Sans MS',10,'normal')).pack(side = RIGHT,padx = 5)

    def saveGame(self,end):
        #check if path was created. If not, create new
        try:
            os.makedirs('data\saved')
        except:
            pass
        
        i = 1
        file = None
        if self.savedName == '':
            #if user plays new game, create new save file
            while os.path.exists('data\\saved\\saved'+str(i)+'.sav'):
                i+=1
            file = open('data\\saved\\saved'+str(i)+'.sav','w+')
        else:
            #if user opens game from saved list, overwrite it
            file = open('data\\saved\\'+self.savedName,'w+')

        #data which need to be written
        writeData = ''
        writeData += ['w','b'][self.game.currentTurn]+';'
        writeData += str(int(self.comPlayer))+';'
        writeData += str(int(self.game.wKMoved))+';'
        writeData += str(int(self.game.bKMoved))+';'
        writeData += str(int(self.game.bQueenSideCastle))+';'
        writeData += str(int(self.game.bKingSideCastle))+';'
        writeData += str(int(self.game.wQueenSideCastle))+';'
        writeData += str(int(self.game.wKingSideCastle))+';'
        writeData += str(int(self.game.enPassant))+';'
        writeData += str(int(self.game.enPassantCol))+';'
        
        for i in range(1,9):
            for j in range(1,9):
                if self.game.board[i][j] != ' ':
                    writeData += str(self.game.board[i][j])+'.'+str(i)+'.'+str(j)+';'

        #saved time
        writeData+='\n'+str(datetime.now())
        
        file.write(writeData)
        file.close()

        #return to menu or exit
        if end:
            self.exit(end)
        else:
            self.menu()

    def loadPuzzle(self):
        #load a puzzle
        try:
            file = open('data\\puzzles\\puzzles.txt')
        except:
            pass
        
        ROOT = Toplevel(height = 200,width = 200)
        self.centre(ROOT)

        Label(ROOT,text = 'Double-click to play!').pack()

        frame = Frame(ROOT)
        frame.pack()

        sb = Scrollbar(frame)
        sb.pack(side = RIGHT,fill = Y)

        lb = Listbox(frame,yscrollcommand = sb.set)

        #display list of puzzles
        i=0
        with file as f:
            for line in f:
                lb.insert(END,'Puzzle '+str(i+1))
                i+=1
        sb.config(command = lb.yview)
        lb.pack(side = LEFT)

        #double-click to play
        lb.bind('<Double-Button-1>',partial(self._loadPuzzle,lb,'data\\puzzles\\sth.txt',ROOT))

    def _loadPuzzle(self,lb,FILE,root,event):
        index = lb.curselection()[0]
        data = 0

        #goto line 'index'
        file = open(FILE)
        with file as f:
            for i in range(index):
                f.readline()
            data = f.readline()

        #load puzzle
        self.load(data)
        file.close()
        
        root.destroy()
        self.startGame(False,False)

    def loadGame(self):
        #check if path is exist
        try:
            listFiles = os.listdir('data\\saved')
        except:
            self.openFileError()
            return
        
        self.window = Toplevel(height = 200,width = 370)
        self.centre(self.window)

        frame = Frame(self.window)
        frame.pack(side = LEFT,padx = 10)

        frame2 = Frame(self.window)
        frame2.pack(side = TOP)

        Label(frame,text = 'Saved games list').pack()
        Label(frame2,text = 'Choose saved game').pack()

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side = RIGHT,fill = Y)

        #list of saved games
        listbox = Listbox(frame,yscrollcommand = scrollbar.set)
        for filename in listFiles:
            listbox.insert(END,filename)

        t = Label(frame2,text = '')

        listbox.pack(side = LEFT)

        #show saved time by double-clicking
        listbox.bind('<Double-Button-1>',partial(self.description,listbox,t))

        scrollbar.config(command = listbox.yview)

        self.filename = Entry(frame2)
        self.filename.pack()

        x = Label(frame2,text = '')
        Button(frame2,text = 'Load',command = partial(self.openFile,frame2,x)).pack()
        x.pack()

        Label(frame2,text = 'Description(Double-click on name)').pack()

        t.pack()

    def description(self,lb,LB,event):
        #show time
        try:
            file = open('data\\saved\\'+lb.get(lb.curselection()[0]),'r')
            time=file.read()
            file.close()
            LB.config(text=time.split('\n')[1])
        except:
            #if there is nothing
            LB.config(text='Nothing to show!')

    def load(self,Data):
        data = Data.split(';')
        self.lastClickedCol,self.lastClickedRow = -1,-1

        #read turn
        if data[0] == 'w':
            self.game.currentTurn = self.game.WHITE
        else:
            self.game.currentTurn = self.game.BLACK

        #neccessary variables
        self.comPlayer = int(data[1])
        self.game.wKMoved = int(data[2])
        self.game.bKMoved = int(data[3])
        self.game.bQueenSideCastle = int(data[4])
        self.game.bKingSideCastle = int(data[5])
        self.game.wQueenSideCastle = int(data[6])
        self.game.wKingSideCastle = int(data[7])
        self.game.enPassant = int(data[8])
        self.game.enPassantCol = int(data[9])

        #load board
        board = []
        for i in range(0,9):
            board.append([])
            for j in range(0,9):
                board[i].append(' ')
        for i in data[10:len(data)-1]:
            x,y,z = i.split('.')
            board[int(y)][int(z)] = int(x)

        #init board
        self.game.initBoard(board)
        
    def openFile(self,frame,lb):
        filename = self.filename.get()

        #check if file is exist
        try:
            file = open('data\\saved\\'+filename,'r')
        except:
            lb.config(text = 'FILE NOT FOUND!',fg = 'red')
            return

        #user opened game from 'filename'
        self.savedName = filename
        
        try:
            self.load(file.read().split('\n')[0])
        except:
            self.openFileError()
            return

        self.saved = True

        self.startGame(reset = False)
        self.window.destroy()

    def openFileError(self):
        #cannot open file so reset board
        self.game.board = copy.deepcopy(self.game.originalBoard)

        self.window = Toplevel(height = 75,width = 500)
        self.centre(self.window)

        Label(self.window,text = 'Unable to open saved game! Click \'OK\' to play new game!',font = ('Comic Sans MS',14,'normal')).pack(pady = 5)
        Button(self.window,text = 'OK',font = ('Comic Sans MS',10,'normal'),width = 10,command = self._startGame).pack()

    def _startGame(self):
        self.window.destroy()
        self.startGame()

    def exit(self,end,popup = True):
        if popup:
            self.window.destroy()
        if end:
            root.destroy()
        else:
            self.menu()

    def clicked(self,event):
        if not self.promoted or self.isEndGame:
            return

        #x,y are the coordinations
        x = floor((event.x - self.squareSize/2)/self.squareSize)
        y = floor((event.y - self.squareSize/2)/self.squareSize)

        print(y,x)

        #if x,y are out of board, do nothing
        if  (x not in range(8) or y not in range(8)) or (self.lastClickedRow == y and self.lastClickedCol == x):
            return

        #if x,y in list of available move
        if [y,x] in self.last:
            #file is not saved
            self.saved = False
            
            no = 1
            if self.game.currentTurn == self.game.BLACK:
                no = 0

            #check for promoting
            if y+1 == [8,1][no] and self.game.board[self.lastClickedRow+1][self.lastClickedCol+1] == [self.game.BPAWN,self.game.WPAWN][no] :
                self.promote(y+1,x+1,self.lastClickedRow+1,self.lastClickedCol+1)
                self.promoted = False
                return

            #move
            self.Next(self.lastClickedRow+1,self.lastClickedCol+1,y+1,x+1)
            return

        #clicked
        self.Board[y][x].FILE = ImageTk.PhotoImage(Image.open('Image\\SquareClicked.gif').resize((self.squareSize,self.squareSize),Image.ANTIALIAS))
        self.Board[y][x].Image()

        #remove all yellow square (can move to)
        self.restore()
        
        found = self.find([y+1,x+1])
        if found != -1:
            for i in range(1,len(self.game.choice[found])):
                #turn
                temp = 0
                if self.game.currentTurn == self.game.WHITE:
                    temp = 1

                #color
                tFile = 'SquareCanMove'
                if abs((self.game.choice[found][i][0]-1)%2-(self.game.choice[found][i][1]-1)%2):
                    tFile += 'Bold'

                #can move to(change color to yellow)
                self.Board[self.game.choice[found][i][0]-1][self.game.choice[found][i][1]-1].FILE = ImageTk.PhotoImage(Image.open('Image\\' +tFile + '.gif').resize((self.squareSize,self.squareSize),Image.ANTIALIAS))
                self.Board[self.game.choice[found][i][0]-1][self.game.choice[found][i][1]-1].Image()
                
                self.last.append([self.game.choice[found][i][0]-1,self.game.choice[found][i][1]-1])

        if self.lastClickedRow != -1  and ([self.lastClickedRow+1,self.lastClickedCol+1] not in self.game.choice[found][1:len(self.game.choice[found])] or found == -1):
            self.Board[self.lastClickedRow][self.lastClickedCol].setRowCol(self.lastClickedRow+1,self.lastClickedCol+1)

        self.lastClickedRow = y
        self.lastClickedCol = x

    def restore(self):
        for i in self.last:
            self.Board[i[0]][i[1]].setRowCol(i[0]+1,i[1]+1)
            self.Board[i[0]][i[1]].Image()    
        self.last = []

    def Next(self,fromx=0,fromy=0,tox=0,toy=0):
        if self.game.currentTurn == self.game.WHITE:
            self.game.wC,self.game.checkMate,self.game.checkWay = False,False,[]
            t = self.game.makeAMove(fromx,fromy,tox,toy)

            if not self.comPlayer:
                self._checkState('black','white',t)
            else:
                self.last = []
                res = self._checkState('black','white',t)

                canvas.delete('all')
                self.display()

                #stop game and run makeAMove to save the last position
                if res == 'win' or res == 'draw':
                    self.game.makeAMove(0,0,0,0)
                    return

                root.update()

                #best move for computer
                tt = time.time()
                self.game.evaluated = 0
                self.game.maxi(self.game.maxDepth)
                print(time.time()-tt,self.game.evaluated)

                #pick randomly from best choices list and move
                a,b,c,d = random.choice(self.game.canmove)
                t = self.game.makeAMove(a,b,c,d)

                #promote
                if c == 8 and self.game.board[c][d] == self.game.BPAWN:
                    self.game.board[c][d] = self.game.BQUEEN
                self.game.checkMate,self.game.checkWay = False,[]
                self._checkState('white','black',t)
        else:
            self.game.checkMate,self.game.checkWay = False,[]
            t = self.game.makeAMove(fromx,fromy,tox,toy)
            self._checkState('white','black',t)

        self.last = []
        canvas.delete('all')
        self.display()

    def nothing(self):
        pass

    def retry(self,root):
        self.Retry = True
        self.game.choice = [[0,0]]
        self.isEndGame = False
        self.game.checkMate,self.game.checkWay = False,[]
        root.destroy()
        
    def _checkState(self,color1,color2,res):
        checkRes = 0
        if not res:
            checkRes = self.game.generateMoves()

        if checkRes == 'checkmate':
            self.checkedRow,self.checkedCol = self.game.find([self.game.BKING,self.game.WKING][color1 == 'white'])

        no = 0
        if color2 == 'white':
            no = 1

        if checkRes == 'win' and not res:
            self.isEndGame = True
            self.saved = True
            
            if not self.Retry:
                self.result[no^1] += 1.0
                
            self.window = Toplevel(width = 300,height = 360)
            self.window.protocol('WM_DELETE_WINDOW',self.endGame)
            self.centre(self.window)
            self.window.title('{} WIN'.format(color2.upper()))
            
            Label(self.window,text = '{} WIN'.format(color2.upper()),fg = color1,bg = color2,font = ('Arial',30,'bold')).pack()

             # if user didn't play a puzzle, show result
            if not self.puzzle:
                self.showResult()
                
            frame = Frame(self.window)
            frame.pack()

            #buttons
            Button(frame,text = 'MENU',font = ('Comic Sans MS',15,'normal'),command = self.endGame,width = 10).pack(side = LEFT,padx = 10)
            if self.comPlayer:
                Button(frame,text = 'RETRY',font = ('Comic Sans MS',15,'normal'),command = partial(self.retry,self.window),width = 10).pack(side = LEFT)
            if not self.puzzle:
                Button(self.window,text = 'REMATCH',font = ('Comic Sans MS',15,'normal'),command = self.startGame,width = 10).pack(pady = 10)
        elif checkRes == 'draw' or res:
            self.isEndGame= True
            self.saved = True
            if not self.Retry:
                self.result = [x+0.5 for x in self.result]
                
            self.window = Toplevel(width = 300,height = 400)
            self.window.protocol('WM_DELETE_WINDOW',self.endGame)
            self.window.title('DRAW')
            self.centre(self.window)

            #3 fold repetition
            if res:
                Label(self.window,text = '3 fold repetition!',font = ('Comic Sans MS',12,'normal')).pack()

            Label(self.window,text = 'DRAW',fg = 'black',bg = 'white',font = ('Arial',30,'bold')).pack()

            # if user didn't play a puzzle, show result
            if not self.puzzle:
                self.showResult()
                
            self.window.protocol('WM_DELETE_WINDOW',self.endGame)
            
            frame = Frame(self.window)
            frame.pack()

            #some buttons
            Button(frame,text = 'MENU',font = ('Comic Sans MS',15,'normal'),width = 10,command = self.endGame).pack(side = LEFT,padx = 10)
            if self.comPlayer:
                Button(frame,text = 'RETRY',font = ('Comic Sans MS',15,'normal'),command = partial(self.retry,self.window),width = 10).pack(side = RIGHT)
            if not self.puzzle:
                Button(self.window,text = 'REMATCH',font = ('Comic Sans MS',15,'normal'),command = self.startGame,width = 10).pack(pady = 10)
        return checkRes
    def showResult(self):
        #pick a random face
        img1 = ImageTk.PhotoImage(Image.open('Image\\HumanFace'+str(random.randrange(1,8))+'.png').resize((100,100),Image.ANTIALIAS))
        img2 = ImageTk.PhotoImage(Image.open('Image\\HumanFace'+str(random.randrange(1,8))+'.png').resize((100,100),Image.ANTIALIAS))

        #computer 
        if self.comPlayer:
            img2 = ImageTk.PhotoImage(Image.open('Image\\computerIcon.png').resize((100,100),Image.ANTIALIAS))

        frame2 = Frame(self.window)
        frame2.pack()

        #show faces
        p1 = Label(frame2,image = img1)
        p1.pack(side = LEFT,padx = 25)
        p1.image = img1

        p2 = Label(frame2,image = img2)
        p2.pack(side = LEFT,padx = 25)
        p2.image = img2

        #show result
        Label(self.window,text = ' WHITE          BLACK',font = ('Comic Sans MS',17,'normal')).pack(pady=5)
        Label(self.window,text = str(self.result[0])+'                  '+str(self.result[1]),font = ('Comic Sans MS',17,'normal')).pack()
    def find(self,x):
        for i in range(len(self.game.choice)):
            if x == self.game.choice[i][0]:
                return i
        return -1

    def promote(self,toRow,toCol,fromRow,fromCol):
        self.window = Toplevel(width = 350,height = 470)
        self.window.title('Promote')
        self.window.protocol('WM_DELETE_WINDOW',self.nothing)
        self.centre(self.window)
        
        _canvas = Canvas(self.window)
        _canvas.pack()
        _canvas.config(height = 0)

        #list of images
        button = [PhotoImage(file = 'C:\\Users\\Admin\\Desktop\\Chess Board Project\\Image\\KnightPromoteButton.gif'),PhotoImage(file = 'Image\\BishopPromoteButton.gif'),PhotoImage(file = 'Image\\RockPromoteButton.gif'),PhotoImage(file = 'Image\\QueenPromoteButton.gif')]

        Label(self.window,text = 'PROMOTE YOUR PAWN',font = ('Comic Sans MS',20,'normal')).pack()

        #knight
        b1 = Button(self.window,image = button[0],command = partial(self.Promote,[self.game.WKNIGHT,self.game.BKNIGHT],self.game.currentTurn,toRow,toCol,fromRow,fromCol))
        b1.image = button[0]
        b1.pack()

        #bishop
        b2 = Button(self.window,image = button[1],command = partial(self.Promote,[self.game.WBISHOP,self.game.BBISHOP],self.game.currentTurn,toRow,toCol,fromRow,fromCol))
        b2.image = button[1]
        b2.pack(pady = 10)

        #rock
        b3 = Button(self.window,image = button[2],command = partial(self.Promote,[self.game.WROCK,self.game.BROCK],self.game.currentTurn,toRow,toCol,fromRow,fromCol))
        b3.image = button[2]
        b3.pack()

        #queen
        b4 = Button(self.window,image = button[3],command = partial(self.Promote,[self.game.WQUEEN,self.game.BQUEEN],self.game.currentTurn,toRow,toCol,fromRow,fromCol))
        b4.image = button[3]
        b4.pack(pady = 10)

    def centre(self,window):
        #move window to center of the screen
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def endGame(self):
        #if user plays a game which is a saved game, delete that file
        if self.savedName != '' and os.path.exists('data\\saved\\'+self.savedName):
            os.remove('data\\saved\\'+self.savedName)

        #reset
        self.game.checkMate = False
        self.savedName = ''
        self.saved = True
        self.window.destroy()
        self.lastClickedRow,self.lastClickedCol = -1,-1

        #return to menu
        self.menu()

    def Promote(self,piece,color,toRow,toCol,fromRow,fromCol):
        self.promoted = 2
        self.window.destroy()
        self.game.board[toRow][toCol] = piece[color]
        self.game.board[fromRow][fromCol] = ' '
        self.Next()

    def display(self):
        #delete everything
        self.Board.clear()

        #renew
        for i in range(8):
            self.Board.append([])
            for j in range(8):
                #new object
                self.Board[i].append(square())
                self.Board[i][j].setObject(self)
                self.Board[i][j].setRowCol(i+1,j+1)

        #checkmate(create a red square)
        if self.checkedCol:
            self.Board[self.checkedRow-1][self.checkedCol-1].FILE = ImageTk.PhotoImage(Image.open('Image\\SquareChecked.gif').resize((self.squareSize,self.squareSize),Image.ANTIALIAS))
            self.Board[self.checkedRow-1][self.checkedCol-1].Image()
        self.checkedRow,self.checkedCol = 0,0

    def autoResizeSquare(self):
        height = root.winfo_screenheight()
        self.squareSize = ceil(height/9)
        self.resizeImage()
        
    def resizeImage(self):
        #resize neccesary images
        self.AFile = ImageTk.PhotoImage(Image.open('Image\\SquareActive.gif').resize((self.squareSize,self.squareSize),Image.ANTIALIAS))
        self.PiecesFile = [ImageTk.PhotoImage(Image.open('Image\\' +  i+'.gif').resize((self.squareSize,self.squareSize),Image.ANTIALIAS)) for i in self.PiecesFileName] 
        self.APieces = [ImageTk.PhotoImage(Image.open('Image\\'+ i+'Act.gif').resize((self.squareSize,self.squareSize),Image.ANTIALIAS)) for i in self.PiecesFileName]
        
game = chessGame()
root.mainloop()
