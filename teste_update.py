import pyodbc
import base64
import os

# Dados de acesso ao banco de dados
dados_conexao = ("Driver={SQL Server};"
                 "Server=192.168.100.242;"
                 "Database=softran_teste;"
                 "UID=softran;"
                 "PWD=sof1209;")
conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()
 
print("Conexão bem sucedida!")
# Valores para identificar a imagem que você quer atualizar
cdempresa = 112
nrseqcontrole = 532172
cdsequencia = 2

# Função para ler e codificar o arquivo de imagem em base64
def ler_imagem_para_base64(caminho_imagem):
    with open(caminho_imagem, 'rb') as arquivo:
        base64_data = base64.b64encode(arquivo.read())
    return base64_data

# Caminho do arquivo da nova imagem que você deseja atualizar
caminho_nova_imagem = r'C:\Users\1rviviani\OneDrive - Frilog Transportes\Documentos\projetos\automação de cte\2.jpg'

# Ler a nova imagem e converter para base64
nova_imagem_base64 = ler_imagem_para_base64(caminho_nova_imagem)

try:
    # Conectar ao banco de dados
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()

    # Instrução SQL para atualizar a imagem
    sql_update = """
        UPDATE dbo.GTCMVEDG
        SET DsArquivo = ?,
            DsNomeArquivo = ?,
            DsTipoArquivo = ?,
            DsCaminhoArquivo = ?
        WHERE CdEmpresa = ? AND NrSeqControle = ? AND CdSequencia = ?
    """

    # Obter o nome do arquivo, o tipo do arquivo e o caminho do arquivo da nova imagem
    nome_nova_imagem = os.path.basename(caminho_nova_imagem)
    tipo_nova_imagem = os.path.splitext(caminho_nova_imagem)[1]
    caminho_nova_imagem = caminho_nova_imagem

    # Executar a instrução SQL de atualização com os valores adequados
    cursor.execute(sql_update, (pyodbc.Binary(nova_imagem_base64), nome_nova_imagem, tipo_nova_imagem, caminho_nova_imagem, cdempresa, nrseqcontrole, cdsequencia))
    conexao.commit()

    print("Atualização da imagem na tabela GTCMVEDG concluída com sucesso.")

except pyodbc.Error as erro:
    print("Ocorreu um erro ao acessar o banco de dados:", erro)

finally:
    if conexao:
        conexao.close()
