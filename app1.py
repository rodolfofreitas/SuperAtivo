import time
import threading
import pyautogui
import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QInputDialog
from PyQt5.QtGui import QIcon
import argparse

# Variáveis globais e variáveis de controle
menu_update_event = threading.Event()  # Evento para sinalização

# Criar um analisador de argumentos
parser = argparse.ArgumentParser(description='SuperAtivo')
parser.add_argument('--interval', type=int, default=10, help='Intervalo de tempo em segundos para manter o computador acordado')

# Analisar os argumentos da linha de comando
arguments = parser.parse_args()

# Configurando o logger
import logging
logging.basicConfig(level=logging.INFO)

# Variáveis globais
start_time = None  # Inicializando start_time como None
keep_awake_thread = None  # Variável global para armazenar a thread de manter o computador acordado

# Função para manter o computador acordado
def keep_awake(interval):
    while getattr(keep_awake_thread, "running", True):
        pyautogui.press('f15')
        logging.info("Simulating F15 keypress")
        time.sleep(interval)

# Função para alternar o estado do programa
def toggle_state():
    if getattr(keep_awake_thread, "running", True):
        keep_awake_thread.running = False
        logging.info("Program is now inactive")
    else:
        keep_awake_thread.running = True
        logging.info("Program is now active")

# Funções para definir o tempo de ativação e o tempo máximo de uso
def set_activation_time():
    global start_time
    if keep_awake_thread and keep_awake_thread.is_alive():
        keep_awake_thread.running = False  # Parar a thread atual, se estiver em execução
    time, ok = QInputDialog.getInt(None, "Set Activation Time", "Enter activation time in seconds:")
    if ok:
        start_time = time
        logging.info(f"Activation time set to {time} seconds")
        start_keep_awake_thread()
        menu_update_event.set()  # Sinalizar para atualizar o menu do sistema

def set_usage_time():
    if keep_awake_thread and keep_awake_thread.is_alive():
        keep_awake_thread.running = False  # Parar a thread atual, se estiver em execução
    time, ok = QInputDialog.getInt(None, "Set Usage Time", "Enter maximum usage time in seconds:")
    if ok:
        logging.info(f"Usage time set to {time} seconds")
        threading.Thread(target=stop_program, args=[time]).start()
        start_keep_awake_thread()
        menu_update_event.set()

def start_keep_awake_thread():
    global keep_awake_thread
    keep_awake_thread = threading.Thread(target=keep_awake, args=[arguments.interval])
    keep_awake_thread.setDaemon = True
    keep_awake_thread.start()

def stop_program(time):
    logging.info(f"Stopping program after {time} seconds")
    time.sleep(time)
    keep_awake_thread.running = False

def create_system_tray_menu():
    global menu
    menu = QMenu()  # Cria o menu apenas uma vez

    # Crie ações que serão reutilizadas
    set_activation_action = menu.addAction("Set Activation Time", set_activation_time)
    set_usage_time_action = menu.addAction("Set Usage Time", set_usage_time)
    toggle_state_action = menu.addAction("Toggle State", toggle_state)
    menu.addAction("Exit", app.quit)

    tray_icon.setContextMenu(menu)

    # Inicie a thread para verificar por atualizações no menu
    threading.Thread(target=check_for_menu_updates).start()

def update_menu():
    # Atualize as labels ou status das ações do menu aqui
    pass

def check_for_menu_updates():
    while getattr(keep_awake_thread, "running", True):
        if menu_update_event.is_set():
            menu_update_event.clear()
            update_menu()
        time.sleep(1)  # Ajuste o intervalo de verificação se necessário

# Inicializando a GUI
app = QApplication(sys.argv)
tray_icon = QSystemTrayIcon(QIcon('active_icon.png'), app)
tray_icon.show()

# Criando o menu do sistema
create_system_tray_menu()

# Iniciando a thread para manter o computador acordado
start_keep_awake_thread()

# Executando o loop de eventos do PyQt5
sys.exit(app.exec_())
