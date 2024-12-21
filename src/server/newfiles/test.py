from newplayer import Player
from newlogics import roulette_logic_dict
from newroulette import Roulette
from newlogics import RouletteLogics
rules = {}

rl= RouletteLogics("1st Dozen", [])

ali = Player(500, 15, 750, 0, "martingale", rl, "1st Dozen" )

players = [ali]
rt = Roulette(players, 20000, rules, "AMERICAN_WHEEL")
rt.roulette_simulator()

ali.ov_data_printer()
