from .constants import *
from uuid import uuid4
from random import randint
import json

class Card:
	suit_chars = {SUIT.D.value: "\u2666",
				SUIT.S.value: "\u2660",
				SUIT.H.value: "\u2665",
				SUIT.C.value: "\u2663"}

	def __init__(self, suit=SUIT.D, num=2, facedown=False):
		self.suit = suit.value
		self.symbol = self.suit_chars[self.suit]
		self.num = str(num)
		self.facedown = facedown
		self.color = COLOR.CARD_RED.value if suit == SUIT.D.value or suit == SUIT.H.value else COLOR.CARD_BLACK.value

	def flip(self):
		self.facedown = not self.facedown

	def serialize(self):
		return {k:v for k, v in self.__dict__.items()}

	def populate(self, dict):
		for k,v in dict.items():
			setattr(self, k, v)
		return self

class Player:
	def __init__(self, host, player_num=None, name=None):
		self.name = name if name is not None else f"Player {player_num}"
		self.id = int(uuid4())
		self.money = STARTING_MONEY
		self.cards = []
		self.color = eval(f"COLOR.P{player_num}").value if player_num else None
		self.symbol = chr(randint(33,126))
		self.avatar_size = 5
		self.avatar = [(randint(0,self.avatar_size-1), randint(0,self.avatar_size-1)) for i in range(20)]
		self.bet = 0
		self.options = []
		self.host = host

	def reset(self):
		self.cards = []
		self.bet = 0
		self.options = []

	def add_card(self, card):
		self.cards.append(card)

	def add_money(self, earnings):
		self.money += int(earnings)
	
	def make_bet(self, amount):
		self.money -= int(amount)
		self.bet = int(amount) 

	def bust(self, cost=0):
		return len(self.sums()) == 0

	def lose(self):
		self.cards = []
		bet = self.bet
		self.bet = 0
		return bet

	def standoff(self):
		self.money += self.bet
		self.bet = 0

	def win(self):
		self.money += self.bet * 2
		self.bet = 0

	def sums(self):
		total = [0]
		for card in self.cards:
			if card.num == 'A':
				temp = [11 + t for t in total]
				total = [1 + t for t in total]
				total.extend(temp)
			elif not card.num.isdigit():
				total = [10 + t for t in total]
			else:
				total = [int(card.num) + t for t in total]
		total = [t for t in total if t <= 21]
		return total

	def get_options(self):
		ret = [CMD.HIT.value, CMD.STAND.value]
		sums = set(self.sums())
		if len(self.cards) == 2 and self.money >= self.bet and (9 in sums or 10 in sums or 11 in sums):
			ret.append(CMD.DOUBLE.value)
		self.options = ret

	def serialize(self):
		ret = {k:v for k, v in self.__dict__.items() if k != 'cards'}
		ret['cards'] = [c.serialize() for c in self.cards]
		return ret

	def populate(self, dict):
		for k,v in dict.items():
			if k != 'cards':
				setattr(self, k, v)
		self.cards = [Card().populate(c) for c in dict['cards']]
		return self

class Dealer(Player):
	def __init__(self, num_decks=NUM_DECKS):
		super().__init__("Dealer",1,"DEALER")
		self.color = COLOR.DEALER.value
		self.avatar = [[randint(0,9), randint(-1,4)] for i in range(45)]
		self.deck = []
		for i in range(num_decks):
			self.init_deck()
		self.bet = "0"
		self.money = 0


	def init_deck(self):
		for num in list(range(2,11)) + ['J','Q','K','A']:
			for suit in SUIT:
				self.deck.append(Card(suit, num))

	def deal(self, facedown=False):
		if len(self.deck) == 0:
			return False
		card = self.deck.pop(randint(0, len(self.deck) - 1))
		if facedown:
			card.flip()
		return card

	def reveal(self):
		self.cards[1].flip()

	def serialize(self):
		ret = {k:v for k, v in self.__dict__.items() if k != 'cards' and k != 'deck'}
		ret['cards'] = [c.serialize() for c in self.cards]
		return ret

if __name__ == '__main__':
	p = Player(True, 1)
	print(p.id)
	j = json.dumps(p.serialize())
	f = json.loads(j)
	p2 = Player(True, 1).populate(f)
	print(p2.id)