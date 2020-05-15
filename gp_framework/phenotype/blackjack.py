from enum import Enum, auto
from typing import List
import random
import struct

from gp_framework.bytegenotype import ByteGenotype
from gp_framework.phenotype.phenotype import PhenotypeConverter


class Card(Enum):
    ace = auto()
    two = auto()
    three = auto()
    four = auto()
    five = auto()
    six = auto()
    seven = auto()
    eight = auto()
    nine = auto()
    ten = auto()
    jack = auto()
    queen = auto()
    king = auto()


value_dict = {Card.two: 2, Card.three: 3, Card.four: 4, Card.five: 5, Card.six: 6, Card.seven: 7, Card.eight: 8,
              Card.nine: 9, Card.ten: 10, Card.jack: 10, Card.queen: 10, Card.king: 10}


class Deck:
    def __init__(self):
        """
        gives the instance a shuffled list of Cards
        """
        self._cards = [Card.ace, Card.two, Card.three, Card.four, Card.five, Card.six, Card.seven, Card.eight,
                       Card.nine, Card.ten, Card.jack, Card.queen, Card.king] * 4
        random.shuffle(self._cards)

    def take_random(self) -> Card:
        """
        :return: a card from deck or None if the deck is empty
        """
        if len(self._cards) == 0:
            return None
        card = self._cards[-1]
        del self._cards[-1]
        return card

    def __len__(self):
        return len(self._cards)


class PlayerStack:
    def __init__(self, starting_cards: List[Card]):
        self._cards = starting_cards

    def __len__(self):
        return len(self._cards)

    def add_card(self, card: Card):
        self._cards.append(card)

    @staticmethod
    def _normalize_score(score) -> int:
        if score > 21:
            return -1
        return score

    @staticmethod
    def _calc_possible_ace_scores(num_aces) -> List[int]:
        if num_aces == 0:
            return []
        possible_scores = [1, 11]
        num_aces -= 1
        for i in range(num_aces):
            possible_scores *= 2  # make a copy of each element
            possible_scores.sort()  # sort the list so that 1 doesn't always add up with 1, 11 with 11, etc
            for j in range(0, len(possible_scores), 2):
                possible_scores[j] += 1
                possible_scores[j + 1] += 11
            # remove duplicates and obvious bad choices
            possible_scores = set(possible_scores)
            for score in possible_scores:
                if score > 21:
                    del score
            possible_scores = list(possible_scores)
        return possible_scores

    @staticmethod
    def _maximize_score(num_aces, preliminary_score) -> int:
        # if there are no aces, return the normalized preliminary score
        if num_aces == 0:
            return PlayerStack._normalize_score(preliminary_score)

        possible_scores = PlayerStack._calc_possible_ace_scores(num_aces)
        for i in range(len(possible_scores)):
            possible_scores[i] = PlayerStack._normalize_score(possible_scores[i] + preliminary_score)
        return max(possible_scores)

    @property
    def score(self) -> int:
        num_aces = 0
        preliminary_score = 0
        for card in self._cards:
            if card == Card.ace:
                num_aces += 1
            else:
                preliminary_score += value_dict[card]
        return PlayerStack._maximize_score(num_aces, preliminary_score)


class PlayerParameters:
    """
    Everything that a Genotype decides about a player.
    """

    def __init__(self, score_weight: float, house_score_weight: float,pgw_weight: float, money_weight: float):
        self.score_weight = score_weight
        self.house_score_weight = house_score_weight
        self.pgw_weight = pgw_weight
        self.money_weight = money_weight

    @staticmethod
    def number_of_parameters() -> int:
        return 4

    @staticmethod
    def from_list(parameter_list: List[float]):
        """
        :param parameter_list: the values for each parameter in PlayerParameters
        :return: a PlayerParameters object
        """
        score_weight = parameter_list[0]
        house_score_weight = parameter_list[1]
        pgw_weight = parameter_list[2]
        money_weight = parameter_list[3]
        return PlayerParameters(score_weight, house_score_weight, pgw_weight, money_weight)


class Player:
    """
    Plays a game of Black Jack
    """
    _HIT_THRESHOLD = 1.0

    def __init__(self, parameters: PlayerParameters):
        self._parameters = parameters
        self._cards = None
        self.reset_cards()
        self._money = 100
        self._games_played = 0
        self._games_won = 0

    def hit(self, house_score: int) -> bool:
        hs_pressure = house_score * self._parameters.house_score_weight
        score_pressure = self._cards.score * self._parameters.score_weight
        return hs_pressure + score_pressure > Player._HIT_THRESHOLD

    def make_bet(self) -> int:
        """
        automatically decreases the Player's money
        :return: the player's starting bet
        """
        if self._games_played == 0:  # avoid div by zero errors
            self._money -= 10
            return 10
        float_bet = min(float(self._money),
                        self._money * self._parameters.money_weight + self.perc_games_won * self._parameters.pgw_weight)
        # converting to an integer like this can result in an OverflowError
        try:
            bet = int(float_bet)
        except OverflowError:
            if float_bet > 0:
                bet = self._money
            else:
                bet = 0

        bet = max(10, bet)
        self._money -= bet
        return bet

    def receive_card(self, card: Card):
        self._cards.add_card(card)

    def reset_cards(self):
        self._cards = PlayerStack([])

    def get_game_results(self, won: bool, winnings: int):
        self._games_played += 1
        if won:
            self._games_won += 1
        self._money += winnings

    @property
    def score(self):
        return self._cards.score

    @property
    def money(self):
        return self._money

    @property
    def perc_games_won(self):
        return self._games_won / self._games_played


class Dealer:
    """
    Acts as the house
    """

    def __init__(self):
        self._deck = Deck()
        hidden_card = self._deck.take_random()
        shown_card = self._deck.take_random()
        self._hidden_stack = PlayerStack([hidden_card, shown_card])
        self._shown_stack = PlayerStack([shown_card])

    def give_card(self) -> Card:
        return self._deck.take_random()

    def give_self_card(self) -> bool:
        """
        :return: whether or not the Dealer gave itself a new card
        """
        if self._hidden_stack.score >= 17:
            return False
        new_card = self._deck.take_random()
        if new_card is None:
            return False
        self._hidden_stack.add_card(new_card)
        self._shown_stack.add_card(new_card)

    @property
    def known_score(self):
        return self._shown_stack.score

    @property
    def hidden_score(self):
        return self._hidden_stack.score


class BlackJackTable:
    def __init__(self, players: List[Player]):
        """
        Important! Do NOT change the ordering of the list of players. It will mess up the mapping of Genotype to Money.
        This really should be fixed.
        """
        self._players = players
        self._payout = 3 / 2

    def _play_round(self):
        # set up
        dealer = Dealer()
        bets = {}
        for player in self._players:
            player.reset_cards()
            bets[player] = player.make_bet()
            # print("A bet of", bets[player], "has been placed.")
            player.receive_card(dealer.give_card())
            player.receive_card(dealer.give_card())

        # play
        cards_given = 0
        for player in self._players:
            while player.hit(dealer.known_score) and player.score > 0:
                new_card = dealer.give_card()
                """if new_card is None:
                    print("Warning! Deck is empty.")
                else:
                    cards_given += 1
                    print("Given {} cards".format(cards_given))"""
                player.receive_card(new_card)
            # print("Player done.\n")

        # payout
        for player in self._players:
            won = False
            winnings = 0
            player_score = player.score
            dealer_score = dealer.hidden_score
            # print("Player score: {} vs Dealer score {}".format(player_score, dealer_score))
            if player.score >= dealer.hidden_score:
                won = True
                winnings = bets[player] * self._payout
                # print("Paying out", winnings)
            player.get_game_results(won, winnings)

    def play_rounds(self, num_rounds):
        for i in range(num_rounds):
            self._play_round()

    @property
    def players(self) -> List[Player]:
        return self._players


class PlayerConverter(PhenotypeConverter):
    def convert(self, genotype: ByteGenotype) -> Player:
        """
        Turn genome into an array of parameters between 0 and 1 to be plugged into
        some application.

        :param genotype: The Genotype to convert
        :return: An array of floats between 0 and 1
        """
        parameters: List[float] = []

        # Each parameter will consume 4 bytes.
        for i in range(PlayerParameters.number_of_parameters()):
            [parameter] = struct.unpack('f', bytes(genotype[i:i + 4]))
            parameters.append(parameter)

        return Player(PlayerParameters.from_list(parameters))
