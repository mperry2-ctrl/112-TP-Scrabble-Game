from cmu_graphics import *
from PIL import Image
import random
import math
import copy
import time




#Wordlist.txt from https://github.com/redbo/scrabble/blob/master/dictionary.txt
scrabbleDictionary = set()
with open('wordlist.txt', 'r') as f:
    for line in f.readlines():
        scrabbleDictionary.add(line[:-1].upper())



#Scrabble feature
specialTiles = [(0, 0, 'red'), (0, 3, 'cyan'), (0, 7, 'red'), (0, 11, 'cyan'), (0, 14, 'red'),
                (1, 1, 'pink'), (1, 5, 'blue'), (1, 9, 'blue'), (1, 13, 'pink'),
                (2, 2, 'pink'), (2, 6, 'cyan'), (2, 8, 'cyan'), (2, 12, 'pink'),
                (3, 0, 'cyan'), (3, 3, 'pink'), (3, 7, 'cyan'), (3, 11, 'pink'), (3, 14,'cyan'),
                (4, 4, 'pink'), (4, 10, 'pink'),
                (5, 1, 'blue'), (5, 5, 'blue'), (5, 9, 'blue'), (5, 13, 'blue'),
                (6, 2, 'cyan'), (6, 6, 'cyan'), (6, 8, 'cyan'), (6, 12, 'cyan'),
                (7, 0, 'red'), (7, 3, 'cyan'), (7, 7, 'pink'), (7, 11, 'cyan'), (7, 14, 'red'),
                (8, 2, 'cyan'), (8, 6, 'cyan'), (8, 8, 'cyan'), (8, 12, 'cyan'),
                (9, 1, 'blue'), (9, 5, 'blue'), (9, 9, 'blue'), (9, 13, 'blue'),
                (10, 4, 'pink'), (10, 10, 'pink'),
                (11, 0, 'cyan'), (11, 3, 'pink'), (11, 7, 'cyan'), (11, 11, 'pink'), (11, 14,'cyan'),
                (12, 2, 'pink'), (12, 6, 'cyan'), (12, 8, 'cyan'), (12, 12, 'pink'),
                (13, 1, 'pink'), (13, 5, 'blue'), (13, 9, 'blue'), (13, 13, 'pink'),
                (14, 0, 'red'), (14, 3, 'cyan'), (14, 7, 'red'), (14, 11, 'cyan'), (14, 14, 'red')]
letters = (['A'] * 9 + ['B'] * 2 + ['C'] * 2 + ['D'] * 4 + ['E'] * 12 +
          ['F'] * 2 + ['G'] * 3 + ['H'] * 2 + ['I'] * 9 + ['J'] + ['K'] + ['L'] * 4
          + ['M'] * 2 + ['N'] * 6 + ['O'] * 8 + ['P'] * 2 + ['Q'] + ['R'] * 6 +
          ['S'] * 4 + ['T'] * 6 + ['U'] * 4 + ['V'] * 2 + ['W'] * 2 + ['X']
          + ['Y'] * 2 + ['Z'] + ['1'] + ['2'])
scores = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 
         'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1,
         'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 
         'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10, '1': 0, '2': 0}
lettersNoBlanks = (['A'] * 9 + ['B'] * 2 + ['C'] * 2 + ['D'] * 4 + ['E'] * 12 +
          ['F'] * 2 + ['G'] * 3 + ['H'] * 2 + ['I'] * 9 + ['J'] + ['K'] + ['L'] * 4
          + ['M'] * 2 + ['N'] * 6 + ['O'] * 8 + ['P'] * 2 + ['Q'] + ['R'] * 6 +
          ['S'] * 4 + ['T'] * 6 + ['U'] * 4 + ['V'] * 2 + ['W'] * 2 + ['X']
          + ['Y'] * 2 + ['Z'])
scoresNoBlanks = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 
         'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1,
         'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 
         'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}



class Board:
    def __init__(self, size, specialTiles):
        self.size = size
        self.specialTiles = specialTiles
        self.colors = [['tan'] * (size) for i in range(size)]
        for (row, col, color) in self.specialTiles:
            self.colors[row][col] = color
        self.board = [[None] * (size) for i in range(size)]
    
    def __repr__(self):
        return f'{self.colors}' + f'{self.board}'

    def getColor(self, row, col):
        return self.colors[row][col]

    def getLetter(self, row, col):
        return self.board[row][col]  
    
    def setLetter(self, row, col, letter):
        self.board[row][col] = letter
    
    def onBoard(self, letter):
        for row in range(self.size):
            if letter in self.board[row]:
                return True
        return False
                    


class Bag:
    def __init__(self, letters, scores):
        self.letters = letters
        self.scores = scores
    
    def takeLetter(self, letter):
        self.letters.remove(letter)
    
    def addLetter(self, letter):
        self.letters.append(letter)
    
    #For debugging purposes
    def __repr__(self):
        return f'{self.letters}'

class Player:
    def __init__(self, name):
        self.hand = []
        self.display = []
        self.score = 0
        self.name = name
    
    def __repr__(self):
        return f'{self.name}'

    def addLetter(self, letter):
        self.hand.append(letter)
    
    def takeLetterFromDisplay(self, index):
        self.display.pop(index)
        self.display.insert(index, '*')
    
    def addLetterToDisplay(self, index, letter):
        self.display.pop(index)
        self.display.insert(index, letter)

    def resetDisplay(self):
        self.display = copy.copy(self.hand)


class Button:
    def __init__(self, type, x, y, width, height):
        self.type = type
        self.left = x
        self.top = y
        self.width = width
        self.height = height
        self.right = self.left + self.width
        self.bottom = self.top + self.height
        
    
    def checkOnButton(self, x, y):
        return ((self.left <= x <= self.right) and (self.top <= y <= self.bottom))
    
    def drawButton(self):
        drawRect(self.left, self.top, self.width, self.height,
                 border='black', fill='white')
        drawLabel(f'{self.type}', self.left+self.width//2,
                  self.top+self.height//2, bold=True, size=14)
    
    def function(self, app):
        if self.type == 'Make Move':
            app.checkingBoard = True
        elif self.type == 'Trade' and app.tradingTiles == False:
            app.tradingTiles = True
            app.clickedPass = False
        elif self.type == 'Trade':
            if len(app.tilesTrading) == 0:
                app.tradingTiles = False
            else:
                tradeTiles(app)
        elif self.type == 'Pass' and app.clickedPass == False:
            app.clickedPass = True
            app.tradingTiles = False
        elif self.type == 'Pass':
            passTurn(app)
        elif self.type == 'Undo Move':
            undoMove(app)
        elif self.type == 'Pass and Play':
            app.player1 = Player('Player 1')
            app.player2 = Player('Player 2')
            app.bag = Bag(copy.copy(letters), scores)
            app.rulesScreen = True
            app.startScreen = False
        elif self.type == 'Play vs. Easy Computer':
            app.player1 = Player('Player 1')
            app.player2 = Player('Computer')
            app.bag = Bag(copy.copy(lettersNoBlanks), scoresNoBlanks)
            app.time = 5
            app.rulesScreen = True
            app.startScreen = False
        elif self.type == 'Play vs. Hard Computer':
            app.player1 = Player('Player 1')
            app.player2 = Player('Computer')
            app.bag = Bag(copy.copy(lettersNoBlanks), scoresNoBlanks)
            app.time = 20
            app.rulesScreen = True
            app.startScreen = False



def onAppStart(app):
    #Image from https://www.mircic91.com/wp-content/uploads/2019/11/Scrabble-600x338.jpeg
    app.image = Image.open("images/ScrabbleStart.gif")
    app.image = CMUImage(app.image)
    app.image2 = Image.open("images/RulesScreen.gif")
    app.image2 = CMUImage(app.image2)
    app.startScreen = True
    app.rulesScreen = False
    app.gameStart = False
    app.gameOver = False
    app.gameOverScored = False
    restartApp(app)
    

def restartApp(app):
    app.width = app.height = 800
    app.board = Board(15, specialTiles)
    app.boardCopy = copy.deepcopy(app.board.board)
    app.cols = app.rows = app.size = app.board.size
    

    app.boardWidth = app.width * app.size / (app.size+3) 
    app.boardHeight = app.height * app.size / (app.size+3)
    app.cellWidth = app.boardWidth / app.cols
    app.cellHeight = app.boardHeight / app.rows
    app.boardLeft = 50
    app.boardTop = 50
    app.cellBorderWidth = 2

    app.handLeft = app.boardLeft + app.boardWidth//2 - (3.5 * app.cellWidth)
    app.handTop = app.boardTop + app.boardHeight + 0.5*app.cellHeight
    app.handBoxLeft = app.handLeft - app.cellWidth/6
    app.handBoxTop = app.handTop - app.cellHeight/6
    app.handBoxWidth = app.cellWidth * 7 + app.cellHeight/3
    app.handBoxHeight = app.cellHeight + app.cellHeight/3
    
    
    app.startButtList = [Button('Pass and Play', 125, 400, 175, 60),
                         Button('Play vs. Easy Computer', 325, 400, 175, 60),
                         Button('Play vs. Hard Computer', 525, 400, 175, 60)]
    app.buttList = [Button('Trade', 640, 740, 60, 40), 
                    Button('Pass', 570, 740, 60, 40),
                    Button('Make Move', 80, 740, 100, 40),
                    Button('Undo Move', 710, 740, 90, 40),
                    Button('Play Again', 272, 450, 89, 40),
                    Button('Exit', 406, 450, 89, 40)]

    app.computer_move = []


    app.selection = None
    app.blank1 = ' '
    app.blank2 = ' '
    app.choosingBlank1 = app.choosingBlank2 = False
    app.tradingTiles = False
    app.tilesTrading = ['*' for _ in range(7)]
    app.turn = 1
    app.move = []
    app.clickedPass = False
    app.moveDirection = 'horizontal'
    app.error = None
    app.checkingBoard = False


#MAKING BOARD FUNCTIONS

def redrawAll(app):
    if app.startScreen:
        drawStartScreen(app)
        drawStartButtons(app)
    elif app.rulesScreen:
        drawRules(app)
    else:
        drawBoard(app)
        drawBoardBorder(app)
        drawHandBox(app)
        drawHand(app)
        drawScores(app)
        if app.error != None:
            drawErrorMessage(app)
        if app.tradingTiles:
            drawTradingTiles(app)
        elif app.clickedPass:
            drawConfirmPass(app)
        if app.gameOver:
            drawGameOver(app)
        drawButtons(app)


def drawStartScreen(app):
    drawImage(app.image, 0, 0, width=app.width, height=app.height)

def drawRules(app):
    drawImage(app.image2, 0, 0, width=app.width, height=app.height)

def drawGameOver(app):
    left, top = getCellLeftTop(app, 4, 4)
    width, height = app.cellWidth*7, app.cellHeight*7
    drawRect(left, top, width, height, fill='gray', border='black')
    drawLabel('GAME OVER!', left+width/2, top+app.cellWidth,
              bold=True, size=30, fill='black')
    drawLabel(f'{app.player1.name}', left+1.75*app.cellWidth, top+2*app.cellWidth,
              align='center', bold=True, size=22, fill='red')
    drawLabel(f'{app.player2.name}', left+5.25*app.cellWidth, top+2*app.cellWidth,
              align='center', bold=True, size=22, fill='blue')
    drawLabel(f'{app.player1.score}', left+1.75*app.cellWidth, top+3*app.cellWidth,
              align='center', bold=True, size=22, fill='red')
    drawLabel(f'{app.player2.score}', left+5.25*app.cellWidth, top+3*app.cellWidth,
              align='center', bold=True, size=22, fill='blue')
    if app.player1.score > app.player2.score:
        message = app.player1.name + ' won!'
        color = 'red'
    elif app.player2.score > app.player1.score:
        message = app.player2.name + ' won!'
        color = 'blue'
    else:
        message = "It's a tie!"
        color = 'purple'
    drawLabel(f'{message}', left+width/2, top+4*app.cellWidth,
              bold=True, size=30, fill=color)

def drawConfirmPass(app):
    left, top = getCellLeftTop(app, 6, 3)
    drawRect(left-0.5*app.cellWidth, top+0.5*app.cellWidth, app.cellWidth*10, app.cellHeight*2,
             fill='gray', border='black')
    drawLabel('Press pass again to give up your turn.',
              app.boardLeft+app.boardWidth/2, app.boardTop+app.boardHeight/2,
              align='center', bold=True, size=23)

def drawTradingTiles(app):
    drawRect(app.handBoxLeft, app.handBoxTop-200, app.handBoxWidth,
             app.handBoxHeight+app.cellHeight, fill='salmon', border='black')
    drawLabel('Click tiles to trade. Click Trade to confirm.',
              app.boardLeft+app.boardWidth/2, 
              app.boardTop+app.boardHeight/2+app.cellHeight*4,
              size=16, bold=True)
    x, y = app.handLeft, app.handTop-200+app.cellHeight
    for letter in app.tilesTrading:
        #Use * as a placeholder of a tile put onto the board
        if letter == '*':
            x += app.cellWidth
            continue
        drawRect(x, y, app.cellWidth, app.cellHeight,
             fill='darkSalmon', border='black', borderWidth=app.cellBorderWidth)
        drawLabel(f'{app.bag.scores[letter]}', x+app.cellWidth/1.2,
                    y+app.cellHeight/1.25, size=13, bold=True)
        if letter == '1' or letter == '2':
            letter = ' '
        drawLabel(f'{letter}', x+app.cellWidth/2, y+app.cellHeight/2,
                    size=25, bold=True)
        x += app.cellWidth


def drawButtons(app):
    for i, butt in enumerate(app.buttList):
        if (i == 4 or i == 5) and app.gameOver:
            butt.drawButton()
        elif i < 4:
            butt.drawButton()
    
def drawStartButtons(app):
    for butt in app.startButtList:
        butt.drawButton()


def drawScores(app):
    drawLabel(f'{app.player1.name}', 755, 300, size=16, bold=True)
    drawLabel(f'{app.player1.score}', 755, 340, size=16, bold=True)
    drawLabel(f'{app.player2.name}', 755, 400, size=16, bold=True)
    drawLabel(f'{app.player2.score}', 755, 440, size=16, bold=True)


def drawHandBox(app):
    drawRect(app.handBoxLeft, app.handBoxTop, app.handBoxWidth,
             app.handBoxHeight, fill='salmon', border='black')


def drawHand(app):
    x = app.handLeft
    y = app.handTop
    if app.turn == 1:
        currHand = app.player1.display
    else:
        currHand = app.player2.display
    for (i, letter) in enumerate(currHand):
        #Use * as a placeholder of a tile put onto the board
        if letter == '*':
            x += app.cellWidth
            continue
        #Selected tile is lit up
        borderColor = 'yellow' if app.selection == i else 'black'
        drawRect(x, y, app.cellWidth, app.cellHeight,
             fill='darkSalmon', border=borderColor,
             borderWidth=app.cellBorderWidth)
        drawLabel(f'{app.bag.scores[letter]}', x+app.cellWidth/1.2,
                  y+app.cellHeight/1.25, size=13, bold=True)
        if letter == '1' or letter == '2':
            letter = ' '
        drawLabel(f'{letter}', x+app.cellWidth/2, y+app.cellHeight/2,
                  size=25, bold=True)
        x += app.cellWidth


def drawErrorMessage(app):
    drawLabel(f'{app.error}', 380, 30, size=25)

#Modified from CSAcademy
def drawBoard(app):
    for row in range(app.size):
        for col in range(app.size):
            drawTile(app, row, col)
    

#Taken from CSAcademy
def drawBoardBorder(app):
    # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)


#Modified from CSAcademy
def drawTile(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellColor = app.board.getColor(row, col)
    letter = app.board.getLetter(row, col)
    #Checking if there is a tile on the space already or not
    if letter != None:
        color = 'white' if (letter == '1' or letter == '2') else 'black'
        drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight,
             fill='darkSalmon', border='black',
             borderWidth=app.cellBorderWidth)
        drawLabel(f'{app.bag.scores[letter]}', cellLeft+app.cellWidth/1.2,
                  cellTop+app.cellHeight/1.25, size=13, bold=True, fill=color)
        if letter == '1':
            letter = app.blank1
        elif letter == '2':
            letter = app.blank2
        drawLabel(f'{letter}', cellLeft+app.cellWidth/2, cellTop+app.cellHeight/2,
                  size=25, bold=True, fill=color)
    else:   
        if (row, col) == (7, 7):
            #Making middle Star
            drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight,
                 fill=cellColor, border='black',
                 borderWidth=app.cellBorderWidth)
            drawStar(app.boardLeft+app.boardWidth/2, app.boardTop+app.boardHeight/2, 
             app.cellWidth/2-4, 5)
        else:
            drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight,
                 fill=cellColor, border='black',
                 borderWidth=app.cellBorderWidth)
            message = getMessage(cellColor)
            #Making the message for special tiles, putting on sep lines
            for (i, line) in enumerate(message.splitlines()):
                drawLabel(f'{line}', cellLeft+app.cellWidth/2, 
                          cellTop+app.cellHeight/2 + (i-1)*9, size=11)


def getMessage(color):
    if color == 'red':
        return '''Triple
Word
Score'''
    elif color == 'pink':
        return '''Double
Word
Score'''
    elif color == 'blue':
        return '''Triple
Letter
Score'''
    elif color == 'cyan':
        return '''Double
Letter
Score'''
    return ''
    

#Taken from CSAcademy
def getCellLeftTop(app, row, col):
    cellLeft = app.boardLeft + col * app.cellWidth
    cellTop = app.boardTop + row * app.cellHeight
    return (cellLeft, cellTop)


#Taken from CSAcademy
def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    row = math.floor(dy / app.cellHeight)
    col = math.floor(dx / app.cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
        return (row, col)
    else:
        return None


#Modified from CSAcademy
def getHandTile(app, x, y):
    #Must add 
    dx = x - app.handLeft
    dy = y - app.handTop
    row = math.floor(dy / app.cellHeight)
    col = math.floor(dx / app.cellWidth)
    if (0 <= col < 7) and row == 0:
        return col
    else:
        return None


def getTradeTile(app, x, y):
    dx = x - app.handLeft
    dy = y - (app.handTop-200+app.cellHeight)
    row = math.floor(dy / app.cellHeight)
    col = math.floor(dx / app.cellWidth)
    if (0 <= col < len(app.tilesTrading)) and row == 0:
        return col
    else:
        return None


def getLettersInDirection(app, row, col, drow, dcol):
    #Base case (when we reach an empty space or end of board)
    if ((col < 0 or col >= app.cols) or (row < 0 or row >= app.rows)
        or app.board.board[row][col] == None):
        return ''
    else:
        #recursive case
        #We always want to read the words left-right and top-bottom,
        #so we ensure that through this conditional
        if drow > 0 or dcol > 0:
            return (app.board.board[row][col] + 
                    getLettersInDirection(app, row+drow, col+dcol, drow, dcol))
        else:
            return (getLettersInDirection(app, row+drow, col+dcol, drow, dcol)
                    + app.board.board[row][col])


def getWord(app, row, col, direction):
    if direction == 'horizontal':
        return getLettersInDirection(app, row, col, 0, -1) + getLettersInDirection(app, row, col+1, 0, 1)
    else:
        return getLettersInDirection(app, row, col, -1, 0) + getLettersInDirection(app, row+1, col, 1, 0)


def getWords(app):
    result = []
    if app.moveDirection == 'horizontal':
        #We know all the tiles we place will make one word in the direction we 
        #played it, but each tile has the ability to make a word in the other
        #direction, so we check that each time. 
        for (row, col, index) in app.move:
            word = getWord(app, row, col, 'vertical')
            #We don't want to add one letter 'words'
            if len(word) != 1:
                result.append(word)
        word = getWord(app, row, col, 'horizontal')
        if len(word) != 1:
            result.append(getWord(app, row, col, 'horizontal'))
    else:
        #Same thing except for vertical moves
        for (row, col, index) in app.move:
            word = getWord(app, row, col, 'horizontal')
            if len(word) != 1:
                result.append(word)
        word = getWord(app, row, col, 'vertical')
        if len(word) != 1:
            result.append(getWord(app, row, col, 'vertical'))
    return result



def isValidMove(app):
    if len(app.move) == 0:
        app.error = 'Make a move, pass, or trade tiles.'
        return False
    rowList = set()
    colList = set()
    for (row, col, index) in app.move:
        rowList.add(row)
        colList.add(col)
    if len(rowList) != 1 and len(colList) != 1:
        app.error = 'Tiles must be player either horizontally or vetically, not both.'
        return False

    if app.board.board[7][7] == None:
        if 7 not in rowList or 7 not in colList:
            app.error = 'First word must be played on the star.'
            return False
    
    #Get the row/column/direction of the move
    if len(rowList) == 1 and len(colList) == 1:
        #This is to check if there is only one tile played
        #Ensures scored correctly
        row, col, _ = app.move[0]
        if ((row-1 < 0 or app.board.board[row-1][col] != None) or 
            (row+1 >= app.rows or app.board.board[row+1][col] != None)):
            rowMove = False
            colNumber = int(str(colList)[1:-1])
            app.moveDirection = 'vertical'
        elif ((col-1 < 0 or app.board.board[row][col-1] != None) or 
            (col+1 >= app.cols or app.board.board[row][col+1] != None)):
            rowMove = True
            rowNumber = int(str(rowList)[1:-1])
            app.moveDirection = 'horizontal'
        else:
            return False
    elif len(rowList) == 1:
        rowMove = True
        rowNumber = int(str(rowList)[1:-1])
        app.moveDirection = 'horizontal'
    else:
        rowMove = False
        colNumber = int(str(colList)[1:-1])
        app.moveDirection = 'vertical'
    
    #Get range from smallest to largest
    #check each spot on board not from move to make sure there is a tile there
    if rowMove:
        #This is if the move is a row move
        lowerBound = min(colList)
        upperBound = max(colList)
        for col in range(lowerBound, upperBound):
            #We only care about spaces where we DONT place a tile
            if col not in colList:
                #If that space does not have a tile, then there is a gap
                if app.board.board[rowNumber][col] == None:
                    app.error = 'All tiles played must be connected.'
                    return False
    else:
        #This is if the move is a col move
        lowerBound = min(rowList)
        upperBound = max(rowList)
        for row in range(lowerBound, upperBound):
            #We only care about spaces where we DONT place a tile
            if row not in rowList:
                #If that space does not have a tile, then there is a gap
                if app.board.board[row][colNumber] == None:
                    app.error = 'All tiles played must be connected.'
                    return False
    if app.boardCopy[7][7] != None and not checkTileConnectedToBoard(app):
        app.error = 'Tiles not connected to current board.'
        return False
    wordsMade = getWords(app)
    for word in wordsMade:
        if '1' in word:
            index = word.index('1')
            word = word[:index] + app.blank1 + word[index+1:]
        if '2' in word:
            index = word.index('2')
            word = word[:index] + app.blank2 + word[index+1:]
        if word.upper() not in scrabbleDictionary:
            app.error = f'{word} is not a valid Scrabble word.'
            return False
    return True

    
def checkTileConnectedToBoard(app):
    adjacentChecks = [(1, 0), (0, 1), (0, -1), (-1, 0)]
    for (row, col, _) in app.move:
        for (drow, dcol) in adjacentChecks:
            if (0 <= row+drow < app.rows and 0 <= col+dcol < app.cols and
                app.boardCopy[row+drow][col+dcol] != None):
                return True
    return False


#GAME FUNCTIONS

def onStep(app):
    if app.gameStart:
        fillHand(app)
        app.gameStart = False
    elif app.gameOver and not app.gameOverScored:
        gameOver(app)
    elif app.gameOver:
        return
    elif app.turn == 2 and app.player2.name == 'Computer' and app.error == None:
        app.error = 'Computer is thinking...'
    elif app.turn == 2 and app.player2.name == 'Computer' and app.computer_move == []:
        t1 = time.time()
        app.computer_move, score = bestMove(app)
        t2 = time.time()
        app.player2.score += score
        computer_makeMove(app)
        app.error = None
        app.computer_move = []
        app.boardCopy = copy.deepcopy(app.board.board)
        passTurn(app)
        if len(app.bag.letters) == 0 and (app.player1.hand == [] or app.player2.hand == []):
            app.gameOver = True
    elif (app.board.onBoard('1') and app.blank1 == ' '):
        app.choosingBlank1 = True
    elif (app.board.onBoard('2') and app.blank2 == ' '):
        app.choosingBlank2 = True
    #This is the trading in tiles portion
    elif app.tradingTiles:
        if app.tilesTrading == ['*' for _ in range(7)]:
            undoMove(app)
    #This is undoing the trading tiles
    elif ['*' for _ in range(7)] != app.tilesTrading:
        app.tilesTrading = ['*' for _ in range(7)]
    elif not app.checkingBoard:
        placeLetters(app)
    else:
        if isValidMove(app):
            #When making a valid move, we want to score it, add score, 
            #refill tiles in hand, and make it the next persons turn
            score = scoreMove(app)
            if app.turn == 1:
                app.player1.score += score
            else:
                app.player2.score += score
            resetHand(app)
            app.checkingBoard = False
            app.move = []
            app.boardCopy = copy.deepcopy(app.board.board)
            passTurn(app)
            if len(app.bag.letters) == 0 and (app.player1.hand == [] or app.player2.hand == []):
                app.gameOver = True
            app.computer_move = []
        else:
            #When making an invalid move, we want to return the tiles to hand,
            #give an error message, and allow them to try again
            undoMove(app)
            app.checkingBoard = False
    
        


def takeLetterFromTrade(app, index):
    app.tilesTrading.pop(index)
    app.tilesTrading.insert(index, '*')


def addLetterFromTrade(app, index, letter):
    app.tilesTrading.pop(index)
    app.tilesTrading.insert(index, letter)

def fillHand(app):
    if len(app.bag.letters) == 0:
        return
    #Adding random letters to each player's hand until hand is full
    while len(app.player1.hand) < 7 and len(app.bag.letters) != 0:
        bagLength = len(app.bag.letters)
        index = random.randint(0, bagLength-1)
        app.player1.addLetter(app.bag.letters[index])
        app.bag.takeLetter(app.bag.letters[index])
    while len(app.player2.hand) < 7 and len(app.bag.letters) != 0:
        bagLength = len(app.bag.letters)
        index = random.randint(0, bagLength-1)
        app.player2.addLetter(app.bag.letters[index])
        app.bag.takeLetter(app.bag.letters[index])
    app.player1.display = copy.copy(app.player1.hand)
    app.player2.display = copy.copy(app.player2.hand)

def resetHand(app):
    if app.turn == 1:
        app.player1.hand = copy.copy(app.player1.display)
        while '*' in app.player1.hand:
            app.player1.hand.remove('*')
    else:
        app.player2.hand = copy.copy(app.player2.display)
        while '*' in app.player2.hand:
            app.player2.hand.remove('*')
    fillHand(app)

def tradeTiles(app):
    if app.tilesTrading != ['*' for _ in range(7)]:
        for tile in app.tilesTrading:
            if tile != '*':
                app.bag.addLetter(tile)
        resetHand(app)
        passTurn(app)
    app.tradingTiles = False


def passTurn(app):
    undoMove(app)
    app.turn = 1 if app.turn == 2 else 2
    app.clickedPass = False

def getWordScore(app, word):
    score = 0
    for letter in word:
        score += app.bag.scores[letter]
    return score

def scoreMove(app):
    result = 0
    if app.moveDirection == 'horizontal':
        #We know all the tiles we place will make one word in the direction we 
        #played it, but each tile has the ability to make a word in the other
        #direction, so we check that each time. 
        for (row, col, index) in app.move:
            bonus = app.board.colors[row][col]
            word = getWord(app, row, col, 'vertical')
            #We don't want to add one letter 'words'
            if len(word) != 1:
                score = getWordScore(app, word)
                if bonus == 'red':
                    score *= 3
                elif bonus == 'pink':
                    score *= 2
                elif bonus == 'cyan':
                    score += app.bag.scores[app.board.board[row][col]]
                elif bonus == 'blue':
                    score += 2*app.bag.scores[app.board.board[row][col]]
                result += score
        word = getWord(app, row, col, 'horizontal')
        score = getWordScore(app, word)
        multiply_by = 1
        #This part is to deal with multiple bonuses occuring for one word
        #We don't have to worry about this previously because we can only
        #place tiles in one direction
        for (row, col, index) in app.move:
            bonus = app.board.colors[row][col]
            if bonus == 'cyan':
                score += app.bag.scores[app.board.board[row][col]]
            elif bonus == 'blue':
                score += 2*app.bag.scores[app.board.board[row][col]]
            elif bonus == 'red':
                multiply_by *= 3
            elif bonus == 'pink':
                multiply_by *= 2
        result += score * multiply_by
    else:
        #Same thing except for vertical moves
        for (row, col, index) in app.move:
            bonus = app.board.colors[row][col]
            word = getWord(app, row, col, 'horizontal')
            #We don't want to add one letter 'words'
            if len(word) != 1:
                score = getWordScore(app, word)
                if bonus == 'red':
                    score *= 3
                elif bonus == 'pink':
                    score *= 2
                elif bonus == 'cyan':
                    score += app.bag.scores[app.board.board[row][col]]
                elif bonus == 'blue':
                    score += 2*app.bag.scores[app.board.board[row][col]]
                result += score
        word = getWord(app, row, col, 'vertical')
        score = getWordScore(app, word)
        multiply_by = 1
        #This part is to deal with multiple bonuses occuring for one word
        #We don't have to worry about this previously because we can only
        #place tiles in one direction
        for (row, col, index) in app.move:
            bonus = app.board.colors[row][col]
            if bonus == 'cyan':
                score += app.bag.scores[app.board.board[row][col]]
            elif bonus == 'blue':
                score += 2*app.bag.scores[app.board.board[row][col]]
            elif bonus == 'red':
                multiply_by *= 3
            elif bonus == 'pink':
                multiply_by *= 2
        result += score * multiply_by
    if len(app.move) == 7:
        result += 50
    return result


def placeLetters(app):
    for (row, col, index) in app.move:
        if app.turn == 1:
            letter = app.player1.hand[index]
        else:
            letter = app.player2.hand[index]
        app.board.setLetter(row, col, letter)
    

def undoMove(app):
    if app.turn == 1:
        app.player1.resetDisplay()
    else:
        app.player2.resetDisplay()
    for (row, col, index) in app.move:
        if app.turn == 1:
            if app.player1.hand[index] == '1':
                app.blank1 = ' '
            elif app.player1.hand[index] == '2':
                app.blank2 = ' '
        else:
            if app.player2.hand[index] == '1':
                app.blank1 = ' '
            elif app.player2.hand[index] == '2':
                app.blank2 = ' '
        app.board.setLetter(row, col, None)
    app.move = []


def gameOver(app):
    if app.player1.hand == []:
        for tile in app.player2.hand:
            app.player1.score += app.bag.scores[tile]
    else:
        for tile in app.player1.hand:
            app.player2.score += app.bag.scores[tile]
    app.gameOverScored = True
    

def homeScreen(app):
    restartApp(app)

def onMousePress(app, mouseX, mouseY):
    if app.startScreen:
        for butt in app.startButtList:
            if butt.checkOnButton(mouseX, mouseY):
                butt.function(app)
    elif app.rulesScreen:
        app.rulesScreen = False
        app.gameStart = True
    if app.gameOver:
        if app.buttList[-2].checkOnButton(mouseX, mouseY):
            restartApp(app)
            app.gameStart = True
            app.gameOver = False
            app.gameOverScored = False
        elif app.buttList[-1].checkOnButton(mouseX, mouseY):
            app.startScreen = True
            app.rulesScreen = False
            app.gameStart = False
            app.gameOver = False
            app.gameOverScored = False
            homeScreen(app)
    else:
        for butt in app.buttList:
            if butt.checkOnButton(mouseX, mouseY):
                butt.function(app)
    if app.error != None:
        app.error = None
    if app.clickedPass and not app.buttList[1].checkOnButton(mouseX, mouseY):
        app.clickedPass = False
    elif app.tradingTiles:
        selectedTile = getHandTile(app, mouseX, mouseY)
        selectedTrade = getTradeTile(app, mouseX, mouseY)
        if selectedTile != None:
            if not ((app.turn == 1 and app.player1.display[selectedTile] == '*') or 
                (app.turn == 2 and app.player2.display[selectedTile] == '*')):
                if app.turn == 1:
                    addLetterFromTrade(app, selectedTile, app.player1.display[selectedTile])
                    app.player1.takeLetterFromDisplay(selectedTile)
                else:
                    addLetterFromTrade(app, selectedTile, app.player2.display[selectedTile])
                    app.player2.takeLetterFromDisplay(selectedTile)
        elif selectedTrade != None:
            if app.tilesTrading[selectedTrade] != '*':
                if app.turn == 1:
                    app.player1.addLetterToDisplay(selectedTrade, app.tilesTrading[selectedTrade])
                    takeLetterFromTrade(app, selectedTrade)
                else:
                    app.player2.addLetterToDisplay(selectedTrade, app.tilesTrading[selectedTrade])
                    takeLetterFromTrade(app, selectedTrade)
    elif not (app.choosingBlank1 or app.choosingBlank2):
        selectedCell = getCell(app, mouseX, mouseY)
        selectedTile = getHandTile(app, mouseX, mouseY)
        #Only want to select a tile from hand if we click on a handtile
        if selectedTile != None:
            if app.selection == selectedTile:
                app.selection = None
            else:
                app.selection = selectedTile
        #If we selected a tile in the hand and we selected a cell on the board
        if selectedCell != None and app.selection != None:
            #Makes so you cannot reuse a tile that has been placed
            if ((app.turn == 1 and app.player1.display[app.selection] == '*') or 
                (app.turn == 2 and app.player2.display[app.selection] == '*')):
                app.selection = None
            
            #Only after all prev conditions satisfied can you actually make move
            if app.selection != None:
                row, col = selectedCell
                if app.board.board[row][col] == None:
                    app.move.append((row, col, app.selection))
                    if app.turn == 1:
                        app.player1.takeLetterFromDisplay(app.selection)
                    else:
                        app.player2.takeLetterFromDisplay(app.selection)
                    app.selection = None

    

def onKeyPress(app, key):
    if app.choosingBlank1 and key.isalpha():
        app.blank1 = key.upper()
        app.choosingBlank1 = False
    elif app.choosingBlank2 and key.isalpha():
        app.blank2 = key.upper()
        app.choosingBlank2 = False
    

# -------------------------------
#       Computer Algorithms
# -------------------------------

#Idea comes from https://www.scotthyoung.com/blog/2013/02/21/wordsmith/#:~:text=The%20basic%20algorithm%20is%20fairly%20simple%3A%201%20Make,all%20new%20crosswords%29%20and%20calculate%20the%20points.%20
def bestMove(app):
    possTiles1 = getPlayableTiles(app, 1)
    possTiles2 = getPlayableTiles(app, 2)
    possTiles3 = getPlayableTiles(app, 3)
    possTiles4 = getPlayableTiles(app, 4)
    triedMoves = set()
    bestMoveScore = 0
    bestMove = None
    t1 = time.time()
    for index in range(len(app.player2.hand)):
        for (row, col) in possTiles1:
            if not computer_checkTileConnectedToBoard(app, [(row, col, index)]):
                continue
            if (row, col, app.player2.hand[index]) in triedMoves:
                continue
            app.computer_move = [(row, col, index)]
            computer_placeLetters(app)
            if computer_isValidMove(app):
                score = computer_scoreMove(app)
                if score > bestMoveScore:
                    bestMove = copy.copy(app.computer_move)
                    bestMoveScore = score
            computer_undoMove(app)
            triedMoves.add((row, col, app.player2.hand[index]))
            app.computer_move = []
    for index1 in range(len(app.player2.hand)):
        for (row1, col1) in possTiles2:
            if not computer_checkTileConnectedToBoard(app, [(row1, col1, index1)]):
                continue
            for index2 in range(len(app.player2.hand)):
                if index1 == index2:
                    continue
                for (row2, col2) in possTiles2:
                    if ((row1, col1) == (row2, col2) or not (row1 == row2 or col1 == col2) or
                        (tuple(sorted([(row1, col1, app.player2.hand[index1]),
                                        (row2, col2, app.player2.hand[index2])]))) in triedMoves):
                        continue
                    app.computer_move = [(row1, col1, index1), (row2, col2, index2)]
                    computer_placeLetters(app)
                    if computer_isValidMove(app):
                        score = computer_scoreMove(app)
                        if score > bestMoveScore:
                            bestMove = copy.copy(app.computer_move)
                            bestMoveScore = score
                    computer_undoMove(app)
                    triedMoves.add(tuple(sorted([(row1, col1, app.player2.hand[index1]),
                                                  (row2, col2, app.player2.hand[index2])])))
                    app.computer_move = []
    for index1 in range(len(app.player2.hand)):
        for (row1, col1) in possTiles3:
            if not computer_checkTileConnectedToBoard(app, [(row1, col1, index1)]):
                continue
            for index2 in range(len(app.player2.hand)):
                if index1 == index2:
                    continue
                for (row2, col2) in possTiles3:
                    if (row1, col1) == (row2, col2) or not (row1 == row2 or col1 == col2):
                        continue
                    for index3 in range(len(app.player2.hand)):
                        if index1 == index3 or index2 == index3:
                            continue
                        for (row3, col3) in possTiles3:
                            t2 = time.time()
                            if ((row3, col3) == (row2, col2) or (row1, col1) == (row3, col3)
                                or not ((row1 == row2 == row3) or (col1 == col2 == col3)) or 
                                (tuple(sorted([(row1, col1, app.player2.hand[index1]),
                                                  (row2, col2, app.player2.hand[index2]),
                                                  (row3, col3, app.player2.hand[index3])]))) in triedMoves):
                                continue
                            app.computer_move = [(row1, col1, index1), (row2, col2, index2), (row3, col3, index3)]
                            computer_placeLetters(app)
                            if (computer_getWord(app, row1, col1, 'horizontal').upper() not in scrabbleDictionary
                                    or computer_getWord(app, row1, col1, 'vertical').upper() not in scrabbleDictionary):
                                computer_undoMove(app)
                                triedMoves.add(tuple(sorted([(row1, col1, app.player2.hand[index1]),
                                                        (row2, col2, app.player2.hand[index2]),
                                                        (row3, col3, app.player2.hand[index3])])))
                            elif computer_isValidMove(app):
                                score = computer_scoreMove(app)
                                if score > bestMoveScore:
                                    bestMove = copy.copy(app.computer_move)
                                    bestMoveScore = score
                                computer_undoMove(app)
                                triedMoves.add(tuple(sorted([(row1, col1, app.player2.hand[index1]),
                                                    (row2, col2, app.player2.hand[index2]),
                                                    (row3, col3, app.player2.hand[index3])])))
                            app.computer_move = []
                            if time.time()-t1 > app.time:
                                return bestMove, bestMoveScore
    for index1 in range(len(app.player2.hand)):
        for (row1, col1) in possTiles4:
            if not computer_checkTileConnectedToBoard(app, [(row1, col1, index1)]):
                continue
            for index2 in range(len(app.player2.hand)):
                if index1 == index2:
                    continue
                for (row2, col2) in possTiles4:
                    if (row1, col1) == (row2, col2) or not (row1 == row2 or col1 == col2):
                        continue
                    for index3 in range(len(app.player2.hand)):
                        if index1 == index3 or index2 == index3:
                            continue
                        for (row3, col3) in possTiles4:
                            if ((row3, col3) == (row2, col2) or (row1, col1) == (row3, col3)
                                or not ((row1 == row2 == row3) or (col1 == col2 == col3))):
                                continue
                            for index4 in range(len(app.player2.hand)):
                                if index1 == index4 or index2 == index4 or index3 == index4:
                                    continue
                                for (row4, col4) in possTiles4:
                                    if ((row4, col4) == (row2, col2) or (row1, col1) == (row4, col4) or (row3, col3) == (row4, col4)
                                    or not ((row1 == row2 == row3 == row4) or (col1 == col2 == col3 == col4)) or
                                    (tuple(sorted([(row1, col1, app.player2.hand[index1]),
                                                  (row2, col2, app.player2.hand[index2]),
                                                  (row3, col3, app.player2.hand[index3]),
                                                  (row4, col4, app.player2.hand[index4])]))) in triedMoves):
                                        continue
                                    app.computer_move = [(row1, col1, index1), 
                                                         (row2, col2, index2), 
                                                         (row3, col3, index3), 
                                                         (row4, col4, index4)]
                                    computer_placeLetters(app)
                                    if (computer_getWord(app, row1, col1, 'horizontal').upper() not in scrabbleDictionary
                                    or computer_getWord(app, row1, col1, 'vertical').upper() not in scrabbleDictionary):
                                        computer_undoMove(app)
                                        triedMoves.add(tuple(sorted([(row1, col1, app.player2.hand[index1]),
                                                        (row2, col2, app.player2.hand[index2]),
                                                        (row3, col3, app.player2.hand[index3]),
                                                        (row4, col4, app.player2.hand[index4])])))
                                    elif computer_isValidMove(app):
                                        score = computer_scoreMove(app)
                                        if score > bestMoveScore:
                                            bestMove = sorted(app.computer_move)
                                            bestMoveScore = score
                                        computer_undoMove(app)
                                        triedMoves.add(tuple(sorted([(row1, col1, app.player2.hand[index1]),
                                                        (row2, col2, app.player2.hand[index2]),
                                                        (row3, col3, app.player2.hand[index3]),
                                                        (row4, col4, app.player2.hand[index4])])))
                                    app.computer_move = []
                                    if time.time()-t1 > app.time:
                                        return bestMove, bestMoveScore
    return bestMove, bestMoveScore


def computer_makeMove(app):
    app.computer_move = sortTupleByIndex(app.computer_move)
    for (row, col, index) in app.computer_move[::-1]:
        letter = app.player2.hand[index]
        app.board.setLetter(row, col, letter)
        app.player2.hand.pop(index)
    fillHand(app)
    

def computer_placeLetters(app):
    for (row, col, index) in app.computer_move:
        letter = app.player2.hand[index]
        app.boardCopy[row][col] = letter

def sortTupleByIndex(L):
    Lcopy = []
    for v in L:
        row, col, index = v
        if Lcopy == []:
            Lcopy.append(v)
        else:
            j = 0
            for (row, col, index2) in Lcopy:
                if index2 >= index:
                    Lcopy.insert(j, v)
                    break
                else:
                    j += 1
            if len(Lcopy) == j:
                Lcopy.append(v)
    return Lcopy
        
        
def computer_undoMove(app):
    for (row, col, index) in app.computer_move:
        app.boardCopy[row][col] = None

def computer_scoreMove(app):
    result = 0
    if app.moveDirection == 'horizontal':
        #We know all the tiles we place will make one word in the direction we 
        #played it, but each tile has the ability to make a word in the other
        #direction, so we check that each time. 
        for (row, col, index) in app.computer_move:
            bonus = app.board.colors[row][col]
            word = computer_getWord(app, row, col, 'vertical')
            #We don't want to add one letter 'words'
            if len(word) != 1:
                score = getWordScore(app, word)
                if bonus == 'red':
                    score *= 3
                elif bonus == 'pink':
                    score *= 2
                elif bonus == 'cyan':
                    score += app.bag.scores[app.boardCopy[row][col]]
                elif bonus == 'blue':
                    score += 2*app.bag.scores[app.boardCopy[row][col]]
                result += score
        word = computer_getWord(app, row, col, 'horizontal')
        score = getWordScore(app, word)
        multiply_by = 1
        #This part is to deal with multiple bonuses occuring for one word
        #We don't have to worry about this previously because we can only
        #place tiles in one direction
        for (row, col, index) in app.computer_move:
            bonus = app.board.colors[row][col]
            if bonus == 'cyan':
                score += app.bag.scores[app.boardCopy[row][col]]
            elif bonus == 'blue':
                score += 2*app.bag.scores[app.boardCopy[row][col]]
            elif bonus == 'red':
                multiply_by *= 3
            elif bonus == 'pink':
                multiply_by *= 2
        result += score * multiply_by
    else:
        #Same thing except for vertical moves
        for (row, col, index) in app.computer_move:
            bonus = app.board.colors[row][col]
            word = computer_getWord(app, row, col, 'horizontal')
            #We don't want to add one letter 'words'
            if len(word) != 1:
                score = getWordScore(app, word)
                if bonus == 'red':
                    score *= 3
                elif bonus == 'pink':
                    score *= 2
                elif bonus == 'cyan':
                    score += app.bag.scores[app.boardCopy[row][col]]
                elif bonus == 'blue':
                    score += 2*app.bag.scores[app.boardCopy[row][col]]
                result += score
        word = computer_getWord(app, row, col, 'vertical')
        score = getWordScore(app, word)
        multiply_by = 1
        #This part is to deal with multiple bonuses occuring for one word
        #We don't have to worry about this previously because we can only
        #place tiles in one direction
        for (row, col, index) in app.computer_move:
            bonus = app.board.colors[row][col]
            if bonus == 'cyan':
                score += app.bag.scores[app.boardCopy[row][col]]
            elif bonus == 'blue':
                score += 2*app.bag.scores[app.boardCopy[row][col]]
            elif bonus == 'red':
                multiply_by *= 3
            elif bonus == 'pink':
                multiply_by *= 2
        result += score * multiply_by
    if len(app.computer_move) == 7:
        result += 50
    return result

def computer_getLettersInDirection(app, row, col, drow, dcol):
    #Base case (when we reach an empty space or end of board)
    if ((col < 0 or col >= app.cols) or (row < 0 or row >= app.rows)
        or app.boardCopy[row][col] == None):
        return ''
    else:
        #recursive case
        #We always want to read the words left-right and top-bottom,
        #so we ensure that through this conditional
        if drow > 0 or dcol > 0:
            return (app.boardCopy[row][col] + 
                    computer_getLettersInDirection(app, row+drow, col+dcol, drow, dcol))
        else:
            return (computer_getLettersInDirection(app, row+drow, col+dcol, drow, dcol)
                    + app.boardCopy[row][col])


def computer_getWord(app, row, col, direction):
    if direction == 'horizontal':
        return computer_getLettersInDirection(app, row, col, 0, -1) + computer_getLettersInDirection(app, row, col+1, 0, 1)
    else:
        return computer_getLettersInDirection(app, row, col, -1, 0) + computer_getLettersInDirection(app, row+1, col, 1, 0)

def computer_getWords(app):
    result = []
    if app.moveDirection == 'horizontal':
        #We know all the tiles we place will make one word in the direction we 
        #played it, but each tile has the ability to make a word in the other
        #direction, so we check that each time. 
        for (row, col, index) in app.computer_move:
            word = computer_getWord(app, row, col, 'vertical')
            #We don't want to add one letter 'words'
            if len(word) != 1:
                result.append(word)
        word = computer_getWord(app, row, col, 'horizontal')
        if len(word) != 1:
            result.append(computer_getWord(app, row, col, 'horizontal'))
    else:
        #Same thing except for vertical moves
        for (row, col, index) in app.computer_move:
            word = computer_getWord(app, row, col, 'horizontal')
            if len(word) != 1:
                result.append(word)
        word = computer_getWord(app, row, col, 'vertical')
        if len(word) != 1:
            result.append(computer_getWord(app, row, col, 'vertical'))
    return result

def computer_checkTileConnectedToBoard(app, L):
    adjacentChecks = [(1, 0), (0, 1), (0, -1), (-1, 0)]
    for (row, col, _) in L:
        for (drow, dcol) in adjacentChecks:
            if (0 <= row+drow < app.rows and 0 <= col+dcol < app.cols and
                app.board.board[row+drow][col+dcol] != None):
                return True
    return False


def computer_isValidMove(app):
    if len(app.computer_move) == 0:
        return False
    rowList = set()
    colList = set()
    for (row, col, index) in app.computer_move:
        rowList.add(row)
        colList.add(col)
    if len(rowList) != 1 and len(colList) != 1:
        return False
    #Get the row/column/direction of the move
    if len(rowList) == 1 and len(colList) == 1:
        row, col, _ = app.computer_move[0]
        if ((row-1 >= 0 and app.boardCopy[row-1][col] != None) or 
            (row+1 < app.rows and app.boardCopy[row+1][col] != None)):
            rowMove = False
            colNumber = int(str(colList)[1:-1])
            app.moveDirection = 'vertical'
        elif ((col-1 >= 0 and app.boardCopy[row][col-1] != None) or 
            (col+1 < app.cols and app.boardCopy[row][col+1] != None)):
            rowMove = True
            rowNumber = int(str(rowList)[1:-1])
            app.moveDirection = 'horizontal'
        else:
            return False
    elif len(rowList) == 1:
        rowMove = True
        rowNumber = int(str(rowList)[1:-1])
        app.moveDirection = 'horizontal'
    else:
        rowMove = False
        colNumber = int(str(colList)[1:-1])
        app.moveDirection = 'vertical'
    
    #Get range from smallest to largest
    #check each spot on board not from move to make sure there is a tile there
    if rowMove:
        #This is if the move is a row move
        lowerBound = min(colList)
        upperBound = max(colList)
        for col in range(lowerBound, upperBound):
            #We only care about spaces where we DONT place a tile
            if col not in colList:
                #If that space does not have a tile, then there is a gap
                if app.boardCopy[rowNumber][col] == None:
                    return False
    else:
        #This is if the move is a col move
        lowerBound = min(rowList)
        upperBound = max(rowList)
        for row in range(lowerBound, upperBound):
            #We only care about spaces where we DONT place a tile
            if row not in rowList:
                #If that space does not have a tile, then there is a gap
                if app.boardCopy[row][colNumber] == None:
                    return False
    if not computer_checkTileConnectedToBoard(app, app.computer_move):
        return False
    wordsMade = computer_getWords(app)
    for word in wordsMade:
        if '1' in word:
            index = word.index('1')
            word = word[:index] + app.blank1 + word[index+1:]
        if '2' in word:
            index = word.index('2')
            word = word[:index] + app.blank2 + word[index+1:]
        if word.upper() not in scrabbleDictionary:
            return False
    return True


def getPlayableTiles(app, depth):
    board = [[False] * app.size for i in range(app.size)]
    possMoves = set()
    for row in range(app.size):
        for col in range(app.size):
            if app.board.board[row][col] != None:
                board[row][col] = None
                for i in range(depth):
                    #These go in each direction i times
                    if row+1+i < app.rows and app.board.board[row+1+i][col] == None:
                        possMoves.add((row+1+i, col))
                        board[row+1+i][col] = True
                    if row-1-i >= 0 and app.board.board[row-1-i][col] == None:
                        possMoves.add((row-1-i, col))
                        board[row-1-i][col] = True
                    if col+1+i < app.cols and app.board.board[row][col+i+1] == None:
                        possMoves.add((row, col+1+i))
                        board[row][col+1+i] = True
                    if col-i-1 >= 0 and app.board.board[row][col-i-1] == None:
                        possMoves.add((row, col-i-1))
                        board[row][col-1-i] = True
                    #These go next to the tile and the vertical if its to the left/right
                    #or horizontal if up/down
                    #These are the ones to the left and right that go up/down
                    if row+i < app.rows and col-1 >= 0 and app.board.board[row+i][col-1] == None:
                        possMoves.add((row+i, col-1))
                        board[row+i][col-1] = True
                    if row+i < app.rows and col+1 < app.cols and app.board.board[row+i][col+1] == None:
                        possMoves.add((row+i, col+1))
                        board[row+i][col+1] = True
                    if row-i >= 0 and col-1 >= 0 and app.board.board[row-i][col-1] == None:
                        possMoves.add((row-i, col-1))
                        board[row-i][col-1] = True
                    if row-i >= 0 and col+1 < app.cols and app.board.board[row-i][col+1] == None:
                        possMoves.add((row-i, col+1))
                        board[row-i][col+1] = True
                    #These are the ones to the up and down that go left/right
                    if col+i < app.cols and row-1 >= 0 and app.board.board[row-1][col+i] == None:
                        possMoves.add((row-1, col+i))
                        board[row-1][col+i] = True
                    if col+i < app.cols and row+1 < app.rows and app.board.board[row+1][col+i] == None:
                        possMoves.add((row+1, col+i))
                        board[row+1][col+i] = True
                    if col-i >= 0 and row-1 >= 0 and app.board.board[row-1][col-i] == None:
                        possMoves.add((row-1, col-i))
                        board[row-1][col-i] = True
                    if col-i >= 0 and row+1 < app.rows and app.board.board[row+1][col-i] == None:
                        possMoves.add((row+1, col-i))
                        board[row+1][col-i] = True
    return list(possMoves)


# ----------------------------
#        Run App
# ----------------------------


def main():
    runApp()
    

main()
