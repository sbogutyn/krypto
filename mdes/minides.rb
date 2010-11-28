#!/usr/bin/ruby -w
# dwa S-boksy [4]->[3] to
# 101 010 001 110 011 100 111 000
# 001 100 110 010 000 111 101 011
#
# 100 000 110 101 111 001 011 010
# 101 011 000 111 110 010 001 100
#
# klucz jest 9-bitowy, klucz dla kazdej runy i (1..8) jest osmiobitowy
# i zaczyna sie od i-tego bitu klucza.
# bloki 12 bitowe, dzielone sa na dwa po 6 bitow , LO, RO
# w kazdej rundzie Li=[Ri-1] Ri = L[i-1]+f(R[i-1], Ki) w ostatniej osmej
# jeszcze zamiana L8 i R8
# f:[6+8]->[6] jest zdefiniowane
# f(R,K)=S1xS2(E(R)+K)

# Opcje wywolania:
# -e -d -a
#
# -e szyfrowanie - program czyta z pliku ciag 12 zer i jedynek
# a z pliku key 9 zer i jedynek i zapisyje na crypto wynik szyfrowania
# -d deszyfrowanie - czyta crypto i zapisuje w decrypt
# -a analiza dzialania programu

require 'optparse'

# nazwy plików
PLAIN = "plain.txt"
CRYPTO = "crypto.txt"
DECRYPT = "decrypt.txt"
KEY = "key.txt"

class Szyfrowanie

  def initialize(tekst, klucz)
    @tekst = tekst
    @klucz = klucz
  end
  

  def to_s
    "Szyfrowanie: \"#{@tekst}\" z kluczem: \"#{@klucz}\""
  end
end

class Deszyfrowanie
  def to_s
    "Deszyfrowanie"
  end
end

class Analiza
  def to_s
    "Analiza"
  end
end

def czytaj_plik(nazwa_pliku)
  tekst = ""
  File.foreach(nazwa_pliku) do |line|
    tekst << line
  end
  tekst.chomp!
end

options = {}

optparse = OptionParser.new do |opts|
  opts.banner = "Usage: minides.rb [opcje]"

  opts.on('-e', '--szyfrowanie', 'Szyfrowanie tekstu z plain.txt do crypto.txt') do
    tekst = czytaj_plik(PLAIN)
    klucz = czytaj_plik(KEY)
    puts Szyfrowanie.new(tekst, klucz)
  end

  opts.on('-d', '--deszyfrowanie', 'Deszyfrowanie tekstu z pliku crypto.txt do decrypt.txt') do
    puts Deszyfrowanie.new
  end

  opts.on('-a', '--analiza', 'Analiza dzialania programu') do
    puts Analiza.new
  end

  opts.on( '-h', '--help', 'Pokaz pomoc' ) do
     puts opts
     exit
  end

end

optparse.parse!
