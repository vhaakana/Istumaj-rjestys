# http://stackoverflow.com/questions/40222971/python-find-equivalent-surrogate-pair-from-non-bmp-unicode-char/40223212#40223212
# Tarvitaan emojeja tai muita BMP-alueen ulkopuolisia sisältävien tiedostojen
# avaamiseen Tkinterillä. Menetelmä toimii oikein vain useita rivejä sallivissa
# tekstibokseissa; jos yhden rivin tekstikenttään laittaa emojin, Windows ei
# pysty lukemaan sen sisältöä (Linuxissa toimii oikein), ja jos esim. otsikkoon
# tai Label-tekstiin laittaa emojin, Ubuntu näyttää sen vain laatikoina
# (tämä taas toimii Windowsissa oikein).

import sys

def remove_surrogates(s):
    return s.encode('utf-16', 'surrogatepass').decode('utf-16')

import re

_nonbmp = re.compile(r'[\U00010000-\U0010FFFF]')

def _surrogatepair(match):
    char = match.group()
    assert ord(char) > 0xffff
    encoded = char.encode('utf-16-le')
    return (
        chr(int.from_bytes(encoded[:2], 'little')) + 
        chr(int.from_bytes(encoded[2:], 'little')))

def _with_surrogates(text):
    return _nonbmp.sub(_surrogatepair, text)


# PÄIVITYS:
# Python 3.7:ssa surrogaatteja ei enää tarvita, mutta Windowsilla ne eivät
# haittaakaan. Linuxilla emojit eivät toimi Python 3.7:ssa tai uudemmissa
# versioissa, jos niitä käyttää. Sen vuoksi täytyy tarkistaa, onko käytössä
# Python 3.7 tai uudempi ja sen perusteella päättää, lisätäänkö surrogaatit vai
# ei. Yllä olevaan, alkujaan StackOverflow'ssa nimellä "with_surrogates"
# julkaistun funktion nimeen on siis lisätty alaviiva, ja ilman alun alaviivaa
# oleva versio tarkistaa Python-version ja palauttaa sen merkkijonon, jonka tk
# vaatii toimiakseen. Samoin yllä oleva väite, että Linux pystyisi lukemaan
# yhden rivin tekstikentän sisällön, vaikka siinä olisi emoji, ei pitänyt
# paikkaansa Ubuntu 22.04.5 -virtuaalikoneella Anacondan kanssa.

_no_emoji_support = sys.version_info[:2] < (3, 7)

def self_return(text):
    return text

if _no_emoji_support:
    with_surrogates = _with_surrogates
else:
    with_surrogates = self_return
