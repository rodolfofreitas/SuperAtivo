"""
SuperAtivo - Automatizador de Atividade

Este módulo implementa um sistema de automação para simular atividade do usuário
através de movimentos do mouse e pressionamento de teclas em intervalos aleatórios.

Features:
- Interface gráfica com ícone na bandeja do sistema
- Controle de tempo de execução
- Movimentos aleatórios do mouse
- Logging detalhado de atividades
- Feedback em tempo real do status

Author: Rodolfo Caldas Freitas
Version: 2.0.0
"""

import time
import threading
import pyautogui
import sys
import argparse
import logging
import random
import os
from dataclasses import dataclass
from typing import Optional
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QInputDialog
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon, QPixmap
from logging.handlers import TimedRotatingFileHandler

# Configurações globais
SCREEN_REFRESH_RATE = 1000  # ms
MIN_INTERVAL = 180  # segundos
MAX_INTERVAL = 240  # segundos
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

@dataclass
class ActivityStatus:
    """Classe para armazenar o estado atual da atividade"""
    message: str = ""
    is_active: bool = False
    last_update: float = time.time()
    remaining_time: Optional[int] = None

class AutoPresser:
    def __init__(self, interval: int):
        """Inicializa o AutoPresser com as configurações básicas"""
        self.base_interval = interval
        self.status = ActivityStatus()
        self.thread: Optional[threading.Thread] = None
        self.should_stop = False
        self.usage_time = 0
        self.usage_start_time = None
        self._setup_logging()
        self.toggle_active(True)

    def _setup_logging(self) -> None:
        """Configura o sistema de logging"""
        self.logger = logging.getLogger(__name__)
        handler = TimedRotatingFileHandler(
            'activity_log.log',
            when='midnight',
            interval=1,
            backupCount=7
        )
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _perform_activity(self) -> None:
        """Executa as ações de movimento do mouse e tecla"""
        try:
            # Obtém dimensões da tela
            screen_size = pyautogui.size()
            
            # Gera posições aleatórias dentro dos limites da tela
            x = random.randint(0, screen_size.width)
            y = random.randint(0, screen_size.height)
            
            # Executa ações
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.press('f15')
            
            self.logger.info(f"Atividade realizada: Mouse ({x}, {y}) e tecla F15")
        except Exception as e:
            self.logger.error(f"Erro ao executar atividade: {str(e)}")
            raise

    def press_key(self) -> None:
        """Loop principal de execução das atividades"""
        while not self.should_stop:
            if self.status.is_active:
                try:
                    current_time = time.time()
                    
                    # Verifica tempo de uso
                    if self._check_usage_time(current_time):
                        continue

                    # Executa ações
                    self._perform_activity()
                    
                    # Intervalo aleatório
                    interval = random.randint(MIN_INTERVAL, MAX_INTERVAL)
                    self.update_status(
                        f"Aguardando {interval/60:.1f} minutos até próxima atividade"
                    )
                    time.sleep(interval)
                    
                except Exception as e:
                    self.logger.error(f"Erro durante execução: {str(e)}", exc_info=True)
                    self.update_status(f"Erro: {str(e)}")
                    time.sleep(5)
            else:
                time.sleep(1)

    def _check_usage_time(self, current_time: float) -> bool:
        """Verifica se o tempo de uso foi atingido"""
        if self.usage_time > 0 and self.usage_start_time:
            remaining = self.usage_time - (current_time - self.usage_start_time)
            self.status.remaining_time = int(remaining)
            
            if remaining <= 0:
                self.update_status("Tempo de uso finalizado")
                self.status.is_active = False
                return True
                
            if int(current_time - self.status.last_update) >= 60:
                self.update_status(
                    f"Em execução - Tempo restante: {int(remaining/60)} minutos"
                )
        return False

    def update_status(self, message: str) -> None:
        """Atualiza o status e propaga para a interface"""
        self.status.message = message
        self.status.last_update = time.time()
        self.logger.info(message)
        
        if hasattr(self, 'tray_icon'):
            self.tray_icon.setToolTip(message)

    def toggle_active(self, active: Optional[bool] = None) -> None:
        """Alterna o estado de ativação do programa"""
        if active is not None:
            self.status.is_active = active
        else:
            self.status.is_active = not self.status.is_active

        if self.status.is_active:
            self.update_status("Programa ativado - Iniciando atividades...")
            if self.thread is None or not self.thread.is_alive():
                self.should_stop = False
                self.thread = threading.Thread(target=self.press_key)
                self.thread.daemon = True
                self.thread.start()
        else:
            self.update_status("Programa pausado")

    def define_usage_time(self) -> None:
        """Define o tempo de uso do programa"""
        tempo_uso, ok = QInputDialog.getInt(
            None, 
            "Tempo de Uso", 
            "Definir tempo de uso (em minutos):",
            30, 1, 1440  # Mínimo 1 minuto, máximo 24 horas
        )
        if ok and tempo_uso > 0:
            self.usage_time = tempo_uso * 60  # Converte para segundos
            self.usage_start_time = time.time()
            if not self.status.is_active:
                self.toggle_active(True)
            self.update_status(f"Tempo de uso definido: {tempo_uso} minutos")

def configure_menu(auto_presser):
    """
    Configura o menu da bandeja do sistema.
    
    Args:
        auto_presser: Instância do AutoPresser
    
    Returns:
        QMenu: Menu configurado
    """
    menu = QMenu()
    
    # Status atual com texto inicial correto
    status_action = menu.addAction(f"Status: {auto_presser.status.message}")
    status_action.setEnabled(False)
    
    menu.addSeparator()
    
    # Ações do menu com ícones
    usage_action = menu.addAction("⏱️ Definir Tempo de Uso")
    usage_action.triggered.connect(auto_presser.define_usage_time)
    
    toggle_action = menu.addAction("⏸️ Pausar" if auto_presser.status.is_active else "▶️ Iniciar")
    
    def toggle_handler():
        auto_presser.toggle_active()
        new_text = "⏸️ Pausar" if auto_presser.status.is_active else "▶️ Iniciar"
        toggle_action.setText(new_text)
    
    toggle_action.triggered.connect(toggle_handler)
    
    menu.addSeparator()
    exit_action = menu.addAction("🚪 Sair")
    exit_action.triggered.connect(
        lambda: [
            auto_presser.update_status("Encerrando..."),
            setattr(auto_presser, 'should_stop', True),
            QApplication.quit()
        ]
    )
    
    # Armazena referências importantes no auto_presser
    auto_presser.status_action = status_action
    auto_presser.toggle_action = toggle_action
    
    return menu  # Retorna apenas o menu

def main():
    """Função principal do programa"""
    parser = argparse.ArgumentParser(
        description="SuperAtivo - Automatizador de Atividade"
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=30,
        help="Intervalo base entre ações (segundos)"
    )
    args = parser.parse_args()

    try:
        auto_presser = AutoPresser(interval=args.interval)
        app = QApplication(sys.argv)
        
        # Configura ícone
        icon_path = "active_icon.png"
        if not os.path.exists(icon_path):
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.transparent)
            icon = QIcon(pixmap)
        else:
            icon = QIcon(icon_path)
        
        tray_icon = QSystemTrayIcon(icon)
        menu = configure_menu(auto_presser)  # Agora recebe apenas o menu
        tray_icon.setContextMenu(menu)
        tray_icon.setVisible(True)
        auto_presser.tray_icon = tray_icon
        
        # Configura timer para atualização do status
        timer = QTimer()
        timer.timeout.connect(lambda: auto_presser.status_action.setText(f"Status: {auto_presser.status.message}"))
        timer.start(1000)  # Atualiza a cada segundo
        
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Erro fatal: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
# End of file