#!/usr/bin/env python
from string import ascii_lowercase, ascii_uppercase, letters, maketrans
from optparse import OptionParser

# szyfruje pojedyncza litera afinicznym (cezar to afiniczny z a = 1)
def zaszyfruj_litere(litera,a,b):
	litery = None
	if (litera >= 'a' and litera <= 'z'):
		litery = ascii_lowercase
	elif (litera >= 'A' and litera <= 'Z'):
		litery = ascii_uppercase
	else:
		return litera;
	kod = list(litery).index(litera)
	nowy_kod = (kod * a + b) % 26
	return list(litery)[nowy_kod]
	
def zaszyfruj_alfabet(a, b):
	return ''.join(map(lambda x : zaszyfruj_litere(x, a, b), list(letters)))

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
	litery = None
	if odw_a != -1:
		if (litera >= 'A' and litera <= 'Z'):
			litery = ascii_uppercase
		elif (litera >= 'a' and litera <= 'z'):
			litery = ascii_lowercase
		else:
			return litera
		kod = list(litery).index(litera)
		nowy_kod = (odw_a * (kod - b)) % 26
		return list(litery)[nowy_kod]

def odszyfruj_alfabet(alfabet, a, b):
	return ''.join(map(lambda x : odszyfruj_litere(x, a, b), list(alfabet)))

def tlumacz_tekst(tekst, alfabet1, alfabet2):
	return tekst.translate(maketrans(alfabet1, alfabet2))

def zaszyfruj_tekst(tekst, a, b):
	return tlumacz_tekst(tekst,letters, zaszyfruj_alfabet(a, b))

def odszyfruj_tekst(tekst, a, b):
	return tlumacz_tekst(tekst, zaszyfruj_alfabet(a, b), letters)

def nwd(a, b):
	x, y = a, b
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

	a = b = 0
	if options.afiniczny_flag:
		(a, b) = wczytaj_klucz(PLIK_KEY)
	elif options.cezar_flag:
		a, b = 1 , wczytaj_klucz(PLIK_KEY)[0]
	else:
		print "Musisz wybrac szyfr afiniczny lub cezara"

	if options.szyfruj_flag:
		print "Szyfrowanie afinicznym"
		klucze = wczytaj_klucz(PLIK_KEY)
		tekst = odczytaj_plik(PLIK_PLAIN)
		zapisz_do_pliku(PLIK_CRYPTO, zaszyfruj_tekst(tekst, a, b))
	elif options.deszyfruj_flag:
		print "Deszyfrowanie afinicznym"
		klucze = wczytaj_klucz(PLIK_KEY)
		zaszyfrowany_tekst = odczytaj_plik(PLIK_CRYPTO)
		zapisz_do_pliku(PLIK_DECRYPT, odszyfruj_tekst(zaszyfrowany_tekst, a, b))
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
				wyniki = wyniki & wynik
		if len(wyniki) == 1:
			(a, b) = wyniki.pop()
			tekst = odszyfruj_tekst(zaszyfrowany_tekst, a, b)
			zapisz_do_pliku(PLIK_DECRYPT, tekst)
		

	elif options.krypto_flag:
		zaszyfrowany_tekst = odczytaj_plik(PLIK_CRYPTO)
		tekst = ""
		for x in range(26):
			if nwd(x , 26) == 1:
				for y in range(26):
					tekst += odszyfruj_tekst(zaszyfrowany_tekst, x , y) + "\n"
		zapisz_do_pliku(PLIK_DECRYPT, tekst)

		print "kryptoanaliza za pomoca kryptogramu"
	
