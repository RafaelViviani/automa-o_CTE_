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

# Função para converter arquivo em base64
def arquivo_para_base64(caminho_arquivo):
    with open(caminho_arquivo, 'rb') as arquivo:
        base64_data = base64.b64encode(arquivo.read())
    return base64_data

# Conectar ao banco de dados
try:
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()

    # Consulta SQL para buscar os valores
    sql_consulta = """
        SELECT 
            a.CdEmpresa AS empresa,
            a.NrSeqControle AS nrcontrole,
            g.CdSequencia AS sequencia
        FROM GTCConhe AS a
        LEFT JOIN GTCNfCon AS d ON a.NrSeqControle = D.NrSeqControle AND a.CdEmpresa = d.CdEmpresa
        LEFT JOIN GTCNf AS b ON d.NrNotaFiscal = b.NrNotaFiscal AND d.CdInscricao = b.CdRemetente
        LEFT JOIN GTCMVEDG AS g ON a.CdEmpresa = g.CdEmpresa AND a.NrSeqControle = g.NrSeqControle
        WHERE b.NrChaveAcessoNFe = '52231131092300000171550010000015911291120237'
    """

    # Executar a consulta SQL
    cursor.execute(sql_consulta)
    resultado = cursor.fetchone()

    # Extrair os valores
    cdempresa = resultado.empresa
    nrseqcontrole = resultado.nrcontrole
    cdsequencia = resultado.sequencia

    # Caminho do arquivo da imagem que deseja inserir na tabela
    caminho_imagem = r'C:\Users\1rviviani\OneDrive - Frilog Transportes\Documentos\projetos\automação de cte\2.jpg'

    # Convertendo a imagem para base64
    imagem_base64 = arquivo_para_base64(caminho_imagem)

    # Instrução SQL de inserção da foto na tabela
    sql_insercao = """
        INSERT INTO dbo.GTCMVEDG (CdEmpresa, NrSeqControle, CdSequencia, DsArquivo, DsNomeArquivo, DsTipoArquivo, DsCaminhoArquivo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    # Obter o nome do arquivo, o tipo do arquivo e o caminho do arquivo
    nome_arquivo = os.path.basename(caminho_imagem)
    tipo_arquivo = os.path.splitext(caminho_imagem)[1]
    caminho_arquivo = caminho_imagem

    # Executar a instrução SQL de inserção com os valores adequados
    cursor.execute(sql_insercao, (cdempresa, nrseqcontrole, cdsequencia, pyodbc.Binary(imagem_base64), nome_arquivo, tipo_arquivo, caminho_arquivo))
    conexao.commit()

    print("Inserção de foto na tabela gtcmvedg concluída com sucesso.")

except pyodbc.Error as erro:
    print("Ocorreu um erro ao acessar o banco de dados:", erro)

finally:
    if conexao:
        conexao.close()
