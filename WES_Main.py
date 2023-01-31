import pygame as p
from Game_WES import WES_Engine

WIDTH = HEIGHT = 512
DIMENSIONS = 5 # dimensions of a chess board are 5x5
SQ_SIZE =HEIGHT // DIMENSIONS
MAX_FPS = 15 #for animations
IMAGES = {}

PLAY_ROLE = [1, 1] # index: 0 for player 1 as wolf and 1 for player 2 as sheep. value: 0 for AI and 1 for human.
initial_board = [
            ['wS', 'wS', 'wS', 'wS', 'wS'],
            ['wS', 'wS', 'wS', 'wS', 'wS'],
            ['--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--'],
            ['--', 'bW', '--', 'bW', '--']]
'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''

def loadImages():
    pieces = ['bW', 'wS']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/'+piece+'.png'), (SQ_SIZE, SQ_SIZE))
    #Note: We can access an image by saying IMAGES[piece], the size can be reset by SQ_SIZE * shape


'''
The main driver for our code, This will handle user input and updating the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = WES_Engine.WES_State()
    moveMade = True # True for wolf and False for Sheep
    moveturn = ['bW', 'wS']


    loadImages() # only load images once before the while loop
    running = True

    sqSelection = () # no square is selected, keep track of the last click of the user{tuple: (row, col)}
    playerClicks = [] # keey track of player clicks {two tuples:[(2,3), (3,3)]}


    font = p.font.init()
    my_font = p.font.SysFont('Comic Sans MS', 30)
    p.display.set_caption('Wolves Eat Sheep')

    if PLAY_ROLE[0] + PLAY_ROLE[1] == 2:
        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                # mouse handler
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos() #(x, y) ->location of mouse[[0,0],...[4,4]] from left top to right bottom
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    #print(row, col)
                    #print(playerClicks)
                    if sqSelection == (row, col): # the user clicked the same square twice
                        sqSelection = () # deselect
                        playerClicks = [] # clear player click
                    else:
                        sqSelection = (row, col)
                        playerClicks.append(sqSelection) # append for both 1st and 2nd clicks
                    if len(playerClicks) == 2: # after 2nd click
                        move = WES_Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        #print(move.getChessNotation())
                        if gs.getValidMoves(move, moveMade):
                            gs.makeMove(move)
                            moveMade = not moveMade
                            #print(moveMade, '1111')
                            sqSelection = () # reset user clicks
                            playerClicks = []
                        else:
                            sqSelection = ()  # reset user clicks
                            playerClicks = []


                #key handler
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z: # undo when 'z' is pressed
                        gs.undoMove()

            drawGameState(screen, gs)
            clock.tick(MAX_FPS)
            winner = gs.checkWinning()
            if winner != 0:
                if winner == 1:
                    surface_1 = my_font.render('Wolves Win!', False, (220, 0, 0))
                    surface_2 = my_font.render('Click Anywhere for A New Game', False, (220, 0, 0))
                    screen.blit(surface_1, (1.7 * SQ_SIZE, 2 * SQ_SIZE))
                    screen.blit(surface_2, (0.2 * SQ_SIZE, 2.4 * SQ_SIZE))
                    if e.type == p.MOUSEBUTTONDOWN:
                        gs.board = initial_board
                if winner == 2:
                    surface_1 = my_font.render('Sheep Win!', False, (220, 0, 0))
                    surface_2 = my_font.render('Click Anywhere for A New Game', False, (220, 0, 0))
                    screen.blit(surface_1, (1.7 * SQ_SIZE, 2 * SQ_SIZE))
                    screen.blit(surface_2, (0.2 * SQ_SIZE, 2.4 * SQ_SIZE))
                    if e.type == p.MOUSEBUTTONDOWN:
                        gs.board = initial_board

            p.display.flip()




'''
Responsible for all graphics within a current game state
'''


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

'''
Draw the squares on the board
'''
def drawBoard(screen):
    colors = [p.Color('lightgreen'), p.Color('lightblue')]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draw the pieces on the board using the current game state on board
'''
def drawPieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def test():
    gs = WES_Engine.WES_State()
    print(gs.checkWinning())


main()
#test()