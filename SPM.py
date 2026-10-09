import sys
import random
import itertools
from numpy.random import choice as numpyrandomchoice
import os
from SPMPoytaSali import *
from tkinter import messagebox
try:
    from time import monotonic as aik
except ImportError:
    print('Jaahas, sinulla ei näytä olevan pääsyä time.monotonic-funktioon... No höh.')
    from time import time as aik

def tulosta(x, chars=500):
    print(str(x)[:chars])

def poistaufeff(s):
    if s.startswith('\ufeff'):
        return s[1:]
    return s

def luo_istumajarjestyksia(data, pituusdata_str, populaation_koko, sukupolvia, mutaatiomaara, max_ilman_edistysta, loppukiriaika):
    
    populaation_koko = int(populaation_koko)
    sukupolvia = int(sukupolvia)
    mutaatiomaara = int(mutaatiomaara)
    max_ilman_edistysta = int(max_ilman_edistysta)
    loppukiriaika = float(loppukiriaika)
    

    if data.endswith(':'):
        data += ' ' # jos viimeinen ilman toiveita...

    osallistujat = {(w.split(': ')[0][:-1], w.split(': ')[0][-1]) for w in data.splitlines()}

    nimet = {w[0] for w in osallistujat}

    snimet = list(nimet)
    random.shuffle(snimet)

    sukupuolet = {nimi:sp for nimi, sp in osallistujat}

    #miehet = {w[0] for w in osallistujat if w[1] == 'm'}
    #naiset = {w[0] for w in osallistujat if w[1] == 'n'}
    #muut = {w[0] for w in osallistujat if w[1] == 'o'}

    miehet = set()
    naiset = set()
    muut = set()

    for w in osallistujat:
        if w[1] == 'm':
            miehet.add(w[0])
        elif w[1] == 'n':
            naiset.add(w[0])
        elif w[1] == 'o':
            muut.add(w[0])
        else:
            raise ValueError('Henkilön {} sukupuoli on kelvoton: {}'.format(w[0], w[1]))

    avecit = {}

    toiveet = {}
    pl = []

    varoitukset = []

    for line in data.splitlines():
        h = line.split(': ')[0][:-1]
        if '|' in line:
            t, avec = line.split(': ')[1].split('|')
            t = t.split(', ')
            avecit[h] = avec
        else:
            t = line.split(': ')[1].split(', ')
        toiveet[h] = {j for j in t if j in nimet}
        ei_mukana = ', '.join([j for j in t if j not in nimet])
        if ei_mukana:
            varoitukset.append('Seuraavat henkilön {} toivelistalla olevat eivät osallistu juhliin: {}'.format(h, ei_mukana))
        pl.append(h)
	
        virheet = []

    for henk in avecit:
        try:
            if avecit[avecit[henk]] != henk:
                virheet.append('Avecien on oltava symmetrisiä. Nyt on määritelty {} henkilön {} aveciksi ja {} henkilön {} aveciksi.'.format(avecit[henk], henk,
                                                                                                                               avecit[avecit[henk]],
                                                                                                                               avecit[henk]))
                break
        except KeyError:
            virheet.append('Henkilölle {} ei ole merkitty avecia, vaikka hänet on merkitty henkilön {} aveciksi.'.format(avecit[henk], henk))

    if virheet:
        if len(virheet) > 10:
            raise AssertionError('\n'.join(virheet[:10]) + '\n...')
        else:
            raise AssertionError('\n'.join(virheet))

    if varoitukset:
        msgbox = messagebox.askquestion('Toivelistauksissa on juhliin osallistumattomia henkilöitä',
                                        '\n'.join(varoitukset) + '\n\nJatketaanko silti?', icon = 'warning')
        if msgbox == 'yes':
            pass
        else:
            raise AssertionError('Suorittaminen pyynnöstäsi keskeytetty. Syy:\n' + '\n'.join(varoitukset))

    #pituudet = [(1, 8), (1, 6)]

    osallistujamaara = len(osallistujat)

    #loppupopulaation_tallennusnimi = 'edellisen_loppupopulaatio.py'

    pituudet = []
	
    pituusdata = pituusdata_str.split()

    for indeksi, luku in enumerate(pituusdata):
        if indeksi % 2 == 0:
            assert luku in {'0', '1', '2'}
            pituudet.append((int(luku), int(pituusdata[indeksi+1])))
        else:
            pass

    lask_osallistujamaara = sum(2*v[1]+v[0] for v in pituudet)

    if osallistujamaara != lask_osallistujamaara:
        raise AssertionError('Osallistujalistassa on {} osallistujaa, mutta antamiisi pöytiin menee {}.'.format(osallistujamaara, lask_osallistujamaara))


    def luo_paikat():
        vastaus = []
        for n, mp in enumerate(pituudet):
            if mp[0] > 0:
                vastaus.append((n, 0, 0))
            for paikka in range(mp[1]):
                vastaus.append((n, 1, paikka))
                vastaus.append((n, 2, paikka))
            if mp[0] == 2:
                vastaus.append((n, 0, 1))
        return vastaus

    paikat = luo_paikat()

    def shuffled(x):
        u = list(x)
        random.shuffle(u)
        return u

    def uusi_sali(permutaatio):
        sali = Sali(pituudet)
        vastaus = []
        for n, henkilo in enumerate(permutaatio):
            pt, rv, pk = paikat[n]
            if rv == 1 and pk == 0:
                if sukupuolet[henkilo] != 'o':
                    sali.sijoita(pt, rv, pk, henkilo, sukupuolet[henkilo])
                else: # Paikalle (1, 0) muunsukupuolinen -> seuraava mies tai nainen ratkaisee sukupuolten määrän.
                    # Jos jäljellä vain muunsukupuolisia, arvotaan (for-else-silmukan else-kohta)
                    jaljella = permutaatio[n+1:]
                    for m, h in enumerate(jaljella):
                        if sukupuolet[h] in {'m', 'n'}:
                            jl = m+1
                            if jl%4 in {1, 2}: # eri sukupuolta
                                sali.sijoita(pt, rv, pk, henkilo, vastakkainen(sukupuolet[h]))
                            else:
                                sali.sijoita(pt, rv, pk, henkilo, sukupuolet[h])
                            break
                    else:
                        sali.sijoita(pt, rv, pk, henkilo, random.choice(['m', 'n']))
            else:
                sali.sijoita(pt, rv, pk, henkilo)
        return sali

    def satunnainen_ij():
        return uusi_sali(shuffled(nimet))

    def vastsij(sali):
        """Vastakkaisen sukupuolen paikalle sijoitetut"""
        sijsuk = sali.sijoitetut_sukupuolet()
        return [w for w in nimet if vastakkaiset(sukupuolet[w], sijsuk[w])]

    def max_min_vastsij():
        """Vastakkaisen sukupuolen paikoille sijoitettujen henkilön minimi- ja maksimimäärät väkipakolla"""
        mcx = list(miehet) # Maksimilasku
        ncx = list(naiset)
        ocx = list(muut)
        mcn = list(miehet) # Minimilasku
        ncn = list(naiset)
        ocn = list(muut)

        # Samaa sukupuolta olevat avecit merkitään laskua varten muunsukupuolisiksi
        ssavecit = {w for w in avecit if samat(sukupuolet[w], sukupuolet[avecit[w]])}
        for i in ssavecit:
            if sukupuolet[i] == 'm':
                mcx.remove(i)
                mcn.remove(i)
            else:
                ncx.remove(i)
                ncn.remove(i)
            ocx.append(i)
            ocn.append(i)

        maksimi = Sali(pituudet)
        minimi = Sali(pituudet)

        if len(mcx) < len(ncx):
            vahemmistox = mcx
        else:
            vahemmistox = ncx

        if len(mcn) > len(ncn):
            enemmiston = mcn
        else:
            enemmiston = ncn

        for pt, rv, pk in paikat:
            # Maksimi
            if rv == 0:
                try: # Sijoita VÄHEMMISTÖsukupuolen edustaja neutraalille paikalle
                    maksimi.sijoita(pt, rv, pk, vahemmistox.pop())
                except IndexError:
                    try:
                        maksimi.sijoita(pt, rv, pk, ocx.pop())
                    except IndexError:
                        if mcx:
                            maksimi.sijoita(pt, rv, pk, mcx.pop())
                        else:
                            maksimi.sijoita(pt, rv, pk, ncx.pop())
            elif rv == 1 and pk == 0:
                try:
                    maksimi.sijoita(pt, rv, pk, mcx.pop(), 'm')
                except IndexError:
                    try:
                        maksimi.sijoita(pt, rv, pk, ncx.pop(), 'n')
                    except IndexError:
                        maksimi.sijoita(pt, rv, pk, ocx.pop(), 'm')
            elif maksimi.poydat[pt].listat[rv][pk][1] == 'n': # Seuraavana vuorossa naisen paikka,
                try: # sijoita nainen
                    maksimi.sijoita(pt, rv, pk, ncx.pop())
                except IndexError:
                    try:
                        maksimi.sijoita(pt, rv, pk, mcx.pop())
                    except IndexError:
                        maksimi.sijoita(pt, rv, pk, ocx.pop())
            elif maksimi.poydat[pt].listat[rv][pk][1] == 'm':
                try:
                    maksimi.sijoita(pt, rv, pk, mcx.pop())
                except IndexError:
                    try:
                        maksimi.sijoita(pt, rv, pk, ncx.pop())
                    except IndexError:
                        maksimi.sijoita(pt, rv, pk, ocx.pop())
            else:
                raise Exception('Käsittämätön virhe')

            # Minimi
            if rv == 0:
                try: # Sijoita ENEMMISTÖsukupuolen edustaja neutraalille paikalle
                    minimi.sijoita(pt, rv, pk, enemmiston.pop())
                except IndexError:
                    try:
                        minimi.sijoita(pt, rv, pk, ocn.pop())
                    except IndexError:
                        if mcn:
                            minimi.sijoita(pt, rv, pk, mcn.pop())
                        else:
                            minimi.sijoita(pt, rv, pk, ncn.pop())
            elif rv == 1 and pk == 0:
                try:
                    minimi.sijoita(pt, rv, pk, mcn.pop(), 'm')
                except IndexError:
                    try:
                        minimi.sijoita(pt, rv, pk, ncn.pop(), 'n')
                    except IndexError:
                        minimi.sijoita(pt, rv, pk, ocn.pop(), 'm')
            elif minimi.poydat[pt].listat[rv][pk][1] == 'n': # Seuraavana vuorossa naisen paikka,
                try: # sijoita nainen
                    minimi.sijoita(pt, rv, pk, ncn.pop())
                except IndexError:
                    try:
                        minimi.sijoita(pt, rv, pk, mcn.pop())
                    except IndexError:
                        minimi.sijoita(pt, rv, pk, ocn.pop())
            elif minimi.poydat[pt].listat[rv][pk][1] == 'm':
                try:
                    minimi.sijoita(pt, rv, pk, mcn.pop())
                except IndexError:
                    try:
                        minimi.sijoita(pt, rv, pk, ncn.pop())
                    except IndexError:
                        minimi.sijoita(pt, rv, pk, ocn.pop())
            else:
                raise Exception('Käsittämätön virhe')
        return len(vastsij(maksimi)), len(vastsij(minimi))

    maxvastsij, minvastsij = max_min_vastsij()
    print('Suurin luonnollinen vastakkaisen sukupuolen paikalle sijoitettujen henkilöiden määrä:', maxvastsij)
    print('Pienin mahdollinen vastakkaisen sukupuolen paikalle sijoitettujen henkilöiden määrä:', minvastsij)

    alkualgoritmi = satunnainen_ij

    SURU = -5 # maksimionnellisuuden vastaluku rangaistukseksi surullisesta henkilöstä
    KATASTROFI = -20 # KATASTROFI*osallistujamaara <= huonoimman mahdollisen istumajärjestyksen hyvyysarvo

    def onnellisuus(henkilo, sali):
        if not toiveet[henkilo] and henkilo not in avecit:
            return 0

        vier, vast, kvast, seur = sali.vier_vast_kvast_seur(henkilo)

        tot = 0

        if henkilo in avecit:
            if avecit[henkilo] not in seur:
                tot -= 10
            elif avecit[henkilo] in kvast:
                tot -= 8
            elif avecit[henkilo] in vast:
                tot -= 6
            for w in toiveet[henkilo]:
                if w in seur:
                    tot += 1
            return tot

        for w in seur:
            if w in toiveet[henkilo]:
                tot += 1

        if not tot:
            return SURU
        else:
            return tot

    def onnellisuudet(sali):
        return [onnellisuus(nimi, sali) for nimi in nimet]

    def kokonaisonnellisuus(sali):
        onnsumma = sum(onnellisuudet(sali))
        sijsuk = sali.sijoitetut_sukupuolet()

        sijoitusvirheet = 0
        paatypisteet = 0

        for henkilo in nimet:
            if vastakkaiset(sukupuolet[henkilo], sijsuk[henkilo]):
                if henkilo in avecit and sukupuolet[henkilo] == sukupuolet[avecit[henkilo]]:
                    continue # Ei vähennystä, jos avecpari on samaa sukupuolta
                sijoitusvirheet += 1
                seurmaara = sali.seuralaisten_maara(henkilo)
                paatypisteet += (5-seurmaara)

        if sijoitusvirheet > maxvastsij:
            sijoitusvirheet *= 9
            return onnsumma - sijoitusvirheet + paatypisteet
        else: # Jos vastakkaisen sukupuolen paikalle sijoitettuja vähemmän kuin maksimimäärä
            ##virheidenvahyyspisteet = 2*(maxvastsij-sijoitusvirheet)
            ##return onnsumma - sijoitusvirheet + paatypisteet + virheidenvahyyspisteet
            #sievennettynä:
            return 2*maxvastsij + onnsumma + paatypisteet - 3*sijoitusvirheet
        
    def optimoi(sali):
        istujat = sali.istujat
        #sijsukupuolet = sali.sijoitetut_sukupuolet()
        onn = kokonaisonnellisuus(sali)

        for comb in shuffled(itertools.combinations(istujat, 2)):
            sali.vaihda(*comb)
            uusi_onn = kokonaisonnellisuus(sali)
            if uusi_onn >= onn:
                onn = uusi_onn
                continue
            else:
                sali.vaihda(*comb)
        return onn

    def rindex(li, item):
        """Alkion item viimeinen esiintymä listasta li.
    Lauseke sivulta https://stackoverflow.com/questions/6890170/how-to-find-the-last-occurrence-of-an-item-in-a-python-list
    vaihdettu 'a' muotoon item"""
        return next(i for i,v in zip(range(len(li)-1, -1, -1), reversed(li)) if v == item)

    kombinaatioita = osallistujamaara*(osallistujamaara-1)//2 # osallistujista muodostettavissa olevien (järjestämättömien) parien lukumäärä

    def mutaatiot(sali, yrityksia):
        if kombinaatioita <= yrityksia:
            return optimoi(sali)
        vaihtokokeilut = [random.sample(paikat, 2) for i in range(yrityksia)]
        onn = kokonaisonnellisuus(sali)
        for vaihto in vaihtokokeilut:
            sali.vaihda(*vaihto)
            uusi_onn = kokonaisonnellisuus(sali)
            if uusi_onn < onn:
                sali.vaihda(*vaihto)
            else:
                onn = uusi_onn
        return onn

    def surulliset(sali):
        return [w for w in snimet if onnellisuus(w, sali) < 0]

    def aikamutaatiot(sali, aika, suosi_surullisia=False):
        if suosi_surullisia:
            v = surulliset(sali)
            if not v:
                suosi_surullisia = False
                print('Tämä sali on muuten suruton!')
                print(sali.merkkijono())
            else:
                for henkilo in tuple(v):
                    for toive in toiveet[henkilo]:
                        v.extend(sali.seuralaiset(toive))
            random.shuffle(v)
        else:
            v = shuffled(paikat)
        alkuaika = aik()
        onn = kokonaisonnellisuus(sali)
        for vaihto in itertools.combinations(v, 2):
            sali.vaihda(*vaihto)
            uusi_onn = kokonaisonnellisuus(sali)
            if uusi_onn < onn:
                sali.vaihda(*vaihto)
            else:
                onn = uusi_onn
            if aik() - alkuaika >= aika:
                return onn
        return onn

    def vaihtele_vastapaisia(sali):
        onn = kokonaisonnellisuus(sali)
        for m, poyta in enumerate(sali.poydat):
            for n in shuffled(range(poyta.pituus)):
                sali.vaihda((m, 1, n), (m, 2, n))
                uusi_onn = kokonaisonnellisuus(sali)
                if uusi_onn < onn:
                    sali.vaihda((m, 1, n), (m, 2, n))
                else:
                    onn = uusi_onn
        return onn

    

    lmp = min(1/populaation_koko, 0.25) # Lisääntymisen aikana tehtävän mutaation todennäköisyys

    def lisaanny(sali1, sali2):
        dh = sorted(random.sample(range(osallistujamaara), 2))
        dh[1] += 1
        ykkosesta = range(*dh)
        permutaatio = [None for i in range(osallistujamaara)]
        maxi = osallistujamaara - 1
        sali1_istujat = sali1.getIstujat()
        permutaatio[ykkosesta[0]:ykkosesta[-1]] = sali1_istujat[ykkosesta[0]:ykkosesta[-1]]
        ykkosenhenkilot = set(sali1_istujat[ykkosesta[0]:ykkosesta[-1]])

        sali2_istujat = [h for h in sali2.getIstujat() if h not in ykkosenhenkilot]

        i = permutaatio.index(None)
        r = rindex(permutaatio, None)
        k = 0

        while i <= maxi and permutaatio[i] is None:
            permutaatio[i] = sali2_istujat[k]
            i += 1
            k += 1

        while r >= 0 and permutaatio[r] is None:
            permutaatio[r] = sali2_istujat[k]
            r -= 1
            k += 1

        answer = uusi_sali(permutaatio)

        while random.random() < lmp: # Pieni mahdollisuus myös epäsuotuisille mutaatioille.
            answer.vaihda(*random.sample(paikat, 2))
        
        vaihtele_vastapaisia(answer)
        return answer

    def kuvaus(sali, istujat=None):
        jarjestys = sali.merkkijono()
        if istujat is None:
            tistujat = sali.getIstujat()
        else:
            tistujat = istujat
        
        informaatio = []
        
        for istuja in tistujat:
            if istuja in avecit:
                informaatio.append('{}, avec {}; {} ({}):'.format(istuja, avecit[istuja], toiveet[istuja], sukupuolet[istuja]))
            else:
                informaatio.append('{} {} ({}):'.format(istuja, toiveet[istuja], sukupuolet[istuja]))
            vier, vast, kvast = sali.vier_vast_kvast(istuja)
            for vierustoveri in vier:
                if vierustoveri in toiveet[istuja]:
                    informaatio.append('Vi {} (TOIVE)'.format(vierustoveri))
                else:
                    informaatio.append('Vi {}'.format(vierustoveri))
            for vastapainen in vast:
                if vastapainen in toiveet[istuja]:
                    informaatio.append('Va {} (TOIVE)'.format(vastapainen))
                else:
                    informaatio.append('Va {}'.format(vastapainen))
            for kulmvast in kvast:
                if kulmvast in toiveet[istuja]:
                    informaatio.append('Ku {} (TOIVE)'.format(kulmvast))
                else:
                    informaatio.append('Ku {}'.format(kulmvast))

            onn = onnellisuus(istuja, sali)

            informaatio.append('Onnellisuus: {}\n'.format(onn))
            
        return '{}\nKokonaisonnellisuus: {}\n\n{}'.format(jarjestys, kokonaisonnellisuus(sali), '\n'.join(informaatio))[:-1]
        
    kuvaukset = set()
    paras_onn = KATASTROFI*osallistujamaara
    #import time;a=time.time()
    #nyksali = alkualgoritmi()

    sukupolvien_parhaat = []

    #assert False

    i = 0

    luovutuksia = 0

    if kombinaatioita < mutaatiomaara:
        messagebox.showinfo('Huomio', 'Pyysit suuremman määrän mutaatioita ({}) kuin osallistujajoukosta saa 2-kombinaatioita ({}). Mutaatioita tehdään siis jälkimmäinen määrä per sukupolvi.'.format(mutaatiomaara, kombinaatioita))
        mutaatiomaara = kombinaatioita

    ALKUP_MUTAATIOMAARA = mutaatiomaara


    if sukupolvia < 2:
        raise AssertionError('Sukupolvia pitää olla vähintään 2.')

    if max_ilman_edistysta < 2:
        raise AssertionError('Ei voida luovuttaa alle 2 edistyksettömän sukupolven jälkeen.')

    if loppukiriaika < 0:
        raise AssertionError('Loppukiriaika ei voi olla negatiivinen.')

    #luovutukset_taynna = False

    suruttomat = set()

    sukupolvi = 1

    print('Sukupolvi {}:'.format(sukupolvi))

    populaatio = [satunnainen_ij() for x in range(populaation_koko)]
    print('Alkupopulaatio luotu.')
    onnellisuusrivin_indeksi = len(populaatio[0].merkkijono().splitlines())

    def onnellisuus_kuvauksesta(guvaus):
        return int(guvaus.splitlines()[onnellisuusrivin_indeksi].split()[-1])

    pdist = [n**3 for n in range(1, populaation_koko + 1)][::-1]
    pdist = [p/sum(pdist) for p in pdist] # lisääntymisten todennäköisyysjakauma

    for sali in populaatio:
        mutaatiot(sali, mutaatiomaara)
    print('Mutaatiot tehty.')

    populaatio.sort(key=lambda x:kokonaisonnellisuus(x), reverse=True)

    sukupolvien_parhaat.append(kuvaus(populaatio[0]))

    sukupolvi += 1

    def lisaantymiset():
        nonlocal populaatio
        indeksi = populaation_koko//2
        while indeksi < populaation_koko:
            arg1_index, arg2_index = numpyrandomchoice(range(populaation_koko), 2, p=pdist)
            populaatio[indeksi] = lisaanny(populaatio[arg1_index], populaatio[arg2_index])
            indeksi += 1


    ilman_edistysta = 0

    try:
        while sukupolvi <= sukupolvia:
            print('Sukupolvi {}:'.format(sukupolvi))
            lisaantymiset()
            print('Lisäännytty.')
            for sl in populaatio:
                mutaatiot(sl, mutaatiomaara)
            print('Mutaatiot tehty.')
            sukupolvi += 1
            populaatio.sort(key=lambda x:kokonaisonnellisuus(x), reverse=True)
            sukupolvien_parhaat.append(kuvaus(populaatio[0]))
            onn = kokonaisonnellisuus(populaatio[0])
            if onn > paras_onn:
                paras_onn = onn
                ilman_edistysta = 0
                if mutaatiomaara != ALKUP_MUTAATIOMAARA:
                    mutaatiomaara = ALKUP_MUTAATIOMAARA
                    print('Mutaatioita kokeillaan jälleen {} kpl/ratkaisuyritys.'.format(mutaatiomaara))
            else:
                ilman_edistysta += 1
                # Tässä sukupuolellisessa versiossa ei ollut seuraavaa 15 riviä graafisen käyttöliittymän alkuvaiheessa.
                if ilman_edistysta == round((3/4)*max_ilman_edistysta):
                    if mutaatiomaara < kombinaatioita:
                        mutaatiomaara = max((mutaatiomaara * 3) // 2, 2) # Loppukiri mutaatioissa
                        print('Mutaatioyritysten määrää suurennettu arvoon', min(mutaatiomaara, kombinaatioita), end='.\n')
                        print('Vaihdellaan vielä vastapäisiä...')
                    else:
                        print('Vaihdellaan vastapäisiä...')
                    for sl in populaatio:
                        vastonn = vaihtele_vastapaisia(sl)
                        if vastonn > paras_onn:
                            ilman_edistysta = 0
                            paras_onn = vastonn
                            if mutaatiomaara != ALKUP_MUTAATIOMAARA: # lisätty vasta graafiseen käyttöliittymään
                                mutaatiomaara = ALKUP_MUTAATIOMAARA # myös sukupuolettomaan versioon
                                print('Koska vastapäisten vaihteleminen auttoi, mutaatioita kokeillaan jatkossa sittenkin vain {} kpl/ratkaisuyritys.'.format(mutaatiomaara))
                if ilman_edistysta >= max_ilman_edistysta:
                    print('Ei edistystä {} sukupolveen.'.format(ilman_edistysta))
                    print('Paras olemassa oleva: {}'.format(paras_onn))
                    if loppukiriaika:
                        print('Loppukiri. {0} s ei suosita surullisia, {0} s suositaan...'.format(loppukiriaika/2))
                        aikamutaatiot(populaatio[0], loppukiriaika/2)
                        loppukirionnellisuus = aikamutaatiot(populaatio[0], loppukiriaika/2, True)
                        if loppukirionnellisuus > paras_onn:
                            paras_onn = loppukirionnellisuus
                            #mutaatiomaara = min(ALKUP_MUTAATIOMAARA + 1, kombinaatioita) #mitähän mahdoin ajatella, kun oli tuo +1?
                            mutaatiomaara = min(ALKUP_MUTAATIOMAARA, kombinaatioita)
                            ilman_edistysta = 0
                            print('LOPPUKIRI AUTTOI! Jatketaan tehden {} mutaatiota per sali.'.format(mutaatiomaara))
                        else:
                            print('Loppukiri ei auttanut.')
                            break
    ##                        hyodytty = False
    ##                        for sl in populaatio:
    ##                            vastonn = vaihtele_vastapaisia(sl)
    ##                            if vastonn > paras_onn:
    ##                                paras_onn = vastonn
    ##                                hyodytty = True
    ##                        if not hyodytty:
    ##                            print('Vastapäisten vaihteleminenkaan ei auttanut. Lopetetaan.')
    ##                            break
    ##                        else:
    ##                            ilman_edistysta = 0
    ##                            mutaatiomaara = ALKUP_MUTAATIOMAARA
    ##                            print('Vastapäisten vaihteleminen auttoi! Uusi paras:', paras_onn)
                    else:
                        #print('Paras olemassa oleva: {}'.format(paras_onn)) # Tulostettu jo aiemmin
    ##                    print('Vaihdellaan vielä vastapäisiä...')
    ##                    hyodytty = False
    ##                    for sl in populaatio:
    ##                        vastonn = vaihtele_vastapaisia(sl)
    ##                        if vastonn > paras_onn:
    ##                            paras_onn = vastonn
    ##                            hyodytty = True
    ##                    if not hyodytty:
    ##                        print('Vastapäisten vaihteleminen ei auttanut. Lopetetaan.')
    ##                        break
    ##                    else:
                        break
            print('Paras olemassa oleva: {}'.format(paras_onn))
            print('Peräkkäisiä edistyksettömiä sukupolvia', ilman_edistysta, end='.\n')
    except Exception as virhe:
        raise virhe
    finally:
        populaatio.sort(key=lambda x:kokonaisonnellisuus(x), reverse=True) # näyttää vahvasti siltä, että tätä tarvitaan
        paremmuusjarjestys = sorted(set(sukupolvien_parhaat), key=lambda x:onnellisuus_kuvauksesta(x), reverse=True)
        tallennettavat = {a for a in paremmuusjarjestys if onnellisuus_kuvauksesta(a) == paras_onn}
        for ratkaisu in populaatio:
            if kokonaisonnellisuus(ratkaisu) == paras_onn:
                tallennettavat.add(kuvaus(ratkaisu))
            else:
                break # populaatio on järjestetty onnellisuuden mukaan
        return list(tallennettavat)

