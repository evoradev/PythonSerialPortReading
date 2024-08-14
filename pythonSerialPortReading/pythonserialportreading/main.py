import serial
import time
import sys

def setup_serial(port, baudrate, timeout=1):
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        return ser
    except serial.SerialException as e:
        print(f"Erro ao abrir a porta {port}: {e}")
        sys.exit(1)

def read_from_serial(serial_port):
    try:
        data = serial_port.readline().decode('utf-8').rstrip()
        return data
    except serial.SerialException as e:
        print(f"Erro de leitura da porta {serial_port.portstr}: {e}")
        return None

def save_data_to_file(data, file_path):
    try:
        with open(file_path, 'a') as file:
            file.write(data + '\n')
    except IOError as e:
        print(f"Erro ao salvar os dados no arquivo {file_path}: {e}")

def main():
    if len(sys.argv) != 4:
        print("Uso: python main.py <porta_com> <velocidade> <arquivo_saida>")
        sys.exit(1)

    port = sys.argv[1]
    baudrate_settings = sys.argv[2]
    file_path = sys.argv[3]

    baudrate, parity, databits, stopbits = baudrate_settings.split(',')
    baudrate = int(baudrate)
    timeout = 1  # Pode ajustar conforme necessário

    # Configurar a porta serial
    ser = setup_serial(port, baudrate, timeout)

    try:
        while True:
            data = read_from_serial(ser)
            if data:
                print(f"Dados recebidos: {data}")
                save_data_to_file(data, file_path)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Interrompido pelo usuário")

    finally:
        ser.close()

if __name__ == "__main__":
    main()
