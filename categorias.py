#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Cadastro de categorias (CRUD) do projeto Finanças da Família."""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import mysql.connector
import repositorio_categoria as repo

TIPOS = {"R": "Receita", "D": "Despesa"}

class Aplicacao:

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("categorias.glade")
        # Widgets que o código vai usar (os ids são os do Glade)
        self.janela = builder.get_object("janela")
        self.ent_nome = builder.get_object("ent_nome")
        self.cmb_tipo = builder.get_object("cmb_tipo")
        self.btn_gravar = builder.get_object("btn_gravar")
        self.btn_editar = builder.get_object("btn_editar")
        self.btn_excluir = builder.get_object("btn_excluir")
        self.lbl_mensagem = builder.get_object("lbl_mensagem")
        self.tvw_categorias = builder.get_object("tvw_categorias")
        self.lst_categorias = builder.get_object("lst_categorias")
        self.selecao = self.tvw_categorias.get_selection()

        self.btn_gravar.connect("clicked", self.ao_gravar)
        self.selecao.connect("changed", self.ao_mudar_selecao)
        self.btn_editar.connect("clicked", self.ao_editar)

        # None = modo "nova categoria"; um número = id da categoria em edição
        self.id_em_edicao = None

        # Ligação dos sinais aos métodos (as próximas etapas acrescentam linhas aqui)
        self.janela.connect("destroy", Gtk.main_quit)
        self.carregar_tabela()
        self.janela.show_all()

    def mostrar_mensagem(self, texto):
        self.lbl_mensagem.set_text(texto)

    def carregar_tabela(self):
        """READ: busca as categorias no banco e preenche a tabela da tela."""
        self.lst_categorias.clear()

        try:
            for id_categoria, nome, tipo in repo.listar():
                self.lst_categorias.append([id_categoria, nome, TIPOS[tipo]])

        except mysql.connector.Error as erro:
            self.mostrar_mensagem(f"Erro ao acessar o banco: {erro.msg}")

    def limpar_formulario(self):
        self.ent_nome.set_text("")
        self.cmb_tipo.set_active_id("D")
        self.id_em_edicao = None
        self.btn_gravar.set_label("Gravar")

    def ao_gravar(self, componente=None, dados=None):
        """CREATE ou UPDATE: grava uma categoria nova ou a que está em edição."""
        nome = self.ent_nome.get_text().strip()
        tipo = self.cmb_tipo.get_active_id()
        if not nome:
            self.mostrar_mensagem("Informe o nome da categoria.")
            return
        try:
            if self.id_em_edicao is None:
                repo.inserir(nome, tipo)
                self.mostrar_mensagem(f"Categoria \"{nome}\" gravada.")
            else:
                repo.atualizar(self.id_em_edicao, nome, tipo)
                self.mostrar_mensagem(f"Categoria \"{nome}\" alterada.")

        except mysql.connector.Error as erro:
            if erro.errno == 1062:          
                self.mostrar_mensagem(f"Já existe uma categoria chamada \"{nome}\".")
            else:
                self.mostrar_mensagem(f"Erro ao gravar: {erro.msg}")
            return
        self.limpar_formulario()
        self.carregar_tabela()

    def linha_selecionada(self):
        modelo, posicao = self.selecao.get_selected()
        if posicao is None:
            return None
        return modelo[posicao][0], modelo[posicao][1], modelo[posicao][2]

    def ao_mudar_selecao(self, componente=None, dados=None):
       tem_selecao = self.linha_selecionada() is not None
       self.btn_editar.set_sensitive(tem_selecao)
       self.btn_excluir.set_sensitive(tem_selecao)

    def ao_editar(self, componente=None, dados=None):
        linha = self.linha_selecionada()
        if linha is None:
            return
        id_categoria, nome, tipo_texto = linha
        self.ent_nome.set_text(nome)
        self.cmb_tipo.set_active_id("R" if tipo_texto == "Receita" else "D")
        self.id_em_edicao = id_categoria
        self.btn_gravar.set_label("Salvar alteração")
        self.mostrar_mensagem(f"Editando \"{nome}\". Altere e clique em Salvar alteração.")

    def ao_excluir(self, componente=None, dados=None):

        linha = self.linha_selecionada()
        if linha is None:
            return
        id_categoria, nome, _ = linha
        dialogo = Gtk.MessageDialog(
            transient_for=self.janela,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f"Excluir a categoria \"{nome}\"?",
        )

        resposta = dialogo.run()
        dialogo.destroy()
        if resposta != Gtk.ResponseType.YES:
            return
        try:
            repo.excluir(id_categoria)
            self.mostrar_mensagem(f"Categoria \"{nome}\" excluída.")
        except mysql.connector.Error as erro:
            if erro.errno == 1451:        
                self.mostrar_mensagem(f"\"{nome}\" não pode ser excluída: existem lançamentos nesta categoria.")
            else:
                self.mostrar_mensagem(f"Erro ao excluir: {erro.msg}")
                return
        self.limpar_formulario()
        self.carregar_tabela()

if __name__ == "__main__":

    Aplicacao()
    Gtk.main()