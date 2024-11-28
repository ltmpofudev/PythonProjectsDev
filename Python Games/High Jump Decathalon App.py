from tkinter import *
import random
 
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

class DecathHighJumpFrame(Frame):

    def __init__(self,master,name):
        Frame.__init__(self,master)
        self.grid()
        Label(self,text=name,font=('Arial',10)).grid(row=0,column=0,columnspan=3,sticky=W)
        self.jumpInfo = Label(self,text='Jump Info: 0 Failed Attempts',font=('Arial',8))
        self.jumpInfo.grid(row=0,column=1,columnspan=3)
        self.scoreLabel = Label(self,text='Jumps: 0',font=('Arial',10))
        self.scoreLabel.grid(row=0,column=4,columnspan=1)
        self.heightLabel = Label(self,text='Height: 10',font=('Arial',10))
        self.heightLabel.grid(row=0,column=5,columnspan=2,sticky=E)
        self.score = 0
        self.jumps = 0
        self.height = 10
        self.gameround = 0
        self.fails = 0
        self.dice = [GUIDie(self,[1,2,3,4,5,6],['black']*6) for i in range(5)]

        for die in self.dice:
            die.grid(row=1,column=self.dice.index(die))
            
        self.rollButton = Button(self,text='Roll',command=self.roll)
        self.rollButton.grid(row=1,columnspan=1,column=5)
        self.keepButton = Button(self,text='Keep',state=DISABLED,command=self.keep)
        self.keepButton.grid(row=1,columnspan=1,column=6)

    def roll(self):
        self.jumps += 1
        for die in self.dice:
            die.roll()
        if self.keepButton['state'] == DISABLED and self.dice_sum() >= self.height:
            self.keepButton['state'] = ACTIVE
            self.scoreLabel['text'] = 'Jumps: '+str(self.jumps)
            self.rollButton['state'] = DISABLED
        if self.dice_sum() < self.height:
            self.fails += 1
        if self.fails == 3:
            self.end('lost...')
        self.jumpInfo['text'] = 'Jump Info: '+str(self.fails)+' Failed Attempts'

    def dice_sum(self):
        sum = 0
        for die in self.dice:
            sum += die.get_top()
        return sum
    def keep(self):
        '''Decath400MFrame.keep()
        handler method for the keep button click'''
        # add dice to score and update the scoreboard
        self.fails = 0
        self.score += self.dice[self.gameround].get_top()
        self.height += 2  # go to next height
        self.heightLabel['text'] = 'Height: '+str(self.height)
        if self.height < 30:  # move buttons to next pair of dice
            self.rollButton['state'] = ACTIVE
            self.keepButton['state'] = DISABLED
        else:
            self.end('Won!')
            
    def end(self,state):
        self.keepButton['state'] = DISABLED
        self.rollButton['state'] = DISABLED
        self.jumpInfo['text'] = 'Game over\nYou '+str(state)
        while True:
            root.update()

root = Tk()
DecathHighJumpFrame(root,'STEMLion')
root.mainloop()
