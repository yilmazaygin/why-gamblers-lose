import flask
from flask import request, Response

import json, sys
sys.path.append("C:\\Users\\Bilgi\\OneDrive\\Masaüstü\\whygamblerslose\\src\\server")
import Player, baccarat, roulette

import json
import sys
import flask_cors

import Player
import baccarat
from betamountstrats import betamountstrats_dict
from baccarat import baccarat_logics_dict
from roulette import roulette_logics_dict


app = flask.Flask(__name__)
int_params = ["starting_bal", "starting_bet", "stop_win", "stop_loss", "simulation_times"]
str_params = ["bet_amount_strategy", "bet_placement_strategy", "bps_argument"]

flask_cors.CORS(app)


def get_param(param):
    parametre = request.args.get(param)
    if not parametre:
        flask.abort(400, f"Parameter {param} is required")
    if param in int_params:
        return int(request.args.get(param))
    return request.args.get(param)

@app.route('/baccarat', methods=['GET'])
def simulate_endpoint_baccarat():
    starting_bal = (get_param("starting_bal")) 
    starting_bet = (get_param("starting_bet"))
    stop_win = (get_param("stop_win"))
    stop_loss = (get_param("stop_loss"))
    simulation_times = (get_param("simulation_times"))
    bet_amount_strategy = get_param("bet_amount_strategy")
    bet_placement_strategy = get_param("bet_placement_strategy")

    plyr = Player.Player(starting_bal, starting_bet, stop_win, stop_loss, betamountstrats_dict[bet_amount_strategy], baccarat_logics_dict[bet_placement_strategy], None)
    bc = baccarat.Baccarat(plyr)
    bc.full_baccarat_simulator(plyr, simulation_times)

    data = {"simulation_history": bc.simulation_history}
    data = json.dumps(data)
    return data
    # http://127.0.0.1:5000/baccarat?starting_bal=500&starting_bet=10&stop_win=550&stop_loss=400&bet_amount_strategy=all_in&simulation_times=2&bet_placement_strategy=random_player_or_banker

@app.route('/roulette', methods=['GET'])
def simulate_endpoint_roulette():
    starting_bal = (get_param("starting_bal")) 
    starting_bet = (get_param("starting_bet"))
    stop_win = (get_param("stop_win"))
    stop_loss = (get_param("stop_loss"))
    simulation_times = (get_param("simulation_times"))
    bet_amount_strategy = get_param("bet_amount_strategy")
    bet_placement_strategy = get_param("bet_placement_strategy")
    bps_argument = get_param("bps_argument")
    #wheel_type = get_param("wheel_type")

    rl = roulette.Roulette(roulette.Roulette.european_wheel)
    plyr = Player.Player(starting_bal, starting_bet, stop_win, stop_loss, betamountstrats_dict[bet_amount_strategy], roulette_logics_dict[bet_placement_strategy], bps_argument)
    rl.full_roulette_simulator(plyr, simulation_times)

    data = {"simulation_history": rl.simulation_history,
            "won_games_count": rl.overall_wins,
            "lost_games_count": rl.overall_losses,
            "total_wager": rl.overall_wager,
            "overall_profit": rl.overall_gain,
            "sims_ended_in_profit": rl.won_sims,
            "sims_ended_in_loss": rl.lost_sims
            }
    
    data = json.dumps(data)
    return data
    # http://127.0.0.1:5000/roulette?starting_bal=500&starting_bet=10&stop_win=550&stop_loss=400&bet_amount_strategy=martingale&simulation_times=2&bet_placement_strategy=random_that&bps_argument=odd_even

app.run(port=5000, debug=True)