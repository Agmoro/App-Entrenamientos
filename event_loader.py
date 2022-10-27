from tkinter import N, IntVar, Text, messagebox
import pandas as pd
import tkinter as tk
from tkinter import END, ttk
from aux_functions import Auxiliary
from tkcalendar import DateEntry
from tkinter import StringVar, IntVar
import datetime as dt
from dateutil.relativedelta import relativedelta

root = tk.Tk()
root.title("Carga de Entrenamientos - FBD")
# root.tk.call("lappend", "auto_path", "awthemes-10.4.0")
# root.tk.call("package", "require", "awarc")
# style = ttk.Style()
# style.theme_use("standar")
# Toma de datos desde excel
workbook = pd.ExcelFile("Cursos-DB.xlsx")
df_cursos = pd.read_excel(workbook, "Cursos")
df_eventos = pd.read_excel(workbook, "Eventos").set_index("IDEvento")
df_pasl = pd.read_excel(workbook, "PASL", index_col=False)
df_empleados = pd.read_excel(workbook, "Empleados", index_col=False)[
    ["Legajo", "Nombre", "Apellido"]
]
df_buscaremp = pd.read_excel(workbook, "Empleados", index_col=False)
df_buscaremp = df_buscaremp.astype({"Linea": str, "Legajo": str})

# Generacion de datos con los que trabajar
seleccion_curso = df_cursos[["IDCurso", "Titulo"]]
seleccion_area = df_pasl["Area"].dropna().drop_duplicates().to_numpy().tolist()
seleccion_sector = df_pasl["Sector"].dropna().drop_duplicates().to_numpy().tolist()

seleccion_linea = (
    df_pasl["Linea"].dropna().drop_duplicates().astype(str).to_numpy().tolist()
)

seleccion_puesto = df_pasl["Puesto"].dropna().drop_duplicates().to_numpy().tolist()

# Variables y var de Tkinter
fecval = StringVar()
cursoval = StringVar()
areaval = StringVar()
sectorval = StringVar()
lineaval = StringVar()
puestoval = StringVar()
legval = StringVar()
savelist = pd.DataFrame()

# Titulo
Titulo_l = ttk.Label(root, text="Carga de fechas de curso")
Titulo_l.grid(column=0, columnspan=20, row=0, pady=0, sticky="s")

# Labels, entries y comboboxes
Curso_l = ttk.Label(root, text="Curso:", width=7, anchor="e")
Curso_l.grid(column=0, row=1, padx=4, sticky="e")
Curso_e = ttk.Entry(root, textvariable=cursoval, state="readonly", width=22)
Curso_e.grid(column=1, row=1, padx=4, sticky="e")
Fecha_l = ttk.Label(root, text="Fecha:", width=7, anchor="e")
Fecha_l.grid(column=0, row=2, sticky="e")
Fecha_e = DateEntry(
    root,
    selectmode="day",
    bg="white",
    width=19,
    date_pattern="dd/MM/yyyy",
    textvariable=fecval,
)
Fecha_e.grid(column=1, row=2, padx=4, sticky="e")
Area_l = ttk.Label(root, text="Area", width=7, anchor="e")
Area_l.grid(column=0, row=3, sticky="e")
Area_c = ttk.Combobox(
    root, values=seleccion_area, textvariable=areaval, state="readonly", width=19
)
Area_c.grid(column=1, row=3, padx=4, sticky="e")
Sector_l = ttk.Label(root, text="Sector:", width=7, anchor="e")
Sector_l.grid(column=0, row=4, sticky="e")
Sector_c = ttk.Combobox(
    root, values=seleccion_sector, textvariable=sectorval, state="readonly", width=19
)
Sector_c.grid(column=1, row=4, padx=4, sticky="e")
Linea_l = ttk.Label(root, text="Linea:", width=7, anchor="e")
Linea_l.grid(column=0, row=5, sticky="e")
Linea_c = ttk.Combobox(
    root, values=seleccion_linea, textvariable=lineaval, state="readonly", width=19
)
Linea_c.grid(column=1, row=5, padx=4, sticky="e")
Puesto_l = ttk.Label(root, text="Puesto:", width=7, anchor="e")
Puesto_l.grid(column=0, row=6, sticky="e")
Puesto_c = ttk.Combobox(
    root, values=seleccion_puesto, textvariable=puestoval, state="readonly", width=19
)
Puesto_c.grid(column=1, row=6, padx=4, sticky="e")

# Treeview
treeframe = tk.Frame(root)
tree = ttk.Treeview(treeframe)

# Instanciacion Clase Auxiliar
auxiliar = Auxiliary(seleccion_curso, tree, treeframe, fecval, cursoval)

# Generacion de Treeview
treeframe.grid(row=1, column=2, rowspan=7, pady=4)
auxiliar.InsertTree()

# Binding con doble click
tree.bind("<Double-1>", auxiliar.clicker)

# Treeview en caso de necesitar adicionar legajos adicionales
treeframeemp = tk.Frame(root)
treeemp = ttk.Treeview(treeframeemp)
auxiliaremp = Auxiliary(df_empleados, treeemp, treeframeemp, fecval, legval)
treeframeemp.grid(row=8, column=2, rowspan=8, pady=4)
treeemp.bind("<Double-1>", auxiliaremp.clicker)

# Textbox para registrar legajos adicionales
legtextbox = tk.Text(root, width=25, height=8, borderwidth=1)


def textbox():
    legtextbox.grid(row=8, column=0, columnspan=2, padx=4)


# Traceback del trace de legval
def writetextbox(*args):
    legtextbox.insert(END, f"{legval.get()} ")


def asociados(*args):
    # apertura de archivo .xlsx y generacion de DataFrames a utilizar
    workbook = pd.ExcelFile("Cursos-DB.xlsx")
    df_cursos = pd.read_excel(workbook, "Cursos")
    df_eventos = pd.read_excel(workbook, "Eventos").set_index("IDEvento")
    df_buscaremp = pd.read_excel(workbook, "Empleados", index_col=False)
    df_buscaremp = df_buscaremp.astype({"Linea": str, "Legajo": str})
    # Busqueda y suma de fecha a repetir el curso
    frecuencia = df_cursos[(df_cursos.IDCurso == cursoval.get())]
    frecuencia = (frecuencia["Frecuencia"].values.tolist())[0]
    if not frecuencia == 0:
        fecha = fecval.get().split("/")
        fechadt = dt.datetime(int(fecha[2]), int(fecha[1]), int(fecha[0]))
        fechanueva = fechadt + relativedelta(months=frecuencia)
        fechanueva = fechanueva.strftime("%d/%m/%Y")
    else:
        fechanueva = False
    # Empieza el proceso de generacion de Legajos asociados al curso seleccionado
    emp_asociados = df_cursos.set_index("IDCurso")
    # Limpiar columnas que no van
    emp_asociados = emp_asociados[
        emp_asociados.columns.difference(
            [
                "Titulo",
                "Descripcion",
                "Calificacion que genera",
                "Periodico?",
                "Frecuencia",
                "Instructor_1",
                "Instructor_2",
                "Instructor_3",
                "Instructor_4",
            ],
            sort=False,
        )
    ]
    emp_asociados = emp_asociados.transpose()
    # Limpiar todos lo que no sean el curso elegido
    emp_asociados.drop(
        emp_asociados[emp_asociados[cursoval.get()] == False].index, inplace=True
    )

    emp_asociados = emp_asociados.index.values.tolist()
    # Buscar legajos con parametros filtrados por Area, sector, puesto y linea
    leg_asociados = df_buscaremp[
        df_buscaremp[["Area", "Sector", "Puesto", "Linea"]].isin(emp_asociados).any(1)
    ]
    leg_asociados = leg_asociados["Legajo"].values.tolist()
    # Agregar "N" al final del legajo para indicar que todavia no hicieron el curso
    contador = 0
    for leg in leg_asociados:
        leg = f"{leg}N"
        leg_asociados[contador] = leg
        contador += 1
    # Cabeceras de columnas de legajos (leg001, leg002.... leg00n)
    collegasoc = []
    for l in range(1, len(leg_asociados) + 1, 1):
        ext = f"leg{str(l).rjust(3,'0')}"
        collegasoc.append(ext)
    # con cabeceras y contenido crear diccionario
    lotuples1 = dict(zip(collegasoc, leg_asociados))
    try:
        lotuples = {
            "IDEvento": df_eventos.index[-1] + 1,
            "IDCurso": cursoval.get(),
            "Fecha Cap.": fecval.get(),
            "Proxima cap.": fechanueva,
        }
    except:
        lotuples = {
            "IDEvento": 0,
            "IDCurso": cursoval.get(),
            "Fecha Cap.": fecval.get(),
            "Proxima cap.": fechanueva,
        }
    # combinar el index generado --> IDEvento, y otros datos a los legajos asociados, index -1 es la ultima entrada
    lotuples.update(lotuples1)
    # generar el DataFrame a agregar
    df_cargaeventos = pd.DataFrame(lotuples, index=[0])
    df_cargaeventos = df_cargaeventos.set_index("IDEvento")
    result = [df_eventos, df_cargaeventos]

    global savelist
    savelist = pd.concat(result)
    print(savelist)
    return savelist


def carga(savelist: pd.DataFrame()):
    with pd.ExcelWriter(
        "Cursos-DB.xlsx", mode="a", engine="openpyxl", if_sheet_exists="overlay"
    ) as writer:
        savelist.to_excel(writer, sheet_name="Eventos")


# Trace de legval y cursoval
legval.trace_add("write", writetextbox)
cursoval.trace_add("write", asociados)

# Frame de botones
botonframe = tk.Frame(root)
botonframe.grid(row=7, column=0, columnspan=2, sticky="n")
# Separator
ahor_sep = ttk.Separator(botonframe, orient="horizontal")
ahor_sep.pack(side="top", fill="x", expand=True, pady=3, padx=4)
# Separator
bhor_sep = ttk.Separator(botonframe, orient="horizontal")
bhor_sep.pack(side="bottom", fill="x", expand=True, pady=3, padx=4)
# Botones
cargar_b = ttk.Button(botonframe, text="Cargar Evento")
cargar_b.pack(side="left", pady=3, padx=4)

extraleg_b = ttk.Button(botonframe, text="Legajos Adicionales")


# Para desabilitar creacion de extra treeviews
def disablebut():
    extraleg_b.config(state="disable")


"""
def carga():
    confirmation = messagebox.askokcancel(
        "Confirmacion",
        message=f"Estas seguro de cargar estos datos?\n\n" +
        f"Curso: {cursoval.get()}\n" + f"Area: {areaval.get()}\n" +
        f"Sector: {sectorval.get()}\n" + f"Puesto: {puestoval.get()}\n" +
        f"Linea: {lineaval.get()}\n" +
        f"Legajos adicionales: {legtextbox.get('1.0', 'end-1c').split()}",
    )
    if confirmation == True:
        if areaval.get() != "Todos":
            emp = df_buscaremp[(df_buscaremp.Area == areaval.get())
                               | (df_buscaremp.Sector == sectorval.get())
                               | (df_buscaremp.Puesto == puestoval.get())
                               | (df_buscaremp.Linea == lineaval.get())]
            emplist = emp["Legajo"].tolist()
        elif areaval.get() == "Todos":
            emplist = df_buscaremp["Legajo"].tolist()
        else:
            messagebox.askokcancel("ERROR!", "Se ha producido un error.")
        # if legtextbox.get("1.0", "end-1c") != " ":
        boxtextlist = legtextbox.get("1.0", "end-1c").split()
        empboxlist = list(set(emplist + boxtextlist))

"""
cargar_b.configure(command=lambda: carga(savelist))

extraleg_b.config(command=lambda: [auxiliaremp.InsertTree(), textbox(), disablebut()])
extraleg_b.pack(side="right", pady=3, padx=4)

root.mainloop()
