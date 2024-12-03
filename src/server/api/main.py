import flask
from flask import request, Response
import json
import sys
sys.path.append("C:\\Users\\Bilgi\\OneDrive\\Masaüstü\\whygamblerslose\\src\\server")
import simulator

app = flask.Flask(__name__)

int_params = ["starting_bet", "starting_balance", "stop_win", "stop_loss", "max_bet", "min_bet", "simulation_count", "max_rounds"]

def get_param(param):
    parametre = request.args.get(param)
    if not parametre:
        flask.abort(400, f"Parameter {param} is required")
    if param in int_params:
        try:
            parametre = int(request.args.get(param))
            return parametre
        except ValueError:
            flask.abort(400, f"Parameter {param} must be a positive integer")

    elif param == "strategy":
        if parametre not in ["martingale", "d'alembert", "labouchere"]:
            flask.abort(400, f"Parameter {param} must be one of martingale, d'alembert, labouchere")
    elif param == "bet_color":
        if parametre not in ["red", "black"]:
            flask.abort(400, f"Parameter {param} must be one of red, black")
    elif param == "wheel_type":
        if parametre not in ["european", "american", "triplezero"]:
            flask.abort(400, f"Parameter {param} must be one of european, american, triplezero")
    return request.args.get(param)


@app.route('/roulette', methods=['GET'])
def simulate_endpoint():

    starting_bet = get_param("starting_bet")
    starting_balance = get_param("starting_balance")
    stop_win = get_param("stop_win")
    stop_loss = get_param("stop_loss")
    strategy = get_param("strategy")
    bet_color = get_param("bet_color")
    wheel_type = get_param("wheel_type")
    max_bet = get_param("max_bet")
    min_bet = get_param("min_bet")
    simulation_count = get_param("simulation_count")

    max_rounds = get_param("max_rounds")
    sim = simulator.Simulator(starting_bet, starting_balance, stop_win, stop_loss, strategy, bet_color, wheel_type, max_bet, min_bet, simulation_count, max_rounds)
    
    sim_out = sim.simualte_all()
    data = {'balance_list': sim_out, "wins": sim.wins, "loses": sim.loses, "ties": sim.ties}
    data = json.dumps(data)
    return data

app.run(port=5000, debug=True)


