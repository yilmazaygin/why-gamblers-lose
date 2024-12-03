import Player
import RouletteTable
import  stratsfile

rt = RouletteTable.RouletteTable(RouletteTable.european_wheel, 10000, 1)

plyr = Player.Player(300, 1, 600, 100, 'martingale', "Red")

wins = 0
loses = 0
i=0
print(plyr.current_bal)
maxBalance = 0
maxBetA = 0
minBalance = plyr.starting_bal

while i<1000:
    isPlayerBet = plyr.place_bet("Red")
    print(isPlayerBet)
    if not isPlayerBet:
        print("Current bet:", plyr.bet_history[-1]["Bet Amount"], "Current Balance:", plyr.current_bal)
        print("Game is end")
        break
    x = rt.spin_the_wheel()
    y =(rt.check_spun_number_properties(x))
    i = i + 1

    if isPlayerBet and y['Color'] == 'Red':
        plyr.current_bal += plyr.bet_history[-1]["Bet Amount"]
        plyr.bet_history[-1]["Bet Condition"] = True
    elif isPlayerBet and not(y['Color'] == 'Red'):
        plyr.current_bal -= plyr.bet_history[-1]["Bet Amount"]
        plyr.bet_history[-1]["Bet Condition"] = False


    if isPlayerBet and maxBalance < plyr.current_bal:
        maxBalance = plyr.current_bal

    if isPlayerBet and maxBetA < plyr.bet_history[-1]["Bet Amount"]:
        maxBetA = plyr.bet_history[-1]["Bet Amount"]
    
    if isPlayerBet and minBalance >= plyr.current_bal:
        minBalance = plyr.current_bal

    if isPlayerBet:
        print("Current bet:", plyr.bet_history[-1]["Bet Amount"], "Current Balance:", plyr.current_bal)
    print(y)

print(plyr.current_bal, maxBalance, maxBetA, minBalance)
