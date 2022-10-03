import pandas as pd
import tkinter as tk
from tkinter import END, Entry, ttk
from aux_functions import Auxiliary
from tkcalendar import DateEntry
from tkinter import StringVar


root = tk.Tk()

# Toma de datos desde excel
workbook = pd.ExcelFile("Cursos-DB.xlsx")
df_cursos = pd.read_excel(workbook, "Cursos")
df_pasl = pd.read_excel(workbook, "PASL")

# Generacion de datos con los que trabajar
seleccion_curso = df_cursos[["ID-Curso", "Titulo"]]
seleccion_area = df_pasl["Area"].dropna().drop_duplicates().to_numpy().tolist()
seleccion_sector = df_pasl["Sector"].dropna().drop_duplicates().to_numpy().tolist()
seleccion_linea = (
    df_pasl["Linea"].dropna().drop_duplicates().astype(str).to_numpy().tolist()
)
seleccion_puesto = df_pasl["Puesto"].dropna().drop_duplicates().to_numpy().tolist()

# Variables de Tkinter
fecval = StringVar()
cursoval = StringVar()
areaval = StringVar()
sectorval = StringVar()
lineaval = StringVar()
puestoval = StringVar()

# Titulo
Titulo_l = tk.Label(root, text="Carga de fechas de curso")
Titulo_l.grid(column=0, columnspan=5, row=0)

# Labels y entries
Curso_l = tk.Label(root, text="Curso:")
Curso_l.grid(column=0, row=1)
Curso_e = Entry(root, textvariable=cursoval, state="readonly")
Curso_e.grid(column=1, row=1)
Fecha_l = tk.Label(root, text="Fecha:")
Fecha_l.grid(column=0, row=2)
Fecha_e = DateEntry(
    root,
    selectmode="day",
    bg="white",
    width=18,
    date_pattern="dd/MM/yyyy",
    textvariable=fecval,
)
Fecha_e.grid(column=1, row=2)
Area_l = tk.Label(root, text="Area")
Area_l.grid(column=0, row=3)
Area_c = ttk.Combobox(
    root,
    values=seleccion_area,
    textvariable=areaval,
    state="readonly",
)
Area_c.grid(column=1, row=3)
Sector_l = tk.Label(root, text="Sector:")
Sector_l.grid(column=0, row=4)
Sector_c = ttk.Combobox(
    root,
    values=seleccion_sector,
    textvariable=sectorval,
    state="readonly",
)
Sector_c.grid(column=1, row=4)
Linea_l = tk.Label(root, text="Linea:")
Linea_l.grid(column=0, row=5)
Linea_c = ttk.Combobox(
    root,
    values=seleccion_linea,
    textvariable=lineaval,
    state="readonly",
)
Linea_c.grid(column=1, row=5)
Puesto_l = tk.Label(root, text="Puesto:")
Puesto_l.grid(column=0, row=6)
Puesto_c = ttk.Combobox(
    root,
    values=seleccion_puesto,
    textvariable=puestoval,
    state="readonly",
)
Puesto_c.grid(column=1, row=6)

# Treeview
treeframe = tk.Frame(root)
tree = ttk.Treeview(treeframe)

# Instanciacion Clase Auxiliar
auxiliar = Auxiliary(seleccion_curso, tree, treeframe, fecval, cursoval)
# Generacion de Treeview
treeframe.grid(row=1, column=2, rowspan=8)
auxiliar.InsertTree()


# Binding con doble click
tree.bind("<Double-1>", auxiliar.clicker)


root.mainloop()
