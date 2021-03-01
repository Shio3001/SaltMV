import tkinter as tk


def test1(event):
    print(event.delta)


window = tk.Tk()

window.bind("<{0}>".format("MouseWheel"), test1, "+")


window.mainloop()
