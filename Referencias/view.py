from tkinter import Label
from tkinter import Radiobutton
from tkinter import Entry
from tkinter import StringVar
from tkinter import Button
from tkinter import Frame
from tkinter import Scrollbar
from tkinter import ttk
from tkinter.font import Font
from tkinter import IntVar
from Referencias.model import ABMC
from tkcalendar import DateEntry
from babel.numbers import *  # esto esta aca por que para hacer un ejecutable, el pyinstaller no encontraba el hidden import

# Lo que sigue a continuación eventualmente lo ########
# metere en otra base de datos, pero no queria ########
# doble CRUD todavia ##################################

def_cajas = [
    "curvas",
    "deslaminadas",
    "error de impresión",
    "error paletizado",
    "humedas/mojadas",
]

def_botellas = [
    "dimensiones fuera de especificación",
    "lamparones",
    "espejadas",
    "weathering",
    "paletizado dañado/hardboard",
    "vidrio fino",
    "contaminación",
    "error palletizado",
]

def_etiquetas = [
    "liner dañado",
    "error de impresión",
    "mal bobinado",
    "error de identificación",
    "no despega",
    "textos desactulizados",
]

def_tapas = [
    "error impresión",
    "medidas fuera de especificación",
    "falta componente",
    "rotas",
    "inserto suelto",
    "golpeadas",
    "contaminación",
]

def_film = ["corta film", "contaminación", "distribución no uniforme"]

prod_cajas = [
    "Caja FB 12/75 cl",
    "Caja CB 6/70 cl",
    "Caja BM 6/75 cl",
    "Caja FB 12/45 cl",
    "Caja Ser Trad 12/70 cl",
    "Caja PEM 6/75 cl" "Caja Carpano Rosso" "Caja Carpano Bianco",
]
prod_botellas = [
    "Bot. FB/BM 75 cl",
    "Bot. FB/BM 45 cl",
    "Bot. CB/BM 70 cl",
    "Bot PEM 75 cl",
    "Bot Carpano 95 cl",
    "Bot Sernova 70 cl",
    "Bot FB/BM/PEM 5 cl",
    "Bot CB 5 cl",
]
prod_etiquetas = [
    "Etiq. FB 75 cl",
    "C/Etiq. FB 75 cl",
    "Etiq. FB 45 cl",
    "C/Etiq. FB 45 cl",
    "Etiq. CB 70 cl",
    "C/Etiq. CB 05 cl",
    "Etiq. BM 75 cl",
    "C/Etiq. BM 75 cl",
    "Etiq. BM 45 cl",
    "C/Etiq. BM 45 cl",
    "Etiq. FB 5 cl",
    "C/Etiq. FB 5 cl",
]
prod_tapas = [
    "Tapa FB 75/100 cl",
    "Tapa PEM 75 cl",
    "Tapa Carpano Rosso",
    "Tapa Carpano Bianco",
    "Tapon Sernova",
    "Tapa BM 75 cl",
    "Tapa FB 45 cl",
    "Tapa BM 45 cl",
    "Tapa PEM 5 cl",
    "Tapa FB 5 cl",
]

prod_film = ["film envolvedora", "film manual", "film techo pallet"]

# Clase Proveedor - maneja los dropboxes ##############
#######################################################


class Proveedor:
    nombre = ""
    defectos = ""
    productos = ""
    mis_proveedores = []
    nom_provs = []
    firstrun = 0

    def __init__(self, nombre, productos, defectos):
        self.nombre = nombre
        self.defectos = defectos
        self.productos = productos
        self.__class__.mis_proveedores.append(self)

    # metodo auxiliar que necesite para que me funcione un bind
    def removerse(self):
        self.__class__.mis_proveedores.remove(self)

    def elijeprov(self, event1):
        for x in range(0, len(self.mis_proveedores), 1):
            if self.mis_proveedores[x].nombre == self.nombre.get():
                self.productos.config(values=self.mis_proveedores[x].defectos)
                self.defectos.config(values=self.mis_proveedores[x].productos)
                self.productos.current(0)
                self.defectos.current(0)

    def elijeprod(self, *args):
        for x in range(0, len(self.mis_proveedores), 1):
            if self.mis_proveedores[x].nombre == self.nombre.get():
                self.productos.config(values=self.mis_proveedores[x].defectos)
                self.defectos.config(values=self.mis_proveedores[x].productos)

    @classmethod
    def listnomprov(cls):
        for x in range(0, len(cls.mis_proveedores), 1):
            cls.nom_provs.append(cls.mis_proveedores[x].nombre)

    @classmethod
    def first_run(cls):
        if cls.firstrun == 0:
            cls.listnomprov()
            cls.firstrun += 1


# clase Ventana - genera la GUI #######################
#######################################################


class Ventana:
    color1 = "khaki"
    color2 = "lightgoldenrod3"
    color3 = "black"
    color4 = "khaki4"
    color5 = "gold2"

    def __init__(self, window):
        self.root = window
        self.root.resizable(False, False)
        self.root.title("Reclamos a Proveedores")
        self.root.configure(background=self.color1)
        # self.root.iconbitmap("F:\Curso Python\App ABMC\pngwing.ico")
        self.root.iconbitmap("pngwing.ico")

        # Definicion de fuentes ###############################
        #######################################################

        self.b_font = Font(family="Helvetica", size=11, weight="bold")
        self.b_font2 = Font(family="Helvetica", size=19, weight="bold")

        # Definicion de variables #############################
        #######################################################

        self.provval = StringVar()
        self.prodval = StringVar()
        self.defval = StringVar()
        self.cantval = StringVar()
        self.fecval = StringVar()
        self.nrecval = StringVar()
        self.mssgval = StringVar()

        # Definicion de Proveedores ###########################
        #######################################################

        self.cartocor = Proveedor("Cartocor", prod_cajas, def_cajas)
        self.multilabel = Proveedor("Multilabel", prod_etiquetas, def_etiquetas)
        self.guala = Proveedor("Guala", prod_tapas, def_tapas)
        self.cattorini = Proveedor("Cattorini Hnos.", prod_botellas, def_botellas)
        self.islagrande = Proveedor("Isla Grande", prod_film, def_film)

        self.primeracorrida = Proveedor.first_run()

        # label titulo principal ##############################
        #######################################################

        self.m_tprin = Frame(self.root)
        self.m_tprin.config(bg=self.color1)
        self.m_tprin.config(bd=3)
        self.m_tprin.config(pady=5)
        self.m_tprin.config(relief="flat")
        self.m_tprin.grid(row=0, columnspan=20)

        self.t_principal = Label(
            self.m_tprin,
            text="                   REGISTRO DE RECLAMOS A PROVEEDORES                   ",
            bg=self.color2,
            font=self.b_font2,
        )
        self.t_principal.pack()

        # labels de campos ####################################
        #######################################################

        self.l_proveedor = Label(self.root, text="Proveedor", bg=self.color1)
        self.l_proveedor.grid(row=1, column=0, sticky="w", padx=8)
        self.l_producto = Label(self.root, text="Producto", bg=self.color1)
        self.l_producto.grid(row=2, column=0, sticky="w", padx=8)
        self.l_defecto = Label(self.root, text="Defecto", bg=self.color1)
        self.l_defecto.grid(row=3, column=0, sticky="w", padx=8)
        self.l_cantidad = Label(self.root, text="Cantidad", bg=self.color1)
        self.l_cantidad.grid(row=4, column=0, sticky="w", padx=8)
        self.l_fecha = Label(self.root, text="Fecha", bg=self.color1)
        self.l_fecha.grid(row=5, column=0, sticky="w", padx=8)
        self.l_nreclamo = Label(self.root, text="N° de Reclamo", bg=self.color1)
        self.l_nreclamo.grid(row=8, column=0, sticky="w", padx=8)
        self.l_colores = Label(self.root, text="Colores de tema", bg=self.color1)
        self.l_colores.grid(row=12, column=0, sticky="w", padx=8)

        # label de notificaciones #############################
        #######################################################

        self.m_f7 = Frame(self.root)
        self.m_f7.config(bg=self.color2)
        self.m_f7.config(bd=1)
        self.m_f7.config(relief="sunken")
        self.m_f7.grid(
            row=9, rowspan=3, column=4, columnspan=6, pady=6, padx=5, sticky="w"
        )

        self.fila7 = Label(
            self.m_f7, textvariable=self.mssgval, bg=self.color2, font=self.b_font
        )
        self.fila7.pack(fill="both", expand="True", side="bottom")
        self.fila7.config(width=61, height=4)

        # Entries #############################################
        #######################################################

        self.e_proveedor = ttk.Combobox(
            self.root,
            values=Proveedor.nom_provs,
            width=18,
            textvariable=self.provval,
            state="readonly",
        )
        self.e_proveedor.grid(row=1, column=1, padx=10, pady=3)

        self.e_proveedor.current(0)

        self.e_producto = ttk.Combobox(
            self.root,
            values=prod_cajas,
            width=18,
            textvariable=self.prodval,
            state="readonly",
        )
        self.e_producto.grid(row=2, column=1, padx=10, pady=3)

        self.e_producto.current(0)

        self.e_defecto = ttk.Combobox(
            self.root,
            values=def_cajas,
            width=18,
            textvariable=self.defval,
            state="readonly",
        )

        self.e_defecto.current(0)
        self.e_defecto.grid(row=3, column=1, padx=10, pady=3)

        self.e_cantidad = Entry(self.root, textvariable=self.cantval, bg="white")
        self.e_cantidad.grid(row=4, column=1, padx=10, pady=3)

        self.e_fecha = DateEntry(
            self.root,
            selectmode="day",
            bg="white",
            width=18,
            date_pattern="dd/MM/yyyy",
            textvariable=self.fecval,
        )
        self.e_fecha.grid(row=5, column=1, padx=10, pady=3)

        self.e_nreclamo = Entry(self.root, textvariable=self.nrecval, bg="white")
        self.e_nreclamo.grid(row=8, column=1, padx=10, pady=3)

        self.provbind = Proveedor(self.e_proveedor, self.e_defecto, self.e_producto)
        self.provbind.removerse()

        self.e_proveedor.bind("<<ComboboxSelected>>", self.provbind.elijeprov)
        self.prodval.trace_add("write", self.provbind.elijeprod)

        # Stilo del Treeview ##################################
        #######################################################

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure(
            "Treeview",
            background=self.color2,
            foreground=self.color3,
            rowheight=20,
            fieldbackground=self.color2,
        )

        self.style.map("Treeview", background=[("selected", self.color4)])

        # Treeview Frame ######################################
        #######################################################

        self.m_arbol = Frame(self.root)
        self.m_arbol.grid(row=1, rowspan=8, column=4, padx=5, pady=4, sticky="n")

        # Treeview Scrollbar ##################################
        #######################################################

        self.scroll_arbol = Scrollbar(self.m_arbol)
        self.scroll_arbol.pack(side="right", fill="y")

        # Treeview ############################################
        #######################################################

        self.arbol = ttk.Treeview(self.m_arbol, yscrollcommand=self.scroll_arbol.set)
        self.arbol["columns"] = (
            "N°",
            "Fecha",
            "Proveedor",
            "Producto",
            "Defecto",
            "Cantidad",
        )

        self.arbol.column("#0", width=0, stretch="no")
        self.arbol.column("N°", anchor="center", width=40)
        self.arbol.column("Fecha", anchor="w", width=60)
        self.arbol.column("Proveedor", anchor="w", width=120)
        self.arbol.column("Producto", anchor="w", width=120)
        self.arbol.column("Defecto", anchor="w", width=120)
        self.arbol.column("Cantidad", anchor="center", width=80)

        self.arbol.heading("#0", text="")
        self.arbol.heading("N°", text="N°", anchor="center")
        self.arbol.heading("Fecha", text="Fecha", anchor="center")
        self.arbol.heading("Proveedor", text="Proveedor", anchor="w")
        self.arbol.heading("Producto", text="Producto", anchor="w")
        self.arbol.heading("Defecto", text="Defecto", anchor="w")
        self.arbol.heading("Cantidad", text="Cantidad", anchor="center")

        self.arbol.pack()

        self.scroll_arbol.config(command=self.arbol.yview)

        # Instanciación del Modelo ############################
        #######################################################

        self.boton = ABMC(
            self.mssgval,
            self.arbol,
            self.nrecval,
            self.provval,
            self.prodval,
            self.defval,
            self.cantval,
            self.fecval,
        )

        # Binding para Mostrar lo doble clickeado #############
        #######################################################

        self.arbol.bind("<Double-1>", self.boton.MostrarDC)

        # Botones #############################################
        #######################################################

        self.b_guardar = Button(
            self.root,
            text="Guardar",
            borderwidth=4,
            command=lambda: self.boton.Guardar(),
            fg=self.color3,
            bg=self.color5,
            width=13,
            font=self.b_font,
        )
        self.b_guardar.grid(row=6, column=1, pady=5)

        self.b_mostrar = Button(
            self.root,
            text="Mostrar",
            borderwidth=4,
            command=lambda: self.boton.Mostrar(),
            fg=self.color3,
            bg=self.color5,
            width=13,
            font=self.b_font,
        )
        self.b_mostrar.grid(row=9, column=1, pady=4)

        self.b_modificar = Button(
            self.root,
            text="Modificar",
            borderwidth=4,
            command=lambda: self.boton.Modificar(),
            fg=self.color3,
            bg=self.color5,
            width=13,
            font=self.b_font,
        )
        self.b_modificar.grid(row=10, column=1, pady=4)

        self.b_borrar = Button(
            self.root,
            text="Borrar",
            borderwidth=4,
            command=lambda: self.boton.Borrar(),
            fg=self.color3,
            bg=self.color5,
            width=10,
            font=self.b_font,
        )
        self.b_borrar.grid(row=10, column=0, pady=4, padx=5)

        self.b_listar = Button(
            self.root,
            text="Listar",
            borderwidth=4,
            command=lambda: self.boton.Listar(),
            fg=self.color3,
            bg=self.color5,
            width=10,
            font=self.b_font,
        )
        self.b_listar.grid(row=9, column=0, pady=4, padx=5)

        # Radio buttons #######################################
        #######################################################

        self.m_radio = Frame(self.root)
        self.m_radio.config(bg=self.color1)
        self.m_radio.config(bd=1)
        self.m_radio.config(relief="flat")
        self.m_radio.grid(row=12, column=1, columnspan=11, pady=5, padx=5, sticky="n")
        self.r = IntVar(value=0)

        # listas de los widgets por color para que maneje el modelo
        self.color1widgets = [
            self.m_tprin,
            self.l_proveedor,
            self.l_producto,
            self.l_defecto,
            self.l_cantidad,
            self.l_fecha,
            self.l_nreclamo,
            self.m_radio,
            self.l_colores,
        ]
        self.colorbotones = [
            self.b_borrar,
            self.b_guardar,
            self.b_listar,
            self.b_modificar,
            self.b_mostrar,
        ]
        self.radio1 = Radiobutton(self.m_radio)
        self.radio2 = Radiobutton(self.m_radio)
        self.radio3 = Radiobutton(self.m_radio)
        # primero se definen los radio botones para que puedan ser agregados en la lista correspondiente
        self.color2widgets = [
            self.t_principal,
            self.m_f7,
            self.fila7,
            self.radio1,
            self.radio2,
            self.radio3,
        ]
        self.radio1.config(
            text="Rosa",
            variable=self.r,
            value=1,
            bg=self.color2,
            command=lambda: self.boton.cambiarcolor(
                self.r,
                self.root,
                self.color1,
                self.color2,
                self.color3,
                self.color4,
                self.color5,
                self.color1widgets,
                self.color2widgets,
                self.colorbotones,
                self.style,
            ),
        )
        self.radio2.config(
            text="Verde",
            variable=self.r,
            value=2,
            bg=self.color2,
            command=lambda: self.boton.cambiarcolor(
                self.r,
                self.root,
                self.color1,
                self.color2,
                self.color3,
                self.color4,
                self.color5,
                self.color1widgets,
                self.color2widgets,
                self.colorbotones,
                self.style,
            ),
        )
        self.radio3.config(
            text="Estandar",
            variable=self.r,
            value=3,
            bg=self.color2,
            command=lambda: self.boton.cambiarcolor(
                self.r,
                self.root,
                self.color1,
                self.color2,
                self.color3,
                self.color4,
                self.color5,
                self.color1widgets,
                self.color2widgets,
                self.colorbotones,
                self.style,
            ),
        )
        self.radio1.config(width=29)
        self.radio1.pack(fill="both", expand="True", side="left")
        self.radio3.config(width=30)
        self.radio3.pack(fill="both", expand="True", side="right")
        self.radio2.config(width=29)
        self.radio2.pack(fill="both", expand="True", side="right")
