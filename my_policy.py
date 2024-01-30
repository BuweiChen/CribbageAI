from policy import CribbagePolicy, CompositePolicy, GreedyThrower, GreedyPegger

class MyPolicy(CribbagePolicy):
    def __init__(self, game):
        self._policy = CompositePolicy(game, GreedyThrower(game), GreedyPegger(game))
        
    def _get_possible_turn_cards(self, hand):
        deck = self._policy._game.deck()
        deck.remove(hand)
        return deck.peek(deck.size())
        
    def keep(self, hand, scores, am_dealer):
        """ basic keep policy: considers turn card and greedy opponent discard
        """
        
        possibleTurnCard = self._get_possible_turn_cards(hand)
        
        return self._policy.keep(hand, scores, am_dealer)


    def peg(self, cards, history, turn, scores, am_dealer):
        return self._policy.peg(cards, history, turn, scores, am_dealer)

    

                                    
