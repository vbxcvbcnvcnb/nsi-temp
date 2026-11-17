import random


class Deck:
    def __init__(self):
        self.card_tab = []

    def create_game(self):
        familles = ["coeur", "carreau", "pique", "trefle"]

        for famille in familles:
            for i in range(1, 14):
                self.card_tab.append((i, famille))

    def get_card_game(self):
        return self.card_tab


class Player:
    def __init__(self, nom):
        self.nom = nom
        self.hand = []

    def gagner(self, liste_card):
        self.hand.extend(liste_card)

    def lose(self, nombre_cartes):
        pertes = self.hand[:nombre_cartes]
        self.hand = self.hand[nombre_cartes:]
        return pertes

    def afficher(self):
        return self.hand

    def renvoyer_derniere_carte(self):
        return self.hand.pop(0)


def valeur(carte):
    # L'as (1) est la carte la plus forte : on lui donne la valeur 14
    return 14 if carte[0] == 1 else carte[0]


def init_game():
    jeu = Deck()
    jeu.create_game()

    player1 = Player("José")
    player2 = Player("Marinette")

    card_available = jeu.get_card_game()

    random.shuffle(card_available)

    milieu = len(card_available) // 2

    first_list = card_available[:milieu]
    second_list = card_available[milieu:]

    player1.gagner(first_list)
    player2.gagner(second_list)

    return player1, player2


def game():
    player1, player2 = init_game()

    face_cachee = []
    nombre_tour = 0

    while player1.hand and player2.hand and nombre_tour < 30:

        print(f"\nTour {nombre_tour + 1}")

        # Chaque joueur tire une carte
        j1_card = player1.renvoyer_derniere_carte()
        j2_card = player2.renvoyer_derniere_carte()

        print(player1.nom, "tire :", j1_card)
        print(player2.nom, "tire :", j2_card)

        face_cachee.extend([j1_card, j2_card])

        # Comparaison des valeurs des cartes (l'as est la plus forte)
        if valeur(j1_card) > valeur(j2_card):

            print(player1.nom, "gagne le tour")

            player1.gagner(face_cachee)
            face_cachee = []

        elif valeur(j2_card) > valeur(j1_card):

            print(player2.nom, "gagne le tour")

            player2.gagner(face_cachee)
            face_cachee = []

        else:
            print("Bataille !")  # valeurs égales : les cartes restent en jeu

        nombre_tour += 1

    # Résultat final
    if len(player1.hand) == 0:
        print(player2.nom, "a gagné !")

    elif len(player2.hand) == 0:
        print(player1.nom, "a gagné !")

    else:
        print("Égalité : nombre maximum de tours atteint.")


game()
