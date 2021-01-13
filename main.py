from tkinter import *
import tkinter.ttk as ttk
import random, time


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title('Tic Tac Toe')
        self.geometry('700x300')
        self.label_text = StringVar()
        self.label_text.set('Choose Player')
        self.label1 = Label(self, textvar =self.label_text)
        self.label1.pack(fill =BOTH, padx =50, pady = 30)
        
        self.play = IntVar()
        self.play.set(1)
        single_play = Radiobutton(self,text = 'Single Player', var = self.play, value =1)
        multi_play = Radiobutton(self,text = 'Multiple Player', var = self.play, value =2)
        single_play.pack()
        multi_play.pack()
        Label(self, textvar = self.play.get()).pack()
        self.style = ttk.Style()
        self.style_1 = {'foreground': 'red', 'background': 'black'}
        self.button_play = ttk.Button(self, text='Play', command= self.enter, style = 'TButton')
        self.button_play.pack(fill = BOTH, padx = 50, pady = 50)

    def enter(self):
        self.style.configure('TButton', ** self.style_1)
        self.new_window = Toplevel(self)
        self.new_window.resizable(False, False)

        Label(self.new_window, text= 'Player X HighScore').grid(row= 0, column =0, columnspan =2)
        Label(self.new_window, text = 'Player O HighScore').grid(row =0, column=3, columnspan =2)
        self.new_window.scoreX = IntVar()
        self.new_window.scoreO = IntVar()
        self.new_window.scoreX.set(0)
        self.new_window.scoreO.set(0)
        Label(self.new_window, textvar = self.new_window.scoreX, font =('Verdana', 11)).grid(row=1, column = 0)
        Label(self.new_window, text = 'versus').grid(row=1, column = 2)
        Label(self.new_window, textvar = self.new_window.scoreO, font =('Verdana', 11)).grid(row=1, column = 4)
            
        self.new_window.rounds = IntVar()
        self.new_window.rounds.set(1)
        Label(self.new_window, text= 'Round').grid(row= 2, column =1, columnspan =2)
        Label(self.new_window, textvar= self.new_window.rounds).grid(row= 2, column =2,)

        self.new_window.status = StringVar()
        self.new_window.status.set('Playing...')
        Label(self.new_window, textvar = self.new_window.status, font =('Verdana', 11),\
              ).grid(row=3, column=1, columnspan =4)
            
        self.new_window.player = 'X'
        self.new_window.box = [[0,0,0],[0,0,0],[0,0,0]]
        self.new_window.states = [[0,0,0],[0,0,0],[0,0,0]]
        self.new_window.stop_game = False

        if self.play.get() == 2:
            for r in range(3):
                for c in range(3):
                    self.new_window.box[r][c] = Button(self.new_window, width = 12,height =5, bg = 'blue',
                                                  font = ('verdana', 15),
                                                  command = lambda r=r, c=c: self.multi_callback(r,c))
                    self.new_window.box[r][c].grid(row= r+5, column =c+1)

        elif self.play.get() == 1:
            Label(self.new_window, text = '(You)', font =('Verdana', 9)).grid(row=1, column = 1)
            Label(self.new_window, text = '(Computer)', font =('Verdana', 9)).grid(row=1, column = 3)
            for r in range(3):
                for c in range(3):
                    self.new_window.box[r][c] = Button(self.new_window, width = 12,height =5, bg = 'blue',
                                                  font = ('verdana', 15),
                                                  command = lambda r=r, c=c: self.single_callback(r,c))
                    self.new_window.box[r][c].grid(row= r+5, column =c+1)

    def single_callback(self, r, c):
        self.new_window.table = [[i,j] for i in range(3) for j in range(3)]        
        if self.new_window.stop_game == False:    
            self.play_game(r, c)
            self.new_window.choose = [self.new_window.table[c] for c in range(len(self.new_window.check)) \
                                      if self.new_window.check[c] == 0]
            if self.new_window.choose:
                self.new_window.choice = random.choice(self.new_window.choose)
                self.new_window.after(400, self.play_game(self.new_window.choice[0],self.new_window.choice[1]))
            else:
                self.new_window.player = 'X'
            self.check_for_winner()
            self.winner(single= True, multi = False)
        if self.new_window.stop_game == True:
            self.new_window.player = 'X'
        
    def multi_callback(self, r, c):
        self.play_game(r, c)
        self.check_for_winner()
        self.winner(single = False, multi = True)
        if self.new_window.stop_game == True:
            self.new_window.player = 'X'

    def play_game(self, r,c):   
        if self.new_window.player == 'X' and self.new_window.states[r][c] ==0 \
           and self.new_window.stop_game == False:
            self.new_window.box[r][c].configure(text= 'X', fg= 'yellow', bg ='white')
            self.new_window.states[r][c] = 'X'
            self.new_window.player = 'O'
        if self.new_window.player == 'O' and self.new_window.states[r][c] ==0 \
           and self.new_window.stop_game == False:
            self.new_window.box[r][c].configure(text= 'O', fg= 'yellow', bg ='black')
            self.new_window.states[r][c] = 'O'
            self.new_window.player = 'X'
        self.new_window.check = self.new_window.states[0] + self.new_window.states[1] + self.new_window.states[2]

    def winner(self, single, multi):
        if not 0 in self.new_window.check and self.new_window.stop_game == False:
            self.new_window.status.set('No Winner!')
            self.new_window.player = 'X'
            self.next_game(single, multi)
            
        if self.new_window.stop_game == True:
            if multi:
                msg = 'Player {} wins round {}'.format(('X' if self.new_window.player == 'O' else 'O'), \
                                                       self.new_window.rounds.get())
                if self.new_window.player == 'O':
                    self.new_window.scoreX.set(self.new_window.scoreX.get() + 5)
                else:
                    self.new_window.scoreO.set(self.new_window.scoreO.get() + 5)
            elif single:
                msg = 'Player {} wins round {}'.format(('X' if self.new_window.player == 'X' else 'O'), \
                                                       self.new_window.rounds.get())
                if self.new_window.player == 'X':
                    self.new_window.scoreX.set(self.new_window.scoreX.get() + 5)
                else:
                    self.new_window.scoreO.set(self.new_window.scoreO.get() + 5)
            self.new_window.status.set(msg)
            
            self.next_game(single, multi)

    def next_game(self, single, multi):
        self.new_window.stop_game = False
        self.new_window.states = [[0,0,0],[0,0,0],[0,0,0]]
        Label(self.new_window, text = 'Playing...').grid(row =4, column =1 , columnspan = 4)
        for r in range(3):
            for c in range(3):
                self.new_window.box[r][c].grid_remove()
        if single:
            for r in range(3):
                for c in range(3):
                    self.new_window.box[r][c] = Button(self.new_window, width = 12,height =5, bg = 'blue',\
                                                       font = ('verdana', 15),\
                                                       command = lambda r=r, c=c: self.single_callback(r,c))
                    self.new_window.box[r][c].grid(row= r+5, column =c+1)
        if multi:
            for r in range(3):
                for c in range(3):
                    self.new_window.box[r][c] = Button(self.new_window, width = 12,height =5, bg = 'blue',\
                                                       font = ('verdana', 15),\
                                                       command = lambda r=r, c=c: self.multi_callback(r,c))
                    self.new_window.box[r][c].grid(row= r+5, column =c+1)
        self.new_window.rounds.set(self.new_window.rounds.get() +1)
            
    def check_for_winner(self):
        #vertical
        for i in range(3):
            if self.new_window.states[0][i]== self.new_window.states[1][i] == \
               self.new_window.states[2][i] != 0:
                self.new_window.box[0][i].configure(bg = 'grey')
                self.new_window.box[1][i].configure(bg = 'grey')
                self.new_window.box[2][i].configure(bg ='grey')
                self.new_window.stop_game = True

        #horizontal
        for i in range(3):
            if self.new_window.states[i][0]== self.new_window.states[i][1] ==\
               self.new_window.states[i][2]!= 0:
                self.new_window.box[i][0].configure(bg = 'grey')
                self.new_window.box[i][1].configure(bg = 'grey')
                self.new_window.box[i][2].configure(bg = 'grey')
                self.new_window.stop_game = True

        #left to right
        if self.new_window.states[0][0]== self.new_window.states[1][1] ==\
           self.new_window.states[2][2]!= 0:
            self.new_window.box[0][0].configure(bg = 'grey')
            self.new_window.box[1][1].configure(bg = 'grey')
            self.new_window.box[2][2].configure(bg = 'grey')
            self.new_window.stop_game = True

        #right to left
        if self.new_window.states[0][2]== self.new_window.states[1][1] ==\
           self.new_window.states[2][0]!= 0:
            self.new_window.box[0][2].configure(bg = 'grey')
            self.new_window.box[1][1].configure(bg = 'grey')
            self.new_window.box[2][0].configure(bg = 'grey')
            self.new_window.stop_game = True

            
window = Window()
window.mainloop()
