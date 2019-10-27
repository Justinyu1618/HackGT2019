from uuid import uuid4
from .src.display_util import DisplayTable
from .src.constants import *
from .src.objects import Card, Player, Dealer
from random import randint
import curses

from abc import ABC, abstractmethod

class NetworkingDelegate(ABC):

    @abstractmethod
    def connected(self):
        pass

    @abstractmethod
    def received_data(self):
        pass

    @abstractmethod
    def disconnected(self):
        pass

class BlackjackDelegate(NetworkingDelegate):

    def __init__(self, handle_data):
        self.handle_data = handle_data

    def connected(self):
        print("connected!")
        pass

    def received_data(self, event, data):
        self.handle_data(event, data)

    def disconnected(self):
        pass


class Game:

    def __init__(self, stdscr, sio, host, match_code, player):
        self.players = []
        self.dealer = Dealer()
        self.display = DisplayTable(stdscr)
        self.screen = stdscr
        self.state = "betting"
        self.host = host
        self.game_state_update = None
        self.resp = None
        self.sio = sio
        self.delegate = BlackjackDelegate(self.handle_data)
        self.turn = None
        self.match_code = match_code
        self.screen.timeout(-1)
        self.player_id = player

    def run(self):
        self.render()
        while(True):
            keep_playing = True
            while(keep_playing):
                curses.napms(100)
                # if self.host:
                self.gameplay()
                self.reset()
                if not self.players:
                    break
                keep_playing = self.end()
            self.end_game()
    
    def change_state(self, new_state):
        self.state = new_state
        self.render()

    def gameplay(self):
        self.change_state("betting")
        self._betting()
        self.change_state("dealing")
        self._dealing()
        self.change_state("turn")
        self._turn()
        self.change_state("scoring")
        self._scoring()
        curses.napms(1000)
        self.check_losers() 

    def update(self):
        game_state = {}
        game_state['players'] = [p.serialize() for p in self.players]
        game_state['dealer'] = self.dealer.serialize()
        game_state['state'] = self.state
        game_state['turn'] = self.turn
        return game_state

    def send_update(self, game_state=None):
        if game_state is None:
            game_state = self.update()
        self.sio.emit('data', {'code': self.match_code, 'state':game_state})


    def render(self, game_state=None):
        if game_state is None:
            game_state = self.update()
        self.send_update(game_state)
        game_state["players"] = [Player().populate(p) for p in game_state["players"]]
        game_state["dealer"] = Dealer().populate(game_state["dealer"])
        self.display.render(game_state)
        

    def handle_data(self, event, data):
        if event == "resp" and self.host:
            self.resp = data

    
    def request(self, player, c_type='ch'):
        if player.id == self.player.id:
            if c_type == 'str':
                if self.msg['type'] == 'ch':
                    return self.screen.getch()
                else:
                    return self.screen.getstr()
        p_id = player_id
        self.sio.emit('req', {'code': self.match_code, 'player_id':p_id, 'type':c_type})
        while(self.resp is None or self.msg['player_id'] != p_id):
            pass
        ret = self.resp['data']
        self.resp = None
        return ret

    def _betting(self):
        for player in self.players:
            self.turn = player.id
            self.render()
            while(not bet.isdigit() or int(bet) > player.money
                    or int(bet) < BET_MIN or int(bet) > BET_MAX):
                bet = self.request(player, 'str')
                self.change_state("betting_error")
            self.change_state("betting")
            player.make_bet(bet)
        self.turn = None
    
    def _dealing(self):
        for i in range(2):
            for p in self.players:
                p.add_card(self.dealer.deal())
                self.render()
                curses.napms(300)
            self.dealer.add_card(self.dealer.deal(facedown = i == 1))
            self.render()

    def _turn(self):
        for i in range(len(self.players)):
            player = self.players[i]
            player.get_options()
            self.turn = player.id
            self.render()
            while(True):
                cmd = None
                while(cmd not in list(map(lambda x:ord(x.value), CMD))):
                    cmd = self.request(player.id)
                if cmd == ord('h'):
                    player.add_card(self.dealer.deal())
                elif cmd == ord(CMD.STAND.value):
                    break
                elif cmd == ord(CMD.DOUBLE.value) and CMD.DOUBLE in set(player.options):
                    player.money -= player.bet
                    player.bet *= 2
                    player.add_card(self.dealer.deal())
                    if player.bust():
                        self.dealer.add_money(player.lose())
                    break
                self.render()
                curses.napms(300)
                if player.bust():
                    self.dealer.add_money(player.lose())
                    break
        self.turn = None
        self.dealer.reveal()
        while(not self.dealer_bust() and max(self.dealer.sums()) < 17):
            self.dealer.add_card(self.dealer.deal())
            self.print("Dealing....", 1000)

    def _scoring(self):
        if(not self.dealer.bust() and any([p.cards for p in self.players])):
            dealer_sum = max(self.dealer.sums())
            for p in self.players:
                if p.cards:
                    self.turn = p.id
                    self.print(f"{p.name} vs Dealer", 1000)
                    if max(p.sums()) > dealer_sum: 
                        self.print(f"{p.name} Wins!")
                        self.dealer.money -= p.bet
                        p.win()
                    elif max(p.sums()) < dealer_sum:
                        self.print("Dealer Wins!")
                        self.dealer.add_money(p.lose())
                    else:
                        self.print("Standoff!")
                        p.standoff()
                    curses.napms(1000)

    def end(self):
        self.change_state("end")
        self.render()
        while(True):
            cmd = self.screen.getch()
            if cmd == ord('y'):
                return True 
            elif cmd == ord('n'):
                return False

    def end_game(self):
        for i in range(5,0,-1):
            self.print(f" Game Over! (restarting in {i})",1000)
        self.display.restart()


    def print(self, msg, delay=0):
        self.display.print(msg)
        curses.napms(delay)

    def reset(self):
        for p in self.players:
            p.reset()
        self.dealer.reset()
        self.turn = None
        self.render()
    
    def check_losers(self):
        to_remove = set()
        for p in self.players:
            if p.money <= 0:
                self.print(f"{p.name} has lost!", 1000)
                to_remove.add(p)
                self.display.remove_player(p)
        for p in to_remove:
            self.players.remove(p)

        
    def dealer_bust(self):
        if self.dealer.bust():
            self.print("Dealer BUST!", 1000)
            for p in self.players:
                if p.cards: 
                    self.dealer.money -= p.bet
                    p.win()
            self.render()
            return True
        return False

    def start(self):
        # curses.echo()
        # if curses.LINES < MIN_HEIGHT:
        #   self.print(f"HEIGHT TOO SMALL ({curses.LINES})")
        #   curses.napms(2000)
        #   return False
        # self.display.set_dealer(self.dealer)
        # max_players = min(int(curses.COLS / MIN_PLAYER_WIDTH), MAX_PLAYERS)
        # self.display.max_players = max_players
        # self.display.set_state("starting")
        # self.display.refresh()
        # if int(curses.COLS / MIN_PLAYER_WIDTH) < MAX_PLAYERS:
        #   self.print("*Screen too small**")
        # p_count = 0
        # key = None
        # while(p_count != max_players and key != ord('s')):
        #   key = self.screen.getch()
        #   if key == ord('n'):
        #       p_count += 1
        #       new_player = Player(f"Player {p_count}", f"P{p_count}")
        #       self.players.append(new_player)
        #       self.display.add_player(new_player)
        return True

class PlayerInterface:

    def __init__(self, stdscr, sio, match_code, player):
        self.player = player
        self.display = DisplayTable(stdscr)
        self.screen = stdscr
        self.delegate = BlackjackDelegate(self.handle_data)
        self.game_update = None
        self.req = None

    def render(self, game_state):
        game_state["players"] = [Player().populate(p) for p in game_state["players"]]
        game_state["dealer"] = Dealer().populate(game_state["dealer"])
        self.display.render(game_state)

    def handle_data(self, event, data):
        if event == "data":
            self.game_update = data
        elif event == "req" and data["player_id"] == self.player.id:
            self.req = data

    def run(self):
        while(True):
            if self.game_update is not None:
                self.render(self.game_update)
                self.game_update = None
            if self.req is not None:
                if self.msg['type'] == 'ch':
                    inp = self.screen.getch()
                else:
                    inp = self.screen.getstr()
                self.sio.emit('resp', {'code': self.match_code, 'player_id':self.player.id, 'data':inp})
                self.req = None



def main(stdscr):
    init_colors()
    game = Game(stdscr)
    game.run()

if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.wrapper(main)    

