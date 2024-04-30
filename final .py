import pygame
import sys
pygame.init()

#Screen setup
width = 800
height = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dots and Boxes Stategy")


#Board + color choice
boardSize = int(input("Choose size: 4, 8, 12"))
lineColor = pygame.color.THECOLORS['black']

player1ColorName = (input("Player 1: Choose a color for lines and boxes: red, green, blue, black, white, yellow, gray, orange, purple, aqua")).lower()
player1Color = pygame.color.THECOLORS[player1ColorName]

player2ColorName = (input("Player 2: Choose a color for lines and boxes: red, green, blue, black, white, yellow, gray, orange, purple, aqua")).lower()
player2Color = pygame.color.THECOLORS[player2ColorName]

boxColor = pygame.color.THECOLORS['black']
dotColor = (0, 0, 0)
clicks = []

#starting board
def intBoard(size):
    lines = {}
    boxes = {}

    for i in range(size +1):
        for j in range(size + 1):

            if i < size:
                lines[((i, j), (i+1, j ))] = None

            if j < size:
                lines[((i, j), (i, j + 1))] = None

            if i < size and j < size:
                boxes[(i, j)] = None
                
    return {"lines": lines, "boxes": boxes}

#starting game
def intGame(boardSize):
    currentPlayer = 1 
    board = intBoard(boardSize)
    score = {1:0, 2:0}
    playerLineLevel = {1:1, 2:1}
    return currentPlayer, board, score, playerLineLevel

#index
def idIndex(id):   
    return id

#moves + validity
def isValid(id1, id2):
    print(id1, id2)
    if id1 not in board['lines'] or id2 not in board['lines']:
        return False

    p1 = board['lines'].get(idIndex(id1))
    p2 = board['lines'].get(idIndex(id2))

    if p1 is None or p2 is None:
        return False
    
    if isConnection(id1, id2):
        return False

    if p1 is None or p2 is None:
        return False 
    if (p1.x == p2.x and abs(p1.y - p2.y) == cellSize) or \
       (p1.y == p2.y and abs(p1.x - p2.x) == cellSize):
        return True
    return False

def isConnection(id1, id2):
    return (id1, id2) in movesDone or (id2, id1) in movesDone

def move(user, id1, id2):

    board[id_to_index(id1)].partners.append(id2)
    board[id_to_index(id2)].partners.append(id1)
    
    movesDone.append((id1, id2))
    movesDonePersons.append(user)
    return checkMoveMadeBox(user, id1, id2)

#user ability to make moves

def userClicks(position, board, boardSize, cellSize, currentPlayer, score):
    global clicks
    
    i = (position[0] - padding) // cellSize
    j = (position[1] - padding) // cellSize

    clickPosition = (i, j)
    clicks.append(clickPosition)

    if len(clicks) == 2:
        click1, click2 = clicks
        line = None

        if abs(click1[0] - click2[0]) == 1 and click1[1] == click2[1]:
            line = (click1, click2)
            
        elif abs(click1[1] - click2[1]) == 1 and click1[0] == click2[0]:
            line = (click1, click2)


        if line and line in board["lines"] and board["lines"][line] is None:
            board["lines"][line] = currentPlayer
            completedBoxes = checkComBox(board, line, currentPlayer)
            
            if completedBoxes > 0:
                score[currentPlayer] += completedBoxes
                return True

            else:
                return False

        clicks = []
    return None

#Box completions
def checkComBox(board, line, currentPlayer):
    completedBoxes = 0
    (x1, y1), (x2, y2) = line

    if x1 == x2:
        boxesCheck = [(x1, y1), (x1 - 1, y1)]

    else:
        boxesCheck = [(x1, y1), (x1, y1 - 1)]

    for box in boxesCheck:
        if box in board["boxes"] and board["boxes"][box] is None:

            top = board["lines"].get(((box[0], box[1]), (box[0], box[1] + 1)))
            bottom = board["lines"].get(((box[0] + 1, box[1]), (box[0] + 1, box[1] + 1)))
            left = board["lines"].get(((box[0], box[1]), (box[0] + 1, box[1])))
            right = board["lines"].get(((box[0], box[1] + 1), (box[0] + 1, box[1] + 1)))

            if top and bottom and left and right:
                board["boxes"][box] = currentPlayer
                completedBoxes += 1

    return completedBoxes
           
#player move
def playerMove(event, currentPlayer, board, score, playerLineLevel):
    if event.type == pygame.MOUSEBUTTONDOWN:
        position = pygame.mouse.get_pos()

        cellSizeFactor = 2
        cellSize = int(screen.get_width() / (boardSize * cellSizeFactor))
        
        i = (position[0] - padding) // cellSize
        j = (position[1] - padding) // cellSize
        logicalPosition = (i, j)

        if len(clicks) == 1:
            click1 = clicks.pop()
            line = None
            
            if abs(click1[0] - logicalPosition[0]) == 1 and click1[1] == logicalPosition[1]:
                line = (click1, logicalPosition)
                
            elif abs(click1[1] - logicalPosition[1]) == 1 and click1[0] == logicalPosition[0]:
                line = (click1, logicalPosition)

            if line and board["lines"].get(line) is None:
                board["lines"][line] = currentPlayer             
                completedBoxes = checkComBox(board, line, currentPlayer)
                score[currentPlayer] += completedBoxes
                
                if completedBoxes == 0:
                    currentPlayer = 2 if currentPlayer == 1 else 1
                else:
                    font = pygame.font.SysFont(None, 36)
                    turnText = f"Player {currentPlayer}'s turn"
                    turnSurface = font.render(turnText, True, (0,0,0))
                    screen.blit(turnSurface, (padding, padding // 2 +40))
                    pass
        else:
            clicks.append(logical_position)

padding = 150
#Game dimmensions
def drawGameState(screen, board, boardSize, player1Color, player2Color, score, currentPlayer):
    
    screen.fill((255, 255, 255))
    lineWidth = 2
    
    cellSize = (screen.get_width() - 2 * padding) // boardSize
    dotSize = 4

    #text display
    font = pygame.font.SysFont(None, 36)
    scoreText = f"Player 1: {score[1]} | Player 2: {score[2]}"
    
    scoreSurface = font.render(scoreText, True, (0,0,0))
    screen.blit(scoreSurface, (padding, padding // 2))

    turnText = f"Player {currentPlayer}'s turn"
    turnSurface = font.render(turnText, True, (0,0,0))
    screen.blit(turnSurface, (padding, padding // 2 +40))
                                
    #dots
    for i in range(boardSize +1):
        for j in range(boardSize + 1):
            dotX = padding + i * cellSize
            dotY = padding + j * cellSize
            pygame.draw.circle(screen, dotColor, (dotX, dotY), 5)
            
    #lines
    for line, owner in board["lines"].items():
        if owner is not None:
            startPos = (padding + line[0][0] * cellSize, padding + line[0][1] * cellSize)
            endPos = (padding + line[1][0] * cellSize, padding + line[1][1] * cellSize)

            lineColor = player1Color if owner == 1 else player2Color
            pygame.draw.line(screen, lineColor, startPos, endPos, lineWidth)

    #boxes
    for box, owner in board["boxes"].items():
        if owner is not None:
            x, y = box
            rectX = padding + x * cellSize
            rectY = padding + y * cellSize
            
            rect = pygame.Rect(rectX, rectY, cellSize, cellSize)
            boxColor = player1Color if owner == 1 else player2Color
            pygame.draw.rect(screen, boxColor, rect)

    winnerText = ""
    if score[1] > score[2]:
        winnerText = "Player 1 Wins!"

    elif score[2] > score[1]:
        winnerText = "Player 2 Wins!"

    elif score[1] + score[2] == boardSize **2:
        winnerText = "It's a tie!"

    winnerSurface = font.render(winnerText, True, (0,0,0))
    screen.blit(winnerSurface, (padding, padding // 2 + 40))
    
#Main game loop
currentPlayer, board, score, playerLineLevel = intGame(boardSize)
running = True

while running:
    
    cellSizeFactor = 2
    cellSize = int(screen.get_width() / (boardSize * cellSizeFactor))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            userClicks(pos, board, boardSize, cellSize, currentPlayer, score)
            
        drawGameState(screen, board, boardSize, player1Color, player2Color, score, currentPlayer)
        pygame.display.update()

pygame.quit()
sys.exit()



    
