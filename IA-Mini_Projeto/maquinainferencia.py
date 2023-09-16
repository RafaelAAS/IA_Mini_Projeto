from tkinter import *
import tkinter

restart = 0
quantidade_pergunta = 0
yes = 0

with open("rules.txt", "r", encoding="utf-8") as arquivo:
    regras = arquivo.readlines()
    novas_regras = set()
    pilha = []

def main():
    global janela, restart, texto_ajuda

    if restart != 0:
        janela_pergunta.destroy()
    else:
        restart += 1


    for linha in regras:
        if linha.startswith("Q"):
            partes = linha.split("SE ")
        if len(partes) == 2:
            palavra = partes[1].split("=")[0].strip()
            novas_regras.add(palavra)
        partes = linha.split("E ")
        if len(partes) > 1:
            for i in range(1, len(partes)):
                palavra = partes[i].split("=")[0].strip()
                novas_regras.add(palavra)

    janela = Tk()
    janela.title("Maquina de Inferência")
    janela.geometry("600x650")
    texto_orientacao = Label(
        janela, text="MENU", wraplength=380, font=("Arial", 12, "bold"))
    texto_orientacao.pack(pady=20)

    botao_comecar = Button(janela, text="COMEÇAR", command=iniciar)
    botao_comecar.pack(pady=20)

    botao_ajuda = Button(janela, text="COMO FUNCIONA", command=ajuda)
    botao_ajuda.pack(pady=20)

    botao_fechar = Button(janela, text="FECHAR", command=quit)
    botao_fechar.pack(pady=20)

    texto_ajuda = Label(janela, text="", wraplength=388,font=("Arial", 12, "bold"))
    texto_ajuda.pack(pady=20)

    janela.mainloop()


def iniciar():
    global indice, pergunta, janela_pergunta,quantidade_pergunta

    janela.destroy()
    janela_pergunta = Tk()
    janela_pergunta.title("Máquina de Inferência")
    janela_pergunta.geometry("600x650")
    pergunta = Label(janela_pergunta, text="", wraplength=380, font=("Arial", 12, "bold"))
    pergunta.pack(pady=20)

    botao_sim = Button(janela_pergunta, text="SIM", command=resposta_sim)
    botao_sim.pack(pady=20)

    botao_nao = Button(janela_pergunta, text="NÃO", command=resposta_nao)
    botao_nao.pack(pady=20)

    if quantidade_pergunta < len(novas_regras):
        palavra = list(novas_regras)[quantidade_pergunta]
        pergunta.config(text=palavra+" é verdadeiro?")
        quantidade_pergunta += 1


def ajuda():
    texto_ajuda["text"] = f'''
        Bem-vindo a Máquina de Inferência!\n
        Observação: Tenha 100% de certeza ao responder, caso necessário pesquise.\n
        Atenção: A base de dados desse projeto é pequena, possa ser que não encontre o seu problema.\n
        Feito por: Rafael Anacleto Alves de Souza
                   Aluno de Eng. da Computação'''


def resposta_sim():
    global quantidade_pergunta

    Sim = "s"

    if Sim == "s" and quantidade_pergunta < len(novas_regras):
        palavra = f"{list(novas_regras)[quantidade_pergunta-1]} = Sim"
        pilha.append(palavra)
    if quantidade_pergunta < len(novas_regras):
        palavra = list(novas_regras)[quantidade_pergunta]
        pergunta.config(text=palavra+" é verdadeiro?")
        quantidade_pergunta += 1
    else:
        conclusao()
def resposta_nao():
    global quantidade_pergunta
    
    if quantidade_pergunta < len(novas_regras):
        palavra = list(novas_regras)[quantidade_pergunta]
        pergunta.config(text=palavra+" é verdadeiro?")
        quantidade_pergunta += 1
    else:
        conclusao()

def conclusao():
    global yes

    total_regras = 1

    for linha in regras:
        yes = linha.count("Sim")
        
        if len(pilha) == yes:
            todas_palavras_presentes = all(palavra in linha for palavra in pilha)
            if todas_palavras_presentes:
                partes = linha.split("ENTÃO ")
                if len(partes) > 1:
                    palavra = partes[1].strip()
                    resposta(palavra)
                   
        if total_regras == len(regras):
            resposta("Não tenho conhecimento sobre!")
        yes = 0
        total_regras += 1
def resposta(palavra):
    global janela_resposta

    janela_resposta = Tk()
    janela_resposta.title("Resposta")
    janela_resposta.geometry("500x400")

    fonte = ("Wingdings", 36)

    label_simbolo = Label(janela_resposta,text="✓", font = fonte)
    label_simbolo.pack(pady=20)

    label_mensagem = Label(janela_resposta, text=palavra, font=("Arial", 12))
    label_mensagem.pack()
    
    botao_fechar = Button(janela_resposta, text="FECHAR", command=quit)
    botao_fechar.pack(pady=20)  

    botao_reiniciar = Button(janela_resposta, text="REINICIAR", command=reiniciar)
    botao_reiniciar.pack(pady=20)

    janela_resposta.mainloop()

def reiniciar():
    global quantidade_pergunta, pilha
    quantidade_pergunta = 0
    pilha.clear()
    janela_resposta.destroy()
    main()

main()
