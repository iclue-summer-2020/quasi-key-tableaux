#!/usr/bin/env python3.6
import argparse
import itertools
import numpy as np

from collections import defaultdict
from QK import QKTableaux, consoleFn

# I am making an assumption that a 0 cannot be marked.
# If it can, I assume I can just add one to each of these bad pattern.
# Now, a number is "marked" iff it is negative.
KM = [(0, 1, 2), (0, 0, 2, 2), (0, 0, 2, 1), (1, 0, 3, 2), (1, 0, 2, 2)]
KMP = [(0, 2, 4), (1, 0, 4, 3), (0, 1, 4, 3), (1, 0, 3, 4), (0, 1, 3, 4)]
ZP = [(1, 0, 3, 3), (0, 0, 2, 2), (0, 0, 3, 2), (0, 1, 3, 3), (0, 0, 2, 3)]

def compositions(k, max_width, unique=False, zeros=False):
  '''
  Generates every weak composition a = (a_1,...,a_l) where:
    - l <= max_width,
    - sum of a_i's is exactly k,
    - a_i > 0.
  '''
  c = [0] * max_width
  def comp(k, w):
    if k == 0:
      if not (unique and len(set(c[:w])) < w):
        yield tuple(c[:w])
    if w == max_width or k < 0:
      yield from ()
      return

    for j in range(int(not zeros), k+1):
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

def cc(a, b, j):
  '''
  Helper method for the `contains` function.
  `j` - is an array which stores the indices. i.e., a[j[s]] is to get the
        corresponding value of b[s].
  '''
  m = len(b)

  # Check the marked property.
  for s in range(m):
    if b[s] < 0 and j[s] >= 1 and a[j[s]] < a[j[s]-1] + 2:
      return False

  # Check the normal properties.
  for s in range(m):
    for t in range(m):
      # Get the magnitude of the bad pattern elements.
      bs, bt = abs(b[s]), abs(b[t])
      if (a[j[s]] <= a[j[t]]) != (bs <= bt): return False
      if abs(a[j[s]]-a[j[t]]) < abs(bs-bt): return False
  return True

def contains(alpha, b):
  '''
  Returns True if alpha contains the composition pattern b.
  '''
  n = len(alpha)
  m = len(b)
  for indices in itertools.combinations(range(n), m):
    j = np.array(indices)
    if cc(alpha, b, j): return True
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
    self.same_weight_samples = None

  def addT(self, alpha, TT):
    l = len(alpha)
    width = max(alpha)

    T = np.zeros((l, width), dtype=np.int32)
    for r, t in enumerate(TT):
      T[r,:len(t)] = t
    w = wt(T)
    ww = tuple(w)
    Ts = self.wts[ww]
    Ts.append(TT)

    if len(Ts) > 1 and self.same_weight_samples is None:
      # We found two tableaux with the same weight.
      # Notice that there will be exactly two samples returned if the
      # composition is not multiplicity free.
      self.same_weight_samples = Ts


def multFree(alpha):
  '''
  Returns True if D(alpha) is multiplicity free.
  '''
  qkt = QKTableaux(alpha)
  mult = Mult()
  status, num_solutions, samples = qkt.findAllSolutions(callbackFn=mult.addT)
  return len(mult.wts) == num_solutions


def multiplicities(alpha):
  '''
  Displays wt(T) for all T in qKT(alpha).
  '''
  qkt = QKTableaux(alpha)
  mult = Mult()
  status, num_solutions, samples = qkt.findAllSolutions(callbackFn=mult.addT)
  print(f'Status: {status}')
  print(f'Number of solutions: {num_solutions}')
  print(f'len of mult: {len(mult.wts)}')
  for w, Ts in mult.wts.items():
    print(w, Ts)


def multFreeCheck(k, max_width):
  for a in compositions(k, max_width):
    alpha = np.array(a)
    mf = multFree(alpha)

    # This is just to see which types of compositions are multiplicity free.
    if not mf:
      print(f'not multiplicity free: {alpha}')

def anomallyCheck(k, max_width):
  '''
  The following was proven to be true.
  '''
  for a in compositions(k, max_width):
    alpha = np.array(a)
    mf = multFree(alpha)

    # We know that if alpha avoids KM, then D(alpha) is multiplicity free.
    if avoidsAll(alpha, KM) and not mf:
      print(f'anomally: {alpha}')

def hypo1(k, max_width):
  for a in compositions(k, max_width):
    alpha = np.array(a)
    mf = multFree(alpha)

    # Next, we check if the converse is true.
    # We are only interested in multiplicity-free compositions.
    if not mf: continue
    contained_pats = [
      pattern
      for pattern in KM
      if not avoids(alpha, pattern)
    ]
    if contained_pats:
      print(f'counterexample: {alpha}; contains patterns: {contained_pats}.')

def hypo2(k, max_width):
  for a in compositions(k, max_width, unique=True):
    alpha = np.array(a)
    mf = multFree(alpha)

    if avoidsAll(alpha, KMP) and not mf:
      print(alpha)

def hypo3(k, max_width):
  for a in compositions(k, max_width, unique=True):
    alpha = np.array(a)
    mf = multFree(alpha)

    if avoidsAll(alpha, KMP) and not mf:
      print(alpha)

def hypo4(k, max_width):
  for a in compositions(k, max_width, unique=True):
    alpha = np.array(a)
    mf = multFree(alpha)

    # Next, we check if the converse is true.
    # We are only interested in multiplicity-free compositions.
    if not mf: continue
    contained_pats = [
      pattern
      for pattern in KMP
      if not avoids(alpha, pattern)
    ]
    if contained_pats:
      print(f'counterexample: {alpha}; contains patterns: {contained_pats}.')


def hypo5(k, max_width):
  QKM = KMP + ZP
  for a in compositions(k, max_width, unique=False):
    alpha = np.array(a)
    mf = multFree(alpha)

    if avoidsAll(alpha, QKM) and not mf:
      print(alpha)

def hypo6(k, max_width):
  QKM = KMP + ZP
  for a in compositions(k, max_width, unique=False):
    alpha = np.array(a)
    mf = multFree(alpha)

    # Next, we check if the converse is true.
    # We are only interested in multiplicity-free compositions.
    if not mf: continue
    contained_pats = [
      pattern
      for pattern in QKM
      if not avoids(alpha, pattern)
    ]
    if contained_pats:
      print(f'counterexample: {alpha}; contains patterns: {contained_pats}.')

def hypo7(k, max_width):
  for a in compositions(k, max_width, unique=True, zeros=True):
    alpha = np.array(a)
    mf = multFree(alpha)

    if avoidsAll(alpha, KMP) and not mf:
      print(alpha)

def hypo8(k, max_width):
  # Negative values are "marked".
  MP = [
    (0,-2,-4),(1,0,-4,3),(0,1,-4, 3),(1,0,-3,4),(0,1,-3,4),
    (1,0,-3,3),(0,0,-2,2),(0,0,-3,2),(0,1,-3,3),(0,0,-2,3),
  ]
  for a in compositions(k, max_width, unique=False):
    alpha = np.array(a)
    mf = multFree(alpha)

    if avoidsAll(alpha, MP) and not mf:
      print(alpha)

def main(args):
  hypo8(args.k, args.max_width)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-k', type=int, required=True)
  parser.add_argument('-w', '--max-width', type=int, required=True)
  args = parser.parse_args()

  main(args)
