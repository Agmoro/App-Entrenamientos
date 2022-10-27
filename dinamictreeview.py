import tkinter as tk
from tkinter import ttk
import pandas as pd

root = tk.Tk()
workbook = pd.ExcelFile("Cursos-DB.xlsx")
df_cursos = pd.read_excel(workbook, "Cursos")
df_empleados = pd.read_excel(workbook, "Empleados")


def Ancho_Columna(df):
    len_col = {"": 0}
    for column in df:
        headcount = 0
        col_element_list = df[column]
        charcount = 0
        headuppcount = 0
        headlowcount = 0
        for character in str(column):
            if character.isupper() or character.isnumeric():
                headuppcount += 4
            elif character.islower() or character.isdigit():
                headlowcount += 3
        headcount = headuppcount + headlowcount

        for element in col_element_list:
            uppernumcount = 0
            lowercount = 0
            charcount_temp = 0

            for character in str(element):
                if character.isupper() or character.isnumeric():
                    uppernumcount += 4
                elif character.islower() or character.isdigit():
                    lowercount += 3
            charcount_temp = lowercount + uppernumcount
            if charcount_temp > charcount:
                charcount = charcount_temp
        if headcount > charcount:
            headict = {column: headcount}
            len_col.update(headict)
        else:
            charcountdict = {column: charcount}
            len_col.update(charcountdict)

    return len_col


def InsertTree(root, df, row, column):
    treeframe = tk.Frame(root)
    tree = ttk.Treeview(treeframe)
    cols = list(df.columns)
    treeframe.grid(row=row, column=column)
    scroll_y_arbol = ttk.Scrollbar(treeframe)
    scroll_y_arbol.pack(side="right", fill="y")
    scroll_h_arbol = ttk.Scrollbar(treeframe, orient=tk.HORIZONTAL)
    scroll_h_arbol.pack(side="bottom", fill="x")
    tree.pack()
    tree["columns"] = cols
    anchocol = Ancho_Columna(df)
    df_rows = df.to_numpy().tolist()
    for i in cols:
        tree.column(i, width=anchocol.get(i) * 3, stretch=False, anchor="w")
        tree.heading(i, text=i, anchor="w")
    for row in df_rows:
        tree.insert("", "end", values=row)
    # for index, row in df.iterrows():
    #     tree.insert("", 0, text=index, values=list(row))
    tree.column("#0",
                width=0)  # manera de que la justificacion de columnas funcione
    scroll_y_arbol.config(command=tree.yview)
    scroll_h_arbol.config(command=tree.xview)


def BorrarArbol(widget):
    widget.pack_forget()
    root.update()


treebutton = tk.Button(root,
                       text="Cursos",
                       command=lambda: InsertTree(root, df_cursos, 1, 2))
treebutton2 = tk.Button(root,
                        text="Empleados",
                        command=lambda: InsertTree(root, df_empleados, 1, 2))
treebutton3 = tk.Button(root, text="Borrar")
treebutton2.grid(row=2, column=1)
treebutton3.grid(row=3, column=1)
treebutton.grid(row=1, column=1)

root.mainloop()
