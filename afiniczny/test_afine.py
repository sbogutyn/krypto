#!/usr/bin/env python
import unittest
import afine

class TestAfiniczneSzyfrowanie(unittest.TestCase):
	
	def setup(self):
		pass

	def test_szyfruj_litere(self):
		self.assertEqual('b', afine.zaszyfruj_litere('a', 1, 1))
	
	def test_bledne_szyfrowanie_litery(self):
		self.assertNotEqual('b', afine.zaszyfruj_litere('a', 5, 5))
	
	def test_szyfruj_tekst(self):
		self.assertEqual("bcd", afine.zaszyfruj_tekst("abc", 1, 1))
	
	def test_nwd(self):
		self.assertEqual(1, afine.nwd(1, 26))
		self.assertEqual(1, afine.nwd(3, 26))
		self.assertEqual(1, afine.nwd(5, 26))
	



if __name__ == "__main__":
	unittest.main()