from tkinter import *
from tkinter import messagebox
import random
import time

class MineSweeperSquare(Button):
    def __init__(self,master,symbol):
        #define the symbol, and useful variables
        self.symbol = symbol
        self.blank = False
        self.bomb = False
        self.flags = 0
        
        #mix up the color of the text (if possible)
        colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
        if self.symbol.isdigit():
            self.fg = colormap[int(self.symbol)]
        elif self.symbol in ['','*']:
            self.fg = 'black'
            
        Button.__init__(self,master,state='normal'\
                        ,relief=RAISED,bg='white',width=2\
                        ,height=1,bd=5 ,highlightcolor='light gray'\
                        ,font=('LCD',8,'bold') ,text='',disabledforeground=self.fg,command=self.clicked)
        
            
        #we need to bind this so that we can add astrics if we right click
        self.bind("<Button-3>",self.flag)
        
    def clicked(self):
        #we make sure it can/should be clicked first
        if self['text'] == '' and self['state'] == 'normal':

            #we change the relief and everything to make it look clicked
            self.config(relief=SUNKEN)
            self.config(bg='light gray')
            self.config(text=self.symbol)
            self['state'] = 'disabled'

            #we set the self.blank, and self.bomb objects to true IF we clicked on one of those types of buttons
            if self.symbol == '':
                self.blank = True
            if self.symbol == '*':
                self.bomb = True

    def set_blank(self,blank):
        #sets self.blank object
        self.blank = blank
        
    def disable(self):
        #disables the button
        self['state'] = 'disabled'

    def get_blank(self):
        #returns self.blank
        return self.blank

    def get_flags(self):
        #returns self.flags
        return self.flags

    def get_bomb(self):
        #returns self.bomb
        return self.bomb
    
    def get_symbol(self):
        #returns self.symbol
        return self.symbol
        
    def flag(self,event):
        #adds astrik, or takes one away depending on whether or not one is already there
        if self['text'] == '' and self['state'] == 'normal':
            self.config(text='*')
            self.flags += 1
        elif self['text'] == '*' and self['state'] == 'normal':
            self.config(text='')
            self.flags -= 1
        
class MineSweeperFrame(Frame):
    
    def __init__(self,master,numbombs,length,width):
        Frame.__init__(self,master)
        self.place()
        self.master = master
        self.length = length
        self.width = width
        self.bombs = numbombs
        
        #creating the map for the self.squares list to help things get organized
        self.squaresMap = ['*'for i in range(self.bombs)]
        self.squaresMap.extend(['0'for i in range((length*width)-self.bombs)])
        random.shuffle(self.squaresMap)
        for square in self.squaresMap:
            self.adjacent_find(square)

        self.squares = [MineSweeperSquare(master,square) for square in self.squaresMap]
        #creating the actual self.squares list
        self.restart = False
        self['bg'] = 'orange'
        counter = 1
        row = 0
        
        #printing the symbol values of both the self.squaresMap, and self.squares list (should be identical)

        '''
        for square in self.squares:
            if counter%(self.length+1) == 0:
                row += 1
                counter = 1
                print('')
            if square.symbol == '':  
                print(square.symbol,end=' :')
            else:
                print(square.symbol,end=':')
            counter += 1
        '''
        
        self.restart_btn = Button(self.master,text='Click to Restart Game',command=lambda:self.restartGame(True),relief=RAISED,bd=5,font=('LCD',10,'bold'),bg='purple')
        self.restart_btn.grid(row=0,column=1,columnspan=self.length)
        self.menu_btn = Button(self.master,text='Click to Return to Menu',command=lambda:self.restartGame('menu'),relief=RAISED,bd=5,font=('LCD',10,'bold'),bg='purple')
        self.menu_btn.grid(row=self.width+1,column=1,columnspan=self.length)

        mineSweeperCoords = []
        #adding buttons to grid
        counter = 1
        row = 1
        for square in self.squares:
            if counter%(self.length+1) == 0:
                row += 1
                counter = 1
            square.grid(row=row,column=counter,sticky="wens")
            counter += 1
        
        #adding flag counter
        self.flagCounter = Label(self.master,text=str(numbombs),font=('LCD',15,'bold'),bg='blue',relief=RAISED,bd=5)
        self.flagCounter.grid(row=self.width+2,column=1,columnspan=self.length)
        self.flags = numbombs

        self.master.update()

    def restartGame(self,val):
        '''sets restart object'''
        self.restart = val
        
    def get_width(self):
        '''returns width of frame'''
        return self.width

    def get_length(self):
        '''returns length of frame'''
        return self.length
    
    #adjacent square finder for creating the Map List above
    def adjacent_find(self,square):
        '''finds number of squares that are adjacent, or touch verticies with
        the square inputted that are bombs, and changes the map of the square
        to that value'''
        x = self.squaresMap.index(square)
        if square != '*':
            squares = 0

            #checks squares above the square
            if (x)%self.length != 0 and x >= (self.length+1) and self.squaresMap[x-(self.length+1)] == '*':
                squares += 1
            if x >= self.length and self.squaresMap[x-self.length] == '*':
                squares += 1
            if (x+1)%self.length != 0 and x >= self.length and self.squaresMap[x-(self.length-1)] == '*':
                squares += 1

            #checks squares below the square
            if x%self.length != 0 and x <= (len(self.squaresMap)-self.length-1) and self.squaresMap[x+self.length-1] == '*':
                squares += 1
            if x <= (len(self.squaresMap)-self.length-1) and self.squaresMap[x+self.length] == '*':
                squares += 1
            if (x+1)%self.length != 0 and x <= (len(self.squaresMap)-self.length-2) and self.squaresMap[x+self.length+1] == '*':
                squares += 1

            #checks squares next to the square
            if x%self.length != 0 and self.squaresMap[x-1] == '*':
                squares += 1
                
            if (x+1)%self.length != 0 and x <= len(self.squaresMap)-1 and self.squaresMap[x+1] == '*':
                squares += 1

            #matches the square to its number  
            list1 = ['','1','2','3','4','5','6','7','8']
            self.squaresMap[x] = list1[squares]
        
    def clicked_bomb(self):
        '''ends game, and returns none'''
        #displays messageBox
        messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)
        
        #shows square if it is a bomb
        for square in self.squares:
            if square.symbol == '*':
                square.clicked()
                square.config(bg='red',fg='blue')
                
            else: #if square is not a bomb, disable it
                square.disable()

        #shows message that the user lost, and returns 'none' to go back to setup menu
        self.flagCounter.config(text='You Lose',relief=SUNKEN)
        self.endgameSetup()
        return 'none'
        
    def has_won(self):
        '''returns if player has clicked all squares that
        are NOT bombs'''
        return len([True for square in self.squares if square['state'] == 'disabled' and square['text'] == square.get_symbol() and square['text'] != '*']) == len(self.squares)-self.bombs
    
    def check_rows_col(self,square,index,toadd):
        '''returns True if the column, and row checked have a square'''
        xrow = square.grid_info()['row'] #get the row of the square
        orow = self.squares[index+toadd].grid_info()['row'] #get the row of the prospective square
        xcolumn = square.grid_info()['column'] #get the column of the square
        ocolumn = self.squares[index+toadd].grid_info()['column'] #get the column of the prospective square
        
        if toadd in [1,-1]:
            #returns True if there is a square to the right or left of the current square  and if that square is clickable
            return (orow == xrow) and (xcolumn+toadd == ocolumn)
        
        elif toadd in [self.length,-(self.length)]:
            #returns True if there is a square to the above or below the current square and if that square is clickable
            return (orow == xrow+(toadd//abs(toadd))) and (xcolumn == ocolumn)

        #returns True if there is a square diagonal to the current square that is clickable
        elif toadd in [-(self.length-1),self.length+1]:
            return (orow == xrow+(toadd//abs(toadd))) and (xcolumn == ocolumn-1)

        elif toadd in [-(self.length+1),self.length-1]:
            return (orow == xrow+(toadd//abs(toadd))) and (xcolumn == ocolumn+1)
        
    def clicked_empty(self,square):
        '''finds, and clicks all surrounding squares of a clicked empty square'''
        x = self.squares.index(square)   
        square.set_blank(False)
        
        if (x <= (len(self.squares)-self.length)) and self.check_rows_col(square,x,(self.length-1)): #we click a squares diagonal to this one
            self.squares[x+(self.length-1)].clicked()

        if (x >= self.length-1) and self.check_rows_col(square,x,-(self.length-1)): #we click a squares diagonal to this one
            self.squares[x-(self.length-1)].clicked()


            
        if (x <= (len(self.squares)-self.length-1)) and self.check_rows_col(square,x,(self.length)): #we click the square above this one
            self.squares[x+self.length].clicked()

        if (x >= self.length) and self.check_rows_col(square,x,-(self.length)): #we click the square below this one
            self.squares[x-(self.length)].clicked()



        if (x <= (len(self.squares)-self.length-2)) and self.check_rows_col(square,x,(self.length+1)): #we click a squares diagonal to this one
            self.squares[x+self.length+1].clicked()

        if (x >= (self.length+1)) and self.check_rows_col(square,x,-(self.length+1)): #we click a squares diagonal to this one
            self.squares[x+-(self.length+1)].clicked()


            
        if (x <= (len(self.squares)-2)) and self.check_rows_col(square,x,1): #we click the square to the right of this one
            self.squares[x+1].clicked()
            
        if (x >= 1) and self.check_rows_col(square,x,-1): #we click the square to the left of this one
            self.squares[x-1].clicked()
            
            
    def endgameSetup(self):
        '''sets up the window and its widgets for the aftermath of the game'''
        self.flagCounter.grid(row=self.width+2,column=1,columnspan=self.length)
        self.restart_btn.config(text='Click to Re-Play Game')
        self.menu_btn.destroy()
            
    def play_game(self):  
        '''plays game'''
        while self.has_won() == False: #while the player has not won
            blank = [] #list to check if there are any blank squares
            bomb = [] #list to check if there are any bomb squares
            flags = 0 #variable to update self.flags object
            
            for square in self.squares:
                blank.append(square.get_blank())
                bomb.append(square.get_bomb())
                flags += square.flags
            self.flags = self.bombs-flags
            
            if True in blank: 
                curSquare = self.squares[blank.index(True)] #we change the square in self.squares to the clicked square
                self.clicked_empty(curSquare)#we run the clicked_empty method
                
            if True in bomb: #if there is a bomb that was clicked
                return self.clicked_bomb()#we cannot continue the loop if the player lost
            
            if self.restart in [True,'menu']: #if the user wants to restart, or return to the menu
                break #we cannot continue the loop if the player wants to restart
            
            self.flagCounter.config(text=self.flags) #update the text to the number of flags not used
            self.master.update() #update the master window
            
        if self.has_won(): #we show the user that they won and we go to the regular end game screen
            self.flagCounter.config(relief=GROOVE,text='You Won')
            messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)
            self.endgameSetup()
            for square in self.squares:
                if square.symbol == '*':
                    square.clicked()
                    square.config(bg='blue',fg='blue')
            return 'none'
            
        if self.restart == True: #we set self.restart to restart and restart the game
            self.restart = False
            return 'restart'

        if self.restart == 'menu':#we change the flag counter text, and take the user back to the menu screen
            self.flagCounter.config(relief=SUNKEN,text='Returning to Menu',font=('LCD',10,'bold'))
            self.destroy()
            self.master.update()
            time.sleep(0.5)
            return 'menu'
               
class MinesweeperSetup:
    def __init__(self,master):
        self.master = master

        #we need to create the menu button to allow the user to return to the screen
        self.menubutton = Button(self.master,text='Click to Return to Menu',state='disabled',command = lambda:self.__init__(self.master),relief=SUNKEN,bd=7,font=('LCD',12,'bold'),bg='purple')
        self.menubutton.place(relx=0.5,rely=0.65,anchor='s')
        
        #creating and setting the text, and int variables
        self.int_var = IntVar()
        self.text_var = StringVar()
        self.text_var.set('Game Rules\n'+'-'*60+'\nLeft click squares to unveil what is underneath\nUse space numbers to determine where bombs are\nRight click to use markers to mark all bombs\nClick empty squares to expose all squares in area\nWhen you have selected all spaces without bombs, you Win!\nSelect a space with a bomb and you lose!\nGood Luck!')
        self.int_var.set(0)

        #creating the frame and widgets
        self.frame = Frame(self.master,relief=RAISED,bd=20,bg='purple',height=400,width=1000)

        #info for radio buttons
        self.choices = [('Easy',0,[7,7,7]),('Medium',1,[12,10,15])\
                        ,('Hard',2,[15,11,20]),('Extreme',3,[25,14,35])\
                        ,('Grandmaster',4,[40,20,150]),('Custom Difficulty',5,[0,0,0])]

        #creates a label
        self.widgets = [Label(self.frame,text='Select Game Difficulty',relief=RAISED,bd=5,font=('LCD',15,'bold'),bg='blue')]

        #creates radio buttons to select the game mode
        self.widgets.extend([Radiobutton(self.frame\
                                         , text=choice, value=index, variable=self.int_var,relief=RAISED,bd=5\
                                         ,font=('LCD',8,'bold'),bg='blue') for choice,index,other in self.choices])

        #creating a button to submit the game mode selected, or inputted
        self.widgets.extend([Button(self.frame\
                                    ,text='Submit Game Mode',command = lambda:self.prep_game(length=self.choices[self.int_var.get()][2][0]\
                                    ,width=self.choices[self.int_var.get()][2][1],bombs = self.choices[self.int_var.get()][2][2]\
                                    ,mode=self.choices[self.int_var.get()][0]),relief=RAISED,bd=5,font=('LCD',12,'bold'),bg='dark orange')])

        self.widgets.extend([Label(self.frame,relief=RAISED,bd=5,font=('LCD',8,'bold'),bg='blue',textvariable = self.text_var)])
        
        #calling modeSelect to start setup
        self.modeSelect()
            
    def modeSelect(self):
        '''places all widgets, and runs prep_game method when the button is clicked'''
        sub = 0 #set the amount to subtract to 0
        otherSub = 0.455 #set the amount for relx in .place()
        toadd = 0.085
        self.frame.place(relx=0.14,rely=0.0) #place frame

        widget = self.place_list(self.widgets[1:7])#we need to place all of the RadioButttons
                        
        #we place the final widgets
        self.widgets[7].place(anchor=CENTER,rely=0.1*(self.widgets.index(widget)-0.85),relx=0.5)
        self.widgets[8].place(anchor=CENTER,rely=0.1*(self.widgets.index(widget)+1.9),relx=0.5)
        self.widgets[0].place(anchor=CENTER,rely=0.1*(self.widgets.index(self.widgets[0])+0.75),relx=0.5)
        
    def place_list(self,widgets):
        '''places widgets in a list'''
        
        sub = 0
        otherSub = 0.425
        toadd = 0.135
        for widget in widgets: #repeat for each widget that is a RadioButton
            widget.place(anchor=CENTER,rely=0.1*(widgets.index(widget)+2-sub),relx=otherSub)#place the widget first
            
            if widgets.index(widget) in [1]: #if the widget is the second in the loop...
                sub -= 1 #we reset the amount to subtract
                otherSub = 0.425-0.135 #we reset the amount for relx in .place()
            if widgets.index(widget) in [3]: #if the widget is the fourth in the loop...
                sub -= 1 #we reset the amount to subtract
                otherSub = 0.425-0.135 #we reset the amount for relx in .place()
                    #toadd = 0.135
                
            sub += 1 #we add one to the amount to subtract
            otherSub += toadd #we add 0.085 to the amount for relx in .place
        return widget

    def prep_game(self,length,width,bombs,mode):
        '''runs the start_game method, or adds places to enter numbers for the objects: length, width, and bombs'''

        self.menubutton.config(state = 'normal',relief=RAISED) #we activate the menubutton since we are no longer on the menu screen, and change the relief
        
        if mode == 'Custom Difficulty': #if this is true, we need to add some things

            for widget in self.widgets[1:7]:#we need to delete all widgets in the middle of the frame
                widget.place_forget()

            vars = [IntVar() for i in range(3)] #create variables

            #create labels for entry widgets
            widgets_lbl = [Label(self.frame,text=string,relief=RAISED,bd=5,font=('LCD',8,'bold'),bg='blue')\
                           for string in ['Enter Length of Game','Enter Width of Game','Enter Bombs in Game']]

            #create entry widgets with variables in vars list
            widgets_ent = [Entry(self.frame,textvariable=vars[i],relief=GROOVE,bd=5,font=('LCD',8,'bold'),bg='blue') for i in range(3)]
            
            #create new command for the set mode button
            self.widgets[7].config(command=lambda:self.start_game(vars[0].get(),vars[1].get(),vars[2].get())) 

            #creating new instructions
            self.text_var.set('Instructions\n'+'-'*40+'\nEnter numbers for the number of bombs, length of game screen,'\
                              ' and width of game screen\nEnter length of game screen greater than 6, and less than 41\n'\
                              'Enter width of game screen greater than 6, and less than 21\nEnter number of bombs great'\
                              'er than -1, and less than the length times the width')

            #create widgets list
            widgets = [widgets_lbl[0],widgets_ent[0],widgets_lbl[1],widgets_ent[1],widgets_lbl[2],widgets_ent[2]]
            self.place_list(widgets)#Then place widgets list
  
        else: #if not, we just run the regular stuff
            self.start_game(length,width,bombs)

    def reset(self):
        '''Erases window, and runs starting function'''
        
        #we destroy all widgets in the window
        for widget in self.master.winfo_children():
            widget.destroy()

        #we run the initiate function
        self.__init__(self.master)
        
    def start_game(self,length,width,bombs):
        '''runs the actual game'''
        
        #we remove all the widgets from the screen
        for widgets in self.master.winfo_children():
            widgets.destroy()

        #we update the window
        self.master.update()

        #we check if the value are less than the possible amount, and if so, set them to the defaults
        if length <= 0 or length > 40:
            length = 7
        if width <= 0 or width > 20:
            width = 7
        if bombs <= 0 or bombs > length*width:
            bombs = 1
            
        #we set restart to restart
        restart = 'restart'

        #we repeat while restart is restart
        while restart == 'restart':

            #we play the game, and update restart
            game = MineSweeperFrame(self.master,bombs,length,width)
            restart = game.play_game()
            
            if restart == 'restart': #if we are continuing the while loop by restarting

                #we remove all of the widgets on the screen
                for widgets in self.master.winfo_children():
                    widgets.destroy() 
                       
        self.master.update()#we update the window
        
        if restart == 'menu': #if the user selected to return to the menu
            self.reset() #we must run the reset function
            return #and return
        
        width = game.get_width()#we need the game frame's width
        length = game.get_length()#and we need the game frame's length

        #create button to allow user to return to the menu, and select a new game mode
        self.menubtn = Button(self.master,text='Click to Return to Menu',command = self.reset,relief=RAISED,bd=5,font=('LCD',10,'bold'),bg='purple')
        self.menubtn.grid(row=width+1,column=1,columnspan=length)
        #create button to allow user to replay with the same selected game mode
        self.replaybtn = Button(self.master,text='Click to Re-Play Game',command = lambda:self.start_game(length,width,bombs),relief=RAISED,bd=5,font=('LCD',10,'bold'),bg='purple')
        self.replaybtn.grid(row=0,column=1,columnspan=length)
        
def play_minesweeper():
    root = Tk() #creates window
    root.title('Minesweeper Game') #sets title
    root.geometry("1600x1600") #sets the dimensions to basically fullscreen
    root.configure(bg='orange')#sets background to orange

    #we allow any widget created to be automatically placed in the cente
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(41, weight=1)
    
    setup = MinesweeperSetup(root) #run the __init__(master) method for the minesweeper setup
    root.mainloop() #infinite repeat for master window
    
play_minesweeper()  #plays minesweeper game
