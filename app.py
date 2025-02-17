import time
import threading
import pyautogui
import sys
import argparse
import logging
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QInputDialog
from PyQt5.QtGui import QIcon

class AutoPresser:
    def __init__(self, interval=30):
        self.interval = interval
        self.active = True
        self.thread = None
        self.start_time = time.time()

    def press_key(self):
        while self.active:
            pyautogui.press('f15')
            logging.info("Tecla F15 pressionada.")
            time.sleep(self.interval)

    def toggle_active(self):
        self.active = not self.active
        if self.active:
            logging.info("Ativando programa.")
            self.thread = threading.Thread(target=self.press_key)
            self.thread.daemon = True
            self.thread.start()
        else:
            logging.info("Desativando programa.")
            if self.thread.is_alive():
                self.thread.join()

    def define_activation_time(self):
        tempo_ativacao, ok = QInputDialog.getInt(None, "Tempo de Ativação", "Definir tempo de ativação (em segundos):", 59, 0)
        if ok:
            self.start_time = time.time() + tempo_ativacao
            logging.info(f"Tempo de ativação definido para {tempo_ativacao} segundos.")

    def define_usage_time(self):
        tempo_uso, ok = QInputDialog.getInt(None, "Tempo de Uso", "Definir tempo de uso (em segundos):", 0, 0)
        if ok:
            logging.info(f"Tempo de uso definido para {tempo_uso} segundos.")

def configure_menu(auto_presser):
    menu = QMenu()
    menu.addAction("Tempo de Ativação").triggered.connect(auto_presser.define_activation_time)
    menu.addAction("Tempo de Uso").triggered.connect(auto_presser.define_usage_time)
    menu.addAction("Alternar Estado").triggered.connect(auto_presser.toggle_active)
    menu.addAction("Sair").triggered.connect(sys.exit)
    return menu

def initialize_app(auto_presser):
    app = QApplication(sys.argv)
    tray_icon = QSystemTrayIcon(QIcon("active_icon.png"))
    tray_icon.setVisible(True)
    tray_icon.setContextMenu(configure_menu(auto_presser))
    logging.info("Aplicação inicializada.")
    return app, tray_icon

if __name__ == "__main__":
    logging.basicConfig(filename='activity_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interval", type=int, default=30, help="Intervalo entre pressionamentos de tecla")
    args = parser.parse_args()

    auto_presser = AutoPresser(interval=args.interval)
    app, tray_icon = initialize_app(auto_presser)

    # Iniciar pressionamento de tecla imediatamente
    auto_presser.toggle_active()

    sys.exit(app.exec_())