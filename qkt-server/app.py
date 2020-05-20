#!/usr/bin/env python3.6
from flask import Flask, jsonify, request
from QK import QKTableaux, consoleFn

app = Flask(__name__)

@app.errorhandler(ValueError)
def handleNotInt(e):
  return str(e), 400

app.register_error_handler(400, handleNotInt)

@app.route('/solve', methods=['GET'])
def hello():
  aalpha = request.args.getlist('alpha[]')
  alpha = [int(x) for x in aalpha]
  qkt = QKTableaux(alpha)
  (status, num_solutions) = qkt.findAllSolutions(callbackFn=consoleFn)
  report = {
    'status': status,
    'num_solutions': num_solutions,
  }
  return jsonify(report)

if __name__ == '__main__':
  app.run(debug=True)
