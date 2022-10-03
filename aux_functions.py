import tkinter as tk
from tkinter import ttk
import pandas as pd


class Auxiliary:
    df = ""
    arbol = ""
    fecval = ""
    cursoval = ""

    def __init__(self, df, arbol, arbolframe, fecval, cursoval):
        self.df = df
        self.arbol = arbol
        self.arbolframe = arbolframe
        self.fecval = fecval
        self.cursoval = cursoval

    def Ancho_Columna(self):
        len_col = {"": 0}
        max_len = 0

        for column in self.df:
            max_len = 0
            headcol = len(str(column))
            for i in range(len(self.df[column])):
                ele_i = len(str(self.df[column][i]))
                if max_len < ele_i:
                    max_len = ele_i
            if headcol > max_len:
                headict = {column: headcol}
                len_col |= headict
            else:
                maxdict = {column: max_len}
                len_col |= maxdict
        return len_col

    def InsertTree(self):
        cols = list(self.df.columns)
        scroll_y_arbol = ttk.Scrollbar(self.arbolframe)
        scroll_y_arbol.pack(side="right", fill="y")
        scroll_h_arbol = ttk.Scrollbar(self.arbolframe, orient=tk.HORIZONTAL)
        scroll_h_arbol.pack(side="bottom", fill="x")
        self.arbol.pack()
        self.arbol["columns"] = cols
        anchocol = self.Ancho_Columna()
        df_rows = self.df.to_numpy().tolist()
        for i in cols:
            self.arbol.column(i, width=anchocol.get(i) * 9, stretch=True, anchor="w")
            self.arbol.heading(i, text=i, anchor="w")
        for row in df_rows:
            self.arbol.insert("", "end", values=row)
        # for index, row in df.iterrows():
        #     arbol.insert("", 0, text=index, values=list(row))
        self.arbol.column(
            "#0", width=20, stretch=True
        )  # manera de que la justificacion de columnas funcione
        scroll_y_arbol.config(command=self.arbol.yview)
        scroll_h_arbol.config(command=self.arbol.xview)

    def clicker(self, e):
        self.cursoval.set("")
        selected = self.arbol.focus()
        values = self.arbol.item(selected, "values")
        self.cursoval.set(values[0])
