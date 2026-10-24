import sqlite3

class ClienteCashless:
    def __init__(self, id_cliente, nome, saldo):
        self.id_cliente = id_cliente
        self.nome = nome
        self.saldo = saldo
        self.status = 'Ativo'

    def debitar(self, valor):
        #conta bloqueada
        if self.status != ('Ativo'):
            print(f"[ERRO] Transação negada. Conta de {self.nome} está {self.status}.")
            return False

        #saldo insuficiente
        if self.saldo >= valor:
            self.saldo -= valor
            print(f"[SUCESSO] Débito: R${valor:,.2f} | Saldo atualizado: R${self.saldo:,.2f}")
            return True
        else:
            print(f"[RECUSADO] Saldo insuficiente para R${valor:,.2f}. Saldo atual: R${self.saldo:,.2f}")
            return False

def executar_motor_transacional():
    #banco de dados temporario
    conexao = sqlite3.connect(':memory:')
    cursor = conexao.cursor()

    #crud
    cursor.execute('''
        CREATE TABLE Contas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titular TEXT,
        saldo REAL,
        status TEXT
        )
    ''')
    cursor.execute("INSERT INTO Contas (titular, saldo, status) VALUES ('Vinicius Tomaz', 500.00, 'Ativo')")
    conexao.commit()

    #buscar dados (R)
    cursor.execute("SELECT id, titular, saldo FROM Contas WHERE id = 1")
    dados_db = cursor.fetchone()

    #instaciar objeto
    cliente = ClienteCashless(id_cliente=dados_db[0], nome=dados_db[1], saldo=dados_db[2])

    #processar fila
    fila_compras = [45, 120, 400, 30]

    print(f"\n--- Processando Lote para: {cliente.nome} ---")
    for compra in fila_compras:
        cliente.debitar(compra)

    #update (U)
    cursor.execute("UPDATE Contas SET saldo = ? WHERE id = ?", (cliente.saldo, cliente.id_cliente))
    conexao.commit()

    #mostrar atualizaçao
    print("\n--- Fechamento Final do Banco de Dados ---")
    cursor.execute("SELECT * FROM Contas")
    estado_final = cursor.fetchall()
    print(f"Registro no BD: {estado_final}")

    conexao.close()

if __name__ == "__main__":
    executar_motor_transacional()