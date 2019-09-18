from __future__ import unicode_literals
import unittest
import re
import sys
import pycodestyle

try:
  from fuzzywuzzy.StringMatcher import StringMatcher 
except ImportError:
    if platform.python_implementation() != "PyPy":
        warnings.warn('Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning')
    from difflib import SequenceMatcher

def intr(n):
  return int(round(n))

class StringMatcherTest(unittest.TestCase):
  def setUp(self):
    self.s1 = "new york mets"
    self.s1a = "new york mets"
    self.s2 = "new YORK mets"
    self.s3 = "the wonderful new york mets"
    self.s4 = "new york mets vs atlanta braves"
    self.s5 = "atlanta braves vs new york mets"
    self.s6 = "new york mets - atlanta braves"
    self.s7 = 'new york city mets - atlanta braves'
    # test silly corner cases
    self.s8 = '{'
    self.s8a = '{'
    self.s9 = '{a'
    self.s9a = '{a'
    self.s10 = 'a{'
    self.s10a = '{b'

  def tearDown(self):
    pass

  def testEqual(self):
    m = StringMatcher(None, self.s1, self.s1a)
    Ratio = m.ratio()
    self.assertEqual(intr(100*Ratio), 100)

    m = StringMatcher(None, self.s8, self.s8a)
    Ratio = m.ratio()
    self.assertEqual(intr(100*Ratio), 100)

    m = StringMatcher(None, self.s9, self.s9a)
    Ratio = m.ratio()
    self.assertEqual(intr(100*Ratio), 100)

  def testCaseInsensitive(self):
    m = StringMatcher(None, self.s1, self.s2)
    Ratio = m.ratio()
    self.assertNotEqual(intr(100*Ratio), 100)

  def testPartialRatio(self):
    if len(self.s1) <= len(self.s3):
      shorter = self.s1
      longer = self.s3
    else:
      shorter = self.s3
      longer = self.s1

    m = StringMatcher(None, shorter, longer)
    blocks = m.get_matching_blocks()
    # each block represents a sequence of matching characters in a string
    # of the form (idx_1, idx_2, len)
    # the best partial match will block align with at least one of those blocks
    #   e.g. shorter = "abcd", longer = XXXbcdeEEE
    #   block = (1,3,3)
    #   best score === ratio("abcd", "Xbcd")
    scores = []
    for block in blocks:
      long_start = block[1] - block[0] if (block[1] - block[0]) > 0 else 0
      long_end = long_start + len(shorter)
      long_substr = longer[long_start:long_end]

      m2 = StringMatcher(None, shorter, long_substr)
      r = m2.ratio()
      if r > .995:
          return 100
      else:
          scores.append(r)

    self.assertEqual(intr(100*max(scores)), 100)

if __name__ == "__main__":
  unittest.main()


