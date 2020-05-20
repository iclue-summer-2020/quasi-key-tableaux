#!/usr/bin/env python3.6
from flask import Flask, jsonify, request
from flask_cors import CORS
from QK import QKTableaux, consoleFn

app = Flask(__name__)
CORS(app)


@app.errorhandler(ValueError)
def handleNotInt(e):
  return str(e), 400

app.register_error_handler(400, handleNotInt)

@app.route('/solve', methods=['GET'])
def hello():
  aalpha = request.args.getlist('alpha[]')
  print(f'aalpha: {aalpha}')
  alpha = [int(x) for x in aalpha]
  qkt = QKTableaux(alpha)
  nullFn = lambda *_: None
  status, num_solutions, sample = qkt.findAllSolutions(callbackFn=nullFn)
  report = {
    'status': status,
    'num_solutions': num_solutions,
    'sample_solution': sample,
  }
  return jsonify(report)

if __name__ == '__main__':
  app.run(debug=True)
