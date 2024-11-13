import pygame
import tkinter as tk
from tkinter import ttk, colorchooser

#-----------------------------------------------------------------------------
class degradadoColores:
    def __init__(self):
        self.ancho_pantalla = 600
        self.alto_pantalla = 400
        self.color_inicial = (255, 0, 0)  # Rojo
        self.color_final = (0, 0, 255)    # Azul
#-----------------------------------------------------------------------------
        # Crear ventana de controles
        self.ventana = tk.Tk()
        self.ventana.title("control de degradado")
        self.ventana.geometry("300x150")
#-----------------------------------------------------------------------------
        # Crear marco de controles
        self.marco = ttk.Frame(self.ventana, padding="10")
        self.marco.grid(row=0, column=0, padx=10, pady=5) #grid (para saber donde esta colocado, en parte de la tabla)
#-----------------------------------------------------------------------------
        # Crear botones de selección de color
        ttk.Button(self.marco, text="color inicial", command=self.seleccionar_color_inicial).grid(row=0, column=0, pady=5, padx=5)
        ttk.Button(self.marco, text="color final", command=self.seleccionar_color_final).grid(row=1, column=0, pady=5, padx=5)
        ttk.Button(self.marco, text="aplicar", command=self.generar_degradado).grid(row=2, column=0, pady=10, padx=5)
#-----------------------------------------------------------------------------
        # Configuración de Pygame
        pygame.init()
        self.pantalla = pygame.display.set_mode((self.ancho_pantalla, self.alto_pantalla))
        pygame.display.set_caption("degradado de colores")
#-----------------------------------------------------------------------------
    def calcular_coeficientes(self, puntos_x, puntos_y):
        coeficientes = [y for y in puntos_y]
        for j in range(1, len(puntos_y)):
            for i in range(len(puntos_y) - 1, j - 1, -1):
                coeficientes[i] = (coeficientes[i] - coeficientes[i - 1]) / (puntos_x[i] - puntos_x[i - j])
        return coeficientes
#-----------------------------------------------------------------------------
    def evaluar_interpolacion(self, puntos_x, coeficientes, valor_x):
        resultado = coeficientes[-1]
        for i in range(len(coeficientes) - 2, -1, -1):
            resultado = resultado * (valor_x - puntos_x[i]) + coeficientes[i]
        return resultado
#-----------------------------------------------------------------------------
    def mezclar_colores(self, color1, color2, porcentaje):
        puntos_x = [0, 1]
        r = [color1[0], color2[0]]
        g = [color1[1], color2[1]]
        b = [color1[2], color2[2]]

        coef_r = self.calcular_coeficientes(puntos_x, r)
        coef_g = self.calcular_coeficientes(puntos_x, g)
        coef_b = self.calcular_coeficientes(puntos_x, b)
#-----------------------------------------------------------------------------
        rojo = int(max(0, min(255, self.evaluar_interpolacion(puntos_x, coef_r, porcentaje))))
        verde = int(max(0, min(255, self.evaluar_interpolacion(puntos_x, coef_g, porcentaje))))
        azul = int(max(0, min(255, self.evaluar_interpolacion(puntos_x, coef_b, porcentaje))))
#-----------------------------------------------------------------------------
        return (rojo, verde, azul)
#-----------------------------------------------------------------------------
    def seleccionar_color_inicial(self):
        color = colorchooser.askcolor(title="selecciona el color inicial", color=self.color_inicial)
        if color[0]:
            self.color_inicial = tuple(map(int, color[0]))
#-----------------------------------------------------------------------------
    def seleccionar_color_final(self):
        color = colorchooser.askcolor(title="selecciona el color final", color=self.color_final)
        if color[0]:
            self.color_final = tuple(map(int, color[0]))
#-----------------------------------------------------------------------------
    def generar_degradado(self):
        for x in range(self.ancho_pantalla):
            porcentaje = x / (self.ancho_pantalla - 1)
            color_interpolado = self.mezclar_colores(self.color_inicial, self.color_final, porcentaje)
            pygame.draw.line(self.pantalla, color_interpolado, (x, 0), (x, self.alto_pantalla))
        pygame.display.flip()
#-----------------------------------------------------------------------------
    def iniciar(self):
        self.generar_degradado()
        self.ventana.mainloop()
#-----------------------------------------------------------------------------
# Crear y ejecutar la aplicación
app = degradadoColores()
app.iniciar()
#-----------------------------------------------------------------------------