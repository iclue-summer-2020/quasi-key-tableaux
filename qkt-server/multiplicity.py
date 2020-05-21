#!/usr/bin/env python3.6
import argparse
import itertools
import numpy as np

from collections import defaultdict
from QK import QKTableaux, consoleFn


def compositions(k, max_width):
  '''
  Generates every weak composition a = (a_1,...,a_l) where:
    - l <= max_width,
    - sum of a_i's is exactly k,
    - a_i > 0.
  '''
  c = [0] * max_width
  def comp(k, w):
    if k == 0: yield tuple(c[:w])
    if w == max_width or k < 0:
      yield from ()
      return

    for j in range(1, k+1):
      old, c[w] = c[w], j
      yield from comp(k-j, w+1)
      c[w] = old

    yield from ()
  yield from comp(k, 0)


def wt(T):
  '''
  Returns wt(T) where T is some member of qKT(alpha).
  Note that T must be a numpy array.
  '''
  B = np.bincount(T.flatten())
  # We don't really need to do this (I think).
  B[0] = 0
  return B

def cc(a, b):
  '''Helper method for the `contains` function.'''
  m = len(b)
  for s in range(m):
    for t in range(m):
      if (a[s] <= a[t]) != (b[s] <= b[t]): return False
      if abs(a[s]-a[t]) < abs(b[s]-b[t]): return False
  return True

def contains(alpha, b):
  '''
  Returns True if alpha contains the composition pattern b.
  '''
  n = len(alpha)
  m = len(b)
  for indices in itertools.combinations(range(n), m):
    a = alpha[np.array(indices)]
    if cc(a, b): return True
  return False

def avoids(alpha, b):
  return not contains(alpha, b)

def avoidsAll(alpha, bs):
  return all(avoids(alpha, b) for b in bs)

class Mult:
  '''
  Helper class for bucketing each T by wt(T).
  '''
  def __init__(self):
    self.wts = defaultdict(list)

  def addT(self, alpha, TT):
    l = len(alpha)
    width = max(alpha)

    T = np.zeros((l, width), dtype=np.int32)
    for r, t in enumerate(TT):
      T[r,:len(t)] = t
    w = wt(T)
    self.wts[tuple(w)].append(T)


def multFree(alpha):
  '''
  Returns True if D(alpha) is multiplicity free.
  '''
  qkt = QKTableaux(alpha)
  mult = Mult()
  status, num_solutions, sample = qkt.findAllSolutions(callbackFn=mult.addT)
  return len(mult.wts) == num_solutions


def multiplicities(alpha):
  '''
  Displays wt(T) for all T in qKT(alpha).
  '''
  qkt = QKTableaux(alpha)
  mult = Mult()
  status, num_solutions, sample = qkt.findAllSolutions(callbackFn=mult.addT)
  print(f'Status: {status}')
  print(f'Number of solutions: {num_solutions}')
  print(f'len of mult: {len(mult.wts)}')
  for w, Ts in mult.wts.items():
    print(w, Ts)


def main(args):
  KM = [(0, 1, 2), (0, 0, 2, 2), (0, 0, 2, 1), (1, 0, 3, 2), (1, 0, 2, 2)]
  for a in compositions(args.k, args.max_width):
    alpha = np.array(a)
    mf = multFree(alpha)

    # We know that if alpha avoids KM, then D(alpha) is multiplicity free.
    if avoidsAll(alpha, KM) and not mf:
      print(f'anomally: {alpha}')

    # Next, we check if the converse is true.
    if mf and not avoidsAll(alpha, KM):
      print(f'counterexample: {alpha}')

if __name__ == '__main__':
  # multiplicities((10, 5, 12, 9, 8, 8, 4, 2, 5, 1, 3))
  # multiplicities(np.array([0, 1, 3, 0]))

  parser = argparse.ArgumentParser()
  parser.add_argument('-k', type=int, required=True)
  parser.add_argument('-w', '--max-width', type=int, default=None)
  args = parser.parse_args()

  main(args)
