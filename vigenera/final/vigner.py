#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser
from string import ascii_lowercase as male_litery
from math import sqrt

TABLICA_CZESTOSCI_LITER = {
	'a':8.167, 'b':1.492, 'c':2.782,
	'd':4.253, 'e':12.702,'f':2.228,
	'g':2.015, 'h':6.094, 'i':6.996,
	'j':0.153, 'k':0.772, 'l':4.025,
	'm':2.406, 'n':6.749, 'o':7.507,
	'p':1.929, 'q':0.095, 'r':5.987,
	's':6.327, 't':9.056, 'u':2.758,
	'v':0.978, 'w':2.360, 'x':0.150,
	'y':1.974, 'z':0.074 
}

def przygotuj_tekst(tekst):
	return filter(str.isalpha, tekst).lower()

def zaszyfruj_litere(litera, litera_klucza):
	return chr((male_litery.index(litera) + male_litery.index(litera_klucza)) % 26 + ord('a'))

def zaszyfruj_tekst(tekst, klucz):
	return ''.join([ zaszyfruj_litere(tekst[i], klucz[i % len(klucz)]) for i in xrange(len(tekst)) ])

def odszyfruj_litere(zaszyfrowana_litera, litera_klucza):
	return chr((male_litery.index(zaszyfrowana_litera) - male_litery.index(litera_klucza)) % 26 + ord('a'))

def odszyfruj_tekst(zaszyfrowany_tekst, klucz):
	return ''.join([ odszyfruj_litere(zaszyfrowany_tekst[i], klucz[i % len(klucz)]) for i in xrange(len(zaszyfrowany_tekst)) ])

def przesun_tekst(tekst, ilosc_liter):
	return ''.join([ tekst[(i - ilosc_liter) % len(tekst)] for i in xrange(len(tekst))])

def sprawdz_ilosc_powtorzen(tekst1, tekst2):
	return len(filter(lambda (x, y) : x == y, zip(tekst1, tekst2)))

def ilosc_powtorzen_na_dlugosc_tekstu(ilosc_powtorzen, dlugosc_tekstu):
	return float(ilosc_powtorzen) / dlugosc_tekstu

def znajdz_wszystkie_dzielniki(liczba):
	dzielniki = []
	for i in xrange(1, int(sqrt(liczba))):
		if liczba % i == 0:
			dzielniki.append(i)
	return dzielniki


def znajdz_dlugosc_klucza(tekst, min_dlugosc_klucza, max_dlugosc_klucza):
	# prawdopodobieństo, że dwie losowo wybrane litery w tekscie będą identyczne dla języka angielskiego
	PRAWDOPODOBIENSTWO_POWTORZEN = 0.0667
	dlugosc_klucza = min_dlugosc_klucza
	czestosci_wystapien = [ilosc_powtorzen_na_dlugosc_tekstu(sprawdz_ilosc_powtorzen(tekst, przesun_tekst(tekst, i)), len(tekst)) for i in xrange(min_dlugosc_klucza, max_dlugosc_klucza + 1)]
	najmniejsza_roznica = -1
	mozliwe_dlugosci = []
	for i in xrange((max_dlugosc_klucza + 1) - min_dlugosc_klucza):
		aktualna_roznica = (PRAWDOPODOBIENSTWO_POWTORZEN - czestosci_wystapien[i])**2
		if najmniejsza_roznica == -1:
			najmniejsza_roznica = aktualna_roznica
		if aktualna_roznica < najmniejsza_roznica:
			#print "aktualna roznica: ", aktualna_roznica, " najmniejsza_roznica: ", najmniejsza_roznica, " dlugosc_klucza: ", dlugosc_klucza
			dlugosc_klucza = min_dlugosc_klucza + i
			if (dlugosc_klucza > 4):
				mozliwe_dlugosci.append(dlugosc_klucza)
			najmniejsza_roznica = aktualna_roznica
	dzielniki = set([])
	for dlugosc in mozliwe_dlugosci:
		tmp = filter(lambda x : x > 4, znajdz_wszystkie_dzielniki(dlugosc))
		if not dzielniki:
			dzielniki = set(tmp)
		else:
			dzielniki &= set(tmp)
	if len(dzielniki) == 1:
		return dzielniki.pop()
	else:
		return 0
	#return min(mozliwe_dlugosci)
	#return dlugosc_klucza





def pobierz_co_nta_litere(tekst, poczatek, n):
	return ''.join([tekst[i] for i in filter(lambda x : x % n == poczatek, range(len(tekst)))])

def oblicz_czestosci_liter(litery_na_kolejnym_miejscu_klucza):
	czestosci = {}
	for i in male_litery:
		czestosci[i] = 0
	for litera in litery_na_kolejnym_miejscu_klucza:
		czestosci[litera] += 1
	for i in male_litery:
		czestosci[i] = float(czestosci[i]) / len(litery_na_kolejnym_miejscu_klucza)
	return czestosci
		

def oblicz_iloczyn_skalarny(czestosci_w_kluczu, czestosci_w_angielskim = TABLICA_CZESTOSCI_LITER):
	iloczyn_skalarny = 0
	for i in male_litery:
		iloczyn_skalarny += czestosci_w_kluczu[i] * czestosci_w_angielskim[i]
	return iloczyn_skalarny

def przesun_wektor(wektor, przesuniecie):
	przesuniety_wektor = {}
	for i in male_litery:
		przesuniety_wektor[i] = wektor[chr((male_litery.index(i) + przesuniecie) % 26 + 97)]
	return przesuniety_wektor

def najlepsze_przesuniecie_cezara(slownik_czestosci_liter):
	iloczyny = [ oblicz_iloczyn_skalarny(slownik_czestosci_liter, przesun_wektor(TABLICA_CZESTOSCI_LITER, i)) for i in xrange(26) ]
	try:
		return iloczyny.index(max(iloczyny))
	except Exception:
		return 0

def znajdz_klucz(tekst, dlugosc_klucza):
	klucz = []
	for i in xrange(dlugosc_klucza):
		slownik_czestosci_liter = oblicz_czestosci_liter(pobierz_co_nta_litere(tekst, i, dlugosc_klucza)) 
		przesuniecie = najlepsze_przesuniecie_cezara(slownik_czestosci_liter) 
		if przesuniecie == 0:
			klucz.append('a')
		else:
			klucz.append(chr(ord('a') + (26 - przesuniecie)))
	return ''.join(klucz)

def odczytaj_plik(nazwa_pliku):
	plik = open(nazwa_pliku, "r")
	tresc = plik.read()
	plik.close()
	return tresc

def zapisz_do_pliku(nazwa_pliku, tresc):
	plik = open(nazwa_pliku, "w+")
	plik.write(tresc)
	plik.close()
	
def main():
	PLIK_PLAIN="plain.txt"
	PLIK_CRYPTO="crypto.txt"
	PLIK_DECRYPT="decrypt.txt"
	PLIK_KEY="key.txt"

	parser = OptionParser(usage="python vigner.py [opcje]",
			version="%prog 1.0")
	parser.add_option("-p", "--przygotuj",
			action="store_true",
			dest="przygotuj_flag",
			default=False,
			help="przygotowuje tekst do szyfrowania")
	parser.add_option("-e", "--szyfrowanie",
			action="store_true",
			dest="szyfruj_flag",
			default=False,
			help="szyfruje przygotowany tekst")
	parser.add_option("-d", "--deszyfrowanie",
			action="store_true",
			dest="deszyfruj_flag",
			default=False,
			help="odszyfrowuje zaszyfrowany tekst")
	parser.add_option("-k", "--kryptoanaliza",
			action="store_true",
			dest="kryptoanaliza_flag",
			default=False,
			help="dokonuje kryptoanalizy zaszyfrowanego tekstu")
	(options, args) = parser.parse_args()

	if len(args) != 0:
		parser.error("Zly parametr")

	if options.przygotuj_flag:
		tekst = odczytaj_plik(PLIK_PLAIN)
		przygotowany_tekst = przygotuj_tekst(tekst)
		zapisz_do_pliku(PLIK_PLAIN, przygotowany_tekst)

	if options.szyfruj_flag:
		tekst = odczytaj_plik(PLIK_PLAIN)
		klucz = przygotuj_tekst(odczytaj_plik(PLIK_KEY))
		zaszyfrowany_tekst = zaszyfruj_tekst(tekst, klucz)
		zapisz_do_pliku(PLIK_CRYPTO, zaszyfrowany_tekst)

	elif options.deszyfruj_flag:
		zaszyfrowany_tekst = przygotuj_tekst(odczytaj_plik(PLIK_CRYPTO))
		klucz = przygotuj_tekst(odczytaj_plik(PLIK_KEY))
		odszyfrowany_tekst = odszyfruj_tekst(zaszyfrowany_tekst, klucz)
		zapisz_do_pliku(PLIK_DECRYPT, odszyfrowany_tekst)

	elif options.kryptoanaliza_flag:
		zaszyfrowany_tekst = przygotuj_tekst(odczytaj_plik(PLIK_CRYPTO))
		dlugosc_klucza = znajdz_dlugosc_klucza(zaszyfrowany_tekst, 5, len(zaszyfrowany_tekst))
		if dlugosc_klucza == 0:
			print "Nie znaleziono klucza"
			return
		print "Dlugosc znalezionego klucza: ", dlugosc_klucza
		klucz = znajdz_klucz(zaszyfrowany_tekst, dlugosc_klucza)
		print "Znaleziony klucz: ", klucz
		odszyfrowany_tekst = odszyfruj_tekst(zaszyfrowany_tekst, klucz)
		zapisz_do_pliku(PLIK_DECRYPT, odszyfrowany_tekst)

if __name__ == "__main__":
	main()