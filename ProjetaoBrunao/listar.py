# -*- coding: utf-8 -*-

from conexao import conectar

def main():
    """ Busca os lançamentos e imprime um por linha. """
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, data, descricao, valor, usuario_id, categoria_id FROM lancamento ORDER BY data")
        linhas = cursor.fetchall()
    print(f"{len(linhas)} lançamentos encontrados\n")

    """formatando os campos"""
    for id_, data, descricao, valor, usuario_id, categoria_id in linhas:
        print(f"id {id_:<6} {data:%d/%m/%Y}  {descricao:<24} R$ {valor:>8}"
              f"   usuário {usuario_id}   categoria {categoria_id}")

if __name__ == "__main__":
   main()