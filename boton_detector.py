# boton_detector.py
import cv2 # type: ignore
import numpy as np
import pyautogui # type: ignore

class BotonDetector:
    def __init__(self, play_template_path, pause_template_path, stop_template_path):
        self.play_template = cv2.imread(play_template_path)
        self.pause_template = cv2.imread(pause_template_path)
        self.stop_template = cv2.imread(stop_template_path)
        self.scales = [0.5, 0.75, 1.0, 1.25, 1.5]

    def detectar_botones(self):
        img = pyautogui.screenshot(region=(0, 0, 860, 1000))
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.namedWindow('Pantalla', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Pantalla', 430, 500) 
        detectado = False

        for scale in self.scales:
            resized_play_template = cv2.resize(self.play_template, (0, 0), fx=scale, fy=scale)
            resized_pause_template = cv2.resize(self.pause_template, (0, 0), fx=scale, fy=scale)
            resized_stop_template = cv2.resize(self.stop_template, (0, 0), fx=scale, fy=scale)

            # Detecta los botones utilizando template matching
            play_result = cv2.matchTemplate(frame, resized_play_template, cv2.TM_CCOEFF_NORMED)
            pause_result = cv2.matchTemplate(frame, resized_pause_template, cv2.TM_CCOEFF_NORMED)
            stop_result = cv2.matchTemplate(frame, resized_stop_template, cv2.TM_CCOEFF_NORMED)

            # Reconoce los botones
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(play_result)
            if max_val > 0.95:
                print("play")
                cv2.rectangle(frame, max_loc, (max_loc[0] + resized_play_template.shape[1], max_loc[1] + resized_play_template.shape[0]), (0, 255, 0), 2)
                detectado = True

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(pause_result)
            if max_val > 0.85:
                print("pause")
                cv2.rectangle(frame, max_loc, (max_loc[0] + resized_pause_template.shape[1], max_loc[1] + resized_pause_template.shape[0]), (0, 255, 0), 2)
                detectado = True

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(stop_result)
            if max_val > 0.70:
                print("stop")
                cv2.rectangle(frame, max_loc, (max_loc[0] + resized_stop_template.shape[1], max_loc[1] + resized_stop_template.shape[0]), (0, 255, 0), 2)
                detectado = True

        cv2.imshow('Pantalla', frame)
        
        return detectado
