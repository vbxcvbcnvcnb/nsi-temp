import random
import time
import subprocess
import sys
import os

class cardDeck():
    def __init__(self, deck_lenght):
        self.deck_lenght = deck_lenght
        self.deck = []
        if self.deck_lenght == 52:
            for i in range(4):
                self.deck.extend([i for i in range(2, 11)])
                self.add_royal()
        else:
            for i in range(4):
                self.deck.extend([i for i in range(7, 11)])
                self.add_royal()

        # les étapes suivantes : ajouter les familles et mélanger le deck
        self.set_families()
        random.shuffle(self.deck)

    def add_royal(self):
        self.deck.append("valet")
        self.deck.append("dame")
        self.deck.append("roi")
        self.deck.append("as")

    def set_families(self):
        self.families = ["coeur", "carreau", "trèfle", "pique"]
        quarter = len(self.deck) // 4
        for index in range(4):
            for i in range(quarter):
                pos = i + index * quarter
                self.deck[pos] = f"{self.deck[pos]} de {self.families[index]}"

    def get_deck(self):
        return self.deck


class playerDeck():
    def __init__(self, deck):
        self.deck = deck

    def get_player_deck(self):
        return self.deck

    def player_lose_cards(self, number_of_cards):
        lost_cards = []
        for i in range(number_of_cards):
            lost_one = self.deck.pop(0)
            lost_cards.append(lost_one)
        return lost_cards

    def player_win_cards(self, cards):
        self.deck.extend(cards)


def valeur_carte(carte):
    # "roi de pique" -> 13, "7 de coeur" -> 7
    mot = carte.split(" ")[0]
    ordre = {"valet": 11, "dame": 12, "roi": 13, "as": 14}
    if mot in ordre:
        return ordre[mot]
    return int(mot)


def init_game(deck_length, nb_players):
    game_deck = cardDeck(deck_length)
    list_cards = game_deck.get_deck()
    players_decks = {}
    for i in range(nb_players):
        players_decks[f"{i}_deck"] = playerDeck([])   # un playerDeck vide par joueur

    index_distrubute = 0
    for i in range(len(list_cards)):
        current_card = list_cards[i]
        if index_distrubute >= nb_players:
            index_distrubute = 0
        players_decks[f"{index_distrubute}_deck"].player_win_cards([current_card])
        index_distrubute += 1
    return players_decks


def in_game():
    deck_lenght = int(input("Entrez le nombre de cartes dans le deck (52 ou 32) : "))
    nb_players = int(input("Entrez le nombre de joueurs : "))
    if deck_lenght not in [32, 52] or nb_players < 2 or nb_players > deck_lenght // 2:
        print("Paramètres invalides, veuillez réessayer")
        return in_game()      # return : sinon la partie continue avec les mauvais paramètres
    players = init_game(deck_lenght, nb_players)

    surplus_cards = []

    def tirer_carte():
        noms = list(players.keys())     # tous les joueurs au début du tour
        en_lice = list(players.keys())  # ceux qui se disputent encore le tour

        while True:
            cards_in_game = []

            # chaque joueur en lice tire sa première carte
            for nom in en_lice:
                carte = players[nom].player_lose_cards(1)[0]
                cards_in_game.append(carte)
                print(f"{nom} : {carte}")

            # toutes les cartes tirées vont sur la table
            surplus_cards.extend(cards_in_game)

            valeurs = []
            for carte in cards_in_game:
                valeurs.append(valeur_carte(carte))
            max_value = max(valeurs)

            # les joueurs qui ont la valeur max (1 seul = il gagne, plusieurs = égalité)
            ex_aequo = []
            for i in range(len(en_lice)):
                if valeurs[i] == max_value:
                    ex_aequo.append(en_lice[i])

            if len(ex_aequo) == 1:
                gagnant = ex_aequo[0]
                break

            print(f"Egalité entre {ex_aequo} : seuls ces joueurs rejouent")

            # un joueur sans carte ne peut pas continuer l'égalité
            en_lice = []
            for nom in ex_aequo:
                if len(players[nom].get_player_deck()) > 0:
                    en_lice.append(nom)

            if len(en_lice) == 1:
                gagnant = en_lice[0]
                break
            if len(en_lice) == 0:
                # personne ne peut continuer : on tire le gagnant au hasard parmi les ex aequo
                gagnant = random.choice(ex_aequo)
                break

        random.shuffle(surplus_cards)   # évite les parties infinies
        players[gagnant].player_win_cards(surplus_cards)
        surplus_cards.clear()
        print(f"Le joueur {gagnant} a gagné le tour")

        # élimination des joueurs sans carte (un seul bloc)
        for nom in noms:
            if len(players[nom].get_player_deck()) == 0:
                print(f"Le joueur {nom} a perdu toutes ses cartes et est éliminé")
                del players[nom]

    turn = 1
    while len(players) > 1:
        if turn > 30:
            print("La partie est trop longue, pas de gagnant")
            break               # on vérifie AVANT de jouer un tour de plus

        tirer_carte()
        time.sleep(1)
        print(f"Tour {turn} terminé, il reste {len(players)} joueurs")
        turn += 1

    if len(players) == 1:
        print(f"Le joueur {list(players.keys())[0]} a gagné la partie")


def cli_or_web():
    choix = input("Voulez-vous jouer en mode CLI ou Web ? (cli/web) : ").strip().lower()
    if choix == "cli":
        in_game()
    elif choix == "web":
        subprocess.run([
            "ttyd", "-W",             # -W : autorise la saisie au clavier
            "-p", str(440),
            "-i", "lo",               # écoute seulement en local (127.0.0.1)
            sys.executable, os.path.abspath(__file__), "--jeu"
        ])
    else:
        print("Choix invalide, veuillez réessayer")
        return cli_or_web()


if __name__ == "__main__":
    if "--jeu" in sys.argv:
        in_game()          # relancé par ttyd : on lance directement la partie
    else:
        cli_or_web()
