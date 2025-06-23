import pyautogui # type: ignore
import time
import random
import pyperclip # type: ignore
import boton_detector as bd
import cv2 # type: ignore

class Mensaje:
    def __init__(self):
        self.mensajes = []

    def copiar_mensaje(self, mensaje):
        #pyautogui.hotkey('ctrl', 'c')
        msg = mensaje.encode('latin1').decode('utf-8')
        self.mensajes.append(msg)
        pyperclip.copy(msg)
        time.sleep(random.uniform(0.2, 0.7))
        pyautogui.hotkey('ctrl', 'v')

    def enviar_mensaje(self, mensaje):
        time.sleep(random.uniform(0.5, 1.0)) 
        #pyautogui.typewrite(mensaje)
        self.copiar_mensaje(mensaje)
        time.sleep(random.uniform(0.5, 0.9))
        pyperclip.paste()
        pyautogui.press('enter')
        print(f"Mensaje enviado: '{mensaje}'")
        return True

    def leer_respuesta(self, espera=2):
        print(f"Esperando respuesta durante {espera} segundos...")
        time.sleep(espera)
        try:
            detector = bd.BotonDetector('play_button.png', 'pause_button.png', 'stop_button.png')
            salir = False
            while not salir:
                detectado = detector.detectar_botones()
                salir = not detectado
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            screenshot = pyautogui.screenshot()
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f'respuesta_{timestamp}.png'
            screenshot.save(filename)
            print(f"Captura de respuesta guardada en: {filename}")
            return filename 
        except Exception as e:
            print(f"Error al capturar la respuesta: {e}")
            return None
