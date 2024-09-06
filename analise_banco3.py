import pyodbc
import base64
import os

# Dados de acesso ao banco de dados
dados_conexao = ("Driver={SQL Server};"
                 "Server=192.168.100.242;"
                 "Database=softran_frilog;"
                 "UID=softran;"
                 "PWD=sof1209;")
conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()

print("Conexão bem sucedida!")

# Função para ler arquivo como binário
def arquivo_para_binario(caminho_arquivo):
    with open(caminho_arquivo, 'rb') as arquivo:
        dados_binarios = arquivo.read()
    return dados_binarios


# Caminho do arquivo da imagem que deseja inserir na tabela
caminho_imagem = r'C:\Users\1rviviani\OneDrive - Frilog Transportes\Documentos\projetos\automação de cte\2.jpg'

# Convertendo a imagem para binário
imagem_binaria = arquivo_para_binario(caminho_imagem)


# Instrução SQL para buscar os valores cdempresa, nrseqcontrole e cdsequencia
sql_busca_valores = """


SELECT a.CdEmpresa, a.NrSeqControle, MAX(m.CdSequencia) AS CdSequencia
FROM GTCConhe AS a
LEFT JOIN GTCNfCon AS d ON a.NrSeqControle = d.NrSeqControle AND a.CdEmpresa = d.CdEmpresa
LEFT JOIN GTCNf AS b ON d.NrNotaFiscal = b.NrNotaFiscal AND d.CdInscricao = b.CdRemetente
LEFT JOIN SISEMPRE AS ee ON a.CdEmpresa = ee.CdEmpresa
LEFT JOIN SISCli E ON a.CdRemetente = E.CdInscricao 
LEFT JOIN SISCli F ON a.CdDestinatario = F.CdInscricao 
LEFT JOIN SISCli I ON a.CdInscricao = I.CdInscricao 
LEFT JOIN SISCliFa H ON I.CdInscricao = H.CdInscricao
LEFT JOIN SISGrupo K ON H.CdGrupoCliente = K.CdGrupoCliente
LEFT JOIN GTCCONCE ON a.CdEmpresa = GTCCONCE.CdEmpresa AND a.NrSeqControle = GTCCONCE.NrSeqControle
LEFT JOIN gtcmoven m ON a.CdEmpresa = m.CdEmpresa AND a.NrSeqControle = m.NrSeqControle
WHERE GTCCONCE.CdChaveAcesso = '35240306979577000173570010008663561408257088'
GROUP BY a.CdEmpresa, a.NrSeqControle


"""

try:
    # Executar a consulta SQL para buscar os valores
    cursor.execute(sql_busca_valores)
    row = cursor.fetchone()

    # Verificar se os valores foram encontrados
    if row:
        cdempresa, nrseqcontrole, cdsequencia = row

        # Nome do arquivo, tipo de arquivo e caminho do arquivo
        nome_arquivo = os.path.basename(caminho_imagem)
        tipo_arquivo = os.path.splitext(caminho_imagem)[1]
        caminho_arquivo = caminho_imagem

        # Instrução SQL para inserir imagem na tabela GTCMVEDG com os valores obtidos
        sql_insercao = """
            INSERT INTO dbo.GTCMVEDG (CdEmpresa, NrSeqControle, CdSequencia, DsArquivo, DsNomeArquivo, DsTipoArquivo)
            VALUES (?, ?, ?, ?, ?, ?)
        """
    
        # Executar a instrução SQL de inserção com os valores adequados
        cursor.execute(sql_insercao, (cdempresa, nrseqcontrole, cdsequencia + 1,imagem_binaria, nome_arquivo, tipo_arquivo))
        conexao.commit()

        print("Inserção de foto na tabela gtcmvedg concluída com sucesso.")
    else:
        print("Não foi possível encontrar os valores necessários.")

except pyodbc.Error as erro:
    print("Ocorreu um erro ao acessar o banco de dados:", erro)

finally:
    if conexao:
        conexao.close()
