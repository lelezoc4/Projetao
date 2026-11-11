# -*- coding: utf-8 -*-

import configparser
import certifi
import mysql.connector

def conectar():
    cfg = configparser.ConfigParser(interpolation=None)
    cfg.read("config.ini", encoding="utf-8")
    banco = cfg["banco"]
    parametros = {
        "host": banco["host"],
        "port": banco.getint("porta"),
        "user": banco["usuario"],
        "password": banco["senha"],
        "database": banco["nome"]
    }

    if banco.get("tls", "sim") == "sim":
        #conexão criptografada
        parametros["ssl_ca"] = certifi.where()
        parametros["ssl_verify_cert"] = True
        parametros["ssl_verify_identity"] = True
    else:
        #servidor local
        parametros["ssl_disabled"] = True
        

    return mysql.connector.connect(**parametros)
    