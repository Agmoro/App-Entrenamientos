import pandas as pd
import numpy as np

# import sys
from tkinter import *
from tkinter import ttk

root = Tk()
# root.geometry("580x250")

dates = pd.date_range("20210101", periods=8)
df = pd.DataFrame(np.random.randn(8, 5), index=dates, columns=list("ABCDE"))

# [txt = Text(root)
# txt.pack()


# class PrintToTXT(object):
#     def write(self, s):
#         txt.insert(END, s)


# sys.stdout = PrintToTXT()

# print(
#     "Pandas date range of 8 values in 1 timestamp column adjacent to a numpy random float array of 8 rows and 4 columns, displayed in a Tkinter table"
# )

# print(dframe)
# print(type(dframe))

# mainloop()]
# root = tk.Tk()

# sample = {"File Name":[f"file_{i}" for i in range(5)],
#           'Sheet Name': [f"sheet_{i}" for i in range(5)],
#           'Number Of Rows': [f"row_{i}" for i in range(5)],
#           'Number Of Columns': [f"col_{i}" for i in range(5)]
#           }
# df = pd.DataFrame(sample)
cols = list(df.columns)

tree = ttk.Treeview(root)
tree.pack()
tree["columns"] = cols
for i in cols:
    tree.column(i, anchor="w")
    tree.heading(i, text=i, anchor="w")

for index, row in df.iterrows():
    tree.insert("", 0, text=index, values=list(row))

root.mainloop()
