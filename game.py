import random
import matplotlib.pyplot as plt
import numpy as np
from time import time

rabbit = 20 #Variable for saving the count of rabbits
players = {} #Dictonary for saving the players and the score
hole = {'Red': 0, 'Green': 0, 'Blue': 0, 'Purple': 0, 'Yellow': 0,'Rabbit': 1}  #The dictonary for keeping track of the holes

class Main():
    '''Creating a class, to handle the single game, and the data within every single game'''
    def __init__(self) -> None:
        '''Using the class function init to only create these self variables to use within the class.'''
        self.hole = hole
        self.players = players
        self.rabbit = rabbit
        self.curplayer = 1

    def __call__(self, players, hole) -> None:
        '''Using the call functions to call in the new variables for each game generation'''
        self.players = players
        self.hole = hole

    def game(self, nop, gamemode):
        '''In the game function each game is beeing run'''
        if nop>0:
            for i in range(nop): #This loop creates the dictonary with the players. Might look like this players = {'Player1': 0, 'Player2': 0}
                varplayer = 'Player'+str(i+1)
                self.players[varplayer] = 0
                

        while self.rabbit > 0: #This is the main gameloop which is beeing run while there is more than 0 rabbits left.
            color = main.dice()
            varplay = 'Player'+str(self.curplayer)
            if color == 'Rabbit':
                if gamemode == 'Fast':
                    while color == 'Rabbit' and self.rabbit !=0:
                        self.players[varplay] = self.players[varplay]+1
                        self.rabbit = self.rabbit-1
                        color = main.dice()
                elif gamemode == 'Normal':
                    self.players[varplay] = self.players[varplay]+1
                    self.rabbit = self.rabbit-1
                elif gamemode == 'Slow':
                    self.players[varplay] = self.players[varplay]-1
                    self.rabbit = self.rabbit+1
            if color != 'Rabbit':
                if self.hole[color]==1:
                    self.players[varplay] = self.players[varplay]+1
                    self.hole[color]=0
                else:
                    self.hole[color]=1
                    self.rabbit = self.rabbit-1
            self.curplayer += 1
            if self.curplayer > nop:
                self.curplayer = 1


    def reset(self):
        '''Function for resetting the gamevalues after each generation'''
        players = {}
        self.rabbit = 20
        self.curplayer = 1
        hole = {'Red': 0, 'Green': 0, 'Blue': 0, 'Purple': 0, 'Yellow': 0,'Rabbit': 1}
        return players, hole

    def dice(self):
        '''Using the random.choice for selecting a pseudo random value from a list.'''
        local_dice = ['Red', 'Green', 'Blue', 'Purple', 'Yellow', 'Rabbit']
        return random.choice(local_dice)


    def updatewin(self, listofwins):
        '''Here the winner(s) is defined after each game, and a total win is added to the winner(s)'''
        winner = [key for key, value in self.players.items() if value == max(self.players.values())]
        for key in winner:
            p = key.split("r")
            p = int((p[1]))-1
            listofwins[p]=listofwins[p]+1

main = Main() #Attribute to class




def monte_carlo(generations, nop, gamemode): 
    '''Here is the monte_carlo method for calculating each players win chance after each game'''
    listofprocent = []
    listofwins = []
    for k in range(nop):
        listofprocent.append( [] )
        listofwins.append(0)
    for k in range(generations):
        players, hole = main.reset()
        main(players, hole)
        main.game(nop, gamemode)
        main.updatewin(listofwins)
        for i in range(nop):
            v = listofwins[i]
            procent = (v/(k+1))*100
            listofprocent[i].append(procent)
    return listofprocent

def confidence_interval(generations, listofprocent):
    '''Here the confidence interval is beeing calculated'''
    con_int = []
    for j in range(len(listofprocent)):
        con_int.append([])
        for jj in range(len(listofprocent[j])):
            listofprocent[j][jj] = listofprocent[j][jj]/100
            con_P = listofprocent[j][jj]+1.96*np.sqrt((listofprocent[j][jj]*(1-listofprocent[j][jj]))/generations)
            con_M = listofprocent[j][jj]-1.96*np.sqrt((listofprocent[j][jj]*(1-listofprocent[j][jj]))/generations)
            con_int[j].append([con_P, con_M])
    return con_int

def run(generations, nop, gamemode, con_int=False):
    '''Here is the main run function, this passes values back to the GUI'''
    starttime = time()
    datapoints = monte_carlo(generations, nop, gamemode)
    playerwins = []
    for k in range(len(datapoints)):
        playerwins.append(datapoints[k][-1])
    confidence_int = confidence_interval(generations, datapoints)
    
    fig, ax = plt.subplots()
    ax.set_facecolor('#324e7b')
    fig.set_facecolor('#324e7b')
    ax.set_ylabel('Probability of winning %', color='white')
    ax.set_xlabel('Number of generations', color='white')
    ax.set_title('Simulation of Kanin Hop Hop', color='white')

    for xtick in ax.get_xticklabels():         
        xtick.set_color('white')     
    for ytick in ax.get_yticklabels():        
        ytick.set_color('white')

    for i in range(len(datapoints)):
        ax.plot(datapoints[i], label=f'Player{i+1} - {round(datapoints[i][-2]*100, 0)}%')
        if con_int == True:
            for g in range(len(confidence_int)):
                con_in = confidence_int[g]
                ax.plot(con_in, color='white', linestyle='--', linewidth=0.1)
    ax.legend()
    end = time()
    exectime = end-starttime

    return(fig, exectime, playerwins)

