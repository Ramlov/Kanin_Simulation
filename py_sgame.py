import pygame
import os
import random
import sys
import numpy as np
from button import Button

'''
Unfortunately due to the way PyGame is created, it is not possible to created the game without a
little bit of global variables. In the main code, there are none, but here was it simply not possible.
'''



pygame.init()
#Define game windows settings
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Kanin Hop Hop")
FPS = 60 #Variable for locking the Frames per second in the game
GARDEN = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'background.png')), (WIDTH, HEIGHT))

#Define system settings
FONT = pygame.font.SysFont("monospace", 25)
BG = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'Background1.png')), (WIDTH, HEIGHT))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

#Define game settings
holecordinates = {'Green': (609,62), 'Red': (356,207), 'Purple':(366,500), 'Yellow': (529,681), 'Blue': (1067, 58)}
holes = {'Red': 0, 'Green': 0, 'Blue': 0, 'Purple': 0, 'Yellow': 0}
rabbit_IMAGE = pygame.image.load(
    os.path.join('assets', 'rabbit.png')) #Loading the rabbit
rabbit_IMAGE = pygame.transform.scale(rabbit_IMAGE, (55, 80)) #WIDTH and HEIGHT of the image of the rabbit

color = 'normal'
listen = []
nop = 3
score = {}
winner = None

def generate():
    '''Here the rabbits in the hole is random generated.'''
    global listen
    global score
    for i in range(20):
        rabbit = (np.random.randint(600,960), np.random.randint(200,500))
        listen.append(rabbit)
    for i in range(nop):
        varplayer = 'Player'+str(i+1)
        score[varplayer] = 0
    return listen
    #pygame.display.update()

hasbeenrun = False
rabbitsleft = 20
curplayer = 1
def updaterabbit(color):
    '''Function to check for the rabbits placement and the score updating'''
    global rabbitsleft
    global curplayer
    color = color
    if rabbitsleft > 0:
        if holes[color] == 1:
            coor = holecordinates.get(color)
            holes[color] = 0
            try:
                listen.remove(coor)
            except Exception:
                print(Exception)
            varplayer = 'Player'+str(curplayer)    
            score.update({varplayer: score.get(varplayer)+1})
            if curplayer == nop:
                curplayer = 1
            else:
                curplayer +=1
            
        else:
            if curplayer == nop:
                curplayer = 1
            else:
                curplayer +=1
            listen.pop(0)
            listen.append(holecordinates.get(color))
            rabbitsleft -=1
            holes[color] = 1
    else:
        return score


def draw_window():
    '''Function to draw the game window'''
    global hasbeenrun
    if not hasbeenrun:
        generate()
        hasbeenrun = True
    WIN.blit(GARDEN, (0, 0))
    WIN.blit(FONT.render("Score:", 1, (255,255,255)), (60, 165))
    lenght = 195
    for i in range(nop):
        WIN.blit(FONT.render(f'Player{i+1}:{score.get("Player"+str(i+1))}', 1, (255,255,255)), (60, lenght))
        lenght += 30
    objects[0].process()
    for i in range(len(listen)):
        WIN.blit(rabbit_IMAGE, listen[i])
    if winner != None:
        winners = [key for key, value in score.items() if value == max(score.values())]
        string = ""
        for i in range(len(winners)):
            string += winners[i]+" "
        WINNER_TEXT = get_font(45).render(f'Winner is {string}', True, "White")
        WINNER_RECT = WINNER_TEXT.get_rect(center=(640, 210))
        WIN.blit(WINNER_TEXT, WINNER_RECT)
        #WIN.blit(FONT.render(f'Winner is {string}', 2, (255,255,255)), (WIDTH/2, HEIGHT/2))
    pygame.display.update()

def play():
    '''Handling the press of the play button'''
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            draw_window()
    pygame.quit()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def options():
    '''This is option screen'''
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        WIN.fill("grey")

        OPTIONS_TEXT = get_font(45).render("Settings: (Players)", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 210))
        PLAYER_TEXT = get_font(25).render(f'There is now {nop} players', True, "Black")
        PLAYER_RECT = PLAYER_TEXT.get_rect(center=(640, 250))
        WIN.blit(PLAYER_TEXT, PLAYER_RECT)
        WIN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            objects[1].process()
            objects[2].process()



            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

            pygame.display.update()



def main_menu():
    '''This is the main menu screen'''
    running = True
    while running:
        WIN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running = False
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running = False
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running = False
                    pygame.quit()
                    sys.exit()

        pygame.display.update() #There is an error here. This is a known bug in PyGame :(



        



objects = []

class But():
    '''Creating a class to create some buttons'''
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
            'Red': '#ff0000',
            'Green': '#007806',
            'Blue': '#1a0099',
            'Purple': '#610099',
            'Yellow': '#fffb00',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = FONT.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()
        
        self.buttonSurface.fill(self.fillColors[color])
        if self.buttonRect.collidepoint(mousePos):
            #self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        WIN.blit(self.buttonSurface, self.buttonRect)

def funccolor():
    '''The function which returns a color, also used as the dice'''

    global color
    global winner
    local_dice = ['Red', 'Green', 'Blue', 'Purple', 'Yellow']
    color = random.choice(local_dice)
    winner = updaterabbit(color)

def player_plus():
    '''Add more players'''
    global nop
    if nop < 6:
        nop += 1

def player_minus():
    '''Remove players'''
    global nop
    if nop > 1:
        nop -= 1

dice = But(1000, 600, 100, 100, 'Dice', funccolor) #The button for the dice
nop_minus = But(680, 300, 100, 100, '1-', player_minus)
nop_minus = But(480, 300, 100, 100, '1+', player_plus)
