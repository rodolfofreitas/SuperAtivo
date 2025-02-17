import time
import threading
import pyautogui
import sys
import argparse
import logging
import random
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QInputDialog
from PyQt5.QtGui import QIcon
from logging.handlers import TimedRotatingFileHandler

# Configuração do logger para registrar atividades em um arquivo de log
handler = TimedRotatingFileHandler('activity_log.log', when='midnight', interval=1, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

class AutoPresser:
    """
    Classe responsável por automatizar o pressionamento da tecla F15 em intervalos definidos.
    Permite definir tempos de ativação e uso, além de ativar/desativar a automação.
    """

    def __init__(self, interval):
        """
        Inicializa a classe AutoPresser.

        :param interval: Intervalo em segundos entre os pressionamentos da tecla.
        """
        self.base_interval = interval  # Intervalo base entre pressionamentos
        self.active = True  # Estado da automação (ativa ou não)
        self.thread = None  # Thread para o pressionamento da tecla
        self.start_time = time.time()  # Tempo de início
        self.usage_time = 0  # Tempo de uso definido
        self.usage_start_time = None  # Tempo de início do uso
        self.toggle_active(True)  # Ativa a automação ao iniciar

    def press_key(self):
        """
        Método que pressiona a tecla F15 em intervalos definidos enquanto a automação estiver ativa.
        """
        while True:
            if self.active:
                # Verifica se o tempo de uso foi atingido
                if self.usage_start_time and (time.time() - self.usage_start_time >= self.usage_time):
                    logging.info("Tempo de uso atingido. Desativando.")
                    self.toggle_active(False)  # Desativa a automação
                    break

                # Simula um movimento do mouse para uma posição aleatória
                x, y = random.randint(0, 1920), random.randint(0, 1080)  # Ajuste os limites conforme a resolução da tela
                pyautogui.moveTo(x, y, duration=0.5)  # Move o mouse para a posição aleatória
                logging.info(f"Mouse movido para a posição: ({x}, {y})")

                # Pressiona a tecla F15
                pyautogui.press('f15')  # Pressiona a tecla F15
                logging.info("Tecla F15 pressionada.")

                # Gera um intervalo aleatório entre 3 a 4 minutos (180 a 240 segundos)
                random_interval = random.randint(180, 240)  # Intervalo aleatório entre 180 e 240 segundos
                time.sleep(random_interval)  # Aguarda o intervalo definido
            else:
                logging.info("AutoPresser desativado.")
                time.sleep(1)  # Aguarda um segundo antes de verificar novamente

    def toggle_active(self, active=None):
        """
        Alterna o estado da automação entre ativo e inativo.

        :param active: Se fornecido, define o estado da automação.
        """
        if active is not None:
            self.active = active  # Atualiza o estado da automação
        if self.active:
            logging.info("Ativando programa.")
            if self.thread is None or not self.thread.is_alive():
                # Inicia uma nova thread para pressionar a tecla
                self.thread = threading.Thread(target=self.press_key)
                self.thread.daemon = True  # Permite que a thread seja encerrada quando o programa principal terminar
                self.thread.start()
        else:
            logging.info("Desativando programa.")
            if self.thread is not None and self.thread.is_alive():
                self.thread.join()  # Aguarda a thread terminar

    def define_activation_time(self):
        """
        Define o tempo de ativação da automação através de um diálogo de entrada.
        """
        tempo_ativacao, ok = QInputDialog.getInt(None, "Tempo de Ativação", "Definir tempo de ativação (em segundos):", 59, 0)
        if ok:
            self.start_time = time.time() + tempo_ativacao  # Define o tempo de ativação
            logging.info(f"Tempo de ativação definido para {tempo_ativacao} segundos.")

    def define_usage_time(self):
        """
        Define o tempo de uso da automação através de um diálogo de entrada.
        """
        tempo_uso, ok = QInputDialog.getInt(None, "Tempo de Uso", "Definir tempo de uso (em segundos):", 0, 0)
        if ok:
            self.usage_time = tempo_uso  # Define o tempo de uso
            self.usage_start_time = time.time()  # Marca o início do uso
            logging.info(f"Tempo de uso definido para {tempo_uso} segundos.")

    def update_menu(self, menu):
        """
        Atualiza o texto do item de menu que alterna o estado da automação.

        :param menu: O menu da bandeja do sistema.
        """
        toggle_action = menu.actions()[2]  # O terceiro item do menu é o que alterna o estado
        toggle_action.setText("Desativar" if self.active else "Ativar")  # Atualiza o texto do item de menu com base no estado atual

def configure_menu(auto_presser):
    """
    Configura o menu da bandeja do sistema para a aplicação.

    :param auto_presser: Instância da classe AutoPresser.
    :return: Menu configurado.
    """
    menu = QMenu()
    menu.addAction("Tempo de Ativação").triggered.connect(auto_presser.define_activation_time)  # Ação para definir o tempo de ativação
    menu.addAction("Tempo de Uso").triggered.connect(auto_presser.define_usage_time)  # Ação para definir o tempo de uso
    toggle_action = menu.addAction("Desativar" if auto_presser.active else "Ativar")  # Ação para ativar/desativar
    toggle_action.triggered.connect(lambda: [auto_presser.toggle_active(not auto_presser.active), auto_presser.update_menu(menu)])  # Alterna o estado e atualiza o menu
    menu.addAction("Sair").triggered.connect(sys.exit)  # Ação para sair da aplicação
    return menu

def initialize_app(auto_presser):
    """
    Inicializa a aplicação e a bandeja do sistema.

    :param auto_presser: Instância da classe AutoPresser.
    :return: Aplicação e ícone da bandeja do sistema.
    """
    app = QApplication(sys.argv)  # Cria a aplicação Qt
    tray_icon = QSystemTrayIcon(QIcon("active_icon.png"))  # Cria o ícone da bandeja do sistema
    tray_icon.setVisible(True)  # Torna o ícone visível
    menu = configure_menu(auto_presser)  # Configura o menu
    tray_icon.setContextMenu(menu)  # Define o menu para o ícone da bandeja
    logging.info("Aplicação inicializada.")  # Log de inicialização
    return app, tray_icon

if __name__ == "__main__":
    # Configuração do logger para registrar atividades em um arquivo de log
    logging.basicConfig(filename='activity_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser()  # Cria o parser de argumentos
    parser.add_argument("-i", "--interval", type=int, default=30, help="Intervalo entre pressionamentos de tecla")  # Argumento para intervalo
    args = parser.parse_args()  # Analisa os argumentos

    auto_presser = AutoPresser(interval=args.interval)  # Cria a instância do AutoPresser
    app, tray_icon = initialize_app(auto_presser)  # Inicializa a aplicação

    sys.exit(app.exec_())  # Executa a aplicação e aguarda a saída
# End of file