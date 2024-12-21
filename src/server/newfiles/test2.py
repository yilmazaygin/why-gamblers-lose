from newplayer import Player
from newlogics import BaccaratLogics
from newbaccarat import Baccarat

rules = {}

ali = Player(500, 15, 750, 0, "martingale", BaccaratLogics.always_that, "Banker" )

players = [ali]

bc = Baccarat(players, 5000, rules, 4)
bc.baccarat_simulator()
ali.ov_data_printer()