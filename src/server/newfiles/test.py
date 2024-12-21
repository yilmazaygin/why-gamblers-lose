# TEST FILE FOR ROULETTE SIMULATOR

from newplayer import Player
from newlogics import roulette_logic_dict
from newroulette import Roulette
from newlogics import RouletteLogics
rules = {}

rl= RouletteLogics("1st Dozen", [])

ali = Player("MALAVURAN", 500, 15, 750, 0, "martingale", rl, "1st Dozen" )
veli = Player("VELI", 500, 15, 750, 0, "reverse_martingale", rl, "1st Dozen" )
cemil = Player("CEMIL", 500, 15, 750, 0, "flat_bet", rl, "1st Dozen" )

players = [ali, veli, cemil]
rt = Roulette(players, 20, rules, "AMERICAN_WHEEL")
rt.roulette_simulator()

ali.ov_data_printer()
veli.ov_data_printer()
cemil.ov_data_printer()

print(rt.datamaster())
