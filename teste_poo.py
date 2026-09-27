class Heroi:
    def __init__(self, nome_digitado, classe_escolhida):
        self.nome = nome_digitado
        self.classe = classe_escolhida
        self.nivel = 1
        self.vida = 20
        self.ouro = 0
        self.mochila = ["Poção de Vida", "Tocha"]

    def apresentar(self):
        print(f"Eu sou {self.nome}, um {self.classe} de nivel {self.nivel}!")

    def tomar_dano (self, dano):
        self.vida -= dano
        print(f"{self.nome} tomou {dano} de dano! Vida restante: {self.vida}!")

class Monstro:
    def __init__ (self, nome_monstro, hp_monstro):
        self.nome = nome_monstro
        self.vida = hp_monstro

    def apresentar(self):
        print(f" AHHHHHHHHH EU SOU O {self.nome}")
        
jogador_1 = Heroi("Alisson", "Ladino")
jogador_2 = Heroi("Brog", "Guerreiro")

jogador_1.apresentar()
jogador_2.apresentar()

jogador_1.tomar_dano(5)

monstro_1 = Monstro("Orc", 25)
monstro_2 = Monstro("Esqueleto", 15)

monstro_1.apresentar()
monstro_2.apresentar()
