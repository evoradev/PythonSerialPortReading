import serial
import time

# Configuração da porta serial (simulando a COM5)
ser = serial.Serial('COM5', baudrate=9600, timeout=1)

# Caminho completo para o arquivo onde os dados serão salvos
output_file_path = r'C:\temp\output.txt'

# Dados simulados a serem enviados
data_to_send = [
    b'\x02    5,0kg     1,0kg TRM\x0F\x0F    3,0kg LIQC\x0E',
    b'\x02    5,0kg     1,0kg TRM\x0F\x0F    3,0kg LIQC\x0E',
    b'\x02    5,0kg     1,0kg TRM\x0F\x0F    3,0kg LIQC\x0E',
    b'\x02    5,0kg     1,0kg TRM\x0F\x0F    3,0kg LIQC\x0E'
]

# Função para salvar os dados no arquivo
def save_data_to_file(data, file_path):
    try:
        with open(file_path, 'a') as file:
            file.write(data + '\n')
    except IOError as e:
        print(f"Erro ao salvar os dados no arquivo {file_path}: {e}")

try:
    while True:
        for data in data_to_send:
            ser.write(data + b'\n')  # Envia dados para a porta COM, adicionando uma nova linha
            time.sleep(1)  # Pausa de 1 segundo entre os envios
            
            # Salva os dados no arquivo
            save_data_to_file(data.decode('utf-8'), output_file_path)

except KeyboardInterrupt:
    print("Interrompido pelo usuário")

finally:
    ser.close()
