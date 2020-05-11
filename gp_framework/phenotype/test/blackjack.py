import unittest

from gp_framework.phenotype.blackjack import PlayerStack, Card, Dealer


class ScoreTest(unittest.TestCase):
    def test_score_basic(self):
        stack = PlayerStack([Card.ten, Card.six])
        self.assertEqual(stack.score, 16)

    def test_score_bust(self):
        stack = PlayerStack([Card.queen, Card.jack, Card.two])
        self.assertEqual(stack.score, -1)

    def test_score_one_ace(self):
        stack = PlayerStack([Card.king, Card.ace])
        self.assertEqual(stack.score, 21)

    def test_score_two_aces(self):
        stack = PlayerStack([Card.ace, Card.ace, Card.nine])
        self.assertEqual(stack.score, 21)

    def test_score_three_aces(self):
        stack = PlayerStack([Card.ace, Card.ace, Card.ace])
        self.assertEqual(stack.score, 13)

    def test_score_four_aces(self):
        stack = PlayerStack([Card.ace, Card.ace, Card.ace, Card.ace, Card.nine])
        self.assertEqual(stack.score, 13)


class DealerTest(unittest.TestCase):
    def test_give_card(self):
        dealer = Dealer()
        # check that the dealer gave itself the correct amount of cards
        self.assertEqual(len(dealer._hidden_stack), 2)
        self.assertEqual(len(dealer._shown_stack), 1)
        self.assertEqual(len(dealer._deck), 50)

        cards = []
        for _ in range(50):
            cards.append(dealer.give_card())
        for elem in cards:
            self.assertIsInstance(elem, Card)
        should_be_none = dealer.give_card()
        self.assertIsNone(should_be_none)


if __name__ == '__main__':
    unittest.main()
