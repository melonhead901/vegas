#!/usr/bin/python

import os
import subprocess

for alpha in range(1,5):
  alpha *= 0.1
  ps = []
  for discount in range(0,5):
    discount *= 0.1
    for epsilon in range(1,4):
      epsilon *= 0.1
      filename = 'q_%.1f_%.1f_%.1f.out' % (alpha, discount, epsilon)
      if not os.path.exists(filename):
        ps.append(subprocess.Popen(['python', 'game.py', '-t10000', '-r1000', '-a%.1f' % alpha, '-d%.1f' % discount, '-e%.1f' % epsilon, '-pQLearningAgent'], stdout=open(filename, 'w')))
  for p in ps:
    p.wait()
