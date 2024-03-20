Título do Projeto: SuperAtivo

Descrição
Estou a desenvolver um utilitário versátil baseado em Python, desenvolvido para prevenir que o seu computador entre em modo de suspensão enquanto executa tarefas, garantindo uma operação ininterrupta. O programa oferece controle customizável sobre tempos de ativação e execução automatizada.

Funcionalidades Principais

Previne a Suspensão do Sistema: O programa simula atividade no teclado (especificamente, pressionando a tecla F15) em intervalos regulares, fazendo com que o sistema operacional pense que o computador está em uso.
Intervalos definidos pelo usuário: Você pode ajustar o intervalo entre as simulações de pressionamento de tecla para se adequar às necessidades de suas tarefas.
Temporizador de Ativação: Defina um atraso de tempo específico (em segundos) antes do programa começar a manter o seu sistema ativamente acordado.
Temporizador Máximo de Uso: Defina um período máximo de uso (em segundos) para parar o programa automaticamente após um tempo designado.
Suporte à Interface de Linha de Comando (CLI): Defina o intervalo padrão de pressionamento de tecla usando um argumento da linha de comando (--interval).
Alternância Flexível de Estado: Pause e retome a atividade do programa conforme necessário.
Integração com a Bandeja do Sistema (PyQt5): Fornece um ícone na bandeja do sistema com as seguintes opções de menu:
"Definir Tempo de Ativação": Configure o atraso de ativação.
"Definir Tempo de Uso": Estabeleça um limite máximo de uso.
"Alternar Estado": Ative ou desative o programa.
"Sair": Termine a aplicação.
Detalhes Técnicos

Dependências Python:
pyautogui (simulação de teclado)
PyQt5 (interface da bandeja do sistema)
argparse (análise de argumentos da linha de comando)
Threading: Utiliza threading para gerenciar a função keep_awake e as atualizações do menu da bandeja do sistema.
Logging: Logging básico para acompanhar os eventos do programa.
Como Usar

Instale as Dependências: pip install requirements.txt
Execute o script: python superativo.py (Opcionalmente, forneça o argumento --interval, por exemplo, python superativo.py --interval 30)
Clique com o botão direito do mouse no Ícone da Bandeja do Sistema: Utilize as opções de menu para controlar o programa.
Exemplo com Intervalo Personalizado e Tempo de Uso

Python
python superativo.py --interval 60
Use o código com cuidado.
Este comando manterá o sistema acordado com um intervalo de 60 segundos entre simulações das teclas.
