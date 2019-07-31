# Chess Game
## 1. Overall
- This is a very simple chess game which is created by using Python. This project was created for entertainment and education purposes.
- Only a little knowledge in Python is required to read this code (I can only write very simple code)
## 2. Project
### a. How it works?
- This project consists of 3 Python files: engine.py, evaluated.py and GUI.py.
- engine.py is used to generate legal moves, evaluated.py is used to evaluate the position(for computer) and GUI.py, of course, create GUI.
```python
import engine
game = engine.chess()
game.initBoard() #initialize a new board
game.displayBoard()
game.generateMoves() #return a list, which consists of many small lists(1 small list for 1 piece). 1st element of a small list is coordinates of a piece, the next elements are coordinates of squares which that piece can move to
game.makeAMove(7,5,5,5) #move a piece from row 7 col 5 to row 5 col 5
game.displayBoard() #see the difference
```
- You can use engine.py and evaluate.py for your own project(you can use it as a library)
### b. How to play?
- User can play 2 mode: computer vs human(easy, medium and hard) or human vs human. 
- This game has save and load game feature.
- Chess puzzles are available
## 3. Contributing
- Any comments, pull requests are welcome!
## 4. License
- My name: Hoang Le
- Feel free to contact: Email: hoangdeptoong@gmail.com
