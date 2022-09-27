from tkinter import *
from tkinter import ttk
import random
import sys


root = Tk()
style = ttk.Style()
style.configure("BW.TLabel", foreground="white", background="darkblue")
txt = Text()
txt.pack(side="bottom")


class PrintToTXT(object):
    def write(self, s):
        txt.insert(END, s)


sys.stdout = PrintToTXT()
print("probando a ver que onda")
print("hola que tal")
contar = 0


def Arbolito():
    global contar
    valores = []

    for i in range(6):
        valores.clear()
        for j in range(6):
            valores.append(random.randint(1, 500))

        arbol.insert(
            parent="",
            index="end",
            iid=contar,
            text="",
            values=valores,
        )
        contar += 1

    return contar


et1 = ttk.Label(root, text="Hola, es una prueba", style="BW.TLabel")
et1.pack()

style2 = ttk.Style()
style2.map(
    "C.TButton",
    foreground=[("pressed", "red"), ("active", "blue")],
    background=[("pressed", "!disabled", "black"), ("active", "white")],
)

colored_btn = ttk.Button(
    text="llenar tabla", style="C.TButton", command=lambda: Arbolito()
)
colored_btn.pack(side="top")
colored_btn2 = ttk.Button(
    text="poner tabla", style="C.TButton", command=lambda: Ponerarbol()
)
colored_btn2.pack(side="top")


def Ponerarbol():
    color2 = "white"
    color3 = "black"
    color4 = "orange"

    m_arbol = Frame(root)
    m_arbol.pack()

    style3 = ttk.Style()
    # style3.theme_use("default")
    style3.configure(
        "Treeview",
        background=color2,
        foreground=color3,
        rowheight=20,
        fieldbackground=color2,
    )

    style3.map("Treeview", background=[("selected", color4)])

    scroll_arbol = Scrollbar(m_arbol)
    scroll_arbol.pack(side="right", fill="y")

    arbol = ttk.Treeview(m_arbol, yscrollcommand=scroll_arbol.set)
    arbol["columns"] = (
        "N°",
        "Fecha",
        "Proveedor",
        "Producto",
        "Defecto",
        "Cantidad",
    )

    arbol.column("#0", width=0, stretch="no")
    arbol.column("N°", anchor="center", width=40)
    arbol.column("Fecha", anchor="w", width=60)
    arbol.column("Proveedor", anchor="w", width=120)
    arbol.column("Producto", anchor="w", width=120)
    arbol.column("Defecto", anchor="w", width=120)
    arbol.column("Cantidad", anchor="center", width=80)

    arbol.heading("#0", text="")
    arbol.heading("N°", text="N°", anchor="center")
    arbol.heading("Fecha", text="Fecha", anchor="center")
    arbol.heading("Proveedor", text="Proveedor", anchor="w")
    arbol.heading("Producto", text="Producto", anchor="w")
    arbol.heading("Defecto", text="Defecto", anchor="w")
    arbol.heading("Cantidad", text="Cantidad", anchor="center")

    arbol.pack(side="bottom")

    scroll_arbol.config(command=arbol.yview)

    global contar
    valores = []

    for i in range(6):
        valores.clear()
        for j in range(6):
            valores.append(random.randint(1, 500))

        arbol.insert(
            parent="",
            index="end",
            iid=contar,
            text="",
            values=valores,
        )
        contar += 1

    return contar


root.mainloop()
