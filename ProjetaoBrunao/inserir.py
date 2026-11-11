# -*- coding: utf-8 -*-

from conexao import conectar

def main():
    """Lê os dados no console e grava um lançamento."""
    
    data = input("Data (aaaa-mm-dd): ")
    descricao = input("Descrição: ")
    valor = input("Valor (use ponto, ex.: 18.50): ")
    usuario_id = input("Id do usuário: ")
    categoria_id = input("Id da categoria: ")
    sql = ("INSERT INTO lancamento (data, descricao, valor, usuario_id, categoria_id) VALUES (%s, %s, %s, %s, %s)")

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(sql, (data, descricao, valor, usuario_id, categoria_id))
        conexao.commit()                 # obrigatório para gravar
        print("Lançamento gravado com id", cursor.lastrowid)

if __name__ == "__main__":
    main()