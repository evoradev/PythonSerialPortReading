import serial
import time

# Configuração da porta serial (simulando a COM5)
port = 'COM5'
baudrate = 9600
parity = 'N'  # N para None, E para Even, O para Odd
databits = 8
stopbits = 1

# Configurações do serial
ser = serial.Serial(
    port=port,
    baudrate=baudrate,
    parity=parity,
    bytesize=databits,
    stopbits=stopbits,
    timeout=1
)

# Dados simulados a serem enviados
data_to_send = [
    b'5,0kg  1,0kg TRM  3,0kg LIQC',
    b'5,0kg  1,0kg TRM  3,0kg LIQC',
    b'5,0kg  1,0kg TRM  3,0kg LIQC',
    b'5,0kg  1,0kg TRM  3,0kg LIQC'
]

try:
    while True:
        for data in data_to_send:
            ser.write(data + b'\n')  # Envia dados para a porta COM, adicionando uma nova linha
            time.sleep(1)  # Pausa de 1 segundo entre os envios

except KeyboardInterrupt:
    print("Interrompido pelo usuário")

finally:
    ser.close()
