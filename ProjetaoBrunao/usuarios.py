# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import mysql.connector
import repositorio_usuario as repo

class Aplicacao:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("usuarios.glade")
        self.janela = builder.get_object("janela")
        self.ent_nome = builder.get_object("ent_nome")
        self.ent_login = builder.get_object("ent_login")
        self.ent_senha = builder.get_object("ent_senha")
        self.btn_gravar = builder.get_object("btn_gravar")
        self.btn_gravar.connect("clicked", self.ao_gravar)
        self.btn_editar = builder.get_object("btn_editar")
        self.btn_excluir = builder.get_object("btn_excluir")
        self.btn_excluir.connect("clicked", self.ao_excluir)
        self.btn_editar.connect("clicked", self.ao_editar)
        self.lbl_mensagem = builder.get_object("lbl_mensagem")
        self.tvw_usuarios = builder.get_object("tvw_usuarios")
        self.lst_usuarios = builder.get_object("lst_usuarios")
        self.selecao = self.tvw_usuarios.get_selection()
        self.selecao.connect("changed", self.ao_mudar_selecao)
        self.id_em_edicao = None
        self.janela.connect("destroy", Gtk.main_quit)
        self.carregar_tabela()
        self.janela.show_all()

    def mostrar_mensagem(self, texto):
        self.lbl_mensagem.set_text(texto)

    def carregar_tabela(self):
        self.lst_usuarios.clear()
        try:
            for id_usuario, nome, login in repo.listar():
                self.lst_usuarios.append([id_usuario, nome, login])
        except mysql.connector.Error as erro:
            self.mostrar_mensagem(f"Erro ao acessar o banco: {erro.msg}")

    def limpar_formulario(self):
        self.ent_nome.set_text("")
        self.ent_login.set_text("")
        self.ent_senha.set_text("")
        self.id_em_edicao = None
        self.btn_gravar.set_label("Gravar")

    def ao_gravar(self, componente=None, dados=None):
        nome = self.ent_nome.get_text().strip()
        login = self.ent_login.get_text().strip()
        senha = self.ent_senha.get_text()
        if not nome or not login or not senha:
            self.mostrar_mensagem("Preencha nome, login e senha")
            return
        try:
            if self.id_em_edicao is None:
                repo.inserir(nome, login, senha)
                self.mostrar_mensagem(f"Usuário \"{login}\" gravado.")
            else:
                repo.atualizar(self.id_em_edicao, nome, login, senha)
                self.mostrar_mensagem(f"Usuário \"{login}\" alterado.")
        
        except mysql.connector.Error as erro:
            if erro.errno == 1062:
                self.mostrar_mensagem(f"O login \"{login}\" já está em uso.")
            else:
                self.mostrar_mensagem(f"Erro ao gravar: {erro.msg}")
            return
        self.limpar_formulario
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
        id_usuario, nome, login = linha
        self.ent_nome.set_text(nome)
        self.ent_login.set_text(login)
        self.ent_senha.set_text("")
        self.id_em_edicao = id_usuario
        self.btn_gravar.set_label("Salvar alteração")
        self.mostrar_mensagem(f"Editando \"{login}\". Digite a senha e clique em Salvar alteração.")

    def ao_excluir(self, componente=None, dados=None):
        linha = self.linha_selecionada()
        if linha is None:
            return
        id_usuario, nome, login = linha
        dialogo = Gtk.MessageDialog(
            transient_for=self.janela,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f"Excluir o usuário \"{login}\" ({nome})?",
        )
        resposta = dialogo.run()
        dialogo.destroy()
        if resposta != Gtk.ResponseType.YES:
            return
        try:
            repo.excluir(id_usuario)
            self.mostrar_mensagem(f"Usuário \"{login}\" excluído.")
        except mysql.connector.Error as erro:
            if erro.errno == 1451:          # a chave estrangeira impediu
                self.mostrar_mensagem(f"\"{login}\" não pode ser excluído!Existem lançamentos registrados no usuário.")
            else:
                self.mostrar_mensagem(f"Erro ao excluir: {erro.msg}")
            return
        self.limpar_formulario()
        self.carregar_tabela()

if __name__ == "__main__":
    Aplicacao()
    Gtk.main()