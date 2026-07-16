class Pokemon:
    def __init__(self, codigo, nombre, tipo, nivel, hp_maximo, hp, ataque, defensa, velocidad):
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel
        self.hp_maximo = hp_maximo
        self.hp = hp
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad

    def esta_debilitado(self):
        return self.hp <= 0

    def recibir_danio(self, danio):
        self.hp = max(0, self.hp - danio)

    def restaurar_hp(self):
        self.hp = self.hp_maximo

class Entrenador:
    def __init__(self, nombre, gimnasio, pokemon_principal, recompensa):
        self.nombre = nombre
        self.gimnasio = gimnasio
        self.pokemon_principal = pokemon_principal
        self.recompensa = recompensa