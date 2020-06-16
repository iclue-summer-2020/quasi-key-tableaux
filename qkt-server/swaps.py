#!/usr/bin/env python3.6
import argparse
import sys

from collections import defaultdict
from multiplicity import Mult
from QK import QKTableaux


def dom(ax, bx):
  '''Returns whether or not `ax` dominates `bx` (<=).'''
  assert len(ax) == len(bx), (len(ax), len(bx))
  asum = 0
  bsum = 0
  for a, b in zip(ax, bx):
    asum += a
    bsum += b
    if asum > bsum: return False
  return True

def lswap(ax):
  '''
  Returns all possible left swaps iteratively.
  Since the number of left swaps can be factorial in the length of `ax`,
  this function can be slow.
  '''
  possible = set()
  seen = set()
  n = len(ax)
  comp = list(ax)

  def _lswap(i):
    tcomp = tuple(comp)
    if (tcomp, i) in seen: return
    possible.add(tcomp)
    seen.add((tcomp, i))

    if i >= n: return

    _lswap(i+1)
    for j in range(i+1, n):
      if comp[i] < comp[j]:
        oci, ocj = comp[i], comp[j]
        comp[i], comp[j] = comp[j], comp[i]
        _lswap(0)
        comp[i], comp[j] = oci, ocj
    return

  _lswap(0)
  return possible


def flat(ax):
  '''Given a composition `ax`, removes any zeros.'''
  return tuple(p for p in ax if p != 0)


def qlswap(ax):
  '''
  Keep only the most dominate compositions in the same equivalency classes of
  `flat`. The following code uses the fact that the relation `dom` is
  transitive.
  '''
  flats = {}
  for comp in lswap(ax):
    fcomp = flat(comp)
    if fcomp not in flats or dom(comp, flats[fcomp]):
      flats[fcomp] = comp
  return set(flats.values())

def kappa(ax):
  '''
  Given a composition `ax`, computes the sum of quasi-key polynomials
  of `qlswap(ax)`. For now, this polynomial will be represented as a dictionary
  mapping each non-zero power to its coefficient.
  '''
  M = max(ax)
  def pad(w):
    return w + (0,)*((M+1)-len(w))
  poly = defaultdict(int)
  for bx in qlswap(ax):
    qkt = QKTableaux(bx)
    mult = Mult()
    status, num_solutions, samples = qkt.findAllSolutions(callbackFn=mult.addT)
    for w, Ts in mult.wts.items():
      # Remove 0's from front since it is always zero.
      poly[pad(w)[1:]] += len(Ts)
  return dict(poly)


def main(args):
  print(kappa(args.a))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description='Print \\kappa_{\\alpha}',
    epilog='Example: python3.6 swaps.py -a 0 3 2',
  )
  parser.add_argument('-a', type=int, nargs='+')
  args = parser.parse_args()
  sys.exit(main(args))
