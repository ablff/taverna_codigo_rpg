import random
import sqlite3

def inicio():
    print("=== Bem-vindo à Taverna do Código! ===")
    print("\nVocê está cansado de viajar, rezando por uma pousada ou uma taverna, enquanto seus pés gritam de dor...")
    print("Mas parece que temos alguém com sorte, ao longe você avista uma simples e singela taverna.")
    print("Mais rápido do que imediatamente, você ruma em direção a ela.\n")
    
    print("Assim que você abre a porta, você vê um salão vazio e atrás do balcão, um meio orc grande e forte.")
    print("Antes que você pudesse dizer algo, ele te olha e te chama com a mão, para o balcão.")
    print("Venha, sente-se perto do balcão!")
    print("O Taverneiro então se aproxima e pergunta:")
    nome_jogador = input("Olá aventureiro, qual é seu nome? ")
    
    print(f"\nMuito prazer {nome_jogador}! Me chamo Brog Magog!\n")
    print("Então ele pergunta..")
    classe = input("Costuma trabalhar com o que? (qual sua classe): ")
    
    print(f"\n{classe}! Olha só, realmente combina com você!")
    print("Vejo que está cansado, se comprar uma refeição completa o quarto sai pela metade do preço.")
    print("O quarto sairia de 1 moeda de prata, para 5 de cobre. A refeição completa é 5 moedas de cobre.")
    promocao = input("Vai querer a refeição? s/n: ")
    
    if promocao.lower() == "s":
        print("Perfeito, irei pedir para começar a preparar a refeição e o quarto!")
        print("Ele sai por um momento e retorna depois de uns dois minutos.")
        print(f"Estão preparando o quarto e a refeição para você, {nome_jogador}.")
    else:
        print("Bom, aparentemente você tem a inteligência tímida.")
        quarto = input("Vai querer o quarto? s/n: ")
        if quarto.lower() == "s":
            print("Bom, irei pedir para que arrumem o quarto para você.")
            print("Ele volta depois de um momento e fala:")
            print("Estão arrumando o seu quarto.")
        else:
            print("Então não posso te ajudar com nada, peço que saia da taverna e pare de tomar meu tempo!")
            print("Passar bem!")
            exit()  
            
    casa = input("\nEnquanto a gente espera, me fala de onde você é?: ")
    print(f"\n{casa}? Não conheço muito bem.")
    longe = input("Fica longe daqui? s/n: ")
    
    if longe.lower() == "s":
        print("Ah, é por isso que eu não conheço.")
    elif longe.lower() == "n":
        print("Que estranho eu não conhecer, moro por aqui há muito tempo.")
    else:
        print("Não entendi o que você disse...")

    input(f"\nMas me fala, o que um {classe} de {casa} está fazendo por essas bandas? ")
    return nome_jogador, classe

def banco():
    conexao = sqlite3.connect("banco_rpg.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS herois (
            nome TEXT PRIMARY KEY,
            classe TEXT,
            nivel INTEGER,
            ouro INTEGER,
            forca INTEGER,
            vida INTEGER,
            mana INTEGER,
            mochila TEXT
        )
    ''')
    conexao.commit()
    conexao.close()

def save_jogo(nome, classe, nivel, ouro, forca, vida, mana, mochila):
    conexao = sqlite3.connect("banco_rpg.db")
    cursor = conexao.cursor()
    mochila_texto = ",".join(mochila)
    cursor.execute('''
        INSERT OR REPLACE INTO herois (nome, classe, nivel, ouro, forca, vida, mana, mochila)
        VALUES (?,?,?,?,?,?,?,?)
    ''', (nome, classe, nivel, ouro, forca, vida, mana, mochila_texto))
    conexao.commit()
    conexao.close()
    print("\nJogo e inventário salvos com sucesso!")

def load():
    conexao = sqlite3.connect("banco_rpg.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, classe, nivel FROM herois")
    todos_herois = cursor.fetchall()

    if len(todos_herois) == 0:
        conexao.close()
        return None

    print("\n" + "="*30)
    print("SAVES ENCONTRADOS")
    print("="*30)

    for heroi in todos_herois:
        print(f"- {heroi[0]} (Nivel {heroi[2]} {heroi[1]})")

    nome_escolhido = input("\n Digite o nome do herói para carregar (ou aperte ENTER para Novo Jogo): ")
    if nome_escolhido == "":
        conexao.close()
        return None

    cursor.execute("SELECT * FROM herois WHERE nome = ?", (nome_escolhido,))
    resultado = cursor.fetchone()
    conexao.close()

    if resultado is not None:
        nome, classe, nivel, ouro, forca, vida, mana, mochila_texto = resultado
        if mochila_texto == "":
            mochila = []
        else:
            mochila = mochila_texto.split(",")

        print(f"\nSave carregado! Bem-vindo de volta, Nível {nivel} {nome}.")
        return nome, classe, nivel, ouro, forca, vida, mana, mochila
    else:
        print("\nHerói não encontrado no banco de dados! Começando Novo Jogo...")
        return None
def atributos():
    print("\nInteressante, isso me faz querer jogar um jogo com você.")
    print("É um jogo de dados simples, só jogue os dados.")
    print("Ele mostra um saco com seis dados de vinte lados.")
    input("[Pressione ENTER para rolar seus atributos iniciais...]")
    forca = random.randint(9, 18)
    destreza = random.randint(9, 18)
    constituicao = random.randint(9, 18)
    carisma = random.randint(9, 18)
    sabedoria = random.randint(9, 18)
    inteligencia = random.randint(9, 18)
    vida = random.randint(10, 20)
    mana = random.randint(10, 20)
    
    print("\n=== FICHA DE ATRIBUTOS ===")
    print(f"Força = {forca}")
    print(f"Destreza = {destreza}")
    print(f"Constituição = {constituicao}")
    print(f"Inteligência = {inteligencia}")
    print(f"Sabedoria = {sabedoria}")
    print(f"Carisma = {carisma}")
    print(f"Vida (HP) = {vida}")
    print(f"Mana (MP) = {mana}\n")
    return forca, vida, mana

def ver_mochila(mochila, arma, vida, mana):
    print("\n" + "="*30)
    print("SEU INVENTÁRIO")
    print("="*30)
    print(f"Arma equipada: {arma}")
    print(f"HP Atual: {vida}")
    print(f"MP Atual: {mana}")
    print("-" * 30)
    print("Itens guardados:")

    if len(mochila) == 0:
        print(" - (Sua mochila está completamente vazia)")
    else:
        for numero, item in enumerate(mochila):
            print(f" {numero + 1}. {item}")
    input("\n[Pressione ENTER para fechar a mochila e voltar à taverna]")

def combate(forca, vida, mana, mochila, nome, arma, nome_monstro, hp_monstro):
    print("\nDe repente, a porta da taverna é arrombada!")
    print(f"Um {nome_monstro} entra furioso!")
    print(f"O {nome_monstro} te encara e grita: 'VOU ARRANCAR SEUS DENTES, {nome.upper()}!'")
    while vida > 0 and hp_monstro > 0:
        print(f"\n--- STATUS: Seu HP: {vida} | MANA: {mana} | HP do {nome_monstro}: {hp_monstro} ---")
        acao = input("O Que você faz? 1) Atacar 2) Beber Poção 3) Habilidade Especial (5MP) 4) Fugir: ")
        
        if acao == "1":
            dano_jogador = random.randint(1,6) + (forca // 3)
            hp_monstro -= dano_jogador
            print(f"\nVocê avança e corta o {nome_monstro} com seu/sua {arma}, causando {dano_jogador} de dano!")
            if hp_monstro > 0:
                dano_monstro = random.randint(1,4)
                vida -= dano_monstro
                print(f"O {nome_monstro} rosna e te esfaqueia! Você perde {dano_monstro} de Vida.")
                
        elif acao == "2":
            if "Poção de Vida" in mochila:
                print("\nVocê puxa a Poção de Vida da mochila e bebe tudo! Você recupera 10 de HP.")
                vida += 10
                mochila.remove("Poção de Vida")
                if hp_monstro > 0:
                    dano_monstro = random.randint(1,4)
                    vida -= dano_monstro
                    print(f"O {nome_monstro} aproveita sua distração e te acerta! Você perde {dano_monstro} de Vida.")
            else:            
                print("\nVocê enfia a mão na mochila, mas só encontra poeira e a sua tocha! Você não tem mais poções.")
                
        elif acao == "3":
            if mana >= 5:
                mana -= 5
                dano_especial = random.randint(10, 20) + forca
                hp_monstro -= dano_especial
                print(f"\nVocê canaliza sua energia e desfere um GOLPE DEVASTADOR com {arma}! Causa absurdos {dano_especial} de dano!")
                if hp_monstro > 0:
                    dano_monstro = random.randint(1,4)
                    vida -= dano_monstro
                    print(f"O {nome_monstro} cambaleia, mas te ataca de volta! Você perde {dano_monstro} de Vida.")
            else:
                print("\nVocê tenta invocar seu poder, mas está exausto! Faltou Mana.")
                
        elif acao == "4":
            print("\nVocê corre para a cozinha da Taverna! Brog Magog balança a cabeça, decepcionado.")
            return 0, 0, vida, mana
        else:
            print("\nVocê gagueja de medo e perde o turno!")
            
    if hp_monstro <= 0:
        print(f"\nO {nome_monstro} cai morto no chão de madeira da taverna. Você sobreviveu à sua batalha!")
        ouro_dropado = random.randint(5, 15) 
        print(f"Você revira os bolsos do monstro e encontra {ouro_dropado} moedas de ouro!")
        print(f"Você encontrou uma Adaga Enferrujada e cortou uma Orelha de {nome_monstro} como troféu!")
        mochila.append("Adaga Enferrujada")
        mochila.append(f"Orelha de {nome_monstro}")
        print(f"Sua mochila agora contém: {mochila}")
        print("\nVocê ganhou 50 pontos de Experiência (XP)!")
        return 50, ouro_dropado, vida, mana
    elif vida <= 0:
        print("\nSua visão escurece... Você morreu. GAME OVER.")
        exit()

def boss(forca, vida, mana, mochila, nome, arma):
    print("\n" + "="*40)
    print(" A BATALHA FINAL ")
    print("="*40)
    print("O chão da taverna treme. Brog Magog se esconde debaixo do balcão!")
    print("Um DRAGÃO NEGRO filhote, mas letal, quebra o teto e pousa rugindo!")
    hp_dragao = 50

    while vida > 0 and hp_dragao > 0:
        print(f"\n---  STATUS: Seu HP: {vida} | MANA: {mana} | HP do Dragão: {hp_dragao} ---")
        acao = input("O Que você faz? 1) Atacar 2) Beber Poção 3) Habilidade Especial 4) Chorar: ")
        
        if acao == "1":
            dano_jogador = random.randint(1,6) + (forca // 3)
            hp_dragao -= dano_jogador
            print(f"\nVocê atinge as escamas do Dragão com seu/sua {arma}, causando {dano_jogador} de dano!")
        elif acao == "2":
            if "Poção de Vida" in mochila:
                print("\nVocê bebe a Poção e recupera 10 de HP.")
                vida += 10
                mochila.remove("Poção de Vida")
            else:
                print("\nSua mochila está vazia de poções!")
        elif acao == "3":
            if mana >= 5:
                mana -= 5
                dano_especial = random.randint(10, 20) + forca
                hp_dragao -= dano_especial
                print(f"\nVocê usa GOLPE DEVASTADOR! O Dragão urra ao perder {dano_especial} de HP!")
            else:
                print("\nSem mana! O ataque falha.")
        else:
            print("\nVocê treme de medo e perde a chance de atacar!")
            
        if hp_dragao > 0:
            print("\n... O Dragão se prepara para agir ...")
            ia_dragao = random.randint(1, 6)
            if ia_dragao <= 3:
                dano_chefe = random.randint(2, 6)
                vida -= dano_chefe
                print(f" O Dragão te ataca com as garras! Você perde {dano_chefe} de Vida.")
            elif ia_dragao <= 5:
                dano_chefe = random.randint(8, 12)
                vida -= dano_chefe
                print(f" O Dragão cospe ÁCIDO! É super efetivo! Você perde {dano_chefe} de Vida.")
            else:
                cura_chefe = random.randint(5, 10)
                hp_dragao += cura_chefe
                print(f" O Dragão bate as asas e canaliza magia negra, recuperando {cura_chefe} de HP!")
                
    if hp_dragao <= 0:
        print("\n VITÓRIA ÉPICA! O Dragão cai, destruindo três mesas da taverna.")
        print("Você salvou o dia (e o que restou da taverna do Brog)!")
        return True
    elif vida <= 0:
        print("\n Você foi engolido pelo Dragão. Brog vai ter que limpar a bagunça... GAME OVER.")
        exit()

def loja(mochila, ouro_atual):
    print("\n=== O BALCÃO DE BROG MAGOG ===")
    print("Brog limpa uma caneca e sorri. 'Sobreviveu, hein? Vejamos o que você tem de ouro.'")
    
    while True:
        print(f"\n Seu Ouro: {ouro_atual} moedas")
        print(f" Sua Mochila: {mochila}")
        print("1) Comprar Poção de Vida (10 moedas)")
        print("2) Sair da Loja")
        
        escolha = input("\nO que vai querer aventureiro? ")

        if escolha == "1":
            if ouro_atual >= 10:
                print("\nBrog te entrega um frasco vermelho brilhante.")
                ouro_atual -= 10
                mochila.append("Poção de Vida")
            else:
                print("\nBrog cruza os braços: 'Sem fiado na minha taverna! Falta ouro aí.'")
        elif escolha == "2":
            print("\nBrog acena com a cabeça. 'Volte quando quiser ser esfolado... digo, comprar mais!'")
            break
        else:
            print("\nBrog te olha confuso. 'Fala direito, não entendi!'")
            
    return ouro_atual

print("=============================")
print("  TAVERNA DO CÓDIGO - RPG")
print("=============================")

banco()
save = load()

if save is not None:
    meu_nome, minha_classe, meu_nivel, meu_ouro, forca_rolada, vida_rolada, mana_rolada, mochila = save  
   
else:
    meu_nome, minha_classe = inicio()
    forca_rolada, vida_rolada, mana_rolada = atributos()
    meu_nivel = 1
    meu_ouro = 0
    mochila = ["Poção de Vida", "Tocha"]

arsenal = {
    "guerreiro": "Montante Pesado",
    "mago": "Cajado Arcano",
    "ladino": "Par de Adagas",
    "bardo": "Alaúde Afinado",
    "paladino": "Martelo de Guerra"
}

minha_arma = arsenal.get(minha_classe.lower(), "Frigideira de Ferro")
print(f"\nBrog Magog te entrega um(a) {minha_arma} antes que os problemas comecem.")
print(f"Você dá uma olhada na sua mochila. Tem lá dentro: {mochila}") 

meu_xp = 0 
print("\nBrog Magog te entrega sua bebida. 'E então, o que vai fazer hoje?'")

while vida_rolada > 0:
    print("\n" + "="*30)
    print("  MENU DA TAVERNA ")
    print("\n" + "="*30)
    print("1) Caçar Monstros")
    print("2) Ver Mochila e Status")
    print("3) Loja do Brog")
    print("4) Desafiar o Dragão (BOSS)")
    print("5) Salvar e Sair do Jogo")
    acao = input("O que você escolhe? ")

    if acao == "1":
        inimigos = [("Goblin", 15), ("Orc", 25), ("Kobold", 10), ("Esqueleto", 18)]
        inimigo_sorteado = random.choice(inimigos)
        nome_inimigo = inimigo_sorteado[0]
        hp_inimigo = inimigo_sorteado[1]

        xp_ganho, ouro_ganho, vida_rolada, mana_rolada = combate(forca_rolada, vida_rolada, mana_rolada, mochila, meu_nome, minha_arma, nome_inimigo, hp_inimigo)
        meu_xp += xp_ganho
        meu_ouro += ouro_ganho

        if meu_xp >= 50:
            meu_nivel += 1
            meu_xp -= 50
            print("\nUM BRILHO INTENSO TOMA CONTA DE VOCÊ! ")
            print(f"Parabéns! Você subiu para o NÍVEL {meu_nivel}!")
            forca_rolada += 2
            vida_rolada += 5
            mana_rolada += 5
    elif acao == "2":
        ver_mochila(mochila, minha_arma, vida_rolada, mana_rolada)

    elif acao == "3":
        meu_ouro = loja(mochila, meu_ouro)

    elif acao == "4":
        venceu = boss(forca_rolada, vida_rolada, mana_rolada, mochila, meu_nome, minha_arma)
        if venceu:
            save_jogo(meu_nome, minha_classe, meu_nivel, meu_ouro, forca_rolada, vida_rolada, mana_rolada, mochila)
            break
    elif acao == "5":
        save_jogo(meu_nome, minha_classe, meu_nivel, meu_ouro, forca_rolada, vida_rolada, mana_rolada, mochila)
        print("\nVocê aluga um quarto e vai dormir. Até a próxima aventura!")
        break
    else:
        print("\nComando Inválido! Escolha um número de 1 a 5")

