from tkinter import *
import random
import time
import cgitb
cgitb.enable()

class C4Square(Canvas):

    def __init__(self,master,x,y,anchor):
        Canvas.__init__(self,master,width=50,height=50,bg='blue',highlightthickness=2, highlightbackground="blue")
        master.create_window(x+7,y+7,anchor=anchor,window=self)
        self.create_oval(5,5,45,45,fill='white')
        
    def changeFill(self,fill):
        self.itemconfig(1,fill = fill)

    def hasCir(self):
        return self.itemcget(1,'fill') in ['red','yellow']

    def cirIsCol(self,col):
        return self.itemcget(1,'fill') == col
    
class C4Board(Canvas):

    def __init__(self,master):
        Canvas.__init__(self,master,bg='blue',width=357,height=307,highlightthickness=7, highlightbackground="yellow")
        self.master = master
        self.grid(row=1,column=1)

        self.turn = random.choice([0,1])
        self.txt = Label(self.master,text='Connect 4',bd=25,relief=RAISED,font=('LCD',15,'bold'),bg='purple',highlightthickness=0)
        self.txt.grid(row=0,column=1)
        self.curCol = ['red','yellow'][self.turn%2]
        self.turnDisplay = Canvas(master,width=50,height=50,bd=2,relief=RAISED)
        self.turnDisplay.create_oval(9,8.5,49,48.5,fill=self.curCol)
        self.turnText = Label(master,text="'s turn",font=('LCD',30,'bold'))
        self.turnText.place(rely=0.85,relx=0.545)
        self.turnDisplay.grid(row=2,column=1)
        self.board = [C4Square(self,i*50,0,'nw') for i in range(7)]
        for j in range(1,6):
            self.board.extend([C4Square(self,i*50,j*50,'nw') for i in range(7)])

        self.placebtns = [Button(master,text='Col '+str(i+1),font=('LCD',10,'bold')) for i in range(7)]
        self.placebtns[0].config(command=lambda:self.place(0))
        self.placebtns[1].config(command=lambda:self.place(1))
        self.placebtns[2].config(command=lambda:self.place(2))
        self.placebtns[3].config(command=lambda:self.place(3))
        self.placebtns[4].config(command=lambda:self.place(4))
        self.placebtns[5].config(command=lambda:self.place(5))
        self.placebtns[6].config(command=lambda:self.place(6))
        
        for btn in self.placebtns:
            index = self.placebtns.index(btn)
            indexes = [0,1,2,3,4,5,6,7]
            toadds = [2.05,1.9,1.75,1.6,1.45,1.3,1.15]
            toadd = toadds[indexes.index(index)]
            btn.place(rely=0.79,relx=0.1*((index+toadd)))

    def changeTurn(self):
        self.turn += 1
        self.curCol = ['red','yellow'][self.turn%2]
        self.turnDisplay.itemconfig(1,fill=self.curCol)
        self.disableCols()
            
    def disableCols(self):
        cols = [[0,7,14,21,28,35],[1,8,15,22,29,36],[2,9,16,23,30,37]\
                ,[3,10,17,24,31,38],[4,11,18,25,32,39],[5,12,19,26,33,40]\
                ,[6,13,20,27,34,41]]
        
        for sublist in cols:
            noCirCount = [1 for index in sublist if self.board[index].hasCir() == False]
            noCirCount = sum(noCirCount)

            self.placebtns[cols.index(sublist)]['state'] = 'normal'
            if noCirCount == 0:
                self.placebtns[cols.index(sublist)]['state'] = 'disabled'
                
    def place(self,col):
        cols = [[0,7,14,21,28,35],[1,8,15,22,29,36],[2,9,16,23,30,37]\
                ,[3,10,17,24,31,38],[4,11,18,25,32,39],[5,12,19,26,33,40]\
                ,[6,13,20,27,34,41]]
        
        for sublist in cols:
            if col in sublist:
                newcols = sublist
                break
            
        newcols.reverse()
        newcolsR = []
        noCirCount = 0
        for index in newcols:
            if self.board[index].hasCir() == False:
                noCirCount += 1
        if noCirCount > 0:
            for btn in self.placebtns:
                btn['state'] = 'disabled'
            for index in newcols:
                if self.board[index].hasCir() == False:
                    for val in newcolsR:
                        newcols.remove(val)
                    newcols.reverse()
                    for index2 in newcols:
                        self.board[index2].changeFill(self.curCol)
                        self.master.update()
                        time.sleep(0.05)
                        self.board[index2].changeFill('white')
                    self.board[index2].changeFill(self.curCol)
                    self.changeTurn()
                    break
            
                else:
                    newcolsR.append(index)
            
        for col in ['red', 'yellow']:
            if self.hasWon(col):
                self.winPage((col[0].upper()+col[1:]))

    def hasWon(self,col):
        
        for item in self.board:
            #check for horizontal win
            if self.board.index(item) in [0,7,14,21,28,35,1,8,15,22,29,36,2,9,16,23,30,37,3,10,17,24,31,38]:
                itemIndex = self.board.index(item)
                if self.board[itemIndex+1].cirIsCol(col) and self.board[itemIndex+2].cirIsCol(col) and self.board[itemIndex+3].cirIsCol(col) and item.cirIsCol(col):
                    return True
                
            #check for vertical wins
            if self.board.index(item) in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]:
                itemIndex = self.board.index(item)
                if self.board[itemIndex+7].cirIsCol(col) and self.board[itemIndex+14].cirIsCol(col) and self.board[itemIndex+21].cirIsCol(col) and item.cirIsCol(col):
                    return True

            #check for diagonal wins
            if self.board.index(item) in [0,1,2,3,7,8,9,10,14,15,16,17]:
                itemIndex = self.board.index(item)
                if self.board[itemIndex+8].cirIsCol(col) and self.board[itemIndex+16].cirIsCol(col) and self.board[itemIndex+24].cirIsCol(col) and item.cirIsCol(col):
                    return True
                
            if self.board.index(item) in [3,4,5,6,10,11,12,13,17,18,19,20]:
                itemIndex = self.board.index(item)
                if self.board[itemIndex+6].cirIsCol(col) and self.board[itemIndex+12].cirIsCol(col) and self.board[itemIndex+18].cirIsCol(col) and item.cirIsCol(col):
                    return True
                
    def winPage(self,winner):
        for btn in self.placebtns:
            btn.destroy()
        self.turnDisplay.destroy()
        self.turnText.destroy()
        self.txt.destroy()
        
        winText = Label(self.master,text=winner+' wins!',bd=25,relief=GROOVE,font=('LCD',40,'bold'),bg='purple',highlightthickness=20,highlightbackground='yellow')
        winBtn = Button(self.master,text='Re-Play\nGame',bd=10,relief=RAISED,font=('LCD',20,'bold'),bg='blue',command=self.restart)
        winText.grid(row=0,column=1)
        winBtn.grid(row=2,column=1)

    def restart(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.master.update()
        return C4Board(self.master)
            
#7x6#
root = Tk()
root.geometry("600x600")
root.title("MasterGamte")
root.resizable(0,0)
root.rowconfigure(0,weight=1)
root.rowconfigure(2,weight=1)
root.columnconfigure(0,weight=1)
root.columnconfigure(3,weight=1)
c4board = C4Board(root)
c4board.mainloop()
