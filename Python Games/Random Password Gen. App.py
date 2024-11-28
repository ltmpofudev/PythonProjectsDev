from tkinter import *
import random
import string
import os

class PasswordGenerator:

    def __init__(self,root):
        self.password = StringVar()
        txt_lbl = Label(root,text="Your Password\n----------").pack(anchor='center')
        pass_lbl = Label(root,textvariable=self.password,font=('LCD',20,'bold')).pack(anchor='center')
        gen_btn = Button(root,text="Generate\nPassword",command=self.generate).place(relx=0.31,rely=0.3)
        copy_btn = Button(root,text="Copy\nPassword",command=self.copy).place(relx=0.49,rely=0.3)

    def generate(self):
        passwordPieces = ["","","_*","",""]
        for index in [0,3]:
            for i in range(3):
                if i != 0:
                    passwordPieces[index] += (random.choice(string.ascii_letters)).lower()
                    continue
                passwordPieces[index] += (random.choice(string.ascii_letters)).upper()
            
        for index in [1,4]:
            for i in range(3):
                passwordPieces[index] += str(random.randint(0,9))

        password = ""
        for item in passwordPieces:
            password += item
        self.password.set(password)
    
    def copy(self):
        command = 'echo ' + self.password.get() + '| clip'
        os.system(command)
        
root = Tk()
root.title("Random Password Generator")
root.geometry("350x300")
root.resizable(0, 0)
app = PasswordGenerator(root)
root.mainloop()
