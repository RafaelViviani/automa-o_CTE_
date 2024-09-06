import os
import win32com.client
import base64
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from virustotal_python import Virustotal
import pythoncom
import hashlib
import time
import psutil
import threading

# Configura o logging
logging.basicConfig(filename=os.path.abspath('app.log'), filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Chave da API do VirusTotal
VIRUSTOTAL_API_KEY = "5ec2e73c55d2ed552318f91028cbfef61a4306c267cdbb108485dbfd231344e6"

# Semáforo para controlar a execução dos trabalhos
semaphore = threading.Semaphore()


class CustomIntervalTrigger(IntervalTrigger):
    """
    Classe personalizada para evitar a execução simultânea de trabalhos.
    """

    def __init__(self, interval, start_date=None, end_date=None, timezone=None):
        super().__init__(interval, start_date, end_date, timezone)

    def get_next_fire_time(self, previous_fire_time, now):
        with semaphore:
            return super().get_next_fire_time(previous_fire_time, now)


class CustomDateTrigger(DateTrigger):
    """
    Classe personalizada para evitar a execução simultânea de trabalhos.
    """

    def __init__(self, run_date, timezone=None):
        super().__init__(run_date, timezone)

    def get_next_fire_time(self, previous_fire_time, now):
        with semaphore:
            return super().get_next_fire_time(previous_fire_time, now)


def get_file_hash(filename):
    """
    Obtém o hash SHA-256 de um arquivo.

    :param filename: Caminho do arquivo.
    :return: Hash SHA-256 do arquivo.
    """
    with open(filename, "rb") as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def is_malicious(filename):
    """
    Verifica se um arquivo é malicioso usando o VirusTotal.

    :param filename: Caminho do arquivo.
    :return: True se o arquivo for malicioso, False se for seguro.
    """
    try:
        vtotal = Virustotal(VIRUSTOTAL_API_KEY)

        # Envio arquivo para análise
        with open(filename, "rb") as f:
            file_data = f.read()
        resp = vtotal.request("files", method="POST", files={"file": (filename, file_data)})
        analysis_id = resp.data["id"]

        # Em seguida, obtenha o relatório de análise
        # Isso pode levar algum tempo
        while True:
            resp = vtotal.request(f"analyses/{analysis_id}")
            status = resp.data["attributes"]["status"]
            if status == "completed":
                break
            elif status == "queued" or status == "running":
                time.sleep(15)  # Aguarde 15 segundos antes de verificar novamente
            else:
                raise Exception(f"Análise falhou com status: {status}")

        malicious = resp.data["attributes"]["stats"]["malicious"]
        if malicious > 0:
            logging.warning(f'Arquivo {filename} é malicioso com {malicious} detecções')
            print(f'Arquivo {filename} é malicioso com {malicious} detecções')
            return True
        else:
            logging.info(f'Arquivo {filename} é seguro')
            print(f'Arquivo {filename} é seguro')
            return False
    except Exception as e:
        logging.error(f'Erro: {str(e)}')
        print(f'Erro: {str(e)}')
        return False


def kill_outlook():
    """
    Encerra o processo do Outlook se estiver em execução.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if 'OUTLOOK.EXE' in proc.info['name']:
            pid = proc.info['pid']
            process = psutil.Process(pid)
            process.terminate()


def check_mail_every_10_seconds():
    """
    Verifica e processa e-mails a cada 10 segundos.
    """
    kill_outlook()  # Mata o processo do Outlook antes de verificar e-mails
    pythoncom.CoInitialize()
    try:
        logging.info('Verificando e-mails...')
        print('Verificando e-mails...')
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = outlook.Folders['edi.notfis@frilog.com.br'].Folders['Caixa de Entrada']

        # Filtra apenas as mensagens não lidas
        messages = inbox.Items.Restrict("[UnRead] = true")

        for message in messages:
            logging.info(f'Lendo mensagem de e-mail de {message.Subject}')
            print(f'Lendo mensagem de e-mail de {message.Subject}')
            message.UnRead = False  # Marca a mensagem como lida

            if message.Attachments.Count > 0:
                for attachment in message.Attachments:
                    prohibited_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx', '.xls',
                                             '.xlsx', '.py', '.js', '.php', '.zip', '.rar', '.exe']
                    if any(attachment.FileName.lower().endswith(ext) for ext in prohibited_extensions):
                        logging.info(f'Arquivo {attachment.FileName} ignorado devido à extensão proibida')
                        continue

                    filePath = os.path.join('C:\\Users\\suporte-atm\\Documents\\Notfis', attachment.FileName)
                    if not os.path.splitext(filePath)[1]:  # Se o arquivo não tem extensão
                        filePath += '.txt'  # Adicione .txt ao final do nome do arquivo

                    # Salva o arquivo para verificação
                    attachment.SaveAsFile(filePath)

                    # Verifica se o arquivo é seguro antes de prosseguir com o download
                    if not is_malicious(filePath):
                        # Move o arquivo para o destino final
                        dest_path = os.path.join('C:\\Users\\suporte-atm\\Documents\\Notfis',
                                                 attachment.FileName)
                        if not os.path.splitext(dest_path)[1]:  # Se o arquivo não tem extensão
                            dest_path += '.txt'  # Adicione .txt ao final do nome do arquivo
                        os.rename(filePath, dest_path)
                        logging.info(f'Arquivo {attachment.FileName} verificado e movido para {dest_path}')
                        print(f'Arquivo {attachment.FileName} verificado e movido para {dest_path}')
                    else:
                        # Remove o arquivo se for malicioso
                        os.remove(filePath)
                        logging.warning(f'Arquivo {attachment.FileName} detectado como malicioso e excluído')
                        print(f'Arquivo {attachment.FileName} detectado como malicioso e excluído')

        logging.info('Verificação concluída.')
        print('Verificação concluída.')
    except Exception as e:
        logging.error(f'Erro: {str(e)}')
        print(f'Erro: {str(e)}')
    finally:
        pythoncom.CoUninitialize()



scheduler = BackgroundScheduler()
scheduler.add_job(check_mail_every_10_seconds, trigger=IntervalTrigger(minutes=5), id='check_mail')
scheduler.start()
logging.info('Agendador de tarefas iniciado')
print('Agendador de tarefas iniciado')

try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
