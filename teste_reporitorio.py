# -*- coding: utf-8 -*-

import repositorio_categoria as repo
print("Antes:", repo.listar())
repo.inserir("Farmácia", "D")
print("Depois de inserir:", repo.listar())
id_farmacia = [c[0] for c in repo.listar() if c[1] == "Farmácia"][0]
repo.atualizar(id_farmacia, "Farmácia e saúde", "D")
print("Depois de atualizar:", repo.listar())
repo.excluir(id_farmacia)
print("Depois de excluir:", repo.listar())