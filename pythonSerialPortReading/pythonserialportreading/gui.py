import tkinter as tk
from tkinter import ttk
import subprocess
import threading

# Dicionário para armazenar processos de cada aba e dados recebidos
process_dict = {}
data_dict = {}  # Armazena os dados recebidos de cada conexão
# Contador global para as conexões
connection_counter = 1

def run_serial_program(tab, port_entry, baudrate_entry, parity_var, stopbits_var, databits_entry):
    global connection_counter

    port = port_entry.get()
    baudrate = baudrate_entry.get()
    parity = parity_var.get()
    stopbits = stopbits_var.get()
    databits = databits_entry.get()

    if port and baudrate and databits:
        command = f'python main.py COM{port} {baudrate},{parity},{databits},{stopbits}'
        print(f"Comando: {command}")  # Debug: Exibe o comando gerado
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        process_dict[port] = process
        data_dict[port] = []  # Inicializa a lista de dados para essa conexão

        tab_name = f"Conexão {connection_counter}"
        tab_control_conexoes.tab(tab, text=tab_name)
        tab_control_conexoes.select(tab)

        connection_counter += 1

        threading.Thread(target=read_output, args=(process, port)).start()
        update_initial_tab()  # Atualiza a aba inicial com a nova conexão
    else:
        print("Por favor, insira todos os dados necessários.")

def read_output(process, port):
    while True:
        line = process.stdout.readline()
        if not line:
            break
        try:
            line = line.decode('utf-8').strip()
            print(f"Saída do processo na porta COM{port}: {line}")  # Debug: Exibe a saída do processo
            data_dict[port].append(line)  # Armazena o dado recebido
            update_initial_tab()  # Atualiza a aba inicial com os novos dados
        except UnicodeDecodeError:
            print(f"Erro de decodificação para a porta COM{port}")

def stop_program(port):
    """Para o processo associado à porta, mas não remove a aba."""
    process = process_dict.get(port, None)
    if process:
        process.terminate()
        print(f"Processo na porta COM{port} foi interrompido.")

def remove_tab(tab, port):
    """Para o processo e remove a aba."""
    stop_program(port)
    tab_control_conexoes.forget(tab)
    data_dict.pop(port, None)  # Remove os dados da conexão
    update_initial_tab()  # Atualiza a aba inicial para refletir a remoção

def create_new_connection():
    tab = ttk.Frame(tab_control_conexoes)
    tab.grid_rowconfigure(5, weight=1)
    tab.grid_columnconfigure(1, weight=1)

    ttk.Label(tab, text="Porta COM:").grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
    port_entry = ttk.Entry(tab)
    port_entry.grid(column=1, row=0, padx=10, pady=10, sticky=tk.EW)

    ttk.Label(tab, text="Velocidade (baudrate):").grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
    baudrate_entry = ttk.Entry(tab)
    baudrate_entry.grid(column=1, row=1, padx=10, pady=10, sticky=tk.EW)

    ttk.Label(tab, text="Paridade:").grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
    parity_var = tk.StringVar(value="N")
    parity_dropdown = ttk.Combobox(tab, textvariable=parity_var)
    parity_dropdown['values'] = ["N", "E", "O"]
    parity_dropdown.grid(column=1, row=2, padx=10, pady=10, sticky=tk.EW)

    ttk.Label(tab, text="Bit de parada:").grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)
    stopbits_var = tk.StringVar(value="1")
    stopbits_dropdown = ttk.Combobox(tab, textvariable=stopbits_var)
    stopbits_dropdown['values'] = ["1", "1.5", "2"]
    stopbits_dropdown.grid(column=1, row=3, padx=10, pady=10, sticky=tk.EW)

    ttk.Label(tab, text="Bits de Dados:").grid(column=0, row=4, padx=10, pady=10, sticky=tk.W)
    databits_entry = ttk.Entry(tab)
    databits_entry.grid(column=1, row=4, padx=10, pady=10, sticky=tk.EW)

    run_button = ttk.Button(tab, text="Executar", command=lambda: run_serial_program(tab, port_entry, baudrate_entry, parity_var, stopbits_var, databits_entry))
    run_button.grid(column=0, row=5, columnspan=2, pady=10)

    stop_button = ttk.Button(tab, text="Parar", command=lambda: stop_program(port_entry.get()))
    stop_button.grid(column=0, row=6, columnspan=2, pady=10)

    remove_button = ttk.Button(tab, text="Remover Aba", command=lambda: remove_tab(tab, port_entry.get()))
    remove_button.grid(column=0, row=7, columnspan=2, pady=10)

    tab_control_conexoes.add(tab, text=f"Conexão {connection_counter}", sticky="nsew")
    tab_control_conexoes.select(tab)

def update_initial_tab():
    """Atualiza a aba inicial com os dados de todas as conexões."""
    for widget in initial_tab.winfo_children():
        widget.destroy()  # Limpa todos os widgets da aba inicial

    row, col = 0, 0
    max_cols = 2  # Definindo o número máximo de colunas

    for port, data_list in data_dict.items():
        if data_list:
            frame = ttk.LabelFrame(initial_tab, text=f"Conexão COM{port}", padding=(10, 5), borderwidth=2, relief="solid")
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            results_table = ttk.Treeview(frame, columns=(1), show="headings", height=5)
            results_table.heading(1, text="Dados Recebidos")
            results_table.pack(fill=tk.BOTH, expand=True)

            for line in data_list:
                results_table.insert("", "end", values=(line,))

            # Controla o layout em grade
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

def create_initial_tab():
    """Cria a aba inicial com espaço para dados de cada conexão."""
    global initial_tab

    initial_tab = ttk.Frame(tab_control_conexoes)
    initial_tab.grid_rowconfigure(0, weight=1)
    initial_tab.grid_columnconfigure(0, weight=1)

    tab_control_conexoes.add(initial_tab, text="Visão Geral")
    tab_control_conexoes.select(initial_tab)

def close_all_connections():
    """Encerra todas as conexões antes de fechar a aplicação."""
    for port in list(process_dict.keys()):
        stop_program(port)
    root.quit()

# Configuração da janela principal
root = tk.Tk()
root.title("Configuração Serial")

root.geometry("600x400")
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use('clam')

main_frame = ttk.Frame(root)
main_frame.pack(expand=1, fill='both')

tab_control_conexoes = ttk.Notebook(main_frame)
tab_control_conexoes.pack(side=tk.LEFT, expand=1, fill='both')

side_frame = ttk.Frame(main_frame)
side_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

new_connection_button = ttk.Button(side_frame, text="Nova Conexão", command=create_new_connection)
new_connection_button.pack(pady=(0, 10))

stop_button = ttk.Button(side_frame, text="Encerrar", command=close_all_connections)
stop_button.pack()

create_initial_tab()  # Cria a aba inicial ao iniciar o programa

root.mainloop()
