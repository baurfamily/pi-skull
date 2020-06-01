from random import choice, randrange

class Player:
    def __str__(self):
        if self.passed:
            status = "(passed)"
        else:
            status = "(active)"
        return f"-{self.score}- {self.name} {status}: {self.bid}"
        
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.fail_count = 0
        self.passed = False
        self.bid = 0
        
    def raise_bid(self, amount):
        self.bid = amount
        
    def pass_turn(self):
        self.bid = 0
        self.passed = True
    
    def succeed(self):
        self.score += 1
        self.reset()
        
    def fail(self):
        self.fail_count += 1
        self.reset()
    
    def reset(self):
        self.bid = 0
        self.passed = False

        
class Game:
    def __str__(self):
        str = ""
        str += f"Current Player: {self.current_player().name}\n"
        str += f"Current bid: {self.current_bid}"
        str += "\n"
        str += f"There are {len(self.players)} players.\n"
        for p in self.players:
            str += f"\t{p}\n"
            
        return str
        
    """players should be an ordered array of names"""
    def __init__(self, names):
        self.players = [Player(n) for n in names]
        self.current_player_index = randrange(len(self.players))
        self.next_round()
        
    def current_player(self):
        return self.players[self.current_player_index]
        
    def complete(self):
        return any(p.score == 2 for p in self.players)
    
    def bid_complete(self):
        return self._bid_complete
    
    def winner(self):
        return [p for p in self.players if p.score == 2][0]
    
    def next_turn(self):
        remaining = list(filter(lambda p: not p.passed, self.players))
        if len(remaining) == 1:
            last_player = remaining[0]
            self.current_player_index = self.players.index(last_player)
            return None
            
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        if self.current_player().passed:
            self.next_turn()

        return self.current_player()
        
    def current_player_pass(self):
        self.current_player().pass_turn()
        player = self.next_turn()
        if player == None:
            self._bid_complete = True
    
    def current_player_raise(self, amount):
        if amount <= self.current_bid:
            raise Exception(f"Raised amount ({amount}) cannot be less than current bid ({self.current_bid}).")
            
        self.current_bid = amount
        player = self.current_player().raise_bid(amount)
        self.next_turn()
        
    def search_succeeded(self):
        self.current_player().succeed()
        self.next_round()
        
    def search_failed(self):
        self.current_player().fail()
        self.next_round()
            
    def next_round(self):
        self.current_bid = 0
        self._bid_complete = False
        for p in self.players:
            p.reset()
    