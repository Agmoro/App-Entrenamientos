from tkinter import *
import pandas as pd
from tkinter import ttk
from aux_functions import Auxiliary
from tkinter import StringVar

root = Tk()
root.title("Calendario - FBD")
workbook = pd.ExcelFile("Cursos-DB.xlsx")
df_eventos = pd.read_excel(workbook, "Eventos")
fecval = StringVar()
cursoval = StringVar()
# Treeview
treeframe = ttk.Frame(root)
tree = ttk.Treeview(treeframe)

# Instanciacion Clase Auxiliar
auxiliar = Auxiliary(df_eventos, tree, treeframe, fecval, cursoval)

# Generacion de Treeview
treeframe.grid(row=1, column=2, rowspan=7, pady=4)
auxiliar.InsertTree()
tree.config(displaycolumns=[0, 1, 2, 3])
# Binding con doble click
tree.bind("<Double-1>", auxiliar.clicker)


root.mainloop()
