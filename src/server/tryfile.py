# A player can bet on multiple places on board
# So we need a total bet amount for each player
initial_bet = {"Bet Amount":0, "Bet Type":0, "Bet Placement":0}
total_bet = {"Total Bet Amount":0, "Balance Before Bets":0, "Balance After Bets":0, "Overall Profit":0, "Bet Condition":0}

player_balance = 1000

example_initial_bets = [{"Bet Amount":100, "Bet Type":"Red/Black", "Bet Placement":"Red"}, 
                {"Bet Amount":100, "Bet Type":"Even/Odd", "Bet Placement":"Even"}]

example_total_bet = {"Total Bet Amount": example_initial_bets[0]["Bet Amount"] + example_initial_bets[1]["Bet Amount"],
                     "Balance Before Bets": player_balance, "Balance After Bets":player_balance - example_total_bet["Total Bet Amount"],
                    "Overall Profit": 0, "Bet Condition": False}

# Bu sadece aklıma gelenleri not almam, düzenlenecek.!!!!