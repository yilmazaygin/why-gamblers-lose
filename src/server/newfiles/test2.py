# TEST FILE FOR BACCARAT SIMULATOR

from newplayer import Player
from newlogics import BaccaratLogics
from newbaccarat import Baccarat
from newutils import default_rules

rules = {}
ali = Player("AMYAKAN", 500, 15, 750, 0, "martingale", BaccaratLogics.always_that, "Banker" )
veli = Player("VELI", 500, 15, 750, 0, "reverse_martingale", BaccaratLogics.always_that, "Player" )
players = [ali, veli]

bc = Baccarat(players, 5000, default_rules, 4)
bc.baccarat_simulator()
ali.ov_data_printer()

print(bc.datamaster())
