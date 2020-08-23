import tkinter as tk
import Othello_process


class EmptyUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("Hello zeke")
        #self.master.background("green")
        self.c = tk.Canvas(self, width=600, height=600)
        self.c.bind("<Button-1>", self.on_click)
        self.x = -1000
        self.y = -1
        self.c.pack()
        self.basic_draw()
        self.c.create_text(50, 50, text="あなたが先手です")
        self.main = Othello_process.Process()
        self.on_click_process()
        self.nowfield,self.res = self.main.Othello_input(self.x, self.y)
        
        for height in range(8):
            for width in range(8):
                if(self.nowfield[height][width] == 2):
                    self.c.create_oval(
                        width*50+100, height*50+100, (width+1)*50+100, (height+1)*50+100, fill='black')
                elif(self.nowfield[height][width] == 1):
                    self.c.create_oval(
                        width*50+100, height*50+100, (width+1)*50+100, (height+1)*50+100, fill='white')
    def basic_draw(self):
        self.c.delete("all")
        self.c.create_rectangle(100, 100, 500, 500, fill='green')  # 塗りつぶし
        for index in range(8):
            self.c.create_line(index*50+100, 100, index*50+100, 500)
            self.c.create_line(100, index*50+100, 500, index*50+100)
        
    
    def on_click(self, event):
        self.x = event.x
        self.y = event.y
        self.on_click_process()

    def on_click_process(self):
        self.Othello_x = int((self.x-100)//50)
        self.Othello_y = int((self.y-100)//50)
        self.basic_draw()
        string = str(self.x)+" "+str(self.x)+"   " + \
            str(self.Othello_x)+" "+str(self.Othello_y)
        self.c.create_text(50, 50, text=string)
        self.nowfield,self.res= self.main.Othello_input(self.Othello_x, self.Othello_y)
        if(self.res == -1):
            self.c.create_text(100, 20, text="適切な入力をお願いします")
        _, _, self.possible_1, _ = self.main.possible_state()
        for height in range(8):
            for width in range(8):
                if(self.nowfield[height][width] == 2):
                    self.c.create_oval(width*50+100, height*50+100, (width+1)*50+100, (height+1)*50+100, fill='black')
                elif(self.nowfield[height][width] == 1):
                    self.c.create_oval(width*50+100, height*50+100, (width+1)*50+100, (height+1)*50+100, fill='white')
                if(self.possible_1[height][width]==1):
                    self.c.create_oval(
                        width*50+100, height*50+100, (width+1)*50+100, (height+1)*50+100, fill='gray')
        
print("hello")

f = EmptyUI()
f.pack()
f.mainloop()
