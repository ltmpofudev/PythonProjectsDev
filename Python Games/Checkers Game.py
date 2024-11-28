'''importing all modules'''
from tkinter import *
import time,random


class CheckerSquare(Canvas):
    '''Implements a canvas(square) in a checker game
        Square has a text feature when kinged, and
        always has a circle'''
    
    def __init__(self,master,x,y,anchor,color='black'):
        '''We setup the square, and all needed variables'''

        #creating canvas
        Canvas.__init__(self,master,width=50,height=50,bg=color,bd=2,highlightbackground=color)

        #adding the canvas to the master canvas so that we can see it
        master.create_window(x+4,y+4,anchor=anchor,window=self)

        #binding all buttons/keys
        self.bind('<Button-1>',self.pressed)
        self.bind('<Button-2>',self.unpressed)
        self.bind('<Button-3>',self.unpressed)

        #creating all of our good variables 
        self.color = color
        self.clickable = True
        self.kinged = False

    def pressed(self,event):
        '''shows the user that the square has been selected when the square is selected'''
        if self['state'] == 'normal': #if this button was just pressed...
            #we move the circle down(looks good)
            coords = self.coords(1)
            self.move(1,(coords[0]-5),(coords[3]-45))
            
            if len(self.find_all()) > 1:#we move the astrik down(looks good) - if there is one
                coords = self.coords(self.find_all()[1])
                self.move(self.find_all()[1],(coords[0]-25),(coords[1]-35))

            #we show the actual graphics for the canvas square being pressed
            self.config(highlightthickness=5,highlightbackground='black',relief=SUNKEN,state='disabled')

    def unpressed(self,event):
        '''shows the user that the square which was previously shown as selected, is unselected'''
        if self['state'] == 'disabled': #if this button was just "unpressed"...
            
            #we move the circle up(looks good)
            coords = self.coords(1)
            self.move(1,-(coords[0]-8),-(coords[3]-48))
            
            if len(self.find_all()) > 1:#we move the astrik up(looks good) - if there is one
                coords = self.coords(self.find_all()[1])
                self.move(self.find_all()[1],-(coords[0]-28),-(coords[1]-38))

            #we show the actual graphics for the canvas square being "unpressed"
            self.config(highlightthickness=2,relief=FLAT,bd=2,highlightbackground=self.color,state='normal')

    def is_clickable(self):
        '''returns clickable object'''
        return self.clickable

    def set_clickable(self,able):
        '''sets clickable object to the able parameter'''
        self.clickable = able
        
    def set_king(self,king):
        '''sets kinged object to the able parameter'''
        self.kinged = king

        if self.kinged == True and len(self.find_all()) == 1: #creates text to show that square is kinged if square is kinged
            self.text = self.create_text(28,38,text='*',font=('LCD',40,'bold'),tag="txt")
        if self.kinged == False and len(self.find_all()) > 1: #if square isn't kinged, deletes any text that may be there
            self.remove_text()
            
    def remove_text(self):
        '''removes the kinged text'''
        self.delete("txt")
        
    def is_king(self):
        '''returns kinged object'''
        return self.kinged

    def get_color(self):
        '''returns color object'''
        return self.color
    
class CheckerBoard(Canvas):        
    '''Implements a checkerboard with checkersquares in tkinter'''
    def __init__(self,master):
        '''Sets everything up'''

        #creating the canvas
        Canvas.__init__(self,master,width=450,height=450,highlightthickness=4, highlightbackground="black")

        #adding a master object that is the master window (for future refrence)
        self.master = master

        self.master.update()
        #finding the current turn, and color
        self.curTurn = random.choice([0,1])
        self.cols = ['orange','red']
        self.curCol = self.cols[self.curTurn%2]

        #setting the regMove, extraJump, and moveChoice variables for future refrence
        self.regMove = False
        self.extraJump = [False,'none',0]
        #self.moveChoice = 'none'

        #creating the tkinter objects to display the current turn and color
        self.text_var = StringVar()
        self.text_var.set("It is "+self.curCol[0].upper()+self.curCol[1:]+"'s Turn")
        self.turnCounter = Canvas(master,width=50,height=50,bg='yellow',relief=RAISED,bd=2,highlightbackground='yellow',state='disabled')
        self.turnCounter.create_oval(8,8,48,48,fill=self.curCol,outline='black',width=2)
        self.infoLbl = Label(master,textvariable=self.text_var,font=('LCD',17,'bold'),bg='yellow')
        self.infoLbl.grid(row=0,column=1,columnspan=1)
        self.turnLabel = Label(master,text='\'s turn.',font=('LCD',17,'bold'),bg='yellow')
        self.turnLabel.place(relx=0.54,rely=0.88)
        self.turnCounter.grid(row=2,column=1)

        #setting the variables for buttons
        self.forfietVar = False
        self.restartVar = False
        self.exitVar = False
        self.quitVar = False
        self.rulesVar = False

        #creating the tkinter buttons to allow users to navigate
        self.exitbtn = Button(self.master,text='Exit\nGame',command=self.exit,font=('LCD',10,'bold'),bd=3,relief=RAISED,bg='yellow',fg='purple')
        self.exitbtn.place(relx=0.03,rely=0.31)
        self.forfietbtn = Button(self.master,text='Forfiet\nGame',command=self.forfiet,font=('LCD',10,'bold'),bd=3,relief=RAISED,bg='yellow',fg='purple')
        self.forfietbtn.place(relx=0.03,rely=0.43)
        self.restartbtn = Button(self.master,text='Restart\nGame',command=self.restart,font=('LCD',10,'bold'),bd=3,relief=RAISED,bg='yellow',fg='purple')
        self.restartbtn.place(relx=0.03,rely=0.55)
        self.quitbtn = Button(self.master,text='Exit\nEverything',command=self.quit,font=('LCD',10,'bold'),bd=3,relief=RAISED,bg='yellow',fg='purple')
        self.quitbtn.place(relx=0.015,rely=0.67)
        self.rulesbtn = Button(self.master,text='View\nRules',command=self.viewRules,font=('LCD',10,'bold'),bd=3,relief=RAISED,bg='yellow',fg='purple')
        self.rulesbtn.place(relx=0.875,rely=0.49)        
        self.master.update()
        #adding the canvas to the screen
        self.grid(row=1,column=1)
        self.master.update()

        #creating a list of colors for the board
        colorlist = ['blue','light green','blue','light green','blue','light green','blue','light green']
        self.board = [CheckerSquare(self,i*56,0,'nw',colorlist[i]) for i in range(8)]
        for j in range(1,8):
            colorlist.reverse()
            self.board.extend([CheckerSquare(self,i*56,j*56,'nw',colorlist[i]) for i in range(8)])
        #we need to add the checkers to each square
        self.checkers = [square.create_oval(8,8,48,48,fill='red',width=2) for square in self.board[:len(self.board)//2]]
        self.checkers.extend([square.create_oval(8,8,48,48,fill='orange',width=2) for square in self.board[(len(self.board)//2):]])

        #we need to also change the checkers that should be blue to blue checkers and the checkers that should be green to green checkers
        for checker in self.board:
            if checker['bg'] == 'blue':
                checker.itemconfig(1,fill = 'blue',outline='blue')

            if self.board.index(checker) in [i for i in range(24,40)] and checker['bg'] == 'light green':                    
                checker.itemconfig(1,fill = 'light green',outline='light green')

        self.master.update()

    def forfiet(self):
        '''sets forfietVar object to True'''
        self.forfietVar = True

    def restart(self):
        '''sets restartVar object to True'''
        self.restartVar = True

    def exit(self):
        '''sets exitVar object to True'''
        self.exitVar = True

    def quit(self):
        '''sets quitVar object to True'''
        self.quitVar = True

    def viewRules(self):
        '''sets rules Var object to its opposite'''
        self.rulesVar = not self.rulesVar

        #if the rulesVar object has been set to False...
        if not self.rulesVar:

            #re-grid/place all objects, and remove the rulesLbl object
            self.grid(row=1,column=1)
            self.infoLbl.grid(row=0,column=1,columnspan=1)
            self.turnLabel.place(relx=0.54,rely=0.88)
            self.exitbtn.place(relx=0.03,rely=0.31)
            self.forfietbtn.place(relx=0.03,rely=0.43)
            self.restartbtn.place(relx=0.03,rely=0.55)
            self.quitbtn.place(relx=0.015,rely=0.67)
            self.rulesbtn.place(relx=0.875,rely=0.49)        
            self.turnCounter.grid(row=2,column=1)
            self.rulesbtn['text'] = 'View\nRules'
            self.rulesLbl.destroy()
            
    def findPossMoves(self,activeSquares):
        '''finds the possible jumps and returns a list of them'''
        possJumps = [] #creating a list
        for square in activeSquares: #we evaluate each square in the active board squares
            if self.board[square].is_king(): #if the square is a king
                for num in [14,-14,18,-18]: #and if we can jump an opponent's piece
                    if (-1 < square+num < 64) and self.board[square+num].itemcget(1,'fill') in ['light green'] and (self.board[square+(num//2)].itemcget(1,'fill') not in [self.curCol,'light green']):
                        possJumps.append(square) #we need to add to the possible jumps list
            else:
                    
                if self.board[square].itemcget(1,'fill') == 'orange': #if the fill of the square is orange
                     for num in [-14,-18]: #if we can jump an opponent's piece
                         if (-1 < square+num < 64) and self.board[square+num].itemcget(1,'fill') in ['light green'] and (self.board[square+(num//2)].itemcget(1,'fill') not in [self.curCol,'light green']):
                             possJumps.append(square) #add to the possJumps list
                                
                elif self.board[square].itemcget(1,'fill') == 'red': #if the fill of the square is red
                    for num in [14,18]: #if we can jump an opponent's piece
                        if (-1 < square+num < 64) and self.board[square+num].itemcget(1,'fill') in ['light green'] and (self.board[square+(num//2)].itemcget(1,'fill') not in [self.curCol,'light green']):
                            possJumps.append(square) #add to the possJumps list
                            
        return possJumps #return the possJumps list
    
    def changeTurn(self):

        #we need to find the current color
        self.curCol = self.cols[self.curTurn%2]

        #we also find the active squares
        activeSquares = [self.board.index(square) for square in self.board if square.itemcget(1, 'fill') == self.curCol]

        possJumps = []
        if self.regMove == False:
            possJumps = self.findPossMoves(activeSquares) #we make the total possJumps a list if it is not a regular move
        self.regMove = False

        #if we have no jumps in our list...       
        if len(possJumps) == 0:
            self.curTurn += 1 #we move to the next turn
            self.turnCounter.itemconfig(1,fill=self.cols[self.curTurn%2]) #change the turnCounter
            
            for square in self.board: #we make every square clickable
                square['state'] = 'normal'
                square.set_clickable(True)
                
            self.curCol = self.cols[self.curTurn%2]
            self.extraJump = [False,'none',0] #we reset the extraJump list
            self.text_var.set("It is "+self.curCol[0].upper()+self.curCol[1:]+"'s turn.") #we set the text_var object
            activeSquares = [self.board.index(square) for square in self.board if square.itemcget(1, 'fill') == self.curCol] #update the activeSquares list
            possJumps = self.findPossMoves(activeSquares) #re-evaluate the possJumps list
        
        #if there is no jump available, but there was a jump beforehand
        if self.extraJump[0] == True and self.extraJump[2] >= 1 and len(possJumps) == 1 and possJumps[0] != self.extraJump[1]:
            #we need to go through the same process as before
            self.curTurn += 1
            self.turnCounter.itemconfig(1,fill=self.cols[self.curTurn%2])
            for square in self.board:
                square['state'] = 'normal'
                square.set_clickable(True)
            self.curCol = self.cols[self.curTurn%2]
            self.extraJump = [False,'none',0]
            self.text_var.set("It is "+self.curCol[0].upper()+self.curCol[1:]+"'s turn.")
            activeSquares = [self.board.index(square) for square in self.board if square.itemcget(1, 'fill') == self.curCol]
            possJumps = self.findPossMoves(activeSquares)
            
        if len(possJumps) >= 1: #if there at least one possible jump...
            self.text_var.set(self.curCol[0].upper()+self.curCol[1:]+", You must jump your opponent") #we update the text_var object
            
            if self.extraJump[0] == True and self.extraJump[2] >= 1 and len(possJumps) > 1: #if we have multiple possible jumps
                #we disable all squares except that one square needed for executing the jump
                for square in activeSquares:
                    if square != self.extraJump[1]:
                        self.board[square]['state'] = 'disabled'
                        self.board[square].set_clickable(False)
                        return
                    
            #we disable all squares not in the possJumps list
            for square in activeSquares:
                if square not in possJumps:
                    self.board[square]['state'] = 'disabled'
                    self.board[square].set_clickable(False)
                    
    def resetSquares(self):
        '''Resets all squares to their normal state'''
        for square in self.board:
            if square.is_clickable() == True:
                square['state'] = 'normal'
    
    def disableSquares(self):
        '''Disables all opponent's squares'''
        for square in self.board:
            if square.itemcget(1, 'fill') not in [self.curCol,'light green']:
                square['state'] = 'disabled'
                    
    def deleteTXT(self,square):
        '''removes text from squares that are not kinged'''
        if square.itemcget(1,'fill') not in ['red','orange'] and len(square.find_all()) > 1:
            square.remove_text()

    def checkForKings(self):
        '''checks squares for kings all over the board'''
        for square in self.board:
            if len(square.find_all()) == 1:
                if (self.board.index(square) in [1,3,5,7] and square.itemcget(1,'fill') == 'orange') or (self.board.index(square) in [62,60,58,56] and square.itemcget(1,'fill') == 'red') or square.is_king():
                    square.set_king(True)
                    prevTXT = self.text_var.get()
                    self.text_var.set("New King")
                    self.master.update()
                    time.sleep(1)
                    self.text_var.set(prevTXT)
                    self.master.update()

            self.deleteTXT(square)
            
    def unpressAll(self,sq1,sq2,event):
        '''unpresses two squares in a given event'''
        for cir in [sq1,sq2]:
            cir.unpressed('there is a circle')
        
    def moveCircles(self,sq1,sq2):
        '''moves the checker pieces given the two clicked checkersquares'''
        #if we are trying to land on an occupied space or jump too far/too little, we need to unpress the two clicked squares 
        if sq2.itemcget(1, 'fill') in ['red','orange'] or self.board.index(sq1)-self.board.index(sq2) not in [7,9,-7,-9,14,18,-14,-18] \
           or self.board.index(sq1)-self.board.index(sq2) in [8,-8,1,-1]:
            return self.unpressAll(sq1,sq2,'cannot click this')

        #if we clicked an un-occupied square, and we did not click too far/too little...
        elif sq2.itemcget(1, 'fill') in ['blue','light green'] and self.board.index(sq1)-self.board.index(sq2) in [14,18,-14,-18,7,-7,9,-9]:

            #if we are not kinged and are trying to move in the wrong direction, we unpress the two clicked squares
            if not sq1.is_king() and \
               ((sq1.itemcget(1, 'fill') == 'red' and self.board.index(sq1)-self.board.index(sq2) not in [-7,-9,-14,-18])\
                or (sq1.itemcget(1, 'fill') == 'orange' and self.board.index(sq1)-self.board.index(sq2) not in [7,9,14,18])):
                return self.unpressAll(sq1,sq2,'cannot move backwards')
            
            #if we are attempting to jump a space
            if self.board.index(sq1)-self.board.index(sq2) in [14,-14,18,-18]:
                jumpedCirI = self.board.index(self.s1i)+((self.board.index(self.s2i)-self.board.index(self.s1i))//2)#the square we're jumping (will come in handy)

                #if we jumped air, we unpress the two clicked squares
                if self.board[jumpedCirI].itemcget(1,'fill') not in ['red','orange']:
                    return self.unpressAll(sq1,sq2,'cannot jump air')

                #we add two to the 2nd extra jump catagory, add the square we're jumping to to the 1st extra jump cat., and set extraJump[0] to True
                if self.extraJump[0] == False and self.extraJump[1] == 'none':
                    self.extraJump = [True,self.board.index(sq2),self.extraJump[2]+1]

                #we need to change the fills of the objects to implement the move
                movecol = sq1.itemcget(1, 'fill')
                erasecol = sq2['bg']
                erasecol2 = self.board[jumpedCirI]['bg']
                sq2.itemconfig(1,fill = movecol,outline="black")
                sq2.set_king(sq1.is_king())

                #we will then need to delete text, and set kings
                sq1.itemconfig(1,fill=erasecol,outline=erasecol)
                self.deleteTXT(sq1)
                sq1.set_king(False)
                self.board[jumpedCirI].set_king(False)

                #we will also need to change the fill of the middle item
                self.board[jumpedCirI].itemconfig(1,fill=erasecol2,outline=erasecol2)

                #then we unpress the two squares
                self.unpressAll(sq1,sq2,'no circle')

            #if we are making a regular move
            elif self.board.index(sq1)-self.board.index(sq2) in [7,-7,9,-9]:
                #we set regmove, and other variables
                self.regMove = True
                movecol = sq1.itemcget(1, 'fill')
                erasecol = sq2['bg']

                #then we delete text, set kings, and change items
                sq2.itemconfig(1,fill = movecol,outline="black")
                sq2.set_king(self.s1i.is_king())
                sq1.itemconfig(1,fill=erasecol,outline=erasecol)
                self.deleteTXT(self.s1i)
                sq1.set_king(False)

                #finally, we unpress the two squares
                self.unpressAll(sq1,sq2,'no circle')

            #we then reset the squares, and chaange turns
            self.resetSquares()
            self.changeTurn()
            #and unpress the two squares
            return self.unpressAll(sq1,sq2,'cannot move backwards')
                
    def has_won(self):
        '''evaluate whether anyone has won, and who the winner is'''

        #we set the count variables to 0
        oC = 0
        rC = 0

        #we add 1 to each counter variable for each square with a circle of the specific color
        for square in self.board:
            if square.itemcget(1,'fill') == 'red':
                rC += 1

            elif square.itemcget(1,'fill') == 'orange':
                oC += 1

        #if any of these equal 0, we change the text_var object, add a label, destroy the turnCounters and turnLabels, and disable all squares in the gameBoard
        if rC == 0 or oC == 0:
            if rC == 0:
                self.text_var.set("Orange has Won")
            elif oC == 0:
                self.text_var.set("Red has Won")
            
            self.lbl = Label(self,text='Game Over',font=('LCD',40,'bold'),bd=5,relief=RAISED,bg='blue')
            self.lbl.grid(row=1,column=1,columnspan=1)
            self.turnCounter.destroy()
            self.turnLabel.destroy()
            for square in self.board:
                square['state'] = 'disabled'

            #we need to return this
            return 'game over'
        
        return 'none'

    def showRules(self):
        '''shows the user the rules'''

        #we get rid of all buttons except for one, and add a label to show the rules of the game
        self.grid_forget()
        self.infoLbl.grid_forget()
        self.turnLabel.place_forget()
        self.exitbtn.place_forget()
        self.forfietbtn.place_forget()
        self.restartbtn.place_forget()
        self.quitbtn.place_forget()    
        self.turnCounter.grid_forget()
        self.rulesbtn['text'] = 'Return\nTo\nGame'
        self.rulesLbl = Label(self.master,text='''Checker Rules
------------------------
(1) Click on a square with one of your pieces and on a square with the same BG color to move
(2) You must always move diagonally
(3) If you can jump an opponent, you must
(4) Double jumps are allowed for both kinged and regular pieces
(5) Left click on a square to select it, but right click on a square to de-select it
(6) Only kings can move any direction they want - regular pieces must move away from their starting side
(7) If you cannot move, press forfiet to forfiet the game
(8) Once a piece reaches the opposite side of where it started, it will become a king
(9) Have Fun!
(10) Click the button on the screen to return to the game''',font=('LCD',7,'bold'))
        self.rulesLbl.grid(row=1,column=1)
        
        while self.rulesVar:
            self.master.update()
        
        
    def playGame(self):
        #constant repeat loop
        while True:
            #check if anyone won the game
            hasWon = self.has_won()
            if hasWon == 'game over':
                self.forfietbtn['state'] = 'disabled'
                break

            self.master.update()
            
            #set the cursquares list to empty
            cursquares = []

            #check for all kings and disable all unwanted squares
            self.checkForKings()
            self.disableSquares() 
                    
            for square in self.board: #find all clicked squares, and add them to the cursquares list
                if square['state'] == 'disabled' and square['relief'] == SUNKEN and (square.is_clickable()):
                    cursquares.append(square)
                    
            if len(cursquares) == 1: #if only one square has been clicked, mark that it has been clicked
                self.s1i = cursquares[0]
                if self.s1i.itemcget(1, 'fill') in ['blue','light green'] or not self.s1i.is_clickable():
                    self.s1i.unpressed('no circle')
                    continue
                
            if len(cursquares) == 2: #if two have been clicked, mark both the squares, and run the moveCircles method
                cursquares.remove(self.s1i)
                self.s2i = cursquares[0]
                
                self.moveCircles(self.s1i,self.s2i)

            #evaluate if we need to stop the game for any reason
            if self.restartVar:
                self.lbl = 'none'
                break
            
            if self.quitVar:
                return self.master.destroy()
            
            if self.exitVar:
                return 'exit'

            if self.forfietVar:
                self.lbl = 'none'
                self.restartVar = False
                break

            if self.rulesVar:
                self.showRules()

        #disable all squares
        for square in self.board:
            square['state'] = 'disabled'
            square.set_clickable(False)

        #change restartbtn text
        self.restartbtn['text'] = 'Re-Play\nGame'

        #repeat while the restart btn hasn't been clicked
        while self.restartVar == False:
            
            if self.forfietVar: #if the forfiet button has been pressed
                self.forfietbtn['state'] = 'disabled' #disable the button
                self.curCol = self.cols[self.curTurn%2] #find the current color
                self.cols.remove(self.curCol) #find the other color
                self.text_var.set(self.cols[0][0].upper()+self.cols[0][1:]+" has Won") #display loser
                forre = StringVar()
                self.rulesbtn['state'] = 'disabled'
                forre.set("The game has been forfieted by: "+str(self.curCol[0].upper())+str(self.curCol[1:])) #display forfieter
                self.infoLbl.config(bg = self.cols[0],bd=25,relief=RAISED)
                self.lbl = Label(self,textvariable=forre,font=('LCD',17,'bold'),bd=5,relief=RAISED,bg=self.curCol) #create label
                self.lbl.grid(row=1,column=1,columnspan=1)
                self.turnCounter.destroy() #destroy turnCounter
                self.turnLabel.destroy() #destroy turnLabel
                self.forfietVar = False #set forfietVar to false

            #return and end loop if needed
            if self.exitVar:
                return 'exit'
                
            if self.quitVar:
                return self.master.destroy()
            
            self.master.update()#update master window

        #return restart  
        return 'restart'

class checkerSetup(Frame):

    def __init__(self,master):
        Frame.__init__(self,master,width=600,height=300,bg='blue',bd=15,relief=GROOVE) #create the frame
        self.grid(row=0,column=1)
        self.master = master
        
        self.lbl = Label(self,text='Play Checkers',bd=5,font=('LCD',30,'bold'),bg='blue',relief=GROOVE) #create label

        #creates entry widgets to enter the game mode
        Button(self,relief=RAISED,bd=7,bg='purple',text='Play Checkers',font=('LCD',10,'bold'),command=self.modeSelect).place(relx = 0.365,rely = 0.35) #make button
        
        #calling modeSelect to start setup
        self.lbl.place(relx = 0.25,rely = 0.05)

    def modeSelect(self):
        self.destroy() #destroy frame
        restart = 'restart' #make variable and loop to easily restart game
        while restart == 'restart':
            for widget in self.master.winfo_children():
                widget.destroy()
            self.master.update()
            checkerGame = CheckerBoard(self.master)
            self.master.update()
            restart = checkerGame.playGame()

        if restart == 'exit': #if we need to restart the class, do it
            for widget in self.master.winfo_children():
                widget.destroy()
            self = checkerSetup(self.master)
            return
        
def play_checkers():
    '''setup master window and run checkerSetup class'''
    root = Tk()
    root.geometry("700x700")
    root.title("Checkers Game")

    #allows for objects in the 1st row and 1st column to be centered
    root.rowconfigure(2,weight=1)
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    root.columnconfigure(2,weight=1)
    
    setup = checkerSetup(root)
    setup.mainloop()
    
play_checkers()
