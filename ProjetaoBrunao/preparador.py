#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Código que cria automaticamente um .venv e abre "teste_conexao.py".
    Feito por Davi Fialho Garcia
    5/11/2026

    O código verifica se existe um 'config.ini'.
    Se não exisitr, então ele cria um arquivo 'config.ini', pede para voce mudar com os dados do seu banco,
    e também cria um .venv já atualizando-o.

    Sempre que você rodar este código o arquivo irá abrir "teste_conexao.py", independentemente do 'config.ini'.
"""

if __name__ == "__main__":
    import subprocess
    import sys
    import os

    if os.name == "nt":  # Windows
        pip_executable = os.path.join(".venv", "Scripts", "pip.exe")
        python_executable = os.path.join(".venv", "Scripts", "python.exe")
    else:  # Linux / macOS
        pip_executable = os.path.join(".venv", "bin", "pip")
        python_executable = os.path.join(".venv", "bin", "python")


    try:
        arq = open("config.ini", "x")
        original = open("config.example.ini")
        for linha in original.read().split("\n"):
            arq.write(linha + "\n")

        arq.close()
        original.close()

        subprocess.run([sys.executable, "-m", "venv", "--system-site-packages", ".venv"])
        subprocess.run([pip_executable, "install", "mysql-connector-python", "certifi"])
        subprocess.run([pip_executable, "install", "--upgrade", "mysql-connector-python"])

        print("\n\n.venv criado com sucesso!")
        print("Mude os respectivos atributos de 'conexao.ini'")
        input("E depois, pressione ENTER para rodar o código.")

    except Exception as erro:
        print(erro)
        print("Config.ini já existe!")
        print("Para criar um .venv, apague 'config.ini'.")

    finally:
        print("-----CÓDIGO-----\n")
        subprocess.run([python_executable,"teste_conexao.py"])
