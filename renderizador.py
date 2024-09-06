import pyodbc
import base64
from PIL import Image
import io

# Dados de acesso ao banco de dados
dados_conexao = ("Driver={SQL Server};"
                 "Server=192.168.100.242;"
                 "Database=softran_frilog;"
                 "UID=softran;"
                 "PWD=sof1209;")

try:
    # Conectar ao banco de dados
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()

    # Consulta SQL para obter a imagem
    sql_select_imagem = """
    SELECT DsArquivo FROM GTCMVEDG
    WHERE CdEmpresa = 112 AND NrSeqControle = 532729 AND CdSequencia = 1
    """

    # Executar a consulta SQL para obter a imagem
    cursor.execute(sql_select_imagem)
    # Check for empty result
    row = cursor.fetchone()
    if row:
        # Get image data
        image_data = row[0]

        # Open image
        image = Image.open(io.BytesIO(image_data))

        # Describe what it's doing
        print("Image retrieved successfully")

        image.show()

    # Close connection is handled by context manager

except Exception as e:
    print("Error:", e)
