import cv2
import pyautogui
import numpy as np
import json
import mensaje as M
import random as rn

class Detector:
    def __init__(self):
        self.imagen_cv = None
        self.acciones = {}
        self.accion_actual = None

    def capturar_pantalla(self):
        imagen = pyautogui.screenshot()
        self.imagen_cv = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)

    def mostrar_ventana(self):
        cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Imagen', 800, 600)  
        cv2.setMouseCallback('Imagen', self.detectar_click)
        cv2.imshow('Imagen', self.imagen_cv)

    def detectar_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.programa_actual:
                accion = input("Ingrese la acción para este click: ")
                self.programas[self.programa_actual].append({"accion": accion, "x": x, "y": y})
                print(f"Acción '{accion}' guardada para el click en ({x}, {y})")

    def crear_accion(self):
        nombre_accion = input("Ingrese el nombre de la accion: ")
        self.acciones[nombre_accion] = []
        self.accion_actual = nombre_accion
        print(f"Accion '{nombre_accion}' creado")

    def ejecutar_accion(self):
        nombre_accion = input("Ingrese el nombre de la accion a ejecutar: ")
        if nombre_accion in self.acciones:
            for accion in self.acciones[nombre_accion]:
                pyautogui.moveTo(accion["x"], accion["y"])
                pyautogui.click()
                lista_p = ["p1.txt"]
                for p in lista_p:
                     
                     with open(p, 'r', encoding='iso-8859-1') as p_file:
                        p_texto = p_file.read()
                        with open("transcripciones.json", 'r', encoding='iso-8859-1') as transcripciones_file:
                                mensaje = M.Mensaje()
                                mensaje.enviar_mensaje(p_texto)
                                mensaje.leer_respuesta()
                                transcripciones = json.load(transcripciones_file)
                                print(f"Ejecutando click '{accion['accion']}' en ({accion['x']}, {accion['y']})")
                                if accion['accion'] == 'chat':
                                    for id_transcripcion in transcripciones["entries"]:
                                        msg = id_transcripcion+": "+transcripciones["entries"][id_transcripcion].strip()
                                        mensaje.enviar_mensaje(msg)
                                        
                                        mensaje.leer_respuesta()
                        
                    
        else:
            print("Accion no encontrada")

    def guardar_acciones(self):
        with open('acciones.json', 'w') as f:
            json.dump(self.acciones, f)

    def cargar_acciones(self):
        try:
            with open('acciones.json', 'r') as f:
                self.acciones = json.load(f)
        except FileNotFoundError:
            pass

    def run(self):
        self.cargar_acciones()
        while True:
            print("1. Crear acciones")
            print("2. Ejecutar acciones")
            print("3. Guardar acciones")
            print("4. Salir")
            opcion = input("Ingrese la opción: ")
            if opcion == "1":
                self.crear_accion()
                self.capturar_pantalla()
                self.mostrar_ventana()
                while True:
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                cv2.destroyAllWindows()
            elif opcion == "2":
                self.ejecutar_accion()
            elif opcion == "3":
                self.guardar_accioness()
            elif opcion == "4":
                break
            else:
                print("Opción inválida")

if __name__ == "__main__":
    detector = Detector()
    detector.run()
