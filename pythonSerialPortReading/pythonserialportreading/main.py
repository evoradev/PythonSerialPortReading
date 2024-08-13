import serial
import time

# Configurar as conexões seriais para cada balança
ser1 = serial.Serial('COM3', baudrate=5800, timeout=1)
ser2 = serial.Serial('COM4', baudrate=4800, timeout=1)
ser3 = serial.Serial('COM5', baudrate=9600, timeout=1)

def read_from_serial(serial_port):
    try:
        # Leia uma linha de dados da porta serial
        data = serial_port.readline().decode('utf-8').rstrip()
        return data
    except serial.SerialException as e:
        print(f"Erro de leitura da porta {serial_port.portstr}: {e}")
        return None

try:
    while True:
        # Leia dados de cada balança
        data1 = read_from_serial(ser1)
        data2 = read_from_serial(ser2)
        data3 = read_from_serial(ser3)
        
        if data1:
            print(f"Dados recebidos da balança 1 (5800 baud): {data1}")
        if data2:
            print(f"Dados recebidos da balança 2 (4800 baud): {data2}")
        if data3:
            print(f"Dados recebidos da balança 3 (9600 baud): {data3}")
        
        # Aguarde um breve momento antes de ler novamente
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrompido pelo usuário")

finally:
    # Fechar as conexões seriais
    ser1.close()
    ser2.close()
    ser3.close()
