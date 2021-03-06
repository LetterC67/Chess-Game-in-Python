# Chess Game
## 1. Overall
- This is a very simple chess game which is created by using Python. This project was created for entertainment and education purposes.
- Only a little knowledge in Python is required to read this code (as this project is very simple and not optimized by using complicated algorithm; however, some lines are a little confusing, I will improve it later)
## 2. Project
### a. How it works?
- This project consists of 3 Python files (engine.py, evaluated.py and GUI.py) and some puzzles, pictures...
- engine.py is used to generate legal moves, evaluated.py is used to evaluate the position(for computer) and GUI.py, of course, creates GUI.
- engine.py(UPDATED v1.1.2)
```python
import engine
game = engine.chess()
game.displayBoard()
game.legalMoves() #see list of legal moves or it will return 'win','draw','checkmate'
game.makeAMove('e7e5') #move a piece from row 7 col 5 to row 5 col 5
game.displayBoard() #see the difference
```
- Some useful functions
```python
game.undo() #undo game
game.computerMove(depth = 3) #depth = 3 is default(can be changed to any integer number which is bigger than 0). Return a list which consists of small lists(all of them are best move). Eg: [[1,2,3,2],[4,3,2,2]], move from row 1,col 2 to row 3 col 2 or row 4 col 3 to row 2 col 2 is the best
game.toNotation(*[1,2,3,2]) # return 'b8b6'
game.toNumber('b8b6') #return [1,2,3,2]
game.gameState() #return 'win','draw' (NOTE: for current player turn)
```
- You can use engine.py and evaluate.py for your own project(you can use it as a library, although it is not optimal)
### b. How to play?
- User can play 2 mode: computer vs human(easy, medium and hard) or human vs human. 
- This game has save and load game feature.
- Chess puzzles are available (human vs computer) 
## 3. Contributing
- Any comments, pull requests are welcome!
## 4. License
- My name: Hoang Le
- Feel free to contact: Email: hoangdeptoong@gmail.com
