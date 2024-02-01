from cribbage import Game
from scoring import score, greedy_throw
import pickle
from os import path
import itertools
from deck import Deck, Card

class Schell:
    def __init__(self):
        self._game = Game()
        self._saveFileName1 = "200000_throws_cribT.pickle"
        self._saveFileName2 = "200000_throws_cribF.pickle"
        self._saveFileSchellsDealerName = "schellsTableDealer.pickle"
        self._saveFileSchellsNonDealerName = "schellsTableNonDealer.pickle"
        self._throws_T_possible = []
        self._throws_F_possible = []
        self.schellsTableDealer = {}
        self.schellsTableNonDealer = {}
        if path.isfile(self._saveFileName1):
            file = open(self._saveFileName1, "rb")
            self._load_200000_throws_T(file)
        else:
            self._throws_T_possible = self._get_200000_throws_possible(self._game, 1)
            file = open(self._saveFileName1, "wb")
            self._save_200000_throws_T(self._throws_T_possible, file)
        if path.isfile(self._saveFileName2):
            file = open(self._saveFileName2, "rb")
            self._load_200000_throws_F(file)
        else:
            self._throws_F_possible = self._get_200000_throws_possible(self._game, -1)
            file = open(self._saveFileName2, "wb")
            self._save_200000_throws_F(self._throws_F_possible, file)
        if path.isfile(self._saveFileSchellsDealerName):
            file = open(self._saveFileSchellsDealerName, "rb")
            self.schellsTableDealer = pickle.load(file)
        else:
            self._calculate_schells_table_for_dealer(self._game)
        if path.isfile(self._saveFileSchellsNonDealerName):
            file = open(self._saveFileSchellsNonDealerName, "rb")
            self.schellsTableNonDealer = pickle.load(file)
        else:
            self._calculate_schells_table_for_non_dealer(self._game)
        
    def _get_200000_throws_possible(self, game, crib):
        deck = Deck((1,2,3,4,5,6,7,8,9,10,11,12,13), ("H"), 4)
        # only have hearts in the deck so the computation isn't affected by flushes
        # effectively, this is equivalent to not considering suits.
        throws = []
        for i in range(0, 200000):
            deck.shuffle()
            throws.append(greedy_throw(game, deck.peek(6), crib)[1])
        return throws
            
    def _save_200000_throws_T(self, throws, file):
        pickle.dump(throws, file)
        
    def _save_200000_throws_F(self, throws, file):
        pickle.dump(throws, file)
        
    def _load_200000_throws_T(self, file):
        self._throws_T_possible = pickle.load(file)
        
    def _load_200000_throws_F(self, file):
        self._throws_F_possible = pickle.load(file)
        
    def _get_all_discard_pairs_possible(self, game):
        cards = []
        for r in range(1, 14):
            cards.append(Card(r, "C"))
        pairs = []
        for r in range(1, 14):
            pairs.append([Card(r, "C"), Card(r, "C")])
        return tuple(pairs) + tuple(itertools.combinations(cards, 2))
    
    def _get_possible_turn_cards(self, game):
        deck = Deck((1,2,3,4,5,6,7,8,9,10,11,12,13), ("H"), 1)
        # again, not considering suit here effectively
        return deck.peek(deck.size())
    
    def _calculate_schells_table_for_dealer(self, game):
        discardsPairs = self._get_all_discard_pairs_possible(game)
        turnCards = self._get_possible_turn_cards(game)
        schellsTable = {}
        for discard in discardsPairs:
            print("computing pair {0}".format(discard), flush=True)
            discard_value = 0
            for turn in turnCards:
                print("computing turn {0}".format(turn), flush=True)
                for op_throw in self._throws_F_possible:
                    # from the opponent's perspective, they don't own the crib
                    cribCards = op_throw
                    discard_value += score(game, list(cribCards) + list(discard), turn, True)[0] / 2600000
                    # the value is normalized to the average score for one round
            print(discard_value, flush=True)
            schellsTable.update({(discard[0].rank(), discard[1].rank()): discard_value})
        
        # save the table
        saveFile = open(self._saveFileSchellsDealerName, "wb")
        pickle.dump(schellsTable, saveFile)
    
    def _calculate_schells_table_for_non_dealer(self, game):
        discardsPairs = self._get_all_discard_pairs_possible(game)
        turnCards = self._get_possible_turn_cards(game)
        schellsTable = {}
        for discard in discardsPairs:
            print("computing pair {0}".format(discard), flush=True)
            discard_value = 0
            for turn in turnCards:
                print("computing turn {0}".format(turn), flush=True)
                for op_throw in self._throws_T_possible:
                    # from the opponent's perspective, they own the crib
                    cribCards = op_throw
                    discard_value -= score(game, list(cribCards) + list(discard), turn, True)[0] / 2600000
                    # the value is normalized to the average score for one round
            print(discard_value, flush=True)
            schellsTable.update({(discard[0].rank(), discard[1].rank()): discard_value})
        
        # save the table
        saveFile = open(self._saveFileSchellsNonDealerName, "wb")
        pickle.dump(schellsTable, saveFile)
        
    def look_up_in_schells_table(self, cards, am_dealer):
        if am_dealer:
            return self.schellsTableDealer[cards[0].rank(), cards[1].rank()]
        else:
            return self.schellsTableNonDealer[cards[0].rank(), cards[1].rank()]

c1 = Card(1, "C")
c2 = Card(11, "H")
s = Schell()
s.look_up_in_schells_table([c1, c2], False)