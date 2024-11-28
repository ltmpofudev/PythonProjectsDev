# Python Class 2965
# Lesson 8 Problem 1 Part (b)
# Author: STEMLion (586980)

from tkinter import *
import random
import cgitb
cgitb.enable()
 
class GUIDie(Canvas):
    '''6-sided Die class for GUI'''
 
    def __init__(self,master,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIDie(master,[valueList,colorList]) -> GUIDie
        creates a GUI 6-sided die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        # create a 60x60 white canvas with a 5-pixel grooved border
        Canvas.__init__(self,master,width=60,height=60,bg='white',\
                        bd=5,relief=GROOVE)
        master.update()
        # store the valuelist and colorlist
        self.valueList = valueList
        self.colorList = colorList
        # initialize the top side
        self.top = 1
        
    def get_top(self):
        return self.valueList[self.top-1]
    
    def roll(self):
        self.top = random.randint(1,6)
        self.draw()

    def draw(self):
        self.erase()
        pipList = [[(1,1)]
                   ,[(0,0),(2,2)]
                   ,[(0,0),(1,1),(2,2)]
                   ,[(0,0),(0,2),(2,0),(2,2)]
                   ,[(0,0),(0,2),(1,1),(2,0),(2,2)]
                   ,[(0,0),(0,2),(1,0),(1,2),(2,0),(2,2)]]
        
        for location in pipList[self.top-1]:
            self.draw_pip(location,self.colorList[self.top-1])

    def draw_pip(self,coords,color):
        coordsBank = [15,35,55]
        self.create_oval((coordsBank[coords[0]]-5)\
                           ,(coordsBank[coords[1]]-5)\
                           ,(coordsBank[coords[0]]+5)\
                           ,(coordsBank[coords[1]]+5)\
                           ,fill=color)
    def erase(self):
        pipList = self.find_all()
        for pip in pipList:
            self.delete(pip)

class Decath1500MFrame(Frame):

    def __init__(self,master,name):
        Frame.__init__(self,master)
        self.grid()
        Label(self,text=name,font=('Arial',18)).grid(row=0,column=0,columnspan=3,sticky=W)
        self.scoreLabel = Label(self,text='Score: 0',font=('Arial',18))
        self.scoreLabel.grid(row=0,column=3,columnspan=2)
        self.rerollLabel = Label(self,text='Rerolls: 5',font=('Arial',18))
        self.rerollLabel.grid(row=0,column=5,columnspan=3,sticky=E)
        self.score = 0
        self.rerolls = 5
        self.gameround = 0
        self.dice = [GUIDie(self,[1,2,3,4,5,-6],['black']*5+['red']) for i in range(8)]

        for die in self.dice:
            die.grid(row=1,column=self.dice.index(die))
            
        self.rollButton = Button(self,text='Roll',command=self.roll)
        self.rollButton.grid(row=2,columnspan=1)
        self.keepButton = Button(self,text='Keep',state=DISABLED,command=self.keep)
        self.keepButton.grid(row=3,columnspan=1)

    def roll(self):
        self.dice[self.gameround].roll()
        if self.keepButton['state'] == DISABLED:
            self.keepButton['state'] = ACTIVE
        elif self.keepButton['state'] == ACTIVE:
            self.rerolls -= 1
            self.rerollLabel['text'] = 'Rerolls: '+str(self.rerolls)
            if self.rerolls == 0:
                self.rollButton['state'] = DISABLED
                
    def keep(self):
        '''Decath400MFrame.keep()
        handler method for the keep button click'''
        # add dice to score and update the scoreboard
        self.score += self.dice[self.gameround].get_top()
        self.scoreLabel['text'] = 'Score: '+str(self.score)
        self.gameround += 1  # go to next round
        if self.gameround < 8:  # move buttons to next pair of dice
            self.rollButton.grid(row=2,column=self.gameround,columnspan=1)
            self.keepButton.grid(row=3,column=self.gameround,columnspan=1)
            self.rollButton['state'] = ACTIVE
            self.keepButton['state'] = DISABLED
        else:  # game over
            self.keepButton.grid_remove()
            self.rollButton.grid_remove()
            self.rerollLabel['text'] = 'Game over'

name = input('Enter your name:')
root = Tk()
game = Decath1500MFrame(root,name)
game.mainloop()
