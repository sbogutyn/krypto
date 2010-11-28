#!/usr/bin/env python -v
# -*- coding: utf-8 -*-

import unittest
import vigner


class TestSzyfrowanieVignera(unittest.TestCase):
	# Testujemy moduł vigner
	def setup(self):
		pass

	# Testuje czy program prawidłowo przygotowuje tekst 
	# (zamienia wszystko na male litery i usuwa to co nie jest litera)
	def test_przygotuj_tekst(self):
		self.assertEqual('testowyprzypadek', vigner.przygotuj_tekst('&Te3[]stowy P93820rz9098yp....ad____e+_+_//k'))
		self.assertEqual('zolw', vigner.przygotuj_tekst('żzóołlw'))
		self.assertEqual('test', vigner.przygotuj_tekst('(TEST)'))
	
	# Szyfruje pojedyncza litere
	def test_zaszyfruj_litere(self):
		klucz = ['s', 'e', 'c', 'r', 'e', 't']
		tekst = ['n', 'a', 'm', 'e', 't', 'e']
		oczekiwany_wynik = ['f', 'e', 'o', 'v', 'x', 'x']
		for i in range(len(klucz)):
			self.assertEqual(oczekiwany_wynik[i], vigner.zaszyfruj_litere(tekst[i], klucz[i]))

	# Szyfruje cały tekst
	def test_zaszyfruj_tekst(self):
		klucz = "secret"
		tekst = "namete"
		oczekiwany_wynik = "feovxx"
		self.assertEqual(oczekiwany_wynik, vigner.zaszyfruj_tekst(tekst, klucz))

	def test_odszyfruj_litere(self):
		klucz = ['s', 'e', 'c', 'r', 'e', 't']
		oczekiwany_wynik = ['n', 'a', 'm', 'e', 't', 'e']
		zaszyfrowany_tekst = ['f', 'e', 'o', 'v', 'x', 'x']
		for i in range(len(klucz)):
			self.assertEqual(oczekiwany_wynik[i], vigner.odszyfruj_litere(zaszyfrowany_tekst[i], klucz[i]))

	# Próbuje odszyfrować tekst
	def test_odszyfruj_tekst(self):
		klucz = "secret"
		oczekiwany_wynik = "namete"
		zaszyfrowany_tekst = "feovxx"
		self.assertEqual(oczekiwany_wynik, vigner.odszyfruj_tekst(zaszyfrowany_tekst, klucz))

	# Testujemy przesunięcie całego tekstu o zadaną ilość znaków (te które wyjdą poza zakres dopisywane są na początek)
	def test_przesun_tekst(self):
		tekst = "alamakota"
		oczekiwany_wynik = "aalamakot"
		self.assertEqual(vigner.przesun_tekst(tekst, 1), oczekiwany_wynik)
		self.assertEqual(vigner.przesun_tekst("testprzesuniecia", 5), "ieciatestprzesun")
	
	def test_ilosc_tych_samych_liter_na_tych_samych_pozycjach(self):
		pierwszy =  "alamakota"
		drugi	 =  "akamarota"
		oczekiwany_wynik = 7
		self.assertEqual(vigner.sprawdz_ilosc_powtorzen(pierwszy, drugi), oczekiwany_wynik)
		self.assertEqual(vigner.sprawdz_ilosc_powtorzen("ala", "ala"), 3)
		self.assertEqual(vigner.sprawdz_ilosc_powtorzen("tomek", "ala"), 0)
		self.assertEqual(vigner.sprawdz_ilosc_powtorzen("tomek", "domek"), 4)

	def test_znajdz_dlugosc_klucza(self):
		tekst_do_zaszyfrowania = """
		The idea behind the Vigenère cipher, like all polyalphabetic ciphers, is to disguise plaintext letter frequencies,
		which interferes with a straightforward application of frequency analysis. For instance, if P is the most frequent
		letter in a ciphertext whose plaintext is in English, one might suspect that P corresponds to E, because E is the most
		frequently used letter in English. However, using the Vigenère cipher, E can be enciphered as different ciphertext letters
		at different points in the message, thus defeating simple frequency analysis. The primary weakness of the Vigenère cipher
		is the repeating nature of its key. If a cryptanalyst correctly guesses the key's length, then the cipher text can be
		treated as interwoven Caesar ciphers, which individually are easily broken. The Kasiski and Friedman tests can help determine the key length.
		"""
		zaszyfrowany_tekst = vigner.zaszyfruj_tekst(vigner.przygotuj_tekst(tekst_do_zaszyfrowania), "secret")
		dlugosc_klucza = vigner.znajdz_dlugosc_klucza(zaszyfrowany_tekst, 4, 9)
		self.assertEqual(dlugosc_klucza, len("secret"))

	def test_pobierz_co_nta_litere(self):
		tekst = "123123"
		self.assertEqual(vigner.pobierz_co_nta_litere(tekst, 0, 3), "11")
		self.assertEqual(vigner.pobierz_co_nta_litere(tekst, 1, 2), "213")

	def test_oblicz_czestosc_liter(self):
		tekst = "aabc"
		czestosci = vigner.oblicz_czestosci_liter(tekst)
		self.assertEqual(czestosci['a'], float(2) / 4)
		self.assertEqual(czestosci['b'], float(1) / 4)
		self.assertEqual(czestosci['c'], float(1) / 4)
		self.assertEqual(czestosci['d'], float(0))

	def test_znajdz_klucz(self):
		tekst_do_zaszyfrowania = """
		The idea behind the Vigenère cipher, like all polyalphabetic ciphers, is to disguise plaintext letter frequencies,
		which interferes with a straightforward application of frequency analysis. For instance, if P is the most frequent
		letter in a ciphertext whose plaintext is in English, one might suspect that P corresponds to E, because E is the most
		frequently used letter in English. However, using the Vigenère cipher, E can be enciphered as different ciphertext letters
		at different points in the message, thus defeating simple frequency analysis. The primary weakness of the Vigenère cipher
		is the repeating nature of its key. If a cryptanalyst correctly guesses the key's length, then the cipher text can be
		treated as interwoven Caesar ciphers, which individually are easily broken. The Kasiski and Friedman tests can help determine the key length.
		"""
		zaszyfrowany_tekst = vigner.zaszyfruj_tekst(vigner.przygotuj_tekst(tekst_do_zaszyfrowania), "secret")
		dlugosc_klucza = 6
		self.assertEqual(vigner.znajdz_klucz(zaszyfrowany_tekst, dlugosc_klucza), "secret")

	def test_odczytaj_klucz_z_pliku(self):
		klucz = vigner.odczytaj_plik('key.txt')
		self.assertEqual(vigner.przygotuj_tekst(klucz), 'secret')






if __name__ == "__main__":
	unittest.main()
