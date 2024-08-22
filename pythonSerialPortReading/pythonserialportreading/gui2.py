import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import serial

# Dicionário para armazenar processos de cada aba e dados recebidos
data_dict = {}

def run_serial_program(port, baudrate, parity, databits, stopbits, results_table):
    command = f'python main.py {port} {baudrate},{parity},{databits},{stopbits}'
    print(f"Comando: {command}")  # Debug: Exibe o comando gerado
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    data_dict[port] = []  # Inicializa a lista de dados para essa conexão

    threading.Thread(target=read_output, args=(process, results_table, port)).start()

def read_output(process, results_table, port):
    while True:
        line = process.stdout.readline()
        if not line:
            break
        try:
            line = line.decode('utf-8').strip()
            print(f"Saída do processo na porta {port}: {line}")  # Debug: Exibe a saída do processo
            results_table.insert("", "end", values=(line,))
            data_dict[port].append(line)  # Armazena o dado recebido
        except UnicodeDecodeError:
            print(f"Erro de decodificação para a porta {port}")

def start_connection():
    port = port_entry.get()
    baudrate = baudrate_entry.get()
    parity = parity_var.get()
    stopbits = stopbits_var.get()
    databits = databits_entry.get()

    if port and baudrate and databits:
        results_table = ttk.Treeview(frame, columns=(1), show="headings", height=10)
        results_table.heading(1, text="Dados Recebidos")
        results_table.pack(fill=tk.BOTH, expand=True)

        run_serial_program(port, baudrate, parity, databits, stopbits, results_table)
    else:
        print("Por favor, insira todos os dados necessários.")

# Configuração da janela principal
root = tk.Tk()
root.title("Configuração Serial")

# Frame para entrada de dados
input_frame = ttk.Frame(root, padding="10")
input_frame.pack(side=tk.TOP, fill=tk.X)

# Entrada da porta COM
ttk.Label(input_frame, text="Porta COM:").grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
port_entry = ttk.Entry(input_frame)
port_entry.grid(column=1, row=0, padx=5, pady=5, sticky=tk.EW)

# Entrada do Baudrate
ttk.Label(input_frame, text="Velocidade (baudrate):").grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
baudrate_entry = ttk.Entry(input_frame)
baudrate_entry.grid(column=1, row=1, padx=5, pady=5, sticky=tk.EW)

# Entrada da Paridade
ttk.Label(input_frame, text="Paridade:").grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)
parity_var = tk.StringVar(value="N")
parity_dropdown = ttk.Combobox(input_frame, textvariable=parity_var)
parity_dropdown['values'] = ["N", "E", "O"]
parity_dropdown.grid(column=1, row=2, padx=5, pady=5, sticky=tk.EW)

# Entrada dos Bits de Parada
ttk.Label(input_frame, text="Bit de parada:").grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)
stopbits_var = tk.StringVar(value="1")
stopbits_dropdown = ttk.Combobox(input_frame, textvariable=stopbits_var)
stopbits_dropdown['values'] = ["1", "1.5", "2"]
stopbits_dropdown.grid(column=1, row=3, padx=5, pady=5, sticky=tk.EW)

# Entrada dos Bits de Dados
ttk.Label(input_frame, text="Bits de Dados:").grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)
databits_entry = ttk.Entry(input_frame)
databits_entry.grid(column=1, row=4, padx=5, pady=5, sticky=tk.EW)

# Botão para iniciar conexão
start_button = ttk.Button(input_frame, text="Iniciar Conexão", command=start_connection)
start_button.grid(column=0, row=5, columnspan=2, pady=10)

# Frame para exibição dos dados
frame = ttk.Frame(root, padding="10")
frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

root.mainloop()
