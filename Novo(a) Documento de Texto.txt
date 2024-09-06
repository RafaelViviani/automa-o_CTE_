<h4 align="center"> 
    :construction:  Projeto em construção  :construction:
<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge"/>
</p>

<h1 align="center"> Sistema de Verificação e Processamento de Emails </h1>

# :hammer: Funcionalidades do projeto

- `Funcionalidade 1`: Verificação de emails a cada 10 segundos.
- `Funcionalidade 2`: Processamento de anexos de emails.
- `Funcionalidade 3`: Verificação de malwares usando a VirusTotal API.
- `Funcionalidade 4`: Renovação automática do token da VirusTotal API.
- `Funcionalidade 5`: Encerramento do processo do Outlook antes da verificação.
- `Funcionalidade 6`: Agendamento de tarefas usando o BackgroundScheduler.
- `Funcionalidade 7`: Registro de atividades em um arquivo de log.

# 🛠️ Tecnologias e Bibliotecas Utilizadas

- [Python](https://www.python.org/)
- [Win32com](https://pythonhosted.org/pywin32/)
- [APScheduler](https://apscheduler.readthedocs.io/en/stable/)
- [VirusTotal API](https://github.com/blacktop/virustotal-api)
- [Pythoncom](https://docs.python.org/3/library/pythoncom.html)
- [Hashlib](https://docs.python.org/3/library/hashlib.html)
- [Psutil](https://psutil.readthedocs.io/en/latest/)

# 📁 Como acessar o projeto

1. Clone o repositório para sua máquina local:
    ```bash
    git clone https://github.com/RafaelViviani/automacao_cte.git
    ```

# 🛠️ Como rodar o projeto

1. Instale as dependências do projeto:
    ```bash
    pip install -r requirements.txt
    ```

2. Execute o script principal:
    ```bash
    python main.py
    ```

# ⚙️ Configurações

- **VIRUSTOTAL_API_KEY**: Chave da API do VirusTotal (necessária para a funcionalidade de verificação de malwares).

# :hammer: Variáveis Globais

- `semaphore`: Semáforo para controlar a execução simultânea de trabalhos.

# ⚙️ Padrão de Projeto

O projeto utiliza a biblioteca APScheduler para agendar tarefas de verificação de emails e processamento de anexos. O código é estruturado de forma a evitar a execução simultânea de trabalhos usando um semáforo (`semaphore`). A comunicação com a VirusTotal API é feita por meio da biblioteca `virustotal_python`.

# 📑 Funcionalidades Detalhadas

### `get_file_hash(filename)`

Obtém o hash SHA-256 de um arquivo.

- **Parâmetros:**
  - `filename`: Caminho do arquivo.

- **Retorno:**
  - Hash SHA-256 do arquivo.

### `is_malicious(filename)`

Verifica se um arquivo é malicioso usando o VirusTotal.

- **Parâmetros:**
  - `filename`: Caminho do arquivo.

- **Retorno:**
  - `True` se o arquivo for malicioso, `False` se for seguro.

### `kill_outlook()`

Encerra o processo do Outlook se estiver em execução.

### `check_mail_every_10_seconds()`

Verifica e processa e-mails a cada 10 segundos.

### `renew_virustotal_token()`

Renova automaticamente o token da VirusTotal API quando expirado.

### `scheduler`

Agendador de tarefas configurado para verificar e processar e-mails a cada 5 minutos.
# :wrench: Detalhes da Função `check_mail_every_10_seconds()`

A função `check_mail_every_10_seconds()` é uma peça central no projeto, responsável por verificar e processar e-mails a cada 10 segundos. Abaixo estão detalhes específicos sobre a implementação e funcionalidades desta função crucial.

### :mag: Visão Geral

Esta função realiza as seguintes operações em um ciclo de 10 segundos:

1. **Encerramento do Outlook:** Antes de verificar e-mails, o processo do Outlook é encerrado para garantir um ambiente limpo.

2. **Verificação de E-mails Não Lidos:** A função acessa a caixa de entrada do Outlook e filtra apenas as mensagens não lidas para processamento.

3. **Processamento de Anexos:** Para cada e-mail com anexos, a função verifica se o arquivo é seguro antes de prosseguir com o download.

4. **Verificação de Malwares:** Utiliza a VirusTotal API para verificar se o arquivo é malicioso.

5. **Movimentação ou Exclusão de Arquivos:** Com base na verificação, o arquivo é movido para o destino final se for seguro, caso contrário, é excluído.

6. **Registro de Atividades:** Todas as atividades são registradas em um arquivo de log (`app.log`).

### :gear: Configurações Adicionais

- **Proibições de Extensões:** A função ignora anexos com extensões específicas, como `.jpg`, `.jpeg`, `.exe`, entre outras.

- **Diretório de Destino:** Os arquivos processados com segurança são movidos para o diretório especificado (`C:\Users\suporte-atm\Documents\Notfis`).

### :warning: Manipulação de Arquivos

- **Extensão Padrão:** Se um anexo não tiver uma extensão, a função adiciona `.txt` ao final do nome do arquivo.

- **Exclusão de Arquivos Maliciosos:** Se um arquivo é detectado como malicioso, é excluído para evitar riscos.

### :computer: Utilização Contínua

A função é integrada ao agendador de tarefas (`scheduler`) para garantir a execução automática a cada 10 segundos.

### :information_source: Log de Atividades

Todas as atividades são registradas no arquivo de log `app.log`, fornecendo uma trilha de auditoria completa.

### :closed_lock_with_key: Semáforo

A execução da função é controlada por um semáforo para evitar a execução simultânea de trabalhos.

### :alarm_clock: Agendamento

A função é agendada para execução pelo `BackgroundScheduler` a cada 5 minutos.

---

**Observação:** Certifique-se de configurar corretamente as permissões e o ambiente para a execução contínua desta função, e mantenha a chave da API do VirusTotal (`VIRUSTOTAL_API_KEY`) válida para garantir a integridade da verificação de malwares.



# 📝 Utilização

O projeto verifica automaticamente e processa anexos de e-mails a cada 5 minutos. Os resultados são registrados no arquivo de log `app.log`.



# 📝 A fazer

- [ ] Transformar o executavel em serviço
- [ ] Trocar a parta para a pasta mapeada do sistema
- [ ] Entregar o projeto até fevereiro.

