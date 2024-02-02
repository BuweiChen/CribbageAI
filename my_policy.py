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
            return self._schell.look_up_in_schells_table(r1, r2, am_dealer)
        else:
            return self._schell.look_up_in_schells_table(r2, r1, am_dealer)
        
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
        """ idea: most of a card's value comes from scoring points, 
            but in the case of tie-breaking, we introduce cards that set up
            future scoring with high probability.
            e.g. bait pair -> 15, bait 15 -> pair
            lower priority: bait pair -> 31
            baiting runs feels too hard to implement
            additionally, try to avoid 5 and 21 (weighted slightly more than bait pairs)
            try to avoid 10 and 26 (weighted at half of prev, since it's likely opponent holds onto 5)
            
            pre-15 strategy: stay low, but try to keep 1, 2, 3, 4 in hand to score go, smaller cards weighed 
            less for playing
            general rule: play cards from large to small
        """
        card_scores = {}
        card_ranks = []
        for card in cards:
            card_ranks.append(card.rank())
            
        # weigh cards from large to small by sorting them in decreasing order, 
        # so exact ties broken by priority
        
        sortedHand = sorted(cards, key=(lambda c: c.rank()), reverse=True)
        
        for card in cards:
            score = history.score(self._policy._game, card, 0 if am_dealer else 1)
            # bait pair 
            if (15 - history.total_points() - 2 * card.rank()) in card_ranks:
                score += 0.4
                
            if (31 - history.total_points() - 2 * card.rank()) in card_ranks:
                score += 0.4
                
            # bait fifteen, weighed less because 0 net gain, but potentially mitigate damage
            if (15 - history.total_points() - card.rank()) in card_ranks:
                score += 0.2
            
            # try to avoid 5 and 21
            if history.total_points() + card.rank() == 5 or history.total_points() + card.rank() == 21:
                score -= 0.5
                
            # try to avoid 10 and 26
            if history.total_points() + card.rank() == 10 or history.total_points() + card.rank() == 26:
                score -= 0.25
            
            card_scores.update({card: score})
            
        best_card = None
        best_score = None
        for card in sortedHand:
            score = card_scores[card]
            if score is not None and (best_score is None or score > best_score):
                best_score = score
                best_card = card
        return best_card

    

                                    
