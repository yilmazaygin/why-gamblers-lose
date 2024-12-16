import flask
from flask import request, Response
import flask_cors
import json, sys
sys.path.append("C:\\Users\\Bilgi\\OneDrive\\Masaüstü\\whygamblerslose\\src\\server")
import player, baccarat, roulette, utils

app = flask.Flask(__name__)
int_params = ["starting_bal", "starting_bet", "stop_win", "stop_loss", "simulation_times"]
str_params = ["bet_amount_strategy", "bet_placement_strategy", "bps_argument"]

flask_cors.CORS(app)

def get_param(param):
    parametre = flask.request.args.get(param)
    if not parametre:
        flask.abort(400, f"Parameter {param} is required")
    if param in int_params:
        return int(flask.request.args.get(param))
    return str(flask.request.args.get(param))

@app.route('/baccarat', methods=['GET'])
def simulate_endpoint_baccarat():
    starting_bal = (get_param("starting_bal")) 
    starting_bet = (get_param("starting_bet"))
    stop_win = (get_param("stop_win"))
    stop_loss = (get_param("stop_loss"))
    simulation_times = (get_param("simulation_times"))
    bet_amount_strategy = get_param("bet_amount_strategy")
    bet_placement_strategy = get_param("bet_placement_strategy")
    bps_argument = get_param("bps_argument")
    upper_bps_argument = bps_argument[0].upper() + bps_argument[1:]
    print(upper_bps_argument)

    ali = player.Player(starting_bal, starting_bet, stop_win, stop_loss, utils.BetAmountStrats.all_in, utils.LogicStrats.always_that, upper_bps_argument)
    bc = baccarat.Baccarat(8, [ali])
    bc.baccarat_simulator(simulation_times)

    data = {"data": bc.overall_data}
    data = json.dumps(data)
    return data
    #http://127.0.0.1:5000/baccarat&starting_bal=500&starting_bet=10&stop_win=1000&stop_loss=100&simulation_times=10&bet_amount_strategy=all_in&bet_placement_strategy=always_that&bps_argument=player

app.run(port=5000, debug=True)

