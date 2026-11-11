# -*- coding: utf-8 -*-

from conexao import conectar

def preparar_senha(senha):
    """ devolve a (senha_hash, salt) para gravar no banco """
    return senha, ""

def listar():
    """ READ: devolve uma lista de tuplas 
    em ordem alfabética.
     ex.: (a, b, c) """

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, login FROM usuario ORDER BY nome")
        return cursor.fetchall()

def inserir(nome, login, senha):
    """ CREATE: grava um novo usuario """
    
    senha_hash, salt = preparar_senha(senha)
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO usuario (nome, login, senha_hash, selt) VALUES (%s, %s, %s, %s)", (nome, login, senha_hash, salt))
        conexao.commit()            

def atualizar(id_usuario, nome, login, senha):
    """ UPDATE: altera o nome, login e senha do usuario com esse id"""
    senha_hash, salt = preparar_senha(senha)
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("UPDATE usuario SET nome = %s, login = %s, senha_hash = %s, salt = %s WHERE id = %s", (nome, login, senha_hash, salt, id_usuario))
        conexao.commit()

def excluir(id_usuario):
    """ DELETE: apaga o usuario com esse id """
    
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM usuario WHERE id = %s", (id_usuario))
        conexao.commit()