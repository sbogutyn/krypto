#!/usr/bin/env python
from string import ascii_lowercase, ascii_uppercase, letters, maketrans
from optparse import OptionParser

# szyfruje pojedyncza litera afinicznym (cezar to afiniczny z a = 1)
def zaszyfruj_litere(litera,a,b):
	if (litera >= 'a' and litera <= 'z'):
		kod = list(ascii_lowercase).index(litera)
		nowy_kod = (kod * a + b) % 26
		return list(ascii_lowercase)[nowy_kod]
	elif (litera >= 'A' and litera <= 'Z'):
		kod = list(ascii_uppercase).index(litera)
		nowy_kod = (kod * a + b) % 26
		return list(ascii_uppercase)[nowy_kod]
	else:
		return litera;
	
def zaszyfruj_alfabet(a, b):
	szyfr = lambda x : zaszyfruj_litere(x, a, b);
	return ''.join(map(szyfr, list(letters)))

def znajdz_odwrotnosc(a, modn):
	for i in xrange(modn):
		if sprawdz_odwrotnosc(a, i, modn):
			return i
	return -1

def sprawdz_odwrotnosc(a, b, modn):
	if ((a * b) % modn) == 1:
		return True
	else:
		return False

def odszyfruj_litere(litera, a, b):
	odw_a = znajdz_odwrotnosc(a, 26)
	if odw_a != -1:
		if (litera >= 'A' and litera <= 'Z'):
			kod = list(ascii_uppercase).index(litera)
			nowy_kod = (odw_a * (kod - b)) % 26
			return list(ascii_uppercase)[nowy_kod]
		elif (litera >= 'a' and litera <= 'z'):
			kod = list(ascii_lowercase).index(litera)
			nowy_kod = (odw_a * (kod - b)) % 26
			return list(ascii_lowercase)[nowy_kod]
		else:
			return litera

def odszyfruj_alfabet(alfabet, a, b):
	odszyfruj = lambda x : odszyfruj_litere(x, a, b)
	return ''.join(map(odszyfruj, list(alfabet)))

def tlumacz_tekst(tekst, alfabet1, alfabet2):
	transtab = maketrans(alfabet1, alfabet2)
	return tekst.translate(transtab)

def zaszyfruj_tekst(tekst, a, b):
	zaszyfrowany_alfabet = zaszyfruj_alfabet(a, b)
	return tlumacz_tekst(tekst,letters, zaszyfrowany_alfabet)

def odszyfruj_tekst(tekst, a, b):
	zaszyfrowany_alfabet = zaszyfruj_alfabet(a, b)
	return tlumacz_tekst(tekst, zaszyfrowany_alfabet, letters)

def nwd(a, b):
	x = a
	y = b
	while (y != 0):
		c = x % y
		x = y
		y = c
	return x

def odczytaj_plik(nazwa_pliku):
	plik = open(nazwa_pliku, "r")
	tresc = plik.read()
	plik.close()
	return tresc

def zapisz_do_pliku(nazwa_pliku, tresc):
	plik = open(nazwa_pliku, "w+")
	plik.write(tresc)
	plik.close()

def wczytaj_klucz(nazwa_pliku):
	tresc = odczytaj_plik(nazwa_pliku)
	wartosci = tresc.split(',')
	if len(wartosci) == 1:
		return (int(wartosci[0]))
	elif len(wartosci) == 2:
		return (int(wartosci[0]), int(wartosci[1]))

if __name__ == "__main__":
	PLIK_PLAIN="plain.txt"
	PLIK_CRYPTO="crypto.txt"
	PLIK_DECRYPT="decrypt.txt"
	PLIK_EXTRA="extra.txt"
	PLIK_KEY="key.txt"

	parser = OptionParser(usage="Program szyfrujacy i deszyfrujacy.",
			version="%prog 1.0")
	parser.add_option("-c", "--cezar",
			action="store_true",
			dest="cezar_flag",
			default=False,
			help="uzyj szyfru cezara")
	parser.add_option("-a", "--afiniczny",
			action="store_true",
			dest="afiniczny_flag",
			default=False,
			help="uzyj szyfru afinicznego")
	parser.add_option("-d", "--deszyfrowanie", 
			action="store_true", 
			dest="deszyfruj_flag",
			default=False,
			help="deszyfrowanie pliku crypto.txt")
	parser.add_option("-e", "--szyfrowanie", 
			action="store_true",
			dest="szyfruj_flag",
			default=False,
			help="szyfrowanie pliku plain.txt")
	parser.add_option("-j", "--jawny",
			action="store_true",
			dest="jawny_flag",
			default=False,
			help="kryptoanaliza z tekstem jawnym")
	parser.add_option("-k", "--krypto",
			action="store_true",
			dest="krypto_flag",
			default=False,
			help="kryptoanaliza tylko za pomoca kryptogramu")
	(options, args) = parser.parse_args()
	if len(args) != 0:
		parser.error("zla liczba argumentow")

	if options.afiniczny_flag:
		if options.szyfruj_flag:
			print "Szyfrowanie afinicznym"
			klucze = wczytaj_klucz(PLIK_KEY)
			tekst = odczytaj_plik(PLIK_PLAIN)
			zapisz_do_pliku(PLIK_CRYPTO, zaszyfruj_tekst(tekst, klucze[0], klucze[1]))
		elif options.deszyfruj_flag:
			print "Deszyfrowanie afinicznym"
			klucze = wczytaj_klucz(PLIK_KEY)
			zaszyfrowany_tekst = odczytaj_plik(PLIK_CRYPTO)
			zapisz_do_pliku(PLIK_DECRYPT, odszyfruj_tekst(zaszyfrowany_tekst, klucze[0], klucze[1]))
		elif options.jawny_flag:
			print "kryptoanaliza z tekstem jawnym"
			pomoc = odczytaj_plik(PLIK_EXTRA).strip()
			zaszyfrowany_tekst = odczytaj_plik(PLIK_CRYPTO)
			if (len(pomoc) < len(zaszyfrowany_tekst)):
				dlugosc = len(pomoc)
			else:
				dlugosc = len(zaszyfrowany_tekst)
			wyniki = set()
			for i in xrange(dlugosc):
				wynik = set()
				for a in range(26):
					if nwd (a, 26) == 1:
						for b in range(26):
							if odszyfruj_litere(zaszyfrowany_tekst[i], a ,b) == pomoc[i]:
								wynik.add( (a, b) )
				if len(wyniki) == 0:
					for i in wynik:
						wyniki.add(i)
				else:
					print "wyniki = ", wyniki, " &  ", wynik
					wyniki = wyniki & wynik
			print pomoc[dlugosc - 1]
			print zaszyfrowany_tekst[dlugosc - 1]
			print wyniki

			

		elif options.krypto_flag:
			zaszyfrowany_tekst = odczytaj_plik(PLIK_CRYPTO)
			tekst = ""
			for a in range(26):
				if nwd(a, 26) == 1:
					for b in range(26):
						tekst += odszyfruj_tekst(zaszyfrowany_tekst, a, b) + "\n"
			zapisz_do_pliku(PLIK_DECRYPT, tekst)

			print "kryptoanaliza za pomoca kryptogramu"
	
	elif options.cezar_flag:
		print "cezar!"
		if options.szyfruj_flag:
			print "szyfrowanie"
		elif options.deszyfruj_flag:
			print "deszyfrowanie"
		elif options.jawny_flag:
			print "kryptoanaliza z tekstem jawnym"
		elif options.krypto_flag:
			print "kryptoanaliza za pomoca kryptogramu"
		else:
			print "Klucze: ", wczytaj_klucz(PLIK_KEY)
			print zaszyfruj_litere('A', 1, 1)
			print zaszyfruj_litere('B', 2, 1)
			print zaszyfruj_litere('Z', 1, 1)
			print zaszyfruj_alfabet(1,1)
			for i in range(1, 25):
				if nwd(i, 26) == 1:
					print "a = ", i
					print "Zaszyfrowany: ", zaszyfruj_tekst("ala ma kota", i, 1)
					print "Odszyfrowany: ", odszyfruj_tekst(zaszyfruj_tekst("ala ma kota", i, 1), i, 1)
			try:
				print odszyfruj_alfabet(zaszyfruj_alfabet(26, 3), 26, 3)
			except TypeError:
				print "NWD(a, 26) != 1"
			try:
				for i in xrange(26):
					print "Odwrotnosc: ", i , " to: ", znajdz_odwrotnosc(i ,26)
			except TypeError:
				print "brak odwrotnosci"
