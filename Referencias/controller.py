from tkinter import Tk
import Referencias.view as view


class Controlador:
    def __init__(self, window):
        self.root = window
        self.objctrl = view.Ventana(self.root)


if __name__ == "__main__":
    root_ctrl = Tk()
    myapp = Controlador(root_ctrl)
    root_ctrl.mainloop()
