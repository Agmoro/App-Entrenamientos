import pandas as pd
import tkinter as tk
from tkinter import ANCHOR, Listbox, ttk, END, MULTIPLE
from aux_functions import Auxiliary
from tkinter import StringVar

root = tk.Tk()
root.title("Generar Resumen de Entrenamiento - FBD")

# Toma de datos desde excel
workbook = pd.ExcelFile("Cursos-DB.xlsx")
df_cursos = pd.read_excel(workbook, "Cursos")
df_eventos = pd.read_excel(workbook, "Eventos")
df_eventos = df_eventos[["IDEvento", "IDCurso", "Fecha Cap.", "Proxima cap."]]

fecval = StringVar()
eventval = StringVar()

# Labels, entries y comboboxes
Curso_l = ttk.Label(root, text="Evento:", width=7, anchor="e")
Curso_l.grid(column=0, row=1, padx=4, sticky="e")
Curso_e = ttk.Entry(root, textvariable=eventval, state="readonly", width=22)
Curso_e.grid(column=1, row=1, padx=4, sticky="e")
lbox1 = tk.Listbox(root, width=10, activestyle="none", selectmode=MULTIPLE)
lbox2 = tk.Listbox(root, width=10)

# Treeview
treeframe = tk.Frame(root)
tree = ttk.Treeview(treeframe)

# Instanciacion Clase Auxiliar
auxiliar = Auxiliary(df_eventos, tree, treeframe, fecval, eventval)

# Generacion de Treeview
treeframe.grid(row=1, column=2, columnspan=4, rowspan=7, pady=4)
auxiliar.InsertTree()

# Binding con doble click
tree.bind("<Double-1>", auxiliar.clicker)


def removerleg(lbox: Listbox):
    for item in reversed(lbox.curselection()):
        lbox.delete(item)


def notoyes(eventval: StringVar):
    workbook = pd.ExcelFile("Cursos-DB.xlsx")
    eventos = pd.read_excel(workbook, "Eventos").set_index("IDEvento")
    eventosmod = pd.read_excel(workbook, "Eventos").set_index("IDEvento")
    # Remover columnas que no necesitan ser modificadas
    eventosmod = eventosmod[
        eventosmod.columns.difference(
            ["IDCurso", "Fecha Cap.", "Proxima Cap.", "Proxima cap."]
        )
    ]
    # Elegir fila a modificar "N" a "Y"
    fila = eventosmod.loc[int(eventval.get())]
    fila = fila.str.replace("N", "Y")  # Devuelve una serie
    fila = fila.to_frame()  # Lo pasamos a DF
    fila = fila.transpose()  # lo acomodamos
    fila.index.rename(
        "IDEvento", inplace=True
    )  # Regeneramos el index con su nombre original
    eventos.update(fila)  # Actualizamos eventos


def detallar(lbox: Listbox):
    lbox.delete(0, END)
    workbook = pd.ExcelFile("Cursos-DB.xlsx")
    eventos = pd.read_excel(workbook, "Eventos").set_index("IDEvento")
    eventosmod = pd.read_excel(workbook, "Eventos").set_index("IDEvento")
    eventosmod = eventosmod[
        eventosmod.columns.difference(
            ["IDCurso", "Fecha Cap.", "Proxima Cap.", "Proxima cap."]
        )
    ]
    fila = eventosmod.loc[int(eventval.get())]
    fila = fila.str.replace("N", "").dropna()
    fila = fila.tolist()
    for f in range(len(fila)):
        lbox.insert(END, fila[f])


# Frame de botones
botonframe = tk.Frame(root)
botonframe.grid(row=7, column=0, columnspan=2, sticky="s")
# Separator
ahor_sep = ttk.Separator(botonframe, orient="horizontal")
ahor_sep.pack(side="top", fill="x", expand=True, pady=3, padx=4)
# Separator
bhor_sep = ttk.Separator(botonframe, orient="horizontal")
bhor_sep.pack(side="bottom", fill="x", expand=True, pady=3, padx=4)
# Botones
realizado_b = ttk.Button(botonframe, text="Evento Realizado")
realizado_b.pack(side="left", pady=3, padx=4)

detalle_b = ttk.Button(botonframe, text="Detallar presentes")
realizado_b.configure(command=lambda: notoyes(eventval))

detalle_b.config(command=lambda: detallar(lbox1))
detalle_b.pack(side="right", pady=3, padx=4)

remover_b = tk.Button(
    root,
    text=f"Remover legajo\n" f"-->",
    justify="center",
    width=15,
    command=lambda: removerleg(lbox1),
)
anadir_b = tk.Button(root, text="Añadir legajo\n" f"<--", justify="center", width=15)
confirmar_b = tk.Button(root, text="Confirmar\n" f"cambios", width=15)

remover_b.grid(column=1, row=8, padx=4, pady=3)
anadir_b.grid(column=1, row=9, padx=4, pady=3)
confirmar_b.grid(column=1, row=10, padx=4, pady=3)

lbox1.grid(column=0, row=8, columnspan=1, rowspan=3, pady=3, padx=4, sticky="nw")
lbox2.grid(column=2, row=8, columnspan=1, rowspan=3, pady=3, padx=4, sticky="nw")

root.mainloop()
