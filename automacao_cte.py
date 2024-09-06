import os
import win32com.client
import base64
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from virustotal_python import Virustotal
import pythoncom
import hashlib
import time
import psutil

# Configura o logging
logging.basicConfig(filename=os.path.abspath('app.log'), filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

VIRUSTOTAL_API_KEY = "5ec2e73c55d2ed552318f91028cbfef61a4306c267cdbb108485dbfd231344e6"

def get_file_hash(filename):
    with open(filename, "rb") as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()

def is_malicious(filename):
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
            logging.info(f'Arquivo {filename} é malicioso com {malicious} detecções')
            return True
        else:
            logging.info(f'Arquivo {filename} é seguro')
            print(f'Arquivo {filename} é seguro')
            return False
    except Exception as e:
        logging.error(f'Erro: {str(e)}')
        print(f'Erro: {str(e)}')

def check_outlook_running():
    for process in psutil.process_iter(['pid', 'name']):
        if 'OUTLOOK.EXE' in process.info['name']:
            return True
    return False

def close_outlook():
    for process in psutil.process_iter(['pid', 'name']):
        if 'OUTLOOK.EXE' in process.info['name']:
            pid = process.info['pid']
            psutil.Process(pid).terminate()

def check_mail_every_10_seconds():
    pythoncom.CoInitialize()
    try:
        logging.info('Verificando e-mails...')
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = outlook.Folders['edi.notfis@frilog.com.br'].Folders['Caixa de Entrada']

        for message in inbox.Items:
            if message.UnRead:
                logging.info(f'E-mail lido - Assunto: {message.Subject}, Remetente: {message.SenderName}, Data de Envio: {message.ReceivedTime}')
                print(f'E-mail lido - Assunto: {message.Subject}, Remetente: {message.SenderName}, Data de Envio: {message.ReceivedTime}')

                if message.Attachments.Count > 0:
                    for attachment in message.Attachments:
                        prohibited_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.py', '.js', '.php', '.exe']
                        if any(attachment.FileName.lower().endswith(ext) for ext in prohibited_extensions):
                            logging.info(f'Arquivo {attachment.FileName} ignorado devido à extensão proibida')
                            continue

                        filePath = os.path.join('C:\\Users\\suporte-atm\\Documents\\Notfis', attachment.FileName)
                        if not os.path.exists(os.path.dirname(filePath)):
                            os.makedirs(os.path.dirname(filePath))
                        attachment.SaveAsFile(filePath)
                        logging.info(f'Arquivo {attachment.FileName} baixado com sucesso. Tamanho: {attachment.Size} bytes, Tipo: {attachment.Type}')
                        print(f'Arquivo {attachment.FileName} baixado com sucesso. Tamanho: {attachment.Size} bytes, Tipo: {attachment.Type}')

                        if ".txt" in attachment.FileName:
                            if is_malicious(filePath):
                                os.remove(filePath)
                                logging.warning(f'Arquivo {attachment.FileName} detectado como malicioso e excluído')
                                print(f'Arquivo {attachment.FileName} detectado como malicioso e excluído')
                            else:
                                dest_path = os.path.join('C:\\Users\\suporte-atm\\Documents\\Notfis', attachment.FileName)
                                os.rename(filePath, dest_path)
                                logging.info(f'Arquivo {attachment.FileName} verificado e movido para {dest_path}')
                                print(f'Arquivo {attachment.FileName} verificado e movido para {dest_path}')

                message.UnRead = False  # Marca a mensagem como lida

        logging.info('Verificação concluída.')
    except Exception as e:
        logging.error(f'Erro: {str(e)}')
        print(f'Erro: {str(e)}')
    finally:
        pythoncom.CoUninitialize()

# Verificar se o Outlook está em execução e fechá-lo se necessário
if check_outlook_running():
    logging.info('Fechando o Outlook...')
    close_outlook()
    time.sleep(10)  # Aguarde alguns segundos para garantir que o Outlook seja fechado
    logging.info('Outlook fechado com sucesso.')

scheduler = BackgroundScheduler()
scheduler.add_job(check_mail_every_10_seconds, 'interval', seconds=15)
scheduler.start()
logging.info('Agendador de tarefas iniciado')
print('Agendador de tarefas iniciado')

try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
