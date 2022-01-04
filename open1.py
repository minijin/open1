#-*-coding:utf8-*-
from threading import*
from time import*
from sys import*
from Tkinter import*
from random import*
from string import*

class game:
    def __init__(self):
        self.all = []#所有未扫区域的列表
        self.mine = []#雷所在区域的列表
        self.sweptlist = []#储存已经扫过的区域
        self.mark = []#储存已标记区域
        self.state= 'reading'#当前游戏状态
        self.timeused = 0
    def size(self,row,column,mine):#创建游戏的函数
        self.row = row#游戏行数
        self.column = column#游戏列数
        self.minenum = mine#游戏雷数
        self.root = Tk()
        self.root.title('扫雷迷你版')
        #显示总雷数与已标记雷数之差
        #计时器
        self.minecount = StringVar()
        self.timecount = StringVar()
        self.label1 = Label(self.root,bg = 'black',height = 2,
                            fg = 'red',width = 6,textvariable = self.timecount).grid(row = 0,column = 0,columnspan = 2)
        self.label2 = Label(self.root,bg = 'black',
                            fg = 'red',height =2,width = 6,textvariable = self.minecount).grid(row = 0,column = self.column - 2,columnspan =2)
        self.minecount.set(self.minenum)
        self.timecount.set('%03d'%0)

        
        for i in range(3,self.row+3):
            for j in range(self.column):
                self.all.append([i,j])
        for i in sample(self.all,self.minenum):
            self.mine.append(i)
        for i in self.mine:
            mine_bt = Button(self.root,width = 2,height = 1)
            mine_bt.bind('<Button-1>',self.left_key1)
            mine_bt.bind('<Button-3>',self.right_key)
            mine_bt.grid(row = i[0],column = i[1])

        for i in self.all:
            if ( i in self.mine) == False:
                self.bt = Button(self.root,width = 2,height = 1)
                self.bt.bind('<Button-1>',self.left_key)
                self.bt.bind('<Button-3>',self.right_key)
                self.bt.grid(row = i[0],column = i[1])
            
        menubar = Menu(self.root)
        for x in [['新游戏',self.new],
                  ['初级',self.beginner],
                  ['中级',self.intermediate],
                  ['高级',self.expert]]:
            menubar.add_command(label = x[0],command = x[1])
        self.root['menu'] = menubar
        self.root.mainloop()

    def beginner(self):
        self.root.destroy()
        self.__init__()
        self.size(9,9,10)
    def intermediate(self):
        self.root.destroy()
        self.__init__()
        self.size(16,16,40)
    def expert(self):
        self.root.destroy()
        self.__init__()
        self.size(16,30,99)


    def new(self):
        self.root.destroy()
        self.__init__()
        if self.column == 9:
            self.size(self.row,self.column,10)
        elif self.column == 16:
            self.size(self.row,self.column,40)
        else:
            self.size(self.row,self.column,99)

    def quiz(self):
        self.root.destroy()
    def start(self):
        self.size(9,9,10)

    def right_key(self,event):
        w= event.widget
        t = w.cget('text')
        g = w.grid_info()
        x = int(g['row'])
        y = int(g['column'])
        if t == '?':
            self.mark.remove([x,y])
            w.config(text = '')
            self.minenum += 1
            self.minecount.set(self.minenum)
        else:
            self.mark.append([x,y])
            w.config(text = '?')
            self.minenum -= 1
            self.minecount.set(self.minenum)

                    
    def left_key1(self,event):
        w = event.widget
        g = w.grid_info()
        x = int(g['row'])
        y = int(g['column'])
        if w.cget('text') != '?':
            self.state = 'fail'
            Button(self.root,text = 'X',fg = 'red',relief=SUNKEN).grid(row = x,column = y)
            tl = Toplevel()
            Label(tl,text = '很抱歉，您输了。',width = 50).pack()
            Button(tl,text = '新游戏',command = self.new,width = 6).pack()
            Button(tl,text = '退出',command = self.quiz,width = 6).pack()
    def fail(self):
        tl = Toplevel()
        Label(tl,text = '很抱歉，您输了。',width = 50).pack()
        Button(tl,text = '新游戏',command = self.new,width = 6).pack()
        Button(tl,text = '退出',command = self.quiz,width = 6).pack()
    def win(self):
        if len(self.all) == len(self.mine):
            self.state = 'win'
            tl = Toplevel()
            bt = Label(tl,text = '恭喜，您赢了！您所用时间为%d秒。'%self.timeused,width = 50).pack()
            Button(tl,text = '再来一局',command = self.new,width = 6).pack()
            Button(tl,text = '退出',command = self.quiz,width = 6).pack()
    def left_key(self,event):
        w = event.widget
        g = w.grid_info()
        x = int(g['row'])
        y = int(g['column'])
        if w.cget('text') != '?':
            self.sweptlist.append([x,y])
            self.count(x,y)
        if self.state == 'reading':
            self.state = 'begin'
            self.f = Thread(target=self.time,args=(),name='thread-')
            self.f.start()
            
    def count(self,i,j):
        self.n =0
        a = max(i - 1,3)
        b = min(i + 2,self.row+3)
        c = max(0,j - 1)
        d = min(j + 2,self.column)
        for r in range(i - 1,i + 2):
            for s in range(j - 1,j+2):
                if ([r,s] in self.mine) == True:
                    self.n +=1
        if self.n == 0:
            Button(self.root,width = 2,height = 1,state = 'disabled',relief = SUNKEN).grid(row = i,column=j)
            if [i,j] in self.all:
                self.all.remove([i,j])
            self.win()
            for r in range(a,b):
                for s in range(c,d):
                    if ([r,s] in self.sweptlist) == False:
                        self.sweptlist.append([r,s])
                        self.count(r,s)
        else:
            a = ['#0000FF','#008000','#FF0000','#00008B','#8B0000','#20B2AA','#000000','#808080']
            x = a[self.n - 1]
            bt = Button(self.root,width = 2,height = 1,fg = x,text = self.n,relief=SUNKEN)
            bt.bind('<Double-Button-1>',self.doubleleft_key)
            bt.grid(row = i,column = j)
            if [i,j] in self.all:
                self.all.remove([i,j])
            self.win()
    def doubleleft_key(self,event):
        mark = 0
        w = event.widget
        g = w.grid_info()
        x = int(g['row'])
        y = int(g['column'])
        a = max(x - 1,3)
        b = min(x+2,self.row +3)
        c = max(0,y-1)
        d = min(y+2,self.column)
        for r in range(a,b):
            for s in range(c,d):
                if [r,s] in self.mark:
                    mark +=1
        if mark == w.cget('text'):
            for r in range(a,b):
                for s in range(c,d):
                    if ([r,s] in self.mark) == False:
                        if [r,s] in self.mine:
                            Button(self.root,text = 'X',fg = 'red',relief=SUNKEN).grid(row = r,column = s)
                            self.state = 'fail'
                        else:
                            if self.state != 'win':
                                self.sweptlist.append([r,s])
                                self.count(r,s)
        if self.state == 'fail':
            self.fail()
    def time(self):
        for i in xrange(1,1000):
            if self.state == 'begin':
                self.timeused = i
                self.timecount.set('%03d'%self.timeused)
                stdout.flush()
                sleep(1)
            
newgame = game()
newgame.start()
