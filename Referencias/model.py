import shelve
from tkinter import messagebox
import re

# Funciones ###########################


class ABMC:
    mssgval = ""
    arbol = ""
    nrecval = ""
    provval = ""
    prodval = ""
    defval = ""
    cantval = ""
    fecval = ""

    def __init__(
        self, mssgval, arbol, nrecval, provval, prodval, defval, cantval, fecval
    ):
        self.mssgval = mssgval
        self.arbol = arbol
        self.nrecval = nrecval
        self.provval = provval
        self.prodval = prodval
        self.defval = defval
        self.cantval = cantval
        self.fecval = fecval

    def Limpiar(self):
        self.provval.set("")
        self.prodval.set("")
        self.defval.set("")
        self.cantval.set("")
        self.fecval.set("")
        self.nrecval.set("")

    def Guardar(self):
        self.mssgval.set("")
        if (
            self.provval.get() == ""
            or self.prodval.get() == ""
            or self.defval.get() == ""
            or self.cantval.get() == ""
            or self.fecval.get() == ""
        ):
            self.mssgval.set("Completa todos los campos arriba de Guardar")
        elif not re.match("^[0-9]+$", self.cantval.get()):
            self.mssgval.set("Cantidad deben ser números.")
            self.cantval.set("")
        else:
            db = shelve.open("reclamos")
            nreclamo = db.get("nreclamo")
            if nreclamo == None:
                nreclamo = 1
            else:
                nreclamo += 1
            db["nreclamo"] = nreclamo
            reclamo = {}
            reclamo["reclamo n°"] = nreclamo
            reclamo["fecha"] = self.fecval.get()
            reclamo["proveedor"] = self.provval.get()
            reclamo["producto"] = self.prodval.get()
            reclamo["defecto"] = self.defval.get()
            reclamo["cantidad"] = self.cantval.get()
            db[str(nreclamo)] = reclamo
            self.Limpiar()
            self.mssgval.set("Se generó el reclamo N°: " + str(nreclamo))
            self.arbol.delete(*self.arbol.get_children())
            self.arbol.insert(
                parent="",
                index="end",
                iid=0,
                text="",
                values=list(db[str(nreclamo)].values()),
            )
            db.close

    def Borrar(self):
        try:
            if self.nrecval.get() == "":
                self.Limpiar()
                self.mssgval.set("Todo limpio, ingrese N° de reclamo a borrar")
                self.arbol.delete(*self.arbol.get_children())
            elif not re.match("^[0-9]+$", self.nrecval.get()):
                self.mssgval.set("Falta algun número en N° de reclamo")
                self.nrecval.set("")
            else:
                db = shelve.open("reclamos")
                confirmacion = messagebox.askquestion(
                    "Confirmación de borrado",
                    "Estas seguro de borrar el reclamo N°" + self.nrecval.get(),
                )
                if confirmacion == "yes":
                    del db[self.nrecval.get()]
                    self.mssgval.set(
                        "Se ha borrado el reclamo N° " + self.nrecval.get()
                    )
                    self.nrecval.set("")
                    db.close
                else:
                    self.mssgval.set(
                        "Se ha cancelado borrar el reclamo N° " + self.nrecval.get()
                    )
                    self.nrecval.set("")
                    db.close
        except KeyError:
            self.mssgval.set("N° de reclamo no existente")
            self.nrecval.set("")

    def Modificar(self):
        self.mssgval.set("")
        try:
            db = shelve.open("reclamos")
            if not re.match("^[0-9]+$", self.nrecval.get()):
                self.mssgval.set(
                    "Ingresa N° de reclamo y al menos un campo a modificar."
                )
                self.nrecval.set("")
                db.close

            elif db.get(self.nrecval.get(), 0) == 0:
                self.mssgval.set("N° de reclamo no hayado")
                self.nrecval.set("")
                db.close
            elif (
                self.provval.get() == ""
                and self.prodval.get() == ""
                and self.defval.get() == ""
                and self.cantval.get() == ""
                and self.fecval.get() == ""
            ):
                self.mssgval.set("Completar al menos un campo arriba de Guardar")
                self.nrecval.set("")
                db.close
            elif self.cantval.get() != "" and not re.match(
                "^[0-9]+$", self.cantval.get()
            ):
                self.mssgval.set("Cantidad deben ser números.")
                self.cantval.set("")
            else:
                reclamo = {}
                reclamo["reclamo n°"] = self.nrecval.get()
                if self.fecval.get() != "":
                    reclamo["fecha"] = self.fecval.get()
                else:
                    reclamo["fecha"] = db[self.nrecval.get()]["fecha"]
                if self.provval.get() != "":
                    reclamo["proveedor"] = self.provval.get()
                else:
                    reclamo["proveedor"] = db[self.nrecval.get()]["proveedor"]
                if self.prodval.get() != "":
                    reclamo["producto"] = self.prodval.get()
                else:
                    reclamo["producto"] = db[self.nrecval.get()]["producto"]
                if self.defval.get() != "":
                    reclamo["defecto"] = self.defval.get()
                else:
                    reclamo["defecto"] = db[self.nrecval.get()]["defecto"]
                if self.cantval.get() != "":
                    reclamo["cantidad"] = self.cantval.get()
                else:
                    reclamo["cantidad"] = db[self.nrecval.get()]["cantidad"]
                db[self.nrecval.get()] = reclamo
                self.mssgval.set("Se modificó el reclamo N°: " + self.nrecval.get())
                self.arbol.delete(*self.arbol.get_children())
                self.arbol.insert(
                    parent="",
                    index="end",
                    iid=0,
                    text="",
                    values=list(db[self.nrecval.get()].values()),
                )
                self.Limpiar()
                db.close
        except KeyError:
            self.mssgval.set("N° de reclamo no existente")
            self.Limpiar()
            db.close

    def Listar(self):
        self.mssgval.set("")
        self.Limpiar()
        self.mssgval.set("Listando reclamos registrados")
        db = shelve.open("reclamos")
        self.arbol.delete(
            *self.arbol.get_children()
        )  # lo que entiendo del splat * aca es que hace unpack de un item sin saber cuantos valores tiene, si lo saco no funciona
        filas = db.get("nreclamo")
        reclist = []
        if filas == None:
            self.mssgval.set("Faltan cargar datos")
            return filas
        for x in list(range(filas, 0, -1)):
            try:
                if db.get(str(x), 0) == 0:
                    continue
                else:
                    reclist.append(x)
            except:
                continue
        else:
            contar = 0
            for i in reclist:
                try:
                    self.arbol.insert(
                        parent="",
                        index="end",
                        iid=contar,
                        text="",
                        values=list(db[str(i)].values()),
                    )
                    contar += 1
                except:
                    continue
        db.close

    def Mostrar(self):
        self.mssgval.set("")
        try:
            if not re.match("^[0-9]+$", self.nrecval.get()):
                self.mssgval.set(
                    "Ingresa N° de reclamo a mostrar (solo números), o doble click en elemento"
                )
                self.nrecval.set("")
            else:
                self.arbol.delete(*self.arbol.get_children())
                db = shelve.open("reclamos")
                try:
                    self.arbol.insert(
                        parent="",
                        index="end",
                        iid=0,
                        text="",
                        values=list(db[self.nrecval.get()].values()),
                    )
                    self.nrecval.set(db[self.nrecval.get()]["reclamo n°"])
                    self.fecval.set(db[self.nrecval.get()]["fecha"])
                    self.provval.set(db[self.nrecval.get()]["proveedor"])
                    self.prodval.set(db[self.nrecval.get()]["producto"])
                    self.defval.set(db[self.nrecval.get()]["defecto"])
                    self.cantval.set(db[self.nrecval.get()]["cantidad"])
                    self.mssgval.set(
                        "Se ha seleccionado el reclamo N° " + self.nrecval.get()
                    )
                except:
                    self.mssgval.set("N° de reclamo no encontrado")
                finally:
                    db.close
        except KeyError:
            self.mssgval.set("N° de reclamo no existe")
            self.nrecval.set("")
            db.close

    def MostrarDC(self, e):
        self.selectfocus = self.arbol.focus()
        self.nrecval.set(str(self.arbol.item(self.selectfocus)["values"][0]))
        self.arbol.delete(*self.arbol.get_children())
        db = shelve.open("reclamos")
        try:
            self.arbol.insert(
                parent="",
                index="end",
                iid=0,
                text="",
                values=list(db[self.nrecval.get()].values()),
            )
            self.nrecval.set(db[self.nrecval.get()]["reclamo n°"])
            self.fecval.set(db[self.nrecval.get()]["fecha"])
            self.provval.set(db[self.nrecval.get()]["proveedor"])
            self.prodval.set(db[self.nrecval.get()]["producto"])
            self.defval.set(db[self.nrecval.get()]["defecto"])
            self.cantval.set(db[self.nrecval.get()]["cantidad"])
            self.mssgval.set("Se ha seleccionado el reclamo N° " + self.nrecval.get())
        except KeyError:
            self.mssgval.set("N° de reclamo no encontrado")
        finally:
            db.close

    def cambiarcolor(
        self,
        r,
        root,
        color1,
        color2,
        color3,
        color4,
        color5,
        listacolor1,
        listacolor2,
        listabotones,
        estilo,
    ):
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.color4 = color4
        self.color5 = color5
        self.r = r
        self.listacolor1 = listacolor1
        self.listacolor2 = listacolor2
        self.listabotones = listabotones
        self.root = root
        self.estilo = estilo
        # Tema segun valor del radio button
        if self.r.get() == 1:
            self.color1 = "#FF88DC"
            self.color2 = "#C297B8"
            self.color3 = "black"
            self.color4 = "#FF5154"
            self.color5 = "#FFFFFF"
        elif self.r.get() == 2:
            self.color1 = "#A1C349"
            self.color2 = "#87A330"
            self.color3 = "black"
            self.color4 = "#2A3C24"
            self.color5 = "#CAD593"
        elif self.r.get() == 3:
            self.color1 = "khaki"
            self.color2 = "lightgoldenrod3"
            self.color3 = "black"
            self.color4 = "khaki4"
            self.color5 = "gold2"

        # Modificación de colores segun grupos de widgets
        for self.wid in self.listacolor1:
            self.wid.configure(bg=self.color1)
        for self.wid in self.listacolor2:
            self.wid.configure(bg=self.color2)
        for self.wid in self.listabotones:
            self.wid.configure(bg=self.color5, fg=self.color3)
        self.root.configure(background=self.color1)
        self.estilo.configure(
            "Treeview",
            background=self.color2,
            foreground=self.color3,
            fieldbackground=self.color2,
        )
        self.estilo.map("Treeview", background=[("selected", self.color4)])
