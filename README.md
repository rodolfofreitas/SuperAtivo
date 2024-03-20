### Título do Projeto: SuperAtivo

#### Descrição
Estou desenvolvendo um utilitário versátil baseado em Python, projetado para prevenir que o seu computador entre em modo de suspensão enquanto executa tarefas, garantindo uma operação ininterrupta. O programa oferece controle customizável sobre tempos de ativação e execução automatizada.

#### Funcionalidades Principais

- **Previne a Suspensão do Sistema:** O programa simula atividade no teclado (especificamente, pressionando a tecla F15) em intervalos regulares, fazendo com que o sistema operacional pense que o computador está em uso.
- **Intervalos definidos pelo usuário:** Você pode ajustar o intervalo entre as simulações de pressionamento de tecla para se adequar às necessidades de suas tarefas.
- **Temporizador de Ativação:** Defina um atraso de tempo específico (em segundos) antes do programa começar a manter o seu sistema ativamente acordado.
- **Temporizador Máximo de Uso:** Defina um período máximo de uso (em segundos) para parar o programa automaticamente após um tempo designado.
- **Suporte à Interface de Linha de Comando (CLI):** Defina o intervalo padrão de pressionamento de tecla usando um argumento da linha de comando (--interval).
- **Alternância Flexível de Estado:** Pause e retome a atividade do programa conforme necessário.
- **Integração com a Bandeja do Sistema (PyQt5):** Fornece um ícone na bandeja do sistema com as seguintes opções de menu:
  - "Definir Tempo de Ativação": Configure o atraso de ativação.
  - "Definir Tempo de Uso": Estabeleça um limite máximo de uso.
  - "Alternar Estado": Ative ou desative o programa.
  - "Sair": Termine a aplicação.

#### Detalhes Técnicos

**Dependências Python:**
- pyautogui (simulação de teclado)
- PyQt5 (interface da bandeja do sistema)
- argparse (análise de argumentos da linha de comando)

- **Threading:** Utiliza threading para gerenciar a função keep_awake e as atualizações do menu da bandeja do sistema.
- **Logging:** Logging básico para acompanhar os eventos do programa.

#### Como Usar

1. **Instale as Dependências:** `pip install requirements.txt`
2. **Execute o script:** `python superativo.py` (Opcionalmente, forneça o argumento --interval, por exemplo, `python superativo.py --interval 30`)
3. **Clique com o botão direito do mouse no Ícone da Bandeja do Sistema:** Utilize as opções de menu para controlar o programa.

#### Exemplo com Intervalo Personalizado e Tempo de Uso

```bash
python superativo.py --interval 60
```
Use o código com cuidado. Este comando manterá o sistema acordado com um intervalo de 60 segundos entre simulações das teclas.


-----------------------------------------------------------------------------------------------------------------------------------------------

### Project Title: SuperActive

#### Description
I'm developing a versatile Python-based utility designed to prevent your computer from entering sleep mode while performing tasks, ensuring uninterrupted operation. The program offers customizable control over activation times and automated execution.

#### Core Features

- **Prevents System Sleep:** The program simulates keyboard activity (specifically, pressing the F15 key) at regular intervals, tricking your operating system into thinking the computer is in use.
- **User-Defined Intervals:** You can adjust the interval between simulated keypresses to suit the needs of your tasks.
- **Activation Timer:** Set a specific time delay (in seconds) before the program begins actively keeping your system awake.
- **Maximum Usage Timer:** Define a maximum usage period (in seconds) to automatically stop the program after a designated time.
- **Command-Line Interface (CLI) Support:** Set the default keypress interval using a command-line argument (--interval).
- **Flexible State Toggling:** Pause and resume the program's activity as needed.
- **System Tray Integration (PyQt5):** Provides a system tray icon with the following menu options:
  - "Set Activation Time": Configure the activation delay.
  - "Set Usage Time": Establish a maximum usage limit.
  - "Toggle State": Enable or disable the program.
  - "Exit": Terminate the application.

#### Technical Details

**Python Dependencies:**
- pyautogui (for keyboard simulation)
- PyQt5 (for system tray interface)
- argparse (command-line argument parsing)

- **Threading:** Employs threading to manage the keep_awake function and handle system tray menu updates.
- **Logging:** Basic logging for tracking program events.

#### How to Use

1. **Install Dependencies:** `pip install requirements.txt`
2. **Run the script:** `python superativo.py` (Optionally, provide the --interval argument, e.g., `python superativo.py --interval 30`)
3. **Right-Click the System Tray Icon:** Utilize the menu options to control the program.

#### Example with Custom Interval and Usage Time

```bash
python superativo.py --interval 60
```
Use the code with caution. This command will keep the system awake with an interval of 60 seconds between keypresses.
