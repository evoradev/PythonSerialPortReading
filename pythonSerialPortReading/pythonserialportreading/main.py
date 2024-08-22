import serial
import time
import sys
import os
import tempfile

def setup_serial(port, baudrate, parity, databits, stopbits, timeout=1):
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            bytesize=databits,
            stopbits=stopbits,
            timeout=timeout
        )
        return ser
    except serial.SerialException as e:
        print(f"Erro ao abrir a porta {port}: {e}")
        sys.exit(1)

def read_from_serial(serial_port):
    try:
        data = serial_port.read(serial_port.in_waiting or 1)  # Lê todos os bytes disponíveis ou pelo menos 1
        return data
    except serial.SerialException as e:
        print(f"Erro de leitura da porta {serial_port.portstr}: {e}")
        return None

def decode_data(data):
    try:
        return data.decode('utf-8').rstrip()
    except UnicodeDecodeError:
        try:
            return data.decode('latin-1').rstrip()  # Tenta outra codificação como fallback
        except UnicodeDecodeError:
            print("Erro de decodificação")
            return None

def save_data_to_file(data, file_path):
    try:
        with open(file_path, 'a') as file:
            file.write(data + '\n')
    except IOError as e:
        print(f"Erro ao salvar os dados no arquivo {file_path}: {e}")

def send_data_to_stdout(data):
    try:
        print(data)  # Envia os dados para stdout
        sys.stdout.flush()  # Garante que os dados sejam enviados imediatamente
    except IOError as e:
        print(f"Erro ao enviar dados para stdout: {e}")

def main():
    if len(sys.argv) != 3:
        print("Uso: python main.py <porta_com> <velocidade>")
        sys.exit(1)

    port = sys.argv[1]
    baudrate_settings = sys.argv[2]

    baudrate, parity, databits, stopbits = baudrate_settings.split(',')
    baudrate = int(baudrate)
    
    # Mapeamento dos parâmetros
    parity = {
        'N': serial.PARITY_NONE,
        'E': serial.PARITY_EVEN,
        'O': serial.PARITY_ODD
    }.get(parity, serial.PARITY_NONE)  # Default para nenhuma paridade

    databits = {
        '8': serial.EIGHTBITS,
        '7': serial.SEVENBITS,
        '6': serial.SIXBITS,
        '5': serial.FIVEBITS
    }.get(databits, serial.EIGHTBITS)  # Default para 8 bits de dados

    stopbits = {
        '1': serial.STOPBITS_ONE,
        '1.5': serial.STOPBITS_ONE_POINT_FIVE,
        '2': serial.STOPBITS_TWO
    }.get(stopbits, serial.STOPBITS_ONE)  # Default para 1 bit de parada

    timeout = 1  # Pode ajustar conforme necessário

    # Diretório TEMP do Windows
    temp_dir = tempfile.gettempdir()
    # Caminho para a pasta SerialWeight dentro do diretório TEMP
    serial_weight_dir = os.path.join(temp_dir, "SerialWeight")

    # Cria a pasta SerialWeight se ela não existir
    if not os.path.exists(serial_weight_dir):
        os.makedirs(serial_weight_dir)

    # Caminho para o arquivo de saída
    file_path = os.path.join(serial_weight_dir, "outputs.txt")
    print(f"Arquivo de saída: {file_path}")

    # Configurar a porta serial
    ser = setup_serial(port, baudrate, parity, databits, stopbits, timeout)

    try:
        while True:
            data = read_from_serial(ser)
            if data:
                decoded_data = decode_data(data)
                if decoded_data:
                    print(f"Dados recebidos: {decoded_data}")
                    save_data_to_file(decoded_data, file_path)  # Salva no arquivo
                    send_data_to_stdout(decoded_data)  # Envia os dados para a GUI via stdout

            time.sleep(1)

    except KeyboardInterrupt:
        print("Interrompido pelo usuário")

    finally:
        ser.close()

if __name__ == "__main__":
    main()
