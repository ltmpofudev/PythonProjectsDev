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
        # store the valuelist and colorlist
        self.valueList = valueList
        self.colorList = colorList
        # initialize the top value
        self.top = 1

    def get_top(self):
        '''GUIDie.get_top() -> int
        returns the value on the die'''
        return self.valueList[self.top-1]

    def roll(self):
        '''GUIDie.roll()
        rolls the die'''
        self.top = random.randrange(1,7)
        self.draw()

    def draw(self):
        '''GUIDie.draw()
        draws the pips on the die'''
        # clear old pips first
        self.erase()
        # location of which pips should be drawn
        pipList = [[(1,1)],
                   [(0,0),(2,2)],
                   [(0,0),(1,1),(2,2)],
                   [(0,0),(0,2),(2,0),(2,2)],
                   [(0,0),(0,2),(1,1),(2,0),(2,2)],
                   [(0,0),(0,2),(1,0),(1,2),(2,0),(2,2)]]
        for location in pipList[self.top-1]:
            self.draw_pip(location,self.colorList[self.top-1])

    def draw_pip(self,location,color):
        '''GUIDie.draw_pip(location,color)
        draws a pip at (row,col) given by location, with given color'''
        (centerx,centery) = (15+20*location[1],15+20*location[0])  # center
        self.create_oval(centerx-5,centery-5,centerx+5,centery+5,fill=color)

    def erase(self):
        '''GUIDie.erase()
        erases all the pips'''
        pipList = self.find_all()
        for pip in pipList:
            self.delete(pip)

            
class ShotPutFrame(Frame):
    '''Frame for ShotPut Game'''
    
    def __init__(self,master,name):
        '''ShotPutFrame(master,name) uses GUIDie to create
          GUI shotput game'''
        Frame.__init__(self,master)
        self.grid()
        
        #creates a label to display the player's name
        Label(self,text=name,font=('Arial',18)).grid(row=0,column=0,columnspan=3,sticky=W)
        
        #we make a label to display the player's score for the current round
        self.scoreLabel = Label(self,text='Attempt #1 Score: 0',font=('Arial',15))
        self.scoreLabel.grid(row=0,column=2,columnspan=3)
        
        #we make a label to display the player's overall highest score
        self.highScoreLabel = Label(self,text='High Score: 0',font=('Arial',17))
        self.highScoreLabel.grid(row=0,column=6,columnspan=2,sticky=E)
        
        self.scores = [0,0,0] #we make the rounds, attempts, and scores
        self.gameround = 0
        self.attempt = 1
        self.highScore = 0
        self.dice = [GUIDie(self,[1,2,3,4,5,6],['red']+['black']*5) for i in range(8)]

        #places eace die in the dice list on the frame
        for die in self.dice:
            die.grid(row=1,column=self.dice.index(die))
            
        self.rollButton = Button(self,text='Roll',command=self.roll)#we create the buttons to roll, stop, and foul
        self.rollButton.grid(row=2,columnspan=1) 
        self.stopButton = Button(self,text='Stop',state=DISABLED,command=self.stop)
        self.stopButton.grid(row=3,columnspan=1)
        self.foulButton = Button(self,text='Foul',state=DISABLED,command=self.stop)

    def roll(self):
        '''Rolls current die and sets up widgets'''
        
        #we need to roll the die for this round
        self.dice[self.gameround].roll()
            
        #we need to activate the stopButton if it is disabled
        if self.stopButton['state'] == DISABLED:
            self.stopButton['state'] = ACTIVE

        #if the rolled value is a one
        if self.dice[self.gameround].get_top() == 1:
            
            #we need to set the score for the attempt to 0
            self.scores[self.attempt-1] = 0
            
            #activate foulButton
            self.foulButton['state'] = ACTIVE
            self.foulButton.grid(row=3,column=self.gameround,columnspan=1)
            
            #remove stopButton
            self.stopButton.grid_forget()
            
            #disable rollButton
            self.rollButton['state'] = DISABLED
            
            #update scoreLabel text
            self.scoreLabel['text'] = 'Fouled Attempt'
            return
        
        self.scores[self.attempt-1] += self.dice[self.gameround].get_top() #update list of scores
        self.scoreLabel['text'] = 'Attempt #'+str(self.attempt)+' Score: '+str(self.scores[self.attempt-1]) #update score
        self.gameround += 1  # go to next round
        
        if self.gameround < 8:  # move buttons to next pair of dice
            self.rollButton.grid(row=2,column=self.gameround,columnspan=1)
            self.stopButton.grid(row=3,column=self.gameround,columnspan=1)
            #set state of buttons
            self.rollButton['state'] = ACTIVE
            self.stopButton['state'] = ACTIVE
            if self.gameround == 0:
                self.stopButton['state'] = DISABLED
            self.foulButton['state'] = DISABLED
        
        #if the rounds are complete
        else:
            self.stop()
            
    def stop(self):
        '''Function that runs whenever there is a foul, the user stops, or the game ends'''
        for die in self.dice:
            die.erase()
        
        #if the game is over
        if self.attempt == 3:
            
            #we need to delete all buttons
            for button in [self.rollButton,self.stopButton,self.foulButton]:
                button.destroy()  
                
            #write the text that says that the game is over and place the text in its correct location
            self.scoreLabel.config(text='Game Over',font=('Arial',18))
            self.scoreLabel.grid(row=1,column=0,columnspan=8)
           
        #if the game is still running    
        elif self.attempt < 3:
            self.gameround = 0 # reset gameround object
            
            #setting state of buttons
            self.rollButton['state'] = ACTIVE
            self.stopButton['state'] = DISABLED
            self.foulButton['state'] = DISABLED
            
            #placing button on screen in its correct place, or removing button
            self.rollButton.grid(row=2,column=self.gameround,columnspan=1)
            self.stopButton.grid(row=3,column=self.gameround,columnspan=1)
            self.foulButton.grid_forget()
            
            #changing the score label text
            self.scoreLabel['text'] = 'Attempt #'+str(self.attempt)+' Score: '+str(self.scores[self.attempt])

        self.attempt += 1#adding 1 to the attempt count
        
        #finding high score and updating label
        self.highScoreLabel['text'] = self.highScoreLabel['text'][:12]+str(max(self.scores))#displaying high score

name = input('Enter your name: ')
root = Tk()
game = ShotPutFrame(root,name)
game.mainloop()
