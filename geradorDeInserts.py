import pandas as pd 
import os 
import tkinter as tk 
from tkinter import filedialog, messagebox

# Função para formatar os valores corretamente para o SQL
def formatar_valor(valor):
    """Formata o valor para o comando SQL."""
    if pd.isna(valor):  # Tratar valores nulos como NULL
        return "NULL"
    elif isinstance(valor, str):  # Escapar strings
        valor_escapado = valor.replace("'", "''")
        return f"'{valor_escapado}'"
    else:  
        return str(valor)

# Função que será chamada ao clicar no botão de gerar os comandos
def gerar_comandos():
    nome_arquivo = arquivo_entry.get()  # Obter o caminho do arquivo
    tabela_mysql = tabela_entry.get()  # Obter o nome da tabela MySQL
    colunas_tabela = colunas_entry.get().split(',')  # Obter as colunas da tabela
    
    # Verificar se todos os campos foram preenchidos
    if not nome_arquivo or not tabela_mysql or not colunas_tabela[0]:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos do formulário.")
        return

    # Verificar se o arquivo existe
    if not os.path.exists(nome_arquivo):
        messagebox.showerror("Erro", f"O arquivo '{nome_arquivo}' não foi encontrado.")
        return

    try:

        df = pd.read_csv(nome_arquivo)

        # Gerar os comandos de INSERT
        comandos_insert = []
        for linha in df.itertuples(index=False, name=None):
            # Formatando os valores das colunas presentes no CSV
            valores = [formatar_valor(valor) for valor in linha]
            
            # Adicionar NULL para as colunas extras na tabela MySQL que não estão no CSV
            if len(valores) < len(colunas_tabela):
                valores += ["NULL"] * (len(colunas_tabela) - len(valores))

            # Gerar o comando INSERT para a linha
            comando = f"INSERT INTO {tabela_mysql} ({', '.join(colunas_tabela)}) VALUES ({', '.join(valores)});"
            comandos_insert.append(comando)

        # Salvar os comandos em um arquivo de texto
        nome_arquivo_saida = "comandos_insert.sql"
        with open(nome_arquivo_saida, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(comandos_insert))

        messagebox.showinfo("Sucesso", f"Comandos INSERT salvos no arquivo '{nome_arquivo_saida}'.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o arquivo CSV: {str(e)}")

# Função para abrir o diálogo de arquivo e selecionar o arquivo CSV
def selecionar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    arquivo_entry.delete(0, tk.END)  # Limpar campo de texto(para novos arquivos)
    arquivo_entry.insert(0, caminho_arquivo)  # Inserir o caminho do arquivo selecionado


root = tk.Tk()
root.title("Gerador de Comandos SQL INSERT")

# Layout da interface
tk.Label(root, text="Selecione o arquivo CSV:").grid(row=0, column=0, padx=10, pady=10)
arquivo_entry = tk.Entry(root, width=40)
arquivo_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Selecionar Arquivo", command=selecionar_arquivo).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Nome da Tabela MySQL:").grid(row=1, column=0, padx=10, pady=10)
tabela_entry = tk.Entry(root, width=40)
tabela_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Colunas da Tabela (separadas por vírgula):").grid(row=2, column=0, padx=10, pady=10)
colunas_entry = tk.Entry(root, width=40)
colunas_entry.grid(row=2, column=1, padx=10, pady=10)

# Botão para gerar os comandos
gerar_button = tk.Button(root, text="Gerar Comandos INSERT", command=gerar_comandos)
gerar_button.grid(row=3, column=0, columnspan=3, pady=20)

# Iniciar a interface
root.mainloop()
