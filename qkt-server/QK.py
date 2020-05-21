#!/usr/bin/env python3.6
import numpy as np

from ortools.sat import cp_model_pb2
from ortools.sat.python import cp_model

def consoleFn(alpha, T):
  l = len(alpha)
  width = max(alpha)

  # Pretty-print the solution.
  TT = np.zeros((l, width))
  for r, t in enumerate(T):
    TT[r,:len(t)] = t
  TT = np.flipud(TT)
  print(TT)


class SolutionReporter(cp_model.CpSolverSolutionCallback):
  '''Callback class for solutions.'''
  def __init__(self, alpha, T, additional_constraints, callbackFn):
    cp_model.CpSolverSolutionCallback.__init__(self)
    self.alpha = alpha
    self.T = T
    self.vars = [v for vv in T for v in vv] + additional_constraints
    self.callbackFn = callbackFn
    self.num_solutions = 0
    self.sample_solution = None

  def on_solution_callback(self):
    '''Called when a solution is found.'''
    self.num_solutions += 1
    TT = [[self.Value(v) for v in vv] for vv in self.T]
    if self.num_solutions == 1 \
    or np.random.rand() < 1/self.num_solutions:
      self.sample_solution = TT

    self.callbackFn(self.alpha, TT)


def createModel(alpha):
  '''
  Creates a model and a quasi-key tableau skeleton from the weak composition.

  Params:
    - alpha: a 1d array of shape (l,) representing the weak composition.
  Returns:
    - a tuple (T, model) consisting of the quasi-key tableau skeleton and the
      CSP model.
  '''
  l = len(alpha)
  k = sum(alpha)

  model = cp_model.CpModel()

  # QK tableau has only positive integers.
  # (QK1, ii): Entries in row i are at most i.
  T = [
    [model.NewIntVar(1, i+1, f'T({i+1}, {j+1})') for j in range(alpha[i])]
    for i in range(l)
  ]

  return (T, model)


def addConstraints(alpha, T, model):
  '''
  Add constraints to the model.

  Params:
    - alpha: a 1d array of shape (l,) representing the weak composition.
    - T:     the quasi-key tableau skeleton.
    - model: the CSP model.
  Returns:
    - additional_constraints: a list of additional variables used.
  '''
  l = len(alpha)
  width = max(alpha)

  # (QK1 i): Entries are weakly decreasing left to right.
  for i in range(l):
    for j in range(alpha[i]-1):
      model.Add(T[i][j] >= T[i][j+1])

  # (QK2 i). Entries in each column are distinct.
  for j in range(width):
    column = [T[i][j] for i in range(l) if alpha[i] > j]
    model.AddAllDifferent(column)

  # (QK2 ii): Entries increase upward in the first column.
  locs = np.where(alpha > 0)[0]
  if locs.size != 0:
    i = locs[0]
    while True:
      llocs = np.where(alpha[i+1:] > 0)[0]
      if llocs.size == 0: break
      ii = (i+1) + llocs[0]
      model.Add(T[i][0] < T[ii][0])
      i = ii

  # (QK3): If i appears above k in the same column and i < k, then j appears
  #        immediately to the right of that k and i < j.
  # (QK3 rephrased): For any c, r < s:
  #                  if T(r, c) > T(s, c), then T(r, c+1) > T(s, c).
  additional_constraints = []
  for r in range(l):
    for s in range(r+1, l):
      c_lim = min(alpha[r]-1, alpha[s])
      for c in range(c_lim):
        b = model.NewBoolVar(f'b{len(additional_constraints)}')
        model.Add(T[r][c] > T[s][c]).OnlyEnforceIf(b)
        model.Add(T[r][c] <= T[s][c]).OnlyEnforceIf(b.Not())

        model.Add(T[r][c+1] > T[s][c]).OnlyEnforceIf(b)
        additional_constraints.append(b)
        # model.Add(q or (not p))

  # (QK4): If (r, c) and (s, c+1) for s > r are both in D(alpha), then
  #        alpha[r] < alpha[s] implies T(r, c) < T(s, c+1).
  for r in range(l):
    for s in range(r+1, l):
      c_lim = min(alpha[r], alpha[s]-1)
      for c in range(c_lim):
        if alpha[r] < alpha[s]:
          model.Add(T[r][c] < T[s][c+1])

  return additional_constraints


class QKTableaux:
  '''
  Helper class for finding quasi-key tableaux.
  '''
  def __init__(self, alpha):
    '''
    Params:
      - alpha: a 1d array of shape (l,) representing the weak composition.
    '''
    self.alpha = np.array(alpha)
    self.T, self.model = createModel(alpha)
    self.more_constraints = addConstraints(self.alpha, self.T, self.model)
    self.model.Validate()

  def findAllSolutions(self, callbackFn):
    '''
    Finds all possible quasi-key tableaux, reporting each solution to
    `callbackFn`.

    Params:
      - callbackFn: function that is called for each solution.
                    It is called with `callbackFn(alpha, T)`, where `T` is the
                    realized value of the particular quasi-key tableau.
    Returns:
      - (status, num_solutions) when done or on error.
    '''
    solver = cp_model.CpSolver()
    alpha, T = self.alpha, self.T
    sol_reporter = SolutionReporter(alpha, T, self.more_constraints, callbackFn)
    status_value = solver.SearchForAllSolutions(self.model, sol_reporter)
    status = cp_model_pb2.CpSolverStatus.Name(status_value)
    num_solutions =  sol_reporter.num_solutions
    sample_solution = sol_reporter.sample_solution
    return (status, num_solutions, sample_solution)


if __name__ == '__main__':
  # Just as an example.
  alpha = (0, 1, 2, 3, 4)
  qkt = QKTableaux(alpha)
  status, num_solutions, sample = qkt.findAllSolutions(callbackFn=consoleFn)
  print(f'Status: {status}')
  print(f'Number of solutions: {num_solutions}')
