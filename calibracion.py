from pynput.mouse import Listener # type: ignore

class Calibracion:
    def __init__(self, config):
        self.config = config

    def calibrar(self):
            print("Haz clic en el campo de texto del chat de Meta AI. Se capturarán los clics hasta que presiones ENTER.")

            clics = []
            detener_listener = False

            def on_click(x, y, button, pressed):
                nonlocal detener_listener
                if pressed:
                    clics.append((x, y))
                    print(f"Clic capturado: ({x}, {y})")
                if detener_listener:
                    return False

            listener = Listener(on_click=on_click)
            listener.start()

            input("Presiona ENTER para terminar la captura de clics...")
            detener_listener = True
            listener.join()

            if clics:
                print("Clics capturados:")
                for i, clic in enumerate(clics):
                    print(f"{i+1}. {clic}")

                respuesta = input("¿Cuál de estos clics corresponde al campo de texto del chat? (ingresa el número): ")
                try:
                    indice = int(respuesta) - 1
                    if indice >= 0 and indice < len(clics):
                        posicion = clics[indice]
                        self.config.config['input_chat_pos'] = list(posicion)
                        print(f"Posición del input del chat guardada: {self.config.config['input_chat_pos']}")
                        self.config.guardar_config()
                    else:
                        print("Número inválido.")
                except ValueError:
                    print("Entrada inválida.")
            else:
                print("No se capturaron clics.")
