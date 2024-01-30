from cribbage import Game
from deck import Card
from my_policy import MyPolicy

game = Game()
p = MyPolicy(game)
hand = [Card(1,'S'), Card(1,'D'), Card(1,'H'), Card(1,'C')]
print(p._get_possible_turn_cards(hand))