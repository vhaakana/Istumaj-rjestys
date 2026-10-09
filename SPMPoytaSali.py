import sys
import copy
import random

sij_str = 'jo sijoitettu'
paa_str = 'sijoita sijoita-metodilla'
paikkavalitus = 'ei paikkoja jäljellä'

def sijsuk(s):
    if s == 'm' or s == 'n':
        return s
    return random.choice(['m', 'n'])

def samat(sp1, sp2):
    return (sp1 == sp2 == 'm') or (sp1 == sp2 == 'n')

def vastakkaiset(sp1, sp2):
    return (sp1 == 'm' and sp2 == 'n') or (sp1 == 'n' and sp2 == 'm')


def vastakkainen(sp):
    if sp == 'n':
        return 'm'
    elif sp == 'm':
        return 'n'
    return 'o'


class Poyta:
    def __init__(self, muoto, pituus):
        self.pituus = pituus
        self.muoto = muoto
        self.paat = [[None, 'o'] for i in range(muoto)]
        self.rivi1 = [[None, 'o'] for i in range(pituus)]
        self.rivi2 = copy.deepcopy(self.rivi1)
        self.listat = [self.paat] + [self.rivi1] + [self.rivi2]
        self.istujat = set()
        self.sijainnit = {} # (rivi, paikka): henkilö
        self.inv_sijainnit = {} # henkilö: (rivi, paikka)

    def vaihda(self, henkilo1, henkilo2):
        rivi1, paikka1 = self.sijainti(henkilo1)
        rivi2, paikka2 = self.sijainti(henkilo2)
        if type(henkilo1) != str:
            henkilo1 = self.listat[rivi1][paikka1][0]
        if type(henkilo2) != str:
            henkilo2 = self.listat[rivi2][paikka2][0]
        self.listat[rivi1][paikka1][0], self.listat[rivi2][paikka2][0] = self.listat[rivi2][paikka2][0], self.listat[rivi1][paikka1][0]
        self.sijainnit[(rivi1, paikka1)] = henkilo2
        self.sijainnit[(rivi2, paikka2)] = henkilo1
        self.inv_sijainnit[henkilo1] = (rivi2, paikka2)
        self.inv_sijainnit[henkilo2] = (rivi1, paikka1)

    def getIstujat_entinen(self):
        vastaus = []
        for rivi in self.listat:
            for henk in rivi:
                vastaus.append(henk[0])
        return vastaus

    def getIstujat(self):
        if self.muoto:
            vastaus = [self.paat[0][0]]
        else:
            vastaus = []
        for h1, h2 in zip(self.rivi1, self.rivi2):
            vastaus.append(h1[0])
            vastaus.append(h2[0])
        if self.muoto == 2:
            vastaus.append(self.paat[-1][0])
        return vastaus

    def sijoitettu_sukupuoli(self, henkilo):
        rv, pk = self.inv_sijainnit[henkilo]
        return self.listat[rv][pk][1]

    def maaraa_sukupuolet(self, eka):
        for n, paikka in enumerate(self.rivi1):
            if n%2 == 0:
                self.rivi1[n][1] = eka
                self.rivi2[n][1] = vastakkainen(eka)
            else:
                self.rivi1[n][1] = vastakkainen(eka)
                self.rivi2[n][1] = eka
##        for n, paikka in enumerate(self.rivi2):
##            if n%2 == 1:
##                self.rivi2[n][1] = eka
##            else:
##                self.rivi2[n][1] = vastakkainen(eka)

    def __repr__(self):
        return 'Pöytä({} henkeä, {} päässä, {} sijoitettua)'.format(2*self.pituus+self.muoto, self.muoto, len(self.istujat))

    def tulosta(self, tiedosto=sys.stdout):
        if self.muoto == 2:
            print(self.paat[1][0], file=tiedosto)
        for h1, h2 in zip(self.rivi1[::-1], self.rivi2[::-1]):
            print(h1[0], h2[0], sep='\t', file=tiedosto)
        if self.muoto > 0:
            print(self.paat[0][0], file=tiedosto)

    def merkkijono(self):
        vastaus = []
        if self.muoto == 2:
            vastaus.append(self.paat[1][0])
        for h1, h2 in zip(self.rivi1[::-1], self.rivi2[::-1]):
            vastaus.append('{}\t{}'.format(h1[0], h2[0]))
        if self.muoto > 0:
            vastaus.append(self.paat[0][0])
        return '\n'.join(vastaus)

    def sijainti(self, henkilo):
        if type(henkilo) == tuple:
            return henkilo
        if henkilo in self.istujat:
            return self.inv_sijainnit[henkilo]
        for n, ryhm in enumerate(self.listat):
            henkt, _ = zip(*ryhm) # _ = sukupuolet
            if henkilo in henkt:
                i = henkt.index(henkilo)
                self.sijainnit[(n, i)] = henkilo # n = rivi, i = paikka
                self.inv_sijainnit[henkilo] = (n, i)
                return (n, i)
            raise KeyError(henkilo)

    def seuralaisten_maara(self, inkilo):
        if type(inkilo) == str:
            rivi, i = self.sijainti(inkilo)
        else:
            rivi, i = inkilo
        
        if i == self.pituus-1:
            i = -1
        
        if rivi == 0: # i on 0 tai 1
            return 2
        elif i == 0:
            if self.paat:
                return 4
            else:
                return 3
        elif i == -1:
            if self.muoto == 2:
                return 4
            else:
                return 3
        else:
            return 5

    def seuralaiset(self, inkilo):
        if type(inkilo) == str:
            rivi, i = self.sijainti(inkilo)
        else:
            rivi, i = inkilo
        
        if i == self.pituus-1:
            i = -1
        
        if rivi == 0: # i on 0 tai 1
            return self.rivi1[-i][0], self.rivi2[-i][0]
        elif rivi == 1 and i == 0:
            if self.paat:
                return self.paat[0][0], self.rivi2[0][0], self.rivi1[1][0], self.rivi2[1][0]
            else:
                return self.rivi2[0][0], self.rivi1[1][0], self.rivi2[1][0]
        elif rivi == 2 and i == 0:
            if self.paat:
                return self.paat[0][0], self.rivi1[0][0], self.rivi1[1][0], self.rivi2[1][0]
            else:
                return self.rivi1[0][0], self.rivi1[1][0], self.rivi2[1][0]
        elif rivi == 1 and i == -1:
            if self.muoto == 2:
                return self.rivi1[-2][0], self.rivi2[-2][0], self.rivi2[-1][0], self.paat[-1][0]
            else:
                return self.rivi1[-2][0], self.rivi2[-2][0], self.rivi2[-1][0]
        elif rivi == 2 and i == -1:
            if self.muoto == 2:
                return self.rivi1[-2][0], self.rivi2[-2][0], self.rivi1[-1][0], self.paat[-1][0]
            else:
                return self.rivi1[-2][0], self.rivi2[-2][0], self.rivi1[-1][0]
        elif rivi == 1:
            return self.rivi1[i-1][0], self.rivi2[i-1][0], self.rivi2[i][0], self.rivi1[i+1][0], self.rivi2[i+1][0]
        elif rivi == 2:
            return self.rivi1[i-1][0], self.rivi2[i-1][0], self.rivi1[i][0], self.rivi1[i+1][0], self.rivi2[i+1][0]

    def vierustoverit(self, inkilo):
        if type(inkilo) == str:
            rivi, i = self.sijainti(inkilo)
        else:
            rivi, i = inkilo
        
        if i == self.pituus-1:
            i = -1
        
        if rivi == 0: # Päässä istuvan seuralaiset ovat vierustovereita
            return self.rivi1[-i][0], self.rivi2[-i][0] # i on 0 tai 1
        elif rivi == 1 and i == 0:
            if self.paat:
                return self.paat[0][0], self.rivi1[1][0]
            else:
                return (self.rivi1[1][0],)
        elif rivi == 2 and i == 0:
            if self.paat:
                return self.paat[0][0], self.rivi2[1][0]
            else:
                return (self.rivi2[1][0],)
        elif rivi == 1 and i == -1:
            if self.muoto == 2:
                return self.rivi1[-2][0], self.paat[-1][0]
            else:
                return (self.rivi1[-2][0],)
        elif rivi == 2 and i == -1:
            if self.muoto == 2:
                return self.rivi2[-2][0], self.paat[-1][0]
            else:
                return (self.rivi2[-2][0],)
        elif rivi == 1:
            return self.rivi1[i-1][0], self.rivi1[i+1][0]
        elif rivi == 2:
            return self.rivi2[i-1][0], self.rivi2[i+1][0]

    def vastapainen(self, inkilo): # Palautetaan monikko eli tuple, vaikka sen pituus onkin 0 tai 1
        if type(inkilo) == str:
            rivi, i = self.sijainti(inkilo)
        else:
            rivi, i = inkilo
        
        if i == self.pituus-1:
            i = -1
        
        if rivi == 0:
            return () # Päässä istuvalla ei ole mahdollisuutta jutella vastapäisen kanssa
        elif rivi == 1:
            return (self.rivi2[i][0],)
        else:
            return (self.rivi1[i][0],)
        
    def kulmittain_vastapaata(self, inkilo):
        if type(inkilo) == str:
            rivi, i = self.sijainti(inkilo)
        else:
            rivi, i = inkilo
        
        if i == self.pituus-1:
            i = -1
        
        if rivi == 0:
            return () # Päässä istuvan seuralaiset lasketaan vierustovereiksi
        elif rivi == 1 and i == 0:
            return (self.rivi2[1][0],)
        elif rivi == 2 and i == 0:
            return (self.rivi1[1][0],)
        elif rivi == 1 and i == -1:
            return (self.rivi2[-2][0],)
        elif rivi == 2 and i == -1:
            return (self.rivi1[-2][0],)
        elif rivi == 1:
            return (self.rivi2[i-1][0], self.rivi2[i+1][0])
        elif rivi == 2:
            return (self.rivi1[i-1][0], self.rivi1[i+1][0])

    def sijoita(self, rivi, paikka, henkilo, sp=None):
        assert type(henkilo) == str
        if paikka == self.pituus-1:
            paikka = -1
        
        if henkilo in self.istujat:
            return sij_str
        if self.listat[rivi][paikka][0] is not None:
            return sij_str
        self.listat[rivi][paikka][0] = henkilo
        self.istujat.add(henkilo)
        self.sijainnit[(rivi, paikka)] = henkilo
        self.inv_sijainnit[henkilo] = (rivi, paikka)
        if sp and rivi == 1 and paikka == 0:
            self.maaraa_sukupuolet(sp)

    def sijoita_seuraan(self, seuralainen, sijoitettava, sp, rivipaikka=None):
        """sp = 'eri' tai 'sama'"""
        if sijoitettava in self.istujat:
            return sij_str
        if rivipaikka: # sijainnin voi antaa nopeuttamiseksi
            rivi, paikka = rivipaikka
        else:
            rivi, paikka = self.sijainti(seuralainen)
        if paikka == -1 or paikka == self.pituus-1:
            return paikkavalitus
        if rivi == 0 and paikka == 0:
            return paa_str
        if sp == 'sama':
            if rivi == 1:
                viesti = self.sijoita(2, paikka+1, sijoitettava)
                if viesti:
                    return viesti
                else:
                    return (2, paikka+1)
            else:
                viesti = self.sijoita(1, paikka+1, sijoitettava)
                if viesti:
                    return viesti
                else:
                    return (1, paikka+1)
        elif sp == 'eri':
            if rivi == 1:
                seura = self.rivi2[paikka], self.rivi1[paikka+1]
                if seura[0][0] is not None: # vastapäätä on jo sijoitettu
                    viesti = self.sijoita(1, paikka+1, sijoitettava)
                    if viesti:
                        return viesti
                    else:
                        return (1, paikka+1)
                elif seura[1][0] is not None: # viereen on jo sijoitettu
                    viesti = self.sijoita(2, paikka, sijoitettava)
                    if viesti:
                        return viesti
                    else:
                        return (2, paikka)
                elif random.choice([0, 1]) == 0:
                    viesti = self.sijoita(1, paikka+1, sijoitettava)
                    if viesti:
                        return viesti
                    else:
                        return (1, paikka+1)
                else:
                    viesti = self.sijoita(2, paikka, sijoitettava)
                    if viesti:
                        return viesti
                    else:
                        return (2, paikka)
            else:
                seura = self.rivi1[paikka], self.rivi2[paikka+1]
                if seura[0][0] is not None: # vastapäätä on jo sijoitettu
                    viesti = self.sijoita(2, paikka+1, sijoitettava)
                    if viesti:
                        return viesti
                    else:
                        return (2, paikka+1)
                elif seura[1][0] is not None: # viereen on jo sijoitettu
                    viesti = self.sijoita(1, paikka, sijoitettava)
                    if viesti:
                        return viesti
                    else:
                        return (1, paikka)
                elif random.choice([0, 1]) == 0:
                    viesti = self.sijoita(2, paikka+1, sijoitettava)
                    if viesti:
                        return viesti
                    else:
                        return (2, paikka+1)
                else:
                    viesti = self.sijoita(1, paikka, sijoitettava)
                    if viesti:
                        return viesti
                    else:
                        return (1, paikka)
    
    def sijoitetut_sukupuolet(self):
        vastaus = {}
        for rivi in self.listat:
            for henkilo in rivi:
                vastaus[henkilo[0]] = henkilo[1]
        return vastaus


class Sali:
    def __init__(self, muodot_ja_pituudet):
        self.poydat = [Poyta(*mp) for mp in muodot_ja_pituudet]
        self.istujat = set()
        self.sijainnit = {} # (pöytä, rivi, paikka): henkilö
        self.inv_sijainnit = {} # henkilö: (pöytä, rivi, paikka)

    def sijainti(self, henkilo):
        if henkilo in self.istujat:
            return self.inv_sijainnit[henkilo]
        for n, poyta in enumerate(self.poydat):
            if henkilo in poyta.istujat:
                vastaus = (n,) + poyta.sijainti(henkilo)
                self.sijainnit[vastaus] = henkilo
                self.inv_sijainnit[henkilo] = vastaus
                return vastaus
        raise KeyError(henkilo)

    def vaihda(self, inkilo1, inkilo2):
        if type(inkilo1) == str:
            pt1, rv1, pk1 = self.sijainti(inkilo1)
            pt2, rv2, pk2 = self.sijainti(inkilo2)
            henkilo1 = inkilo1
            henkilo2 = inkilo2
        else:
            pt1, rv1, pk1 = inkilo1
            pt2, rv2, pk2 = inkilo2
            henkilo1 = self.sijainnit[pt1, rv1, pk1]
            henkilo2 = self.sijainnit[pt2, rv2, pk2]
            
        
        self.sijainnit[pt1, rv1, pk1] = henkilo2
        self.sijainnit[pt2, rv2, pk2] = henkilo1
        self.inv_sijainnit[henkilo1] = (pt2, rv2, pk2)
        self.inv_sijainnit[henkilo2] = (pt1, rv1, pk1)
        
        if pt1 == pt2:
            return self.poydat[pt1].vaihda((rv1, pk1), (rv2, pk2))
        
        self.poydat[pt1].listat[rv1][pk1][0], self.poydat[pt2].listat[rv2][pk2][0] = self.poydat[pt2].listat[rv2][pk2][0], self.poydat[pt1].listat[rv1][pk1][0]
        
        
        self.poydat[pt1].istujat.remove(henkilo1)
        self.poydat[pt1].istujat.add(henkilo2)
        self.poydat[pt1].sijainnit[(rv1, pk1)] = henkilo2
        del self.poydat[pt1].inv_sijainnit[henkilo1]
        self.poydat[pt1].inv_sijainnit[henkilo2] = (rv1, pk1)

        # edellinen_koodilohko.translate({ord('1'):'2', ord('2'):'1'})
        self.poydat[pt2].istujat.remove(henkilo2)
        self.poydat[pt2].istujat.add(henkilo1)
        self.poydat[pt2].sijainnit[(rv2, pk2)] = henkilo1
        del self.poydat[pt2].inv_sijainnit[henkilo2]
        self.poydat[pt2].inv_sijainnit[henkilo1] = (rv2, pk2)

    def sijoitettu_sukupuoli(self, henkilo):
        pt, rv, pk = self.inv_sijainnit[henkilo]
        return self.poydat[pt].listat[rv][pk][1]

    def seuralaisten_maara(self, henkilo):
        pt, rv, pk = self.sijainti(henkilo)
        return self.poydat[pt].seuralaisten_maara(henkilo)

    def seuralaiset(self, henkilo):
        pt, rv, pk = self.sijainti(henkilo)
        return self.poydat[pt].seuralaiset(henkilo)

    def tulosta(self, tiedosto=sys.stdout):
        for poyta in self.poydat:
            poyta.tulosta(tiedosto=tiedosto)
            print('', file=tiedosto)

    def vier_vast_kvast(self, henkilo):
        """Vierustoverit, vastapäiset ja kulmittain vastapäiset tupleina listaan"""
        pt, rv, pk = self.sijainti(henkilo)
        return [self.poydat[pt].vierustoverit(henkilo), self.poydat[pt].vastapainen(henkilo), self.poydat[pt].kulmittain_vastapaata(henkilo)]

    def vier_vast_kvast_seur(self, henkilo):
        """Vierustoverit, vastapäiset, kulmittain vastapäiset ja kaikki seuralaiset tupleina listaan"""
        pt, rv, pk = self.sijainti(henkilo)
        answer = [self.poydat[pt].vierustoverit(henkilo), self.poydat[pt].vastapainen(henkilo), self.poydat[pt].kulmittain_vastapaata(henkilo)]
        answer.append(answer[0]+answer[1]+answer[2])
        return answer

    def sijoita(self, poyta, rivi, paikka, henkilo, sp=None):
        if henkilo in self.istujat:
            return sij_str
        s = self.poydat[poyta].sijoita(rivi, paikka, henkilo, sp=sp)
        if s is not None:
            return s
        self.istujat.add(henkilo)
        self.sijainnit[(poyta, rivi, paikka)] = henkilo
        self.inv_sijainnit[henkilo] = (poyta, rivi, paikka)

    def sijoita_seuraan(self, seuralainen, sijoitettava, sp):
        if sijoitettava in self.istujat:
            return sij_str
        pt, rv, pk = self.sijainti(seuralainen)
        uusisijainti = self.poydat[pt].sijoita_seuraan(seuralainen, sijoitettava, sp, (rv, pk))
        if type(uusisijainti) == str:
            return sij_str
        uusirivi, uusipaikka = uusisijainti
        self.istujat.add(sijoitettava)
        self.sijainnit[(pt, uusirivi, uusipaikka)] = sijoitettava
        self.inv_sijainnit[sijoitettava] = (pt, uusirivi, uusipaikka)

    def getIstujat_entinen(self):
        vastaus = []
        for poyta in self.poydat:
            for rivi in poyta.listat:
                for henk in rivi:
                    vastaus.append(henk[0])
        return vastaus

    def getIstujat(self):
        vastaus = []
        for poyta in self.poydat:
            vastaus.extend(poyta.getIstujat())
        return vastaus

    def sijoitetut_sukupuolet(self):
        vastaus = {}
        for poyta in self.poydat:
            vastaus.update(poyta.sijoitetut_sukupuolet())
        return vastaus

    def merkkijono(self):
        vastaus = []
        for poyta in self.poydat:
            vastaus.append(poyta.merkkijono())
        return '\n\n'.join(vastaus)
