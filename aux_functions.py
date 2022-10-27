import tkinter as tk
from tkinter import ttk


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
        len_col = {
            "": 0
        }  # diccionario que guarda longitudes de characteres key=column:value=long
        for column in self.df:
            # element count variables
            col_element_list = self.df[column]
            charcount = 0
            # heading count variables
            headcount = 0
            headuppcount = 0
            headlowcount = 0

            # heading count
            for character in str(column):
                if character.isupper() or character.isnumeric():
                    headuppcount += 4
                elif character.islower() or character.isdigit():
                    headlowcount += 3
            headcount = headuppcount + headlowcount

            # element count
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

            # count pass to dict
            if headcount > charcount:
                headict = {column: headcount}
                len_col.update(headict)
            else:
                charcountdict = {column: charcount}
                len_col.update(charcountdict)

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
            self.arbol.column(i, width=anchocol.get(i) * 3, stretch=True, anchor="w")
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
        selected = self.arbol.focus()
        values = self.arbol.item(selected, "values")
        self.cursoval.set(values[0])
        return self.cursoval.get()
