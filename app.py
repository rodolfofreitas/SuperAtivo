import time
import threading
import pyautogui
import sys
import argparse
import logging
import psutil
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QInputDialog
from PyQt5.QtGui import QIcon

# Configurar o logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Variáveis globais
start_time = time.time()
ativo = True
args = None

def manter_acordado(intervalo, args):
    """
    Função para manter o computador acordado simulando o pressionamento de tecla.

    Argumentos:
        intervalo (int): Intervalo em segundos entre os pressionamentos de tecla.
        args (Namespace): Argumentos da linha de comando.
    """
    global start_time
    try:
        while True:
            # Simular pressionamento da tecla F15
            pyautogui.press('f15')
            #print("Pressionando F15...")
            time.sleep(intervalo)

            # Desativar se uso da CPU estiver alto
            if args.cpu and psutil.cpu_percent() > args.cpu:
                logging.info("Uso da CPU acima do limite, desativando...")
                alternar_estado()
                break

            # Desativar se tempo de uso expirar
            if args.tempo_uso and time.time() - start_time > args.tempo_uso:
                logging.info("Tempo de uso expirado, desativando...")
                alternar_estado()
                break
    except Exception as e:
        logging.error(f"Erro ao manter o computador acordado: {e}")

def alternar_estado():
    """
    Função para alternar o estado ativo/inativo do programa.
    """
    global ativo, thread
    try:
        ativo = not ativo
        if ativo:
            tray_icon.setIcon(QIcon("active_icon.png"))
            thread = threading.Thread(target=manter_acordado, args=(intervalo, args))
            thread.daemon = True
            thread.start()
        else:
            tray_icon.setIcon(QIcon("inactive_icon.png"))
            if thread.is_alive():
                thread.join()
    except Exception as e:
        logging.error(f"Erro ao alternar estado: {e}")

def definir_tempo_ativacao():
    """
    Função para definir o tempo de ativação do programa através de uma caixa de diálogo.
    """
    global start_time
    try:
        tempo_ativacao, ok = QInputDialog.getInt(None, "Tempo de Ativação", "Definir tempo de ativação (em segundos):", 59, 0)
        if ok:
            args.tempo = tempo_ativacao
            logging.info(f"Tempo de ativação definido para {tempo_ativacao} segundos.")
            # Atualizar tempo de início após definir tempo de ativação
            start_time = time.time()
    except Exception as e:
        logging.error(f"Erro ao definir tempo de ativação: {e}")

def definir_tempo_uso():
    """
    Função para definir o tempo de uso do programa através de uma caixa de diálogo.
    """
    try:
        tempo_uso, ok = QInputDialog.getInt(None, "Tempo de Uso", "Definir tempo de uso (em segundos):", 0, 0)
        if ok:
            args.tempo_uso = tempo_uso
            logging.info(f"Tempo de uso definido para {tempo_uso} segundos.")
    except Exception as e:
        logging.error(f"Erro ao definir tempo de uso: {e}")

try:
    # Inicialização do aplicativo e configuração da bandeja do sistema e ícones
    app = QApplication(sys.argv)
    tray_icon = QSystemTrayIcon()
    tray_icon.setVisible(True)
    menu = QMenu()

    # Adicionando ação ao menu da bandeja do sistema
    action_tempo_ativacao = menu.addAction("Tempo de Ativação")
    action_tempo_uso = menu.addAction("Tempo de Uso")
    action_toggle = menu.addAction("Alternar Estado")
    action_exit = menu.addAction("Sair")

    action_tempo_ativacao.triggered.connect(definir_tempo_ativacao)
    action_tempo_uso.triggered.connect(definir_tempo_uso)
    action_toggle.triggered.connect(alternar_estado)
    action_exit.triggered.connect(app.quit)
    tray_icon.setContextMenu(menu)

    # Processar argumentos da linha de comando
    args = argparse.Namespace(xx=59, tempo=None, cpu=None, tempo_uso=None)  # Argumentos padrão

    # Definir o ícone padrão
    tray_icon.setIcon(QIcon("active_icon.png"))

    # Tempo de início para monitorar o tempo de ativação
    start_time = time.time()

    # Thread para manter o computador acordado
    intervalo = args.xx
    thread = threading.Thread(target=manter_acordado, args=(intervalo, args))
    thread.daemon = True

    # Executar o aplicativo
    sys.exit(app.exec_())

except Exception as e:
    logging.error(f"Erro durante a execução do programa: {e}")
    sys.exit(1)
