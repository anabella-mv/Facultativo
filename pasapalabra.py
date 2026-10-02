import tkinter as tk
from tkinter import messagebox, ttk
import math
import unicodedata

# PREGUNTAS DEL ROSCO
ROSCO = [
    {"letra": "A", "tipo": "Empieza con", "pista": "Medida de la superficie que ocupa una figura geométrica.", "respuesta": "area"},
    {"letra": "B", "tipo": "Empieza con", "pista": "Semirrecta que divide a un ángulo exactamente en dos partes iguales.", "respuesta": "bisectriz"},
    {"letra": "C", "tipo": "Empieza con", "pista": "Línea curva cerrada y plana cuyos puntos equidistan del centro.", "respuesta": "circunferencia"},
    {"letra": "D", "tipo": "Empieza con", "pista": "Segmento que une dos puntos de la circunferencia pasando por el centro.", "respuesta": "diametro"},
    {"letra": "E", "tipo": "Empieza con", "pista": "Igualdad algebraica que se verifica para determinados valores de las incógnitas.", "respuesta": "ecuacion"},
    {"letra": "F", "tipo": "Empieza con", "pista": "Relación entre dos conjuntos donde a cada elemento del dominio le corresponde una única imagen.", "respuesta": "funcion"},
    {"letra": "G", "tipo": "Empieza con", "pista": "Unidad de medida angular del sistema sexagesimal (°).", "respuesta": "grado"},
    {"letra": "H", "tipo": "Empieza con", "pista": "Lado de mayor longitud en un triángulo rectángulo, opuesto al ángulo recto.", "respuesta": "hipotenusa"},
    {"letra": "I", "tipo": "Empieza con", "pista": "Desigualdad entre dos expresiones algebraicas (usa <, >, <= o >=).", "respuesta": "inecuacion"},
    {"letra": "J", "tipo": "Contiene la", "pista": "Línea recta de referencia que se utiliza para medir distancias, ubicar puntos o definir la simetría de una figura", "respuesta": "eje"},
    {"letra": "L", "tipo": "Empieza con", "pista": "Operación inversa a la exponenciación; exponente al que hay que elevar una base.", "respuesta": "logaritmo"},
    {"letra": "M", "tipo": "Empieza con", "pista": "Valor con mayor frecuencia absoluta dentro de un conjunto de datos estadísticos.", "respuesta": "moda"},
    {"letra": "N", "tipo": "Empieza con", "pista": "Término superior de una fracción que indica cuántas partes se toman de la unidad.", "respuesta": "numerador"},
    {"letra": "O", "tipo": "Empieza con", "pista": "Punto de intersección de los ejes cartesianos (0, 0).", "respuesta": "origen"},
    {"letra": "P", "tipo": "Empieza con", "pista": "Curva abierta simétrica obtenida al graficar una función cuadrática.", "respuesta": "parabola"},
    {"letra": "R", "tipo": "Empieza con", "pista": "Segmento que une el centro con cualquier punto de una circunferencia.", "respuesta": "radio"},
    {"letra": "S", "tipo": "Empieza con", "pista": "Conjunto de dos o más ecuaciones cuyas soluciones comunes se buscan.", "respuesta": "sistema"},
    {"letra": "T", "tipo": "Empieza con", "pista": "Proposición cuya veracidad se demuestra mediante axiomas y deducción (ej. Pitágoras).", "respuesta": "teorema"},
    {"letra": "U", "tipo": "Empieza con", "pista": "Operación entre conjuntos que reúne todos los elementos sin duplicarlos.", "respuesta": "union"},
    {"letra": "V", "tipo": "Empieza con", "pista": "Punto extremo de una parábola o punto de intersección de lados de un polígono.", "respuesta": "vertice"},
    {"letra": "X", "tipo": "Contiene la", "pista": "Valor máximo o punto más alto alcanzado por una función en su dominio.", "respuesta": "maximo"},
    {"letra": "Z", "tipo": "Contiene la", "pista": "Cuadrilátero que no tiene ningún lado paralelo a otro", "respuesta": "trapezoide"}
]

# Colores
COLOR_PENDIENTE = "#2b6cb0"  # Azul
COLOR_ACTUAL = "#ecc94b"     # Amarillo
COLOR_ACIERTO = "#38a169"    # Verde
COLOR_ERROR = "#e53e3e"      # Rojo
COLOR_FONDO = "#1a202c"      # Gris azulado oscuro

def normalizar(texto):
    texto = texto.strip().lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

class PasapalabraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pasapalabra Matemático - Secundaria")
        self.root.geometry("920x780")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)

        # Estado del juego
        self.tiempo_restante = 360
        self.timer_id = None
        self.aciertos = 0
        self.errores = 0
        self.estados = ["pendiente"] * len(ROSCO)
        self.respuestas_usuario = [""] * len(ROSCO)  # Guardar lo que escribió el usuario
        self.pendientes = list(range(len(ROSCO)))
        self.indice_turno = 0

        self._crear_interfaz()
        self._dibujar_rosco()
        self._mostrar_pregunta_actual()
        self._iniciar_temporizador()

    def _crear_interfaz(self):
        panel_top = tk.Frame(self.root, bg=COLOR_FONDO)
        panel_top.pack(fill="x", padx=20, pady=10)

        self.lbl_aciertos = tk.Label(panel_top, text="Aciertos: 0", font=("Arial", 14, "bold"), fg="#48bb78", bg=COLOR_FONDO)
        self.lbl_aciertos.pack(side="left")

        self.lbl_errores = tk.Label(panel_top, text="Errores: 0", font=("Arial", 14, "bold"), fg="#f56565", bg=COLOR_FONDO)
        self.lbl_errores.pack(side="left", padx=20)

        self.lbl_tiempo = tk.Label(panel_top, text=f"Tiempo: {self.tiempo_restante}s", font=("Arial", 16, "bold"), fg="#ecc94b", bg=COLOR_FONDO)
        self.lbl_tiempo.pack(side="right")

        self.canvas = tk.Canvas(self.root, width=420, height=420, bg=COLOR_FONDO, highlightthickness=0)
        self.canvas.pack(pady=5)

        self.lbl_tipo = tk.Label(self.root, text="", font=("Arial", 12, "italic"), fg="#a0aec0", bg=COLOR_FONDO)
        self.lbl_tipo.pack()

        self.lbl_pista = tk.Label(self.root, text="", font=("Arial", 11), fg="white", bg=COLOR_FONDO, wraplength=700, justify="center", height=3)
        self.lbl_pista.pack(pady=5)

        panel_input = tk.Frame(self.root, bg=COLOR_FONDO)
        panel_input.pack(pady=5)

        self.entry_resp = tk.Entry(panel_input, font=("Arial", 13), width=24, justify="center")
        self.entry_resp.grid(row=0, column=0, padx=5)
        self.entry_resp.bind("<Return>", lambda e: self.verificar_respuesta())
        self.entry_resp.focus_set()

        btn_enviar = tk.Button(panel_input, text="Responder", font=("Arial", 11, "bold"), bg="#3182ce", fg="white", padx=10, command=self.verificar_respuesta)
        btn_enviar.grid(row=0, column=1, padx=5)

        btn_pasar = tk.Button(panel_input, text="Pasapalabra", font=("Arial", 11, "bold"), bg="#d69e2e", fg="white", padx=10, command=self.pasapalabra)
        btn_pasar.grid(row=0, column=2, padx=5)

    def _dibujar_rosco(self):
        self.canvas.delete("all")
        cx, cy, r = 210, 210, 165
        total = len(ROSCO)

        for i, item in enumerate(ROSCO):
            angulo = math.radians((i / total) * 360 - 90)
            x = cx + r * math.cos(angulo)
            y = cy + r * math.sin(angulo)

            estado = self.estados[i]
            if len(self.pendientes) > 0 and i == self.pendientes[self.indice_turno]:
                color = COLOR_ACTUAL
            elif estado == "acierto":
                color = COLOR_ACIERTO
            elif estado == "error":
                color = COLOR_ERROR
            else:
                color = COLOR_PENDIENTE

            radio_nodo = 16
            self.canvas.create_oval(
                x - radio_nodo, y - radio_nodo,
                x + radio_nodo, y + radio_nodo,
                fill=color, outline="white", width=1.5
            )
            self.canvas.create_text(
                x, y, text=item["letra"], fill="black" if color == COLOR_ACTUAL else "white",
                font=("Arial", 11, "bold")
            )

    def _iniciar_temporizador(self):
        if self.tiempo_restante > 0 and len(self.pendientes) > 0:
            self.tiempo_restante -= 1
            self.lbl_tiempo.config(text=f"Tiempo: {self.tiempo_restante}s")
            self.timer_id = self.root.after(1000, self._iniciar_temporizador)
        elif self.tiempo_restante <= 0:
            self._finalizar_juego("¡Se acabó el tiempo!")

    def _mostrar_pregunta_actual(self):
        if not self.pendientes:
            self._finalizar_juego("¡Has completado el rosco!")
            return

        idx_actual = self.pendientes[self.indice_turno]
        item = ROSCO[idx_actual]

        self.lbl_tipo.config(text=f"{item['tipo']} la letra '{item['letra']}'")
        self.lbl_pista.config(text=item["pista"])
        self.entry_resp.delete(0, tk.END)
        self._dibujar_rosco()

    def verificar_respuesta(self):
        if not self.pendientes:
            return

        idx_actual = self.pendientes[self.indice_turno]
        texto_ingresado = self.entry_resp.get()
        respuesta_usuario = normalizar(texto_ingresado)
        respuesta_correcta = ROSCO[idx_actual]["respuesta"]

        if not respuesta_usuario:
            return

        if respuesta_usuario in ["pasapalabra", "p"]:
            self.pasapalabra()
            return

        self.respuestas_usuario[idx_actual] = texto_ingresado.strip()

        if respuesta_usuario == respuesta_correcta:
            self.estados[idx_actual] = "acierto"
            self.aciertos += 1
            self.lbl_aciertos.config(text=f"Aciertos: {self.aciertos}")
        else:
            self.estados[idx_actual] = "error"
            self.errores += 1
            self.lbl_errores.config(text=f"Errores: {self.errores}")

        self.pendientes.pop(self.indice_turno)
        if self.pendientes:
            self.indice_turno %= len(self.pendientes)
        self._mostrar_pregunta_actual()

    def pasapalabra(self):
        if not self.pendientes:
            return
        self.indice_turno = (self.indice_turno + 1) % len(self.pendientes)
        self._mostrar_pregunta_actual()

    def _mostrar_ventana_revision(self):
        """Abre una ventana con el detalle de errores y letras sin responder."""
        ventana_rev = tk.Toplevel(self.root)
        ventana_rev.title("Revisión de Respuestas")
        ventana_rev.geometry("750x550")
        ventana_rev.configure(bg="#2d3748")

        lbl_titulo = tk.Label(
            ventana_rev, 
            text="Detalle de Respuestas Incorrectas y No Respondidas", 
            font=("Arial", 14, "bold"), 
            fg="white", 
            bg="#2d3748"
        )
        lbl_titulo.pack(pady=12)

        # Contenedor con Scrollbar
        frame_scroll = tk.Frame(ventana_rev, bg="#2d3748")
        frame_scroll.pack(fill="both", expand=True, padx=15, pady=5)

        canvas_rev = tk.Canvas(frame_scroll, bg="#1a202c", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas_rev.yview)
        scrollable_frame = tk.Frame(canvas_rev, bg="#1a202c")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_rev.configure(scrollregion=canvas_rev.bbox("all"))
        )
        canvas_rev.create_window((0, 0), window=scrollable_frame, anchor="nw", width=700)
        canvas_rev.configure(yscrollcommand=scrollbar.set)

        canvas_rev.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Generar lista de revisión
        hay_pendientes_o_errores = False
        for i, item in enumerate(ROSCO):
            estado = self.estados[i]
            if estado in ["error", "pendiente"]:
                hay_pendientes_o_errores = True
                color_tarjeta = "#742a2a" if estado == "error" else "#2c5282"
                tipo_texto = "❌ ERROR" if estado == "error" else "⏳ SIN RESPONDER"

                card = tk.Frame(scrollable_frame, bg=color_tarjeta, bd=1, relief="solid")
                card.pack(fill="x", padx=10, pady=6, ipadx=5, ipady=5)

                lbl_letra = tk.Label(
                    card, 
                    text=f"[{item['letra']}] {tipo_texto} ({item['tipo']} {item['letra']})", 
                    font=("Arial", 11, "bold"), 
                    fg="#fbd38d", 
                    bg=color_tarjeta, 
                    anchor="w"
                )
                lbl_letra.pack(fill="x", padx=5, pady=2)

                lbl_pista = tk.Label(
                    card, 
                    text=f"Definición: {item['pista']}", 
                    font=("Arial", 10), 
                    fg="white", 
                    bg=color_tarjeta, 
                    wraplength=660, 
                    justify="left", 
                    anchor="w"
                )
                lbl_pista.pack(fill="x", padx=5, pady=1)

                if estado == "error":
                    lbl_ingresada = tk.Label(
                        card, 
                        text=f"Tu respuesta: \"{self.respuestas_usuario[i]}\"", 
                        font=("Arial", 10, "italic"), 
                        fg="#fed7d7", 
                        bg=color_tarjeta, 
                        anchor="w"
                    )
                    lbl_ingresada.pack(fill="x", padx=5, pady=1)

                lbl_correcta = tk.Label(
                    card, 
                    text=f"Respuesta correcta: {item['respuesta'].upper()}", 
                    font=("Arial", 10, "bold"), 
                    fg="#9ae6b4", 
                    bg=color_tarjeta, 
                    anchor="w"
                )
                lbl_correcta.pack(fill="x", padx=5, pady=2)

        if not hay_pendientes_o_errores:
            lbl_felicidades = tk.Label(
                scrollable_frame, 
                text="¡Felicitaciones! ¡Acertaste todas las letras del rosco! 🏆", 
                font=("Arial", 13, "bold"), 
                fg="#68d391", 
                bg="#1a202c"
            )
            lbl_felicidades.pack(pady=40)

        btn_cerrar = tk.Button(
            ventana_rev, 
            text="Cerrar Revisión", 
            font=("Arial", 11, "bold"), 
            bg="#4a5568", 
            fg="white", 
            command=ventana_rev.destroy
        )
        btn_cerrar.pack(pady=10)

    def _finalizar_juego(self, motivo):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.entry_resp.config(state="disabled")
        self._dibujar_rosco()
        
        mensaje = (
            f"{motivo}\n\n"
            f"Resultados Finales:\n"
            f"• Aciertos: {self.aciertos}\n"
            f"• Errores: {self.errores}\n"
            f"• No respondidas: {len(self.pendientes)}\n"
            f"• Porcentaje: {(self.aciertos / len(ROSCO)) * 100:.1f}%\n\n"
            f"Haz clic en Aceptar para ver la revisión de respuestas."
        )
        messagebox.showinfo("Fin de la Partida", mensaje)
        self._mostrar_ventana_revision()

if __name__ == "__main__":
    ventana = tk.Tk()
    app = PasapalabraGUI(ventana)
    ventana.mainloop()