# TEST FILE FOR ROULETTE SIMULATOR

from newplayer import Player
from newlogics import roulette_logic_dict
from newroulette import Roulette
from newlogics import RouletteLogics
from newutils import default_rules

rl= RouletteLogics("1st Dozen", [])

ali = Player("MALAVURAN", 500, 15, 750, 0, "martingale", rl, "1st Dozen" )
veli = Player("VELI", 500, 15, 750, 0, "reverse_martingale", rl, "1st Dozen" )

players = [ali, veli]
rt = Roulette(players, 5000, default_rules, "AMERICAN_WHEEL")
rt.roulette_simulator()

print(rt.datamaster_data)
