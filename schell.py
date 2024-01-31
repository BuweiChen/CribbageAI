from cribbage import Game
from scoring import score, greedy_throw
import pickle
from os import path
import itertools

class Schell:
    def __init__(self):
        self._game = Game()
        self._saveFileName = "two_mil_hands.pickle"
        self._hands_possible = []
        if path.isfile(self._saveFileName):
            file = open(self._saveFileName, "rb")
            self._load_2_million_hands(file)
        else:
            self._hands_possible = self._get_2_million_hands_possible(self._game)
            file = open(self._saveFileName, "wb")
            self._save_2_million_hands(self._hands_possible, file)
        
    def _get_2_million_hands_possible(self, game):
        deck = game.deck()
        hands = []
        for i in range(0, 2000000):
            deck.shuffle()
            hands.append(deck.peek(6))
        return hands
            
    def _save_2_million_hands(self, hands, file):
        pickle.dump(hands, file)
        
    def _load_2_million_hands(self, file):
        self._hands_possible = pickle.load(file)
        
    def _get_all_discard_pairs_possible(self, game):
        cards = game.deck().peek(52)
        return itertools.combinations(cards, 2)
    
    def _get_possible_turn_cards(self, game):
        deck = game.deck()
        return deck.peek(deck.size())
    
    def _calculate_snells_table_for_dealer(self, game):
        discardsPairs = self._get_all_discard_pairs_possible(game)
        turnCards = self._get_possible_turn_cards(game)
        snellsTable = {}
        # discardLimit = 5
        for discard in discardsPairs:
            print("computing pair {0}".format(discard), flush=True)
            # if discardLimit == 0:
            #     break
            # print("discard")
            # print(discard)
            # turnLimit = 5
            discard_value = 0
            for turn in turnCards:
                print("computing turn {0}".format(turn), flush=True)
                # if turnLimit == 0:
                #     turnLimit = 5
                #     break
                # print("turn")
                # print(turn)
                # handLimit = 5
                for op_hand in self._hands_possible:
                    # print("computing op_hand {0}".format(op_hand), flush=True)
                    # if handLimit == 0:
                    #     handLimit = 5
                    #     break
                    # print("hand")
                    # print(op_hand)
                    cribCards = greedy_throw(game, op_hand, -1)[1]
                    # from the opponent's perspective, we own the crib
                    # print("throw")
                    # print(cribCards)
                    discard_value += score(game, list(cribCards) + list(discard), turn, True)[0] / 1058643040
                    # the value is normalized to the average score for one round
            #         handLimit -= 1
            #     turnLimit -= 1
            # discardLimit -= 1
            # print("discard value")
            # print(discard_value)
            snellsTable.update({discard: discard_value})
        
        # save the table
        saveFile = open("snellsTableDealer.pickle", "wb")
        pickle.dump(snellsTable, saveFile)
    
    def _calculate_snells_table_for_non_dealer(self, game):
        discardsPairs = self._get_all_discard_pairs_possible(game)
        turnCards = self._get_possible_turn_cards(game)
        snellsTable = {}
        # discardLimit = 5
        for discard in discardsPairs:
            print("computing pair {0}".format(discard), flush=True)
            # if discardLimit == 0:
            #     break
            # print("discard")
            # print(discard)
            # turnLimit = 5
            discard_value = 0
            for turn in turnCards:
                # if turnLimit == 0:
                #     turnLimit = 5
                #     break
                # print("turn")
                # print(turn)
                # handLimit = 5
                for op_hand in self._hands_possible:
                    # if handLimit == 0:
                    #     handLimit = 5
                    #     break
                    # print("hand")
                    # print(op_hand)
                    cribCards = greedy_throw(game, op_hand, 1)[1]
                    # from the opponent's perspective, they own the crib
                    # print("throw")
                    # print(cribCards)
                    discard_value += score(game, list(cribCards) + list(discard), turn, True)[0] / 1058643040
                    # the value is normalized to the average score for one round
            #         handLimit -= 1
            #     turnLimit -= 1
            # discardLimit -= 1
            # print("discard value")
            # print(discard_value)
            snellsTable.update({discard: discard_value})
        
        # save the table
        saveFile = open("snellsTableNonDealer.pickle", "wb")
        pickle.dump(snellsTable, saveFile)
        
s = Schell()
s._calculate_snells_table_for_dealer(s._game)
