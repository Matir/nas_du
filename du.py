from __future__ import division
import os
import os.path
import sys
import time

class DULED(object):
  SIDES = ['left', 'right']

  def __init__(self, path):
    self._path = path
    self.roll()

  def run(self):
    while True:
      used = self.percent_used()
      print "%0.0f%% used" % used
      self.setpct(used)
      time.sleep(10)

  def percent_used(self):
    try:
      stat = os.statvfs(self._path)
    except OSError:
      self.blink()
      raise
    return (1 - (stat.f_bavail / stat.f_blocks)) * 100

  def setpct(self, percent):
    if percent > 95:
      self.blink()
      return
    for i in xrange(0, 8):
      cutoff = (i / 8) * 100
      if percent > cutoff:
        self._ledon(i)
      else:
        self._ledoff(i)

  def blink(self):
    for i in xrange(0, 8):
      self._ledblink(i)

  def roll(self):
    for i in xrange(0, 8):
      self._ledon(i)
      time.sleep(0.250)
    for i in xrange(0, 8):
      self._ledoff(i)
      time.sleep(0.250)

  def _ledpath(self, led):
    if not 0 <= led <= 7:
      raise ValueError("0 <= led <= 7")
    side = DULED.SIDES[led // 4]
    led = led % 4
    return "/sys/class/leds/status:white:%s%d" % (side, led)

  def _ledwrite(self, led, state, target="trigger"):
    path = self._ledpath(led)
    path = os.path.join(path, target)
    open(path, "w").write(state)

  def _ledon(self, led):
    self._ledwrite(led, 'default-on')

  def _ledoff(self, led):
    self._ledwrite(led, 'none')

  def _ledblink(self, led):
    self._ledwrite(led, 'timer')
    self._ledwrite(led, '250', 'delay_on')
    self._ledwrite(led, '250', 'delay_off')


def main(argv):
  if len(argv) < 2:
    sys.stderr.write("Usage: %s <filesystem>\n")
    sys.exit(1)
  du = DULED(argv[1])
  du.run()

if __name__ == "__main__":
  main(sys.argv)
