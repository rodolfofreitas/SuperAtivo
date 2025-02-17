import keyboard
import time
import logging
from datetime import datetime

# Configuração do logger
logging.basicConfig(filename='activity_log.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Função para simular pressionamento da tecla F15
def simulate_key_press():
    keyboard.press_and_release('F15')

# Função para ativar o sistema
def activate_system(interval, duration):
    logging.info('Sistema ativado.')
    logging.info(f'Pressionar tecla F15 a cada {interval} segundos.')
    logging.info(f'Sistema irá desativar após {duration} segundos de uso.')

    end_time = time.time() + duration
    while time.time() < end_time:
        simulate_key_press()
        time.sleep(interval)

    logging.info('Sistema desativado.')

# Função principal
def main():
    interval = int(input('Definir intervalo para pressionar a tecla F15 (em segundos): '))
    duration = int(input('Definir tempo de atividade do programa (em segundos, 0 para nunca desativar): '))

    logging.info('Iniciando o programa.')

    if duration == 0:
        logging.info('Definido para nunca desativar.')
    else:
        logging.info(f'Desativar automaticamente após {duration} segundos.')

    activate_system(interval, duration)

# Executar o programa
if __name__ == '__main__':
    main()
