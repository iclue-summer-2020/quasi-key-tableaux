#!/usr/bin/env python3.6
import argparse
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

from multiplicity import Mult
from QK import QKTableaux, consoleFn


app = Flask(__name__)
CORS(app)


@app.errorhandler(ValueError)
def handleNotInt(e):
  return str(e), 400

app.register_error_handler(400, handleNotInt)

@app.route('/solve', methods=['GET'])
def solve():
  '''
  Finds all qkT for a given composition.

  Query Parameters:
    - alpha: a list representing the composition.
    - num_samples: the number of sample qkTs to be returned. Default is 0.

  Returns (JSON):
    {
      status: OPTIMAL/FEASIBLE/INFEASIBLE,
      num_solutions: the number of solutions,
      sample_solutions: a list of sample qkTs of length `num_samples`,
      same_weight_samples: null or a list of two sample qkT with the same wt,
    }
  '''
  aalpha = request.args.getlist('alpha[]')
  print(f'aalpha: {aalpha}')
  alpha = [int(x) for x in aalpha]
  qkt = QKTableaux(alpha)

  mult = Mult()
  nnum_samples = request.args.get('num_samples')
  num_samples = int(nnum_samples) if nnum_samples is not None else 0
  status, num_solutions, samples = qkt.findAllSolutions(
    callbackFn=mult.addT,
    num_samples=num_samples,
  )
  report = {
    'status': status,
    'num_solutions': num_solutions,
    'sample_solutions': samples,
    'same_weight_samples': mult.same_weight_samples,
  }
  return jsonify(report)


def main(args):
  app.run(
    debug=args.debug,
    host='0.0.0.0',
    port=args.port,
  )


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--debug', action='store_true')
  parser.add_argument('--port', type=int, default=5000)
  args = parser.parse_args()
  sys.exit(main(args))
