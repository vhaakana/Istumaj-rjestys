import sys
import random

sij_str = 'jo sijoitettu'
paa_str = 'sijoita sijoita-metodilla'
paikkavalitus = 'ei paikkoja jäljellä'

class Poyta:
    def __init__(self, muoto, pituus):
        self.pituus = pituus
        self.muoto = muoto
        self.paat = [None for i in range(muoto)]
        self.rivi1 = [None for i in range(pituus)]
        self.rivi2 = [None for i in range(pituus)]
        self.listat = [self.paat] + [self.rivi1] + [self.rivi2]
        self.istujat = set()
        self.sijainnit = {} # (rivi, paikka): henkilö
        self.inv_sijainnit = {} # henkilö: (rivi, paikka)

    def vaihda(self, henkilo1, henkilo2):
        rivi1, paikka1 = self.sijainti(henkilo1)
        rivi2, paikka2 = self.sijainti(henkilo2)
        self.listat[rivi1][paikka1], self.listat[rivi2][paikka2] = self.listat[rivi2][paikka2], self.listat[rivi1][paikka1]
        self.sijainnit[(rivi1, paikka1)] = henkilo2
        self.sijainnit[(rivi2, paikka2)] = henkilo1
        self.inv_sijainnit[henkilo1] = (rivi2, paikka2)
        self.inv_sijainnit[henkilo2] = (rivi1, paikka1)

    def getIstujat(self):
        if self.muoto:
            vastaus = [self.paat[0]]
        else:
            vastaus = []
        for n, h in enumerate(self.rivi1):
            vastaus.append(h)
            vastaus.append(self.rivi2[n])
        if self.muoto == 2:
            vastaus.append(self.paat[1])
        return vastaus

    def __repr__(self):
        return 'Pöytä({} henkeä, {} päässä, {} sijoitettua)'.format(2*self.pituus+self.muoto, self.muoto, len(self.istujat))

    def tulosta(self, tiedosto=sys.stdout):
        if self.muoto == 2:
            print(self.paat[1], file=tiedosto)
        for h1, h2 in zip(self.rivi1[::-1], self.rivi2[::-1]):
            print(h1, h2, sep='\t', file=tiedosto)
        if self.muoto > 0:
            print(self.paat[0], file=tiedosto)

    def merkkijono(self):
        vastaus = []
        if self.muoto == 2:
            vastaus.append(self.paat[1])
        for h1, h2 in zip(self.rivi1[::-1], self.rivi2[::-1]):
            vastaus.append('{}\t{}'.format(h1, h2))
        if self.muoto > 0:
            vastaus.append(self.paat[0])
        return '\n'.join(vastaus)

    def sijainti(self, henkilo):
        return self.inv_sijainnit[henkilo]
##        for n, ryhm in enumerate(self.listat):
##            henkt, _ = zip(*ryhm) # _ = sukupuolet
##            if henkilo in henkt:
##                i = henkt.index(henkilo)
##                self.sijainnit[(n, i)] = henkilo # n = rivi, i = paikka
##                self.inv_sijainnit[henkilo] = (n, i)
##                return (n, i)
##            raise KeyError(henkilo)

    def seuralaiset(self, inkilo):
        if type(inkilo) == str:
            rivi, i = self.sijainti(inkilo)
        else:
            rivi, i = inkilo
        
        if i == self.pituus-1:
            i = -1
        
        if rivi == 0: # i on 0 tai 1
            return self.rivi1[-i], self.rivi2[-i]
        elif rivi == 1 and i == 0:
            if self.paat:
                return self.paat[0], self.rivi2[0], self.rivi1[1], self.rivi2[1]
            else:
                return self.rivi2[0], self.rivi1[1], self.rivi2[1]
        elif rivi == 2 and i == 0:
            if self.paat:
                return self.paat[0], self.rivi1[0], self.rivi1[1], self.rivi2[1]
            else:
                return self.rivi1[0], self.rivi1[1], self.rivi2[1]
        elif rivi == 1 and i == -1:
            if self.muoto == 2:
                return self.rivi1[-2], self.rivi2[-2], self.rivi2[-1], self.paat[-1]
            else:
                return self.rivi1[-2], self.rivi2[-2], self.rivi2[-1]
        elif rivi == 2 and i == -1:
            if self.muoto == 2:
                return self.rivi1[-2], self.rivi2[-2], self.rivi1[-1], self.paat[-1]
            else:
                return self.rivi1[-2], self.rivi2[-2], self.rivi1[-1]
        elif rivi == 1:
            return self.rivi1[i-1], self.rivi2[i-1], self.rivi2[i], self.rivi1[i+1], self.rivi2[i+1]
        elif rivi == 2:
            return self.rivi1[i-1], self.rivi2[i-1], self.rivi1[i], self.rivi1[i+1], self.rivi2[i+1]

    def vierustoverit(self, inkilo):
        if type(inkilo) == str:
            rivi, i = self.sijainti(inkilo)
        else:
            rivi, i = inkilo
        
        if i == self.pituus-1:
            i = -1
        
        if rivi == 0: # Päässä istuvan seuralaiset ovat vierustovereita
            return self.rivi1[-i], self.rivi2[-i] # i on 0 tai 1
        elif rivi == 1 and i == 0:
            if self.paat:
                return self.paat[0], self.rivi1[1]
            else:
                return (self.rivi1[1],)
        elif rivi == 2 and i == 0:
            if self.paat:
                return self.paat[0], self.rivi2[1]
            else:
                return (self.rivi2[1],)
        elif rivi == 1 and i == -1:
            if self.muoto == 2:
                return self.rivi1[-2], self.paat[-1]
            else:
                return (self.rivi1[-2],)
        elif rivi == 2 and i == -1:
            if self.muoto == 2:
                return self.rivi2[-2], self.paat[-1]
            else:
                return (self.rivi2[-2],)
        elif rivi == 1:
            return self.rivi1[i-1], self.rivi1[i+1]
        elif rivi == 2:
            return self.rivi2[i-1], self.rivi2[i+1]

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
            return (self.rivi2[i],)
        else:
            return (self.rivi1[i],)
        
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
            return (self.rivi2[1],)
        elif rivi == 2 and i == 0:
            return (self.rivi1[1],)
        elif rivi == 1 and i == -1:
            return (self.rivi2[-2],)
        elif rivi == 2 and i == -1:
            return (self.rivi1[-2],)
        elif rivi == 1:
            return (self.rivi2[i-1], self.rivi2[i+1])
        elif rivi == 2:
            return (self.rivi1[i-1], self.rivi1[i+1])

    def sijoita(self, rivi, paikka, henkilo):
        if paikka == self.pituus-1:
            paikka = -1
        
        if henkilo in self.istujat:
            return sij_str
        if self.listat[rivi][paikka] is not None:
            return sij_str
        self.listat[rivi][paikka] = henkilo
        self.istujat.add(henkilo)
        self.sijainnit[(rivi, paikka)] = henkilo
        self.inv_sijainnit[henkilo] = (rivi, paikka)

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


class Sali:
    def __init__(self, muodot_ja_pituudet):
        self.mp = muodot_ja_pituudet
        self.poydat = [Poyta(*mpp) for mpp in muodot_ja_pituudet]
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

    def vaihda(self, henkilo1, henkilo2):
        if type(henkilo1) == str:
            pt1, rv1, pk1 = self.sijainti(henkilo1)
            pt2, rv2, pk2 = self.sijainti(henkilo2)
        else:
            pt1, rv1, pk1 = henkilo1
            pt2, rv2, pk2 = henkilo2
            henkilo1 = self.sijainnit[pt1, rv1, pk1]
            henkilo2 = self.sijainnit[pt2, rv2, pk2]
        
        self.sijainnit[pt1, rv1, pk1] = henkilo2
        self.sijainnit[pt2, rv2, pk2] = henkilo1
        self.inv_sijainnit[henkilo1] = (pt2, rv2, pk2)
        self.inv_sijainnit[henkilo2] = (pt1, rv1, pk1)
        
        if pt1 == pt2:
            return self.poydat[pt1].vaihda(henkilo1, henkilo2)
        
        self.poydat[pt1].listat[rv1][pk1], self.poydat[pt2].listat[rv2][pk2] = self.poydat[pt2].listat[rv2][pk2], self.poydat[pt1].listat[rv1][pk1]
        
        
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

    def seuralaiset(self, henkilo):
        pt, rv, pk = self.sijainti(henkilo)
        return self.poydat[pt].seuralaiset(henkilo)

    def vierustoverit(self, henkilo):
        pt, rv, pk = self.sijainti(henkilo)
        return self.poydat[pt].vierustoverit(henkilo)

    def vastapainen(self, henkilo):
        pt, rv, pk = self.sijainti(henkilo)
        return self.poydat[pt].vastapainen(henkilo)

    def kulmittain_vastapaata(self, henkilo):
        pt, rv, pk = self.sijainti(henkilo)
        return self.poydat[pt].kulmittain_vastapaata(henkilo)

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

    def tulosta(self, tiedosto=sys.stdout):
        for poyta in self.poydat:
            poyta.tulosta(tiedosto=tiedosto)
            print('', file=tiedosto)

    def sijoita(self, poyta, rivi, paikka, henkilo):
        if henkilo in self.istujat:
            return sij_str
        s = self.poydat[poyta].sijoita(rivi, paikka, henkilo)
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

    def getIstujat(self):
        vastaus = []
        for poyta in self.poydat:
            vastaus.extend(poyta.getIstujat())
        return vastaus

    def merkkijono(self):
        vastaus = []
        for poyta in self.poydat:
            vastaus.append(poyta.merkkijono())
        return '\n\n'.join(vastaus)
