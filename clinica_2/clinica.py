import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Criar a conexão com o banco de dados
conexao = sqlite3.connect("clinica.sqlite")
cursor = conexao.cursor()

# Criar tabelas no banco de dados
def criar_tabelas():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(100), 
        celular VARCHAR(100)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produto (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_produto VARCHAR(100), 
        valor REAL, 
        quantidade INTEGER
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consumo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        FOREIGN KEY(cliente_id) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
        FOREIGN KEY(produto_id) REFERENCES produto(id_produto) ON DELETE CASCADE
    );
    """)
    conexao.commit()

# Criar tabelas no banco de dados
criar_tabelas()

# Função para adicionar um novo cliente
def adicionar_cliente():
    nome = entry_nome_cliente.get()
    celular = entry_celular_cliente.get()

    if nome and celular:
        cursor.execute("INSERT INTO cliente (nome, celular) VALUES (?, ?)", (nome, celular))
        conexao.commit()
        entry_nome_cliente.delete(0, tk.END)
        entry_celular_cliente.delete(0, tk.END)
        atualizar_lista_clientes()
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos!")

# Função para adicionar um novo produto
def adicionar_produto():
    nome_produto = entry_nome_produto.get()
    valor = entry_valor_produto.get()
    quantidade = entry_quantidade_produto.get()

    if nome_produto and valor and quantidade:
        cursor.execute("INSERT INTO produto (nome_produto, valor, quantidade) VALUES (?, ?, ?)", 
                       (nome_produto, float(valor), int(quantidade)))
        conexao.commit()
        entry_nome_produto.delete(0, tk.END)
        entry_valor_produto.delete(0, tk.END)
        entry_quantidade_produto.delete(0, tk.END)
        atualizar_lista_produtos()
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos!")

# Função para atualizar a lista de clientes
def atualizar_lista_clientes():
    for row in tree_clientes.get_children():
        tree_clientes.delete(row)

    cursor.execute("SELECT * FROM cliente")
    for row in cursor.fetchall():
        tree_clientes.insert("", tk.END, values=row)

# Função para atualizar a lista de produtos
def atualizar_lista_produtos():
    for row in tree_produtos.get_children():
        tree_produtos.delete(row)

    cursor.execute("SELECT * FROM produto")
    for row in cursor.fetchall():
        tree_produtos.insert("", tk.END, values=row)

# Criar a interface gráfica
root = tk.Tk()
root.title("Gerenciamento de Clínica")
root.geometry("600x600")

# Frame para cadastrar clientes
frame_clientes = tk.LabelFrame(root, text="Cadastro de Cliente", padx=10, pady=10)
frame_clientes.pack(padx=10, pady=10, fill="both")

tk.Label(frame_clientes, text="Nome:").grid(row=0, column=0)
entry_nome_cliente = tk.Entry(frame_clientes)
entry_nome_cliente.grid(row=0, column=1)

tk.Label(frame_clientes, text="Celular:").grid(row=1, column=0)
entry_celular_cliente = tk.Entry(frame_clientes)
entry_celular_cliente.grid(row=1, column=1)

btn_add_cliente = tk.Button(frame_clientes, text="Adicionar Cliente", command=adicionar_cliente)
btn_add_cliente.grid(row=2, column=0, columnspan=2, pady=5)

# Frame para cadastrar produtos
frame_produtos = tk.LabelFrame(root, text="Cadastro de Produto", padx=10, pady=10)
frame_produtos.pack(padx=10, pady=10, fill="both")

tk.Label(frame_produtos, text="Nome do Produto:").grid(row=0, column=0)
entry_nome_produto = tk.Entry(frame_produtos)
entry_nome_produto.grid(row=0, column=1)

tk.Label(frame_produtos, text="Valor:").grid(row=1, column=0)
entry_valor_produto = tk.Entry(frame_produtos)
entry_valor_produto.grid(row=1, column=1)

tk.Label(frame_produtos, text="Quantidade:").grid(row=2, column=0)
entry_quantidade_produto = tk.Entry(frame_produtos)
entry_quantidade_produto.grid(row=2, column=1)

btn_add_produto = tk.Button(frame_produtos, text="Adicionar Produto", command=adicionar_produto)
btn_add_produto.grid(row=3, column=0, columnspan=2, pady=5)

# Frame para listar clientes
frame_lista_clientes = tk.LabelFrame(root, text="Lista de Clientes", padx=10, pady=10)
frame_lista_clientes.pack(padx=10, pady=10, fill="both")

tree_clientes = ttk.Treeview(frame_lista_clientes, columns=("ID", "Nome", "Celular"), show="headings")
tree_clientes.heading("ID", text="ID")
tree_clientes.heading("Nome", text="Nome")
tree_clientes.heading("Celular", text="Celular")
tree_clientes.pack(fill="both")

# Frame para listar produtos
frame_lista_produtos = tk.LabelFrame(root, text="Lista de Produtos", padx=10, pady=10)
frame_lista_produtos.pack(padx=10, pady=10, fill="both")

tree_produtos = ttk.Treeview(frame_lista_produtos, columns=("ID", "Nome", "Valor", "Quantidade"), show="headings")
tree_produtos.heading("ID", text="ID")
tree_produtos.heading("Nome", text="Nome")
tree_produtos.heading("Valor", text="Valor")
tree_produtos.heading("Quantidade", text="Quantidade")
tree_produtos.pack(fill="both")

# Atualizar as listas ao iniciar
atualizar_lista_clientes()
atualizar_lista_produtos()

# Iniciar a interface gráfica


# Frame para registrar consumo
frame_consumo = tk.LabelFrame(root, text="Registrar Consumo", padx=10, pady=10)
frame_consumo.pack(padx=10, pady=10, fill="both")

tk.Label(frame_consumo, text="Cliente:").grid(row=0, column=0)
cliente_combobox = ttk.Combobox(frame_consumo, state="readonly")
cliente_combobox.grid(row=0, column=1)

tk.Label(frame_consumo, text="Produto:").grid(row=1, column=0)
produto_combobox = ttk.Combobox(frame_consumo, state="readonly")
produto_combobox.grid(row=1, column=1)

tk.Label(frame_consumo, text="Quantidade:").grid(row=2, column=0)
entry_quantidade_consumo = tk.Entry(frame_consumo)
entry_quantidade_consumo.grid(row=2, column=1)

btn_add_consumo = tk.Button(frame_consumo, text="Registrar Consumo", command=lambda: adicionar_consumo())
btn_add_consumo.grid(row=3, column=0, columnspan=2, pady=5)


# Frame para listar consumo
frame_lista_consumo = tk.LabelFrame(root, text="Lista de Consumo", padx=10, pady=10)
frame_lista_consumo.pack(padx=10, pady=10, fill="both")

tree_consumo = ttk.Treeview(frame_lista_consumo, columns=("ID", "Cliente", "Produto", "Quantidade"), show="headings")
tree_consumo.heading("ID", text="ID")
tree_consumo.heading("Cliente", text="Cliente")
tree_consumo.heading("Produto", text="Produto")
tree_consumo.heading("Quantidade", text="Quantidade")
tree_consumo.pack(fill="both")


# Função para registrar consumo
def adicionar_consumo():
    cliente_nome = cliente_combobox.get()
    produto_nome = produto_combobox.get()
    quantidade = entry_quantidade_consumo.get()

    if cliente_nome and produto_nome and quantidade:
        # Obter IDs correspondentes
        cursor.execute("SELECT id_cliente FROM cliente WHERE nome = ?", (cliente_nome,))
        cliente_id = cursor.fetchone()
        cursor.execute("SELECT id_produto FROM produto WHERE nome_produto = ?", (produto_nome,))
        produto_id = cursor.fetchone()

        if cliente_id and produto_id:
            cursor.execute("INSERT INTO consumo (cliente_id, produto_id, quantidade) VALUES (?, ?, ?)",
                           (cliente_id[0], produto_id[0], int(quantidade)))
            conexao.commit()
            entry_quantidade_consumo.delete(0, tk.END)
            atualizar_lista_consumo()
            messagebox.showinfo("Sucesso", "Consumo registrado com sucesso!")
        else:
            messagebox.showerror("Erro", "Cliente ou Produto inválido!")
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos!")


# Função para atualizar a lista de consumo
def atualizar_lista_consumo():
    for row in tree_consumo.get_children():
        tree_consumo.delete(row)

    cursor.execute("""
        SELECT consumo.id, cliente.nome, produto.nome_produto, consumo.quantidade
        FROM consumo
        JOIN cliente ON consumo.cliente_id = cliente.id_cliente
        JOIN produto ON consumo.produto_id = produto.id_produto
    """)
    for row in cursor.fetchall():
        tree_consumo.insert("", tk.END, values=row)


def atualizar_lista_clientes():
    for row in tree_clientes.get_children():
        tree_clientes.delete(row)

    cursor.execute("SELECT * FROM cliente")
    clientes = cursor.fetchall()
    cliente_combobox["values"] = [c[1] for c in clientes]  # Atualiza combobox

    for row in clientes:
        tree_clientes.insert("", tk.END, values=row)

def atualizar_lista_produtos():
    for row in tree_produtos.get_children():
        tree_produtos.delete(row)

    cursor.execute("SELECT * FROM produto")
    produtos = cursor.fetchall()
    produto_combobox["values"] = [p[1] for p in produtos]  # Atualiza combobox

    for row in produtos:
        tree_produtos.insert("", tk.END, values=row)


atualizar_lista_consumo()
root.mainloop()
