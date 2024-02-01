from policy import CribbagePolicy, CompositePolicy, GreedyThrower, GreedyPegger
from schell import Schell
from deck import Card
import itertools
import scoring

class MyPolicy(CribbagePolicy):
    def __init__(self, game):
        self._policy = CompositePolicy(game, GreedyThrower(game), GreedyPegger(game))
        self._schell = Schell()
        
    def _get_possible_turn_cards(self, hand):
        deck = self._policy._game.deck()
        deck.remove(hand)
        return deck.peek(deck.size())
    
    def _get_comb_of_any_four(self, hand):
        """ returns a list of possible kept hand and throws
        """
        all_combinations = []
        for combination in itertools.combinations(hand, 4):
            remaining_cards = tuple(set(hand) - set(combination))
            all_combinations.append((combination, remaining_cards))
        
        return all_combinations
    
    def _get_value_of_crib_discard_pair(self, cards, am_dealer):
        r1 = cards[0].rank()
        r2 = cards[1].rank()
        if r1 < r2:
            return self._schell.look_up_in_schells_table([cards[0], cards[1]], am_dealer)
        else:
            return self._schell.look_up_in_schells_table([cards[1], cards[0]], am_dealer)
        
    def keep(self, hand, scores, am_dealer):
        """ basic keep policy: considers turn card and greedy opponent discard
        """
        
        # print("new hand! ~~~~~")
        
        possibleTurnCard = self._get_possible_turn_cards(hand)
        possibleKeepThrow = self._get_comb_of_any_four(hand)
        
        bestKeepThrow = ()
        bestKeepThrowScore = float('-inf')
        for comb in possibleKeepThrow:
            score = self._get_value_of_crib_discard_pair(comb[1], am_dealer)
            for card in possibleTurnCard:
                score += (scoring.score(self._policy._game, comb[0], card, False)[0]) / 46
                # score normalized to average score per round
                # print("turn: {0} card: {1} score: {2}".format(card, comb[0], score))
            if score > bestKeepThrowScore:
                    bestKeepThrow = comb
                    bestKeepThrowScore = score
            
        
        # print("best keep is {0} with score {1}".format(list(bestKeepThrow[1]), bestKeepThrowScore))
                    
        return list(bestKeepThrow[0]), list(bestKeepThrow[1])


    def peg(self, cards, history, turn, scores, am_dealer):
        return self._policy.peg(cards, history, turn, scores, am_dealer)

    

                                    
