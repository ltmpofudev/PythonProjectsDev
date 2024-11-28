# Python Class 2965
# Lesson 8 Problem 3 Part (b)
# Author: STEMLion (586980)

# Python Class 2965
# Lesson 8 Problem 3 Part (a)
# Author: STEMLion (586980)

from tkinter import *
import random

class GUIDieO(Canvas):
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
        pipList = [[(1,1)],[(0,0),(2,2)],[(0,0),(1,1),(2,2)],[(0,0),(0,2),(2,0),(2,2)]
                   ,[(0,0),(0,2),(1,1),(2,0),(2,2)],[(0,0),(0,2),(1,0),(1,2),(2,0),(2,2)]]
        
        for location in pipList[self.get_top()-1]:
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

class GUIDie(GUIDieO):
    '''a GUIDie that can be "frozen" so that it can't be rolled'''

    def __init__(self,master,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIFreezeableDie(master,[valueList,colorList]) -> GUIFreezeableDie
        creates a GUI 6-sided freeze-able die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        GUIDieO.__init__(self,master,valueList,colorList)
        self.isFrozen = False

    def is_frozen(self):
        '''GUIFreezeableDie.is_frozen() -> bool
        returns True if the die is frozen, False otherwise'''
        return self.isFrozen
    
    def freezeDie(self):
        '''GUIFreezeableDie.toggle_freeze()
        toggles the frozen status'''
        self.isFrozen = not self.isFrozen
        self.config(background = ['gray','white'][[True,False].index(self.isFrozen)])

    def roll(self):
        '''GuiFreezeableDie.roll()
        overloads GUIDie.roll() to not allow a roll if frozen'''
        if not self.isFrozen:
            super().roll()

class DiscusFrame(Frame):

    def __init__(self,master,name):
        Frame.__init__(self,master)
        self.grid()
        Label(self,text=name,font=('Arial',11)).grid(row=0,column=0,columnspan=3,sticky=W)
        self.scoreLabel = Label(self,text='Attempt #1 Score: 0',font=('Arial',15))
        self.scoreLabel.grid(row=0,column=2,columnspan=2)
        self.highScoreLabel = Label(self,text='High Score: 0',font=('Arial',15))
        self.highScoreLabel.grid(row=0,column=6,columnspan=1,sticky=E)
        self.scores = [0,0,0]
        self.attempt = 1
        self.highScore = 0
        self.dice = [GUIDie(self,[1,2,3,4,5,6],['red','black','red','black','red','black']) for i in range(5)]

        for die in self.dice:
            die.grid(row=1,column=self.dice.index(die))
            
        self.rollButton = Button(self,text='Roll',command=self.roll)
        self.rollButton.grid(row=1,columnspan=1,column=6)
        self.stopButton = Button(self,text='Stop',state=DISABLED,command=self.stop)
        self.stopButton.grid(row=2,columnspan=1,column=6)
        self.foulButton = Button(self,text='Foul',state=DISABLED,command=self.stop)
        self.freezeButtons = []
        for n in range(0,5):
            self.freezeButtons.append(Button(self,text='Freeze',state=DISABLED,command=self.dice[n].freezeDie))
        for button in self.freezeButtons:
            button.grid(row=2,columnspan=1,column=self.freezeButtons.index(button))
            
    def roll(self):
        for freezeBtn in self.freezeButtons:
            freezeBtn['state'] = DISABLED
            
        for die in self.dice:
            die.roll()
        
        if self.stopButton['state'] == DISABLED:
            self.stopButton['state'] = ACTIVE

        self.frozenCount = self.find_score()
        self.redsCount = 0
        
        for die in self.dice:
            if self.dice[self.dice.index(die)].get_top() in [2,4,6] and not die.is_frozen():
                self.freezeButtons[self.dice.index(die)]['state'] = ACTIVE
            if die.get_top() in [1,3,5]:
                self.redsCount += 1
                
        # add dice to score and update the scoreboard
        if False:
            self.scores[self.attempt-1] = 0
            self.scoreLabel['text'] = 'Attempt #'+str(self.attempt)+' Score: '+str(score)
            self.foulButton['state'] = ACTIVE

            self.rollButton['state'] = DISABLED
            self.scoreLabel['text'] = 'Fouled Attempt'
            return
        
        self.scoreLabel['text'] = 'Attempt #'+str(self.attempt)+' Score: '+str(self.scores[self.attempt-1])
        self.round()

    def round(self):
        if self.frozenCount + self.redsCount < 5:
            self.rollButton['state'] = ACTIVE
            self.stopButton['state'] = ACTIVE
        else:
            if self.redsCount > 0:
                self.scores[self.attempt-1] = 0
                self.foulButton.grid(column=6,row=2,columnspan=1)
                self.foulButton['state'] = ACTIVE
                self.rollButton['state'] = DISABLED
                self.stopButton.grid_forget()
                self.scoreLabel['text'] = 'Fouled Attempt'
            else:
                self.stop()
            
    def find_score(self):
        count = 0
        self.scores[self.attempt-1] = 0
        for die in self.dice:
            if die.is_frozen():
                count += 1
                self.scores[self.attempt-1] += die.get_top()
        return count
    
    def stop(self):
        count = 0
        for die in self.dice:
            if die.get_top() not in [1,3,5]:
                count += 1
        if count == 5:
           self.find_score()
        for die in self.dice:
            die.erase()
            if die.is_frozen():
                die.freezeDie()
        if self.attempt == 3:
            self.attempt += 1
            self.rollButton.grid_remove()
            self.stopButton.grid_remove()
            self.foulButton.grid_remove()
            self.scoreLabel['text'] = 'Game Over'
            self.scoreLabel.config(font=('Arial',18))
            self.scoreLabel.grid(row=1,column=0,columnspan=8)
            
        elif self.attempt < 3:
            self.attempt += 1
            self.rollButton['state'] = ACTIVE
            self.stopButton['state'] = DISABLED
            self.foulButton['state'] = DISABLED
            self.foulButton.grid_forget()
            self.scoreLabel['text'] = 'Attempt #'+str(self.attempt)+' Score: '+str(self.scores[self.attempt-1])

        for score in self.scores:
            if score > self.highScore:
                self.highScore = score
                self.highScoreLabel['text'] = self.highScoreLabel['text'][:12]+str(score)

name = input('Enter your name: ')
root = Tk()
game = DiscusFrame(root,name)
game.mainloop()
