####
## desc: sudoku solver, brute force, gui using tkinter
####


from tkinter import *
from random import randint
from collections import Counter


# constants so gui can be easily modified for testing, etc

HEIGHT = 850
WIDTH = 800


# main window
class MainWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.mainsetup(master)
        self.master.title("sudoku solver 5000")

    def mainsetup(self, master):
        for r in range(3):
            self.master.rowconfigure(r, weight=1)
        for c in range(2):
            self.master.columnconfigure(c, weight=1)
        frame_numblock = Frame(master, bg="red", bd=1, relief=GROOVE)
        frame_numblock.grid(row=0, column=0, columnspan=2, sticky=W + E + N + S)
        frame_board = Frame(master, bg="blue", bd=2)
        frame_board.grid(row=1, column=0)

        # def lock(self, *args):
        #     temp = limiter.get()
        #     if len(temp) > 2: limiter.set(temp[:2])
        #
        # limiter = StringVar()
        # limiter.trace('w', lock)
        def lock(*args):
            temp = oneChar.get()
            if len(temp) > 1: oneChar.set(temp[:1])

        oneChar = StringVar()
        oneChar.trace('w', lock)

            # e1 = Entry(frame_numblock, textvariable=0, font=("Arial", 30))
            # e1.pack(ipady=5)
            # e2 = Entry(frame_numblock, textvariable=oneChar, font=("Arial", 30))
            # e2.pack(ipady=5)
            # e3 = Entry(frame_numblock, textvariable=oneChar, width=3, justify=CENTER, font=("Arial", 30))
            # e3.pack(ipady=5)

        b1 = Button(frame_numblock, text="get thing",
                    command=lambda: print("The value in this place is {}.".format(pos_list[0][2].get())))
        b1.grid()
        b2 = Button(frame_numblock, text="get different thing",
                    command=lambda: print("The value in this place is {}.".format(pos_list[0][2].set("xx"))))
        b2.grid()
        b3 = Button(frame_numblock, text="get gridvals",
                    command=lambda: get_grid_vals())
        b3.grid()
        b4 = Button(frame_numblock, text="print value grid formatted",
                    command=lambda: print_grid_formatted())
        b4.grid()
        b5 = Button(frame_numblock, text="print raw gridvals (row)",
                    command=lambda: print_grid_formatted("raw"))
        b5.grid(row=0, column=3)
        b6 = Button(frame_numblock, text="solve",
                    command=lambda: solver())
        b6.grid(row=1, column=5)
        b7 = Button(frame_numblock, text="check rows",
                    command=lambda: check_all())
        b7.grid(row=2, column=5)
        b8 = Button(frame_numblock, text="convert raw list to column",
                    command=lambda: col_test())
        b8.grid(row=1, column=3)
        b9 = Button(frame_numblock, text="convert raw list to grid",
                    command=lambda: grid_test())
        b9.grid(row=2, column=3)

        b9 = Button(frame_numblock, text="randomly fill grid",
                    command=lambda: grid_fill())
        b9.grid(row=4, column=4)
        b9 = Button(frame_numblock, text="row fill grid",
                    command=lambda: grid_fill("ROW"))
        b9.grid(row=5, column=4)
        b9 = Button(frame_numblock, text="column fill grid",
                    command=lambda: grid_fill("COLUMN"))
        b9.grid(row=6, column=4)
        # b9 = Button(frame_numblock, text="grid fill grid",        ##this is harder to do.
        #             command=lambda: grid_fill("GRID"))
        # b9.grid(row=7, column=4)

        b9 = Button(frame_numblock, text="clear grid",
                    command=lambda: grid_clear())
        b9.grid(row=3, column=4)

        b9 = Button(frame_numblock, text="lock input",
                    command=lambda: lock_input())
        b9.grid(row=0, column=5)

        def get_grid_vals():
            gridlist = []
            for i in range(ROWS):
                gridlist.append([])
                for k in range(COLS):
                    temp = pos_list[i][k].get()
                    try:
                        temp=int(temp)
                    except ValueError:
                        temp=0
                    gridlist[i].append(temp)
            return gridlist

        # generates nums with commas, spaces, []
        def print_grid_formatted(*formats):
            raw = get_grid_vals()
            if "raw" in formats:
                print(raw)
            else:
                for i in range(ROWS):
                    print(raw[i])



        def close(*args):
            temp = oneChar.get()
            if len(temp) > 1: oneChar.set(temp[:1])

        oneChar = StringVar()
        oneChar.trace('w', lock)

        ROWS = COLS = 9
        pos_list = [0] * ROWS
        val_list = [0] * ROWS
        for x in range(ROWS):
            pos_list[x] = [0] * COLS
            val_list[x] = [0] * COLS
        ##for character limiting through textvariable, potentially

        for i in range(ROWS):
            for k in range(COLS):
                color = "white"
                # gray pattern for NSWE blocks
                if i in [0, 1, 2, 6, 7, 8] and k in [3, 4, 5] or i in [3, 4, 5] and k in [0, 1, 2, 6, 7, 8]:
                    color = "#BEBEBE"
                pos_list[i][k] = Entry(frame_board, width=3, bg=color, justify=CENTER, font=("Arial", 30))
                pos_list[i][k].grid(row=i, column=k)
                ##testing
                # print(pos_list[i][k])
                # print(val_list)
######## testing
        def grid_clear():
            for i in range(9):
                for k in range(9):
                    pos_list[i][k].delete(0,END)


        def grid_fill(*args):
            arglist = ["ROW", "COL"]
            for arglist in args:
                if arglist == "ROW":
                    for i in range(9):
                        for k in range(9):
                            pos_list[i][k].delete(0, END)
                            pos_list[i][k].insert(0, k+1)
                else:
                    for i in range(9):
                        for k in range(9):
                            pos_list[i][k].delete(0, END)
                            pos_list[i][k].insert(0, i+1)
                return
            for i in range(9):
                for k in range(9):
                    pos_list[i][k].delete(0, END)
                    pos_list[i][k].insert(0,randint(1,9))



        def check_all():
            key = make_key()

            raw = get_grid_vals()
            arg = "row"
            ok = check_each(raw, key, arg)
            if ok is False: return

            col_list = column_format(raw)
            arg = "col"
            ok = check_each(col_list, key, arg)
            if ok is False: return

            grid_list = grid_format(get_grid_vals())
            arg = "grid"
            ok = check_each(grid_list, key, arg)
            if ok is False: return
            print("looks like it worked")


###### very wip

        def lock_input():   #set initial input values as "do not change" for solving algorithm
            #get values, go through list, if value !=0, append the position to a list.
            #then we can compare each position value to see if its on that list, if no, it's free to change
            locked_positions = []
            raw = get_grid_vals() #get all values, 0 for empty, else whole num
            for i in range(9):
                for k in range(9):
                    pos_list[i][k].config(fg="black", relief="groove")   #resets color on empty cells, for relocking
                    if raw[i][k] != 0:
                        #returns list with format ['row, column']
                        locked_positions.append("{},{}".format(i,k))
                        #recolor locked positions, so it's obvious they've changed
                        #maybe change the border or something?
                        pos_list[i][k].config(fg="red", relief="solid")
            print(locked_positions)

######### formatting data for checking

        # works perfectly
        def column_format(rawlist):
            col_list = []
            for i in range(9):
                temp = []
                for k in range(9):
                    temp.append(rawlist[k][i])
                col_list.append(temp)
            return col_list

        #works perfectly
        def grid_format(rawlist):
            grid_list = []
            for x in range(9): # 9 total passes for 9 total grids
                temp = []   #clear every pass for a new grid
                for i in range(3):  #columns
                    for k in range(3):  #rows
                        temp.append(rawlist[i].pop(0)) # remove left-most column element every pass
                if (x+1)%3 == 0:    #every 3 passes, delete the first three lists (ie: the top 3 grids)
                    for y in range(3):
                        del rawlist[0]
                grid_list.append(temp)
            return grid_list


        def col_test():
            raw=get_grid_vals()
            col_list = column_format(raw)
            print(col_list)

        def grid_test():
            raw=get_grid_vals()
            grid_list = grid_format(raw)
            print(grid_list)


############# checking correctness
        def make_key():
            keylist = []
            for i in range(1, 10):
                keylist.append(i)
            return Counter(keylist)

        def check_each(rawlist, key, *args):
            # takes perfect keylist [1,9], counts occurrences, if count of current row matches, it's valid, sort independent
            options = ["row", "col", "grid"]
            type_ = "pass"
            for options in args:
                type_ = options

            print(rawlist)
            for i in range(ROWS):
                currentrow = Counter(rawlist[i])
                if currentrow == key:
                    print("{} {} is valid".format(type_, i + 1))
                else:
                    print("fail on {} {}".format(type_, i + 1))
                    return False

        # def checker(rawlist):
        #     arg = "row"
        #     key = make_key()
        #     check_each(rawlist, key, arg)

        def solver():
            #current_list = get_grid_vals()
            checker(get_grid_vals())


def begin():
    pass


####################
w1 = Tk()
w1.geometry("{}x{}".format(WIDTH, HEIGHT))
introscreen = MainWindow(w1)
mainloop()
