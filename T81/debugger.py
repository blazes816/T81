from tkinter import *

class Debugger(Frame):
    """ A debugging panel for the T81 CPU and environment """
    def __init__(self, master, size=(600, 400)):
        self.master, self.size = master, size
        super().__init__(master, width=size[0], height=size[1])
        self.pack()
        self.load()

    def load(self):
        self.l_registers = Label(self, text="Registers:")
        self.l_registers.pack()

        for r in list(cpu.REGISTERS.keys()).sort():
          attr, label = "l_%s" % r, "%s:" % r
          setattr(self, attr , Label(self, text=label, pady=10))
          getattr(self, attr).pack(side=LEFT)

          attr = attr + "_val"
          setattr(self, attr , Label(self, text="FF00FF00", pady=10))
          getattr(self, attr).pack(side=LEFT)


def Start():
    root = Tk()
    app = Debugger(root, (600, 400))
    root.mainloop()
