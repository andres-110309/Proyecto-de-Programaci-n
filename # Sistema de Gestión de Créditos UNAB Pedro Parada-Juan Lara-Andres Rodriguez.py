# Sistema de Gestion de Creditos UNAB

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from fpdf import FPDF  # pip install fpdf2

# =========================
# CLASE ESTUDIANTE
# =========================
class Estudiante:
    def __init__(self, nombre, codigo, programa,
                 semestre, creditos_cursados,
                 creditos_totales, promedio,
                 categoria="Academico"):

        self.__nombre            = nombre
        self.__codigo            = codigo
        self.__programa          = programa
        self.__semestre          = semestre
        self.__creditos_cursados = creditos_cursados
        self.__creditos_totales  = creditos_totales
        self.__promedio          = promedio
        self.__categoria         = categoria   

    # --- GETTERS ---
    def get_nombre(self):            return self.__nombre
    def get_codigo(self):            return self.__codigo
    def get_programa(self):          return self.__programa
    def get_semestre(self):          return self.__semestre
    def get_creditos_cursados(self): return self.__creditos_cursados
    def get_creditos_totales(self):  return self.__creditos_totales
    def get_promedio(self):          return self.__promedio
    def get_categoria(self):         return self.__categoria

    # --- SETTERS ---
    def set_nombre(self, v):            self.__nombre = v
    def set_codigo(self, v):            self.__codigo = v
    def set_programa(self, v):          self.__programa = v
    def set_semestre(self, v):          self.__semestre = v
    def set_creditos_cursados(self, v): self.__creditos_cursados = v
    def set_creditos_totales(self, v):  self.__creditos_totales = v
    def set_promedio(self, v):          self.__promedio = v
    def set_categoria(self, v):         self.__categoria = v

    def to_dict(self):
        return {
            "nombre":            self.__nombre,
            "codigo":            self.__codigo,
            "programa":          self.__programa,
            "semestre":          self.__semestre,
            "creditos_cursados": self.__creditos_cursados,
            "creditos_totales":  self.__creditos_totales,
            "promedio":          self.__promedio,
            "categoria":         self.__categoria
        }

# =========================
# ARCHIVOS JSON
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RUTA     = os.path.join(DATA_DIR, "estudiantes.json")
RUTA_HISTORIAL = os.path.join(DATA_DIR, "historial.json")   

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.isfile(RUTA):
    with open(RUTA, "w") as f:
        json.dump({"data": []}, f)

if not os.path.isfile(RUTA_HISTORIAL):
    with open(RUTA_HISTORIAL, "w") as f:
        json.dump({"historial": []}, f)

# =========================
# FUNCIONES JSON
# =========================
def cargar_datos():
    with open(RUTA, "r") as f:
        return json.load(f)

def guardar_datos(data):
    with open(RUTA, "w") as f:
        json.dump(data, f, indent=4)

def cargar_historial():
    with open(RUTA_HISTORIAL, "r") as f:
        return json.load(f)

def guardar_historial(h):
    with open(RUTA_HISTORIAL, "w") as f:
        json.dump(h, f, indent=4)

# =========================
# FUNCION 13  HISTORIAL
# Usamos una PILA (stack): append = push, pop = deshacer
# =========================
def registrar_historial(accion, detalle):
    h = cargar_historial()
    h["historial"].append({
        "accion":  accion,
        "detalle": detalle
    })
    guardar_historial(h)

def ver_historial():
    h = cargar_historial()
    if not h["historial"]:
        messagebox.showinfo("Historial", "No hay cambios registrados aún.")
        return

    # Mostramos los Ultimos 10 como pila
    pila = list(reversed(h["historial"]))[:10]
    texto = "ÚLTIMOS CAMBIOS (más reciente primero):\n\n"
    for i, item in enumerate(pila, 1):
        texto += f"{i}. [{item['accion']}] {item['detalle']}\n"

    messagebox.showinfo("Historial de Cambios", texto)

# =========================
# VALIDACIONES
# =========================
def solo_numeros(char):
    return char.isdigit() or char == ""

# =========================
#   ALERTA DE CREDITOS FALTANTES
# Se ejecuta automaticamente al agregar/editar
# =========================
def verificar_alerta_creditos(cursados, totales, nombre):
    try:
        cursados = int(cursados)
        totales  = int(totales)
        faltantes   = totales - cursados
        porcentaje  = (cursados / totales) * 100

        if porcentaje < 50:
            messagebox.showwarning(
                "⚠️ Alerta de Créditos",
                f"El estudiante {nombre} tiene menos del 50% de créditos completados.\n"
                f"Créditos faltantes: {faltantes} de {totales}"
            )
        elif faltantes <= 10:
            messagebox.showinfo(
                "🎯 Próximo a Graduarse",
                f"{nombre} está muy cerca de completar su carrera.\n"
                f"Solo le faltan {faltantes} créditos!"
            )
    except:
        pass

# =========================
# FUNCIONES CRUD
# =========================
def listar_estudiantes(filtro=""):
    data = cargar_datos()
    lista.delete(0, tk.END)

    for item in data["data"]:
        texto_busqueda = (
            item["nombre"] + item["codigo"] + item["programa"]
        ).lower()

        if filtro.lower() in texto_busqueda:
            texto = f'{item["codigo"]} - {item["nombre"]} - Sem {item["semestre"]}'
            lista.insert(tk.END, texto)


def agregar_estudiante():
    nombre           = entry_nombre.get()
    codigo           = entry_codigo.get()
    programa         = combo_programa.get()
    semestre         = entry_semestre.get()
    creditos_cursados = entry_cursados.get()
    creditos_totales  = entry_totales.get()
    promedio         = entry_promedio.get()
    categoria        = combo_categoria.get()   

    if nombre == "" or codigo == "" or programa == "":
        messagebox.showerror("Error", "Complete todos los campos obligatorios")
        return

    try:
        promedio_num = float(promedio)
        if promedio_num < 0 or promedio_num > 5:
            messagebox.showerror("Error", "El promedio debe estar entre 0 y 5")
            return
    except:
        messagebox.showerror("Error", "Promedio inválido")
        return

    data = cargar_datos()

    for estudiante in data["data"]:
        if estudiante["codigo"] == codigo:
            messagebox.showerror("Error", "Código ya registrado")
            return

    estudiante = Estudiante(
        nombre, codigo, programa, semestre,
        creditos_cursados, creditos_totales, promedio, categoria
    )

    data["data"].append(estudiante.to_dict())
    guardar_datos(data)

    
    #registrar en historial
    registrar_historial("AGREGAR", f"{nombre} (Código: {codigo})")

    #alerta automatica
    verificar_alerta_creditos(creditos_cursados, creditos_totales, nombre)

    limpiar_campos()
    listar_estudiantes()
    messagebox.showinfo("Éxito", "Estudiante registrado correctamente")


def eliminar_estudiante():
    seleccion = lista.curselection()
    if not seleccion:
        messagebox.showwarning("Aviso", "Seleccione un estudiante")
        return

    index    = seleccion[0]
    data     = cargar_datos()
    eliminado = data["data"].pop(index)
    guardar_datos(data)

    #historial
    registrar_historial("ELIMINAR", f"{eliminado['nombre']} (Código: {eliminado['codigo']})")

    listar_estudiantes()
    messagebox.showinfo("Eliminado", f'{eliminado["nombre"]} eliminado correctamente')


def cargar_formulario(event=None):
    seleccion = lista.curselection()
    if not seleccion:
        return

    index = seleccion[0]
    data  = cargar_datos()
    e     = data["data"][index]

    limpiar_campos()
    entry_nombre.insert(0, e["nombre"])
    entry_codigo.insert(0, e["codigo"])
    combo_programa.set(e["programa"])
    entry_semestre.insert(0, e["semestre"])
    entry_cursados.insert(0, e["creditos_cursados"])
    entry_totales.insert(0, e["creditos_totales"])
    entry_promedio.insert(0, e["promedio"])
    combo_categoria.set(e.get("categoria", "Académico"))   # FUNCIÓN 15


def editar_estudiante():
    seleccion = lista.curselection()
    if not seleccion:
        messagebox.showwarning("Aviso", "Seleccione un estudiante")
        return

    index = seleccion[0]
    data  = cargar_datos()

    nuevo = Estudiante(
        entry_nombre.get(),
        entry_codigo.get(),
        combo_programa.get(),
        entry_semestre.get(),
        entry_cursados.get(),
        entry_totales.get(),
        entry_promedio.get(),
        combo_categoria.get()   # FUNCIÓN 15
    )

    data["data"][index] = nuevo.to_dict()
    guardar_datos(data)

    #historial
    registrar_historial("EDITAR", f"{nuevo.get_nombre()} (Código: {nuevo.get_codigo()})")

    #alerta
    verificar_alerta_creditos(nuevo.get_creditos_cursados(), nuevo.get_creditos_totales(), nuevo.get_nombre())

    listar_estudiantes()
    limpiar_campos()
    messagebox.showinfo("Actualizado", "Datos actualizados correctamente")

# =========================
# FUNCIONES EXTRA
# =========================
def ver_detalles(event=None):
    seleccion = lista.curselection()
    if not seleccion:
        return

    index = seleccion[0]
    data  = cargar_datos()
    e     = data["data"][index]

    cursados  = int(e["creditos_cursados"])
    totales   = int(e["creditos_totales"])
    faltantes = totales - cursados
    porcentaje = (cursados / totales) * 100

    mensaje = f"""
Nombre:    {e['nombre']}
Código:    {e['codigo']}
Programa:  {e['programa']}
Semestre:  {e['semestre']}
Categoría: {e.get('categoria', 'Académico')}

Créditos cursados:  {cursados}
Créditos faltantes: {faltantes}
Promedio:           {e['promedio']}

Carrera completada: {porcentaje:.2f}%
"""
    messagebox.showinfo("Información del estudiante", mensaje)


def mostrar_promedio_general():
    data = cargar_datos()
    if len(data["data"]) == 0:
        messagebox.showwarning("Aviso", "No hay estudiantes")
        return

    suma = sum(float(e["promedio"]) for e in data["data"])
    promedio_general = suma / len(data["data"])
    messagebox.showinfo("Promedio General", f"El promedio general es: {promedio_general:.2f}")


def mostrar_mejor_promedio():
    data = cargar_datos()
    if len(data["data"]) == 0:
        messagebox.showwarning("Aviso", "No hay estudiantes")
        return

    mejor = max(data["data"], key=lambda x: float(x["promedio"]))
    messagebox.showinfo("Mejor Promedio", f'Estudiante: {mejor["nombre"]}\nPromedio: {mejor["promedio"]}')


def mostrar_total_estudiantes():
    data  = cargar_datos()
    total = len(data["data"])
    messagebox.showinfo("Total de estudiantes", f"Hay {total} estudiantes registrados")


# =========================
# REPORTE PDF
# =========================
def exportar_pdf():
    data = cargar_datos()

    if not data["data"]:
        messagebox.showwarning("Aviso", "No hay estudiantes para exportar")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "REPORTE DE ESTUDIANTES CGU - UNAB", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "", 11)

    for e in data["data"]:
        cursados   = int(e["creditos_cursados"])
        totales    = int(e["creditos_totales"])
        faltantes  = totales - cursados
        porcentaje = (cursados / totales) * 100 if totales > 0 else 0

        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, f"  {e['nombre']}  (Cod: {e['codigo']})", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 7, f"  Programa: {e['programa']}  |  Semestre: {e['semestre']}  |  Categoria: {e.get('categoria','Academico')}", ln=True)
        pdf.cell(0, 7, f"  Creditos: {cursados}/{totales}  |  Faltantes: {faltantes}  |  Avance: {porcentaje:.1f}%  |  Promedio: {e['promedio']}", ln=True)
        pdf.ln(3)
        pdf.set_draw_color(180, 180, 180)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)

    ruta_pdf = os.path.join(DATA_DIR, "reporte_CGU.pdf")
    pdf.output(ruta_pdf)
    messagebox.showinfo("PDF Generado", f"Reporte PDF guardado en:\n{ruta_pdf}")

    registrar_historial("REPORTE PDF", f"Exportado con {len(data['data'])} estudiantes")


def exportar_txt():
    data = cargar_datos()
    ruta_txt = os.path.join(DATA_DIR, "reporte_estudiantes.txt")

    with open(ruta_txt, "w", encoding="utf-8") as archivo:
        archivo.write("REPORTE DE ESTUDIANTES CGU\n\n")
        for e in data["data"]:
            archivo.write(f"""
Nombre:    {e['nombre']}
Código:    {e['codigo']}
Programa:  {e['programa']}
Promedio:  {e['promedio']}
Categoría: {e.get('categoria','Académico')}
-------------------------
""")
    messagebox.showinfo("Reporte .txt generado", f"Guardado en:\n{ruta_txt}")


# =========================
# SIMULADOR DE PROMEDIO
# =========================
def abrir_simulador():
    sim = tk.Toplevel(ventana)
    sim.title("Simulador de Promedio")
    sim.geometry("380x320")
    sim.config(bg="#1e1e2f")

    tk.Label(sim, text="Simulador de Promedio Futuro",
             font=("Arial", 13, "bold"), bg="#1e1e2f", fg="white").pack(pady=12)

    frame_sim = tk.Frame(sim, bg="#2a2a40")
    frame_sim.pack(pady=5, padx=20)

    def lbl(texto, fila):
        tk.Label(frame_sim, text=texto, bg="#2a2a40", fg="white").grid(row=fila, column=0, padx=8, pady=5, sticky="w")

    lbl("Promedio actual (0-5):", 0)
    e_actual = tk.Entry(frame_sim, width=15)
    e_actual.grid(row=0, column=1, pady=5)

    lbl("Créditos cursados hasta ahora:", 1)
    e_cursados = tk.Entry(frame_sim, width=15)
    e_cursados.grid(row=1, column=1, pady=5)

    lbl("Nota esperada próx. materia:", 2)
    e_nota = tk.Entry(frame_sim, width=15)
    e_nota.grid(row=2, column=1, pady=5)

    lbl("Créditos de esa materia:", 3)
    e_cred_materia = tk.Entry(frame_sim, width=15)
    e_cred_materia.grid(row=3, column=1, pady=5)

    resultado_lbl = tk.Label(sim, text="", bg="#1e1e2f",
                             fg=("#F39C12"), font=("Arial", 12, "bold"))
    resultado_lbl.pack(pady=10)

    def calcular():
        try:
            p_actual     = float(e_actual.get())
            c_cursados   = float(e_cursados.get())
            nota_nueva   = float(e_nota.get())
            cred_materia = float(e_cred_materia.get())

            # Promedio ponderado
            nuevo_promedio = (
                (p_actual * c_cursados) + (nota_nueva * cred_materia)
            ) / (c_cursados + cred_materia)

            color = "#27AE60" if nuevo_promedio >= p_actual else "#E74C3C"
            resultado_lbl.config(
                text=f"Nuevo promedio estimado: {nuevo_promedio:.2f}",
                fg=color
            )
        except:
            resultado_lbl.config(text="Verifica los datos ingresados", fg="#E74C3C")

    tk.Button(sim, text="Calcular", command=calcular,
              bg="#4CAF50", fg="white", width=20).pack(pady=5)


def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_codigo.delete(0, tk.END)
    combo_programa.set("")
    entry_semestre.delete(0, tk.END)
    entry_cursados.delete(0, tk.END)
    entry_totales.delete(0, tk.END)
    entry_promedio.delete(0, tk.END)
    combo_categoria.set("Académico")   # FUNCIÓN 15

# =========================
# LOGIN
# =========================
def verificar_login():
    usuario  = entry_usuario.get()
    password = entry_password.get()

    if usuario == "admin" and password == "1234":
        login.destroy()
        iniciar_sistema()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# =========================
# INTERFAZ PRINCIPAL
# =========================
def iniciar_sistema():
    global ventana, lista
    global entry_nombre, entry_codigo, combo_programa
    global entry_semestre, entry_cursados, entry_totales
    global entry_promedio, entry_buscar, combo_categoria

    ventana = tk.Tk()
    ventana.title("Sistema CGU - Créditos para Grado UNAB")
    ventana.geometry("900x720")
    ventana.config(bg="#1e1e2f")

    tk.Label(ventana, text="Sistema de Gestión de Créditos UNAB",
             font=("Arial", 18, "bold"), bg="#1e1e2f", fg="white").pack(pady=10)

    frame = tk.Frame(ventana, bg="#2a2a40")
    frame.pack(pady=10, padx=10)

    def crear_label(texto, fila):
        tk.Label(frame, text=texto, bg="#2a2a40", fg="white").grid(
            row=fila, column=0, padx=5, pady=4, sticky="w")

    vcmd = (ventana.register(solo_numeros), "%P")

    crear_label("Nombre *", 0)
    entry_nombre = tk.Entry(frame, width=30)
    entry_nombre.grid(row=0, column=1, pady=4)

    crear_label("Código *", 1)
    entry_codigo = tk.Entry(frame, validate="key", validatecommand=vcmd, width=30)
    entry_codigo.grid(row=1, column=1, pady=4)

    crear_label("Programa *", 2)
    combo_programa = ttk.Combobox(frame, width=27, values=[
        "Enfermería","Medicina","Psicología","Química Farmacéutica",
        "Derecho","Artes Audiovisuales","Comunicación Social","Diseño",
        "Gastronomía y Alta Cocina","Licenciatura en Educación Infantil",
        "Literatura","Música","Administración de Empresas","Contaduría Pública",
        "Economía","Finanzas","Marketing","Negocios Internacionales",
        "Seguridad y Salud en el Trabajo","Ingeniería Biomédica",
        "Ingeniería de Sistemas","Ingeniería en Energía y Sostenibilidad",
        "Ingeniería Financiera","Ingeniería Industrial","Ingeniería Mecatrónica",
        "Ciencia de Datos","Licenciatura en Ciencias Sociales",
        "Licenciatura en Lenguas Extranjeras","Desarrollo de Software",
        "Gestión de Negocios","Gestión Gastronómica","Gestión Humana",
        "Investigación Criminal y Ciencias Forenses"
    ])
    combo_programa.grid(row=2, column=1, pady=4)

    crear_label("Semestre", 3)
    entry_semestre = tk.Entry(frame, width=30)
    entry_semestre.grid(row=3, column=1, pady=4)

    crear_label("Créditos cursados", 4)
    entry_cursados = tk.Entry(frame, validate="key", validatecommand=vcmd, width=30)
    entry_cursados.grid(row=4, column=1, pady=4)

    crear_label("Créditos totales", 5)
    entry_totales = tk.Entry(frame, validate="key", validatecommand=vcmd, width=30)
    entry_totales.grid(row=5, column=1, pady=4)

    crear_label("Promedio", 6)
    entry_promedio = tk.Entry(frame, width=30)
    entry_promedio.grid(row=6, column=1, pady=4)

    #Categoria de creditos
    crear_label("Categoría CGU", 7)
    combo_categoria = ttk.Combobox(frame, width=27, values=[
        "Académico", "Cultural", "Deportivo",
        "Social", "Investigación", "Emprendimiento"
    ])
    combo_categoria.set("Académico")
    combo_categoria.grid(row=7, column=1, pady=4)

    # BOTONES FILA 1
    btn_frame = tk.Frame(ventana, bg="#1e1e2f")
    btn_frame.pack(pady=8)

    def boton(texto, comando, fila, col, color="#4CAF50"):
        tk.Button(btn_frame, text=texto, command=comando,
                  bg=color, fg="white", width=17).grid(
                  row=fila, column=col, padx=4, pady=4)

    boton("Agregar",          agregar_estudiante,    0, 0)
    boton("Editar",           editar_estudiante,     0, 1)
    boton("Eliminar",         eliminar_estudiante,   0, 2, "#E74C3C")
    boton("Promedio General", mostrar_promedio_general, 0, 3)

    boton("Mejor Promedio",   mostrar_mejor_promedio,   1, 0)
    boton("Total Estudiantes",mostrar_total_estudiantes, 1, 1)
    boton("Exportar TXT",     exportar_txt,              1, 2)

    # ── BOTONES FILA 2 — funciones nuevas ──
    boton("📄 Exportar PDF",  exportar_pdf,     2, 0, "#1B4F72")  # F11
    boton("📊 Simulador",     abrir_simulador,  2, 1, "#8E44AD")  # F12
    boton("📋 Historial",     ver_historial,    2, 2, "#E67E22")  # F13

    # ── BUSCADOR ──
    tk.Label(ventana, text="Buscar estudiante:",
             bg="#1e1e2f", fg="white").pack()
    entry_buscar = tk.Entry(ventana, width=40)
    entry_buscar.pack(pady=4)

    def actualizar_busqueda(event):
        listar_estudiantes(entry_buscar.get())

    entry_buscar.bind("<KeyRelease>", actualizar_busqueda)

    # ── LISTA ──
    lista = tk.Listbox(ventana, width=95, height=12, bg="white")
    lista.pack(pady=8)
    lista.bind("<<ListboxSelect>>", cargar_formulario)
    lista.bind("<Double-Button-1>", ver_detalles)

    listar_estudiantes()
    ventana.mainloop()

# =========================
# PANTALLA LOGIN
# =========================
login = tk.Tk()
login.title("Login Sistema CGU")
login.geometry("350x260")
login.config(bg="#1e1e2f")

tk.Label(login, text="Ingreso al Sistema",
         font=("Arial", 16, "bold"), bg="#1e1e2f", fg="white").pack(pady=15)

frame_login = tk.Frame(login, bg="#2a2a40")
frame_login.pack(pady=10)

tk.Label(frame_login, text="Usuario",    bg="#2a2a40", fg="white").grid(row=0, column=0, padx=5, pady=5)
entry_usuario = tk.Entry(frame_login)
entry_usuario.grid(row=0, column=1)

tk.Label(frame_login, text="Contraseña", bg="#2a2a40", fg="white").grid(row=1, column=0, padx=5, pady=5)
entry_password = tk.Entry(frame_login, show="*")
entry_password.grid(row=1, column=1)

tk.Button(login, text="Ingresar", command=verificar_login,
          bg="#4CAF50", fg="white", width=20).pack(pady=15)

tk.Label(login, text="Usuario: admin | Contraseña: 1234",
         bg="#1e1e2f", fg="gray").pack()

login.mainloop()