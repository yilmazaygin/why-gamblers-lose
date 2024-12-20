from newplayer import Player
from newlogics import roulette_logic_dict
from newroulette import Roulette

ali = Player(500, 10, 1000, 0, "martingale", roulette_logic_dict["random_color"], None )
veli = Player(500, 15, 1500, 0, "martingale", roulette_logic_dict["last_color_again"], None )

players = [ali, veli]
rt = Roulette(players, 100, "AMERICAN_WHEEL")
rt.roulette_simulator()

ali.ov_data_printer()
veli.ov_data_printer()