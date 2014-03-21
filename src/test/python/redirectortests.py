import unittest
from kairos import redirector

class RedirectorTestCase(unittest.TestCase):
	def setUp(self):
		print "setUp"
		
	def tearDown(self):
		print "tearDown"
		
	def testOne(self):
		print "Test one"
		
	def testTwo(self):
		print "Test two"


if __name__ == "__main__":
	unittest.main()
