from skull import Game

name = "na"
names = []

while name != '':
    name = str(input("Enter player name: "))
    if name != '':
        names.append(name)
        

print("------------")

g = Game( names )

def choose_player_index(prompt):
    print(prompt)
    for i in range(len(g.players)):
        print(f"\t{i+1}. {g.players[i].name}")
    result = input("Pick a player: ")
    
    return int(result) - 1

while not g.complete():
    print(g)
    g.current_player_index = choose_player_index("Who started the bid?")
    while not g.bid_complete():
        print(g)
        action = input(f"{g.current_player().name}, enter number to bid, - to pass: ")

        if action == '-':
            g.current_player_pass()
        else:
            try:
                bid = int(action)
                g.current_player_raise(bid)
            except ValueError:
                print("ugh... enter a number!!")
            except:
                print("Did you *actually* raise?")
    
    print(f"{g.current_player().name} has to find {g.current_bid} flowers.")
    action = input('Did they succeed? [yn]: ')
    if action == 'y':
        g.search_succeeded()
    else:
        g.search_failed()

print("Game over!")
print(f"{g.winner().name} has won!")