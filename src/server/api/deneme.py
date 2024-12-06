import flask
from flask import request, Response
import json
import Player
import baccarat

app = flask.Flask(__name__)

def get_param(param):
    parametre = request.args.get(param)

    if not parametre:
        flask.abort(400, f"Parameter {param} is required")
    
    return request.args.get(param)

@app.route('/baccarat', methods=['GET'])
def simulate_endpoint():
    starting_bal = get_param("starting_bal") 
    starting_bet = get_param("starting_bet")
    stop_win = get_param("stop_win")
    stop_loss = get_param("stop_loss")
    bet_amount_strategy = get_param("bet_amount_strategy")
    bet_placement_strategy = get_param("bet_placement_strategy")
    simulation_times = get_param("simulation_times")

    player = Player(starting_bal, starting_bet, stop_win, stop_loss, bet_amount_strategy, bet_placement_strategy)
    baccarat.full_baccarat_simulator(player, simulation_times)

    data = {"simulation_history": baccarat.simulation_history}
    data = json.dumps(data)
    return data

app.run(port=5000, debug=True)

