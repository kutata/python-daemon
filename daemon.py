#!/usr/bin/env python

import sys
from os import listdir, execv, execl, kill
from os.path import getmtime, isfile, join
import signal

def listmydir():
  onlyFiles = [f for f in listdir('./') if isfile(join('./', f))]
  return onlyFiles

FILES = listmydir()
FILES_MTIMES = [(f, getmtime(f)) for f in FILES]

import time
from subprocess import call, Popen

p = None
pid = None

if len(sys.argv) > 2:
  pid = int(sys.argv[2])

try:
  if pid is not None:
    kill(pid, signal.SIGTERM)

  p = Popen(['python', sys.argv[1]])

except KeyboardInterrupt:
  print KeyboardInterrupt

try:
  while True:
    for f, mtime in FILES_MTIMES:
      if getmtime(f) != mtime:
        print('--------- restarted --------')
        if p is None:
          execv(__file__, sys.argv)
        else:
          argv = sys.argv[:2] + [str(p.pid)]
          execv(__file__, argv)

    time.sleep(1)

except KeyboardInterrupt:
  p.kill()
  print '\nStoped'
