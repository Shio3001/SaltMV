# test
from copy import deepcopy
import tkinter as tk


class main:
    def __init__(self):
        pass

    def main(self):
        self.window = tk.Tk()
        self.window.title("name")

        M = tk.Menu(self.window)
        self.window.config(menu=M)

        def aba():
            print("aba")

        r = tk.Menu(M, tearoff=0)
        r.add_command(label="みなさん", command=aba)  # それぞれ
        r.add_command(label="ああああ", command=aba)  # それぞれ
        r.add_command(label="いいいい", command=aba)  # それぞれ

        M.add_cascade(label="ee", menu=r)  # それぞれ

        self.window.mainloop()
        #self.pull_down[main_bar].add_command(label=n, command=p)


main1 = main()
main1.main()
