import sys
from tkinter import Tk, Label, Entry, Text, IntVar, Button, Checkbutton, Toplevel, Frame
from tkinter import END, E, W, TOP, BOTTOM, LEFT
from tkinter import messagebox
from tkinter import filedialog
import os
import SPM
import SPT
from SurrogatePair import remove_surrogates, with_surrogates
#from data import images

def resource_path(relative_path): # function written by Gemini and edited by Claude
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # If not running as exe, use the script's own folder
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

def aseta_ikoni(ikkuna):
    try:
        ikkuna.iconbitmap(icon_path) # .ico-ikonit toimivat vain Windowsissa
    except Exception:
        pass

nyk = SPT

root = Tk()
root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())

icon_path = resource_path("ticon.ico")

aseta_ikoni(root)

#https://stackoverflow.com/questions/3949844/how-to-get-the-screen-size-in-tkinter/3949983#3949983
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()

data_text_width = max(23, screenwidth//25) # ei voi olla 23:a pienempi, että Avaa... ja Laske osallistujamäärä saadaan samaan soluun.
data_text_height = max(10, screenheight//40)
#data_text_width = 23
#data_text_height = 10

def onnellisuus_kuvauksesta(guvaus):
    for i in guvaus.splitlines():
        if i.startswith('Kokonaisonnellisuus: '):
            return int(i.split(': ')[-1])

def surulliset_kuvauksesta(guvaus):
    rivit = guvaus.splitlines()
    vastaus = []
    muistuttaa_istumajarjestysta = False
    for n, i in enumerate(rivit):
        if n < 3:
            continue
        if i.startswith('Onnellisuus: '):
            muistuttaa_istumajarjestysta = True
            onn = int(i.split()[-1])
            if onn < 0:
                ti = n
                while rivit[ti] and ti>0:
                    ti -= 1
                vastaus.append(rivit[ti+1][:-1])
    return vastaus, muistuttaa_istumajarjestysta

root.title('Istumajärjestys')

poydatkentta = "Pöytien muodot ja pituudet"

Label(root, text="Juhla").grid(row=1, sticky=E)
Label(root, text=poydatkentta).grid(row=2, sticky=E)
Label(root, text="Populaation koko").grid(row=3, sticky=E)
Label(root, text="Max sukupolvia").grid(row=4, sticky=E)
Label(root, text="Mutaatioita/ratk.ehd./sukupolvi").grid(row=5, sticky=E)
Label(root, text="Max peräkk. edistyksettömiä sukupolvia").grid(row=6, sticky=E)
Label(root, text="Loppukiriaika").grid(row=7, sticky=E)
Label(root, text="Osallistujien tiedot").grid(row=9, sticky=E)

ohje_mj = r"""Nappi "Avaa" avaa tiedoston ja laittaa sen polun kenttään Juhla ja sisällön kenttään Osallistujien tiedot. Juhla-kentän sisältö vaikuttaa siihen, millä nimillä istumajärjestykset tallennetaan. Oletusarvoisesti ne tallennetaan samaan kansioon Avaa-napilla avatun osallistujalistatiedoston kanssa nimillä, joiden tiedostopäätettä ennen on _ + onnellisuus + _ + numero.

{0}{1}-kenttään tulee lukuja välilyönneillä erotettuna, esim. 2 8 1 5 0 4 tarkoittaa, että ensimmäisessä pöydässä on 8 henkilöä rivillä ja kummassakin päässä istuu joku (2*8+2=18 henkilöä), seuraavassa pöydässä on 5 henkilöä per rivi ja vain toisessa päässä istuu joku (2*5+1=11 henkilöä) ja viimeisessä on 4 henkilöä rivillä (8 yhteensä), kun kummassakaan päässä ei istu kukaan. Kentästä saatavan osallistujamäärän on täsmättävä todelliseen osallistujamäärään, mainitussa esimerkkitapauksessa siis 2+8*2+1+5*2+0+4*2 = 37.

Populaation koko tarkoittaa sitä, kuinka monta ratkaisuehdotusta tutkitaan kerrallaan. Jos istujia 30 tai alle, tämä luku voi olla vaikkapa 100. Jos osallistujia on paljon, kannattanee käyttää pienempää populaatiota.

Max sukupolvia -kenttään tulee se lukumäärä, kuinka monen sukupolven jälkeen ratkaisujen hakeminen viimeistään lopetetaan.

Mutaatioita/ratk.ehd./sukupolvi-kenttään tulee se lukumäärä, kuinka monta kertaa kokeillaan vaihtaa henkilöiden paikkaa per ratkaisuehdotus per sukupolvi. Suurimmillaan tämä luku voi olla osallistujamäärästä saatava 2-kombinaatioiden eli järjestämättömien parien lukumäärä: n*(n-1)/2, missä n on osallistujamäärä.

Max peräkk. edistyksettömiä sukupolvia -kenttään tulee se lukumäärä, kuinka monta sukupolvea saadaan mennä peräkkäin ilman, että paras ratkaisuehdotus on yhtään sen parempi. Jos mennään näin monta sukupolvea eteenpäin ilman, että on yhtään edistytty, algoritmin suorittaminen lopetetaan.

Loppukiriaika tarkoittaa sitä, kuinka monta sekuntia algoritmin suorittamisen jälkeen yritetään vielä viimeisen kerran parantaa parasta toistaiseksi löydettyä istumajärjestystä. Tämän todennäköisyys osoittautua hyödylliseksi on pieni, siispä kentässä on oletusarvona nolla. Tähän voi laittaa desimaaliluvun, mutta siinä pitää käyttää desimaalipistettä (ei pilkkua). Loppukiri jää välistä, jos maksimimäärä sukupolvia on täynnä.

Osallistujien tiedot annetaan muodossa: "Nimi(sukupuoli): Toive1, Toive2, ..., ToiveN|avec". Sukupuoli, jos se halutaan ottaa huomioon, on joko m (mies), n (nainen), o (muu eli voidaan sijoittaa sekä naisen että miehen paikalle). Se kirjoitetaan suoraan nimen perään, esim. Matti Virtanenm: Liisa Korhonen, ... Jos sukupuolia ei haluta ottaa huomioon, niitä ei saa olla merkittynäkään. Sukupuolimerkinnät voi poistaa klikkaamalla Poista sukupuolet.

Jos henkilöllä ei ole toiveita eikä avecia, hänen nimensä ja mahdollisen sukupuolensa perään on kuitenkin kirjoitettava kaksoispiste ja välilyönti.

Kun algoritmi on suoritettu, ensimmäinen löydetty ratkaisu ilmestyy oikeanpuoleiseen tekstikenttään, Ehdotus-sanan alle. Voit selailla ehdotuksia tallentamatta niitä Edellinen- ja Seuraava -napeilla. Voit tallentaa kaikki ehdotukset klikkaamalla Tallenna kaikki. Tiedostot tallennetaan Juhla-kentässä annetun tiedostonimen mukaan. Esimerkiksi jos Juhla-kentässä lukee C:/Users/nimi/Documents/istumajärjestys.txt ja löydettyjen istumajärjestysten onnellisuus on 30, tiedostot tallennetaan kansioon C:/Users/nimi/Documents/ ja nimet ovat muotoa istumajärjestys_30_0.txt, istumajärjestys_30_1.txt, istumajärjestys_30_2.txt jne.

Painike "Suorita" suorittaa algoritmin, kun kaikki tiedot ja parametrit on annettu. Painike "Surulliset?" luettelee näkyvissä olevan ratkaisun surulliset henkilöt eli ne, jotka eivät ole avecinsa vieressä tai joilla on toiveita muttei avecia, ja yksikään toive ei ole toteutettu.

Painike "Laske osallistujamäärä" kertoo, kuinka monta osallistujaa sitseillä on annetun osallistujalistan sekä {0}{1}-kentän mukaan (niiden on oltava samat, jotta istumajärjestyksiä voidaan hakea) sekä myös sen, kuinka monta järjestämätöntä paria saadaan osallistujalistan mukaisesta osallistujamäärästä. Tämä on siis suurin mahdollinen mutaatiomäärä, jolla algoritmi voidaan suorittaa.

"""[:-2].format(poydatkentta, ' ' if ' ' in poydatkentta else '')

def set_text(entry, text):
    entry.delete(0,END)
    entry.insert(0,text)

juhla_entry = Entry(root, width=data_text_width)
poydat_entry = Entry(root)
populaatio_entry = Entry(root)
sukupolvet_entry = Entry(root)
mutaatiot_entry = Entry(root)
luovutus_entry = Entry(root)
loppukiriaika_entry = Entry(root)
data_text = Text(root, width=data_text_width, height=data_text_height)
answer_text = Text(root, width=data_text_width, height=data_text_height)

def avaa_tiedosto():
    filename = filedialog.askopenfilename(filetypes=(('Tekstitiedostot', '*.txt'), ('Kaikki tiedostot', '*.*')))
    if not filename:
        return None
    try:
        with open(filename, 'rt', encoding='utf-8') as file:
            content = file.read()
            content = with_surrogates(content[content.startswith('\ufeff'):])
        set_text(juhla_entry, filename)
        data_text.delete('1.0', END)
        data_text.insert(END, content)
    except Exception as e:
        messagebox.showinfo('Virhe', str(type(e)) + '\n' + str(e))

set_text(loppukiriaika_entry, '0')

juhla_entry.grid(row=1, column=1, sticky=W)
poydat_entry.grid(row=2, column=1, sticky=W)
populaatio_entry.grid(row=3, column=1, sticky=W)
sukupolvet_entry.grid(row=4, column=1, sticky=W)
mutaatiot_entry.grid(row=5, column=1, sticky=W)
luovutus_entry.grid(row=6, column=1, sticky=W)
loppukiriaika_entry.grid(row=7, column=1, sticky=W)
sph_intvar = IntVar()
sukupuoltenhuomiointi = Checkbutton(root, text="Ota sukupuolet huomioon", variable=sph_intvar)
sukupuoltenhuomiointi.grid(row=8, column=1, sticky=W)
Label(root, text="Ehdotus").grid(row=8, column=2)

def poista_sukupuolet():
    nyk_data = data_text.get("1.0","end-1c")
    uusi_data = []
    try:
        for rivi in nyk_data.splitlines():
            #print(rivi)
            nimi, listaukset = rivi.split(': ')
            if not (nimi.endswith('m') or nimi.endswith('n') or nimi.endswith('o')):
                messagebox.showinfo('Virhe', '{} ei pääty m:ään, n:ään eikä o:hon.'.format(nimi))
                return None
            uusi_data.append(nimi[:-1] + ': ' + listaukset)
        data_text.delete('1.0', END)
        data_text.insert(END, '\n'.join(uusi_data))
        sph_intvar.set(0)
    except Exception as e:
        messagebox.showinfo('Virhe', str(type(e)) + '\n' + str(e))
        #raise

data_text.grid(row=9, column=1)
answer_text.grid(row=9, column=2)


def messageboxohje(ikkuna):
    messagebox.showinfo('Käyttöohje', ohje_mj)
    ikkuna.destroy()

def vasenohje(ikkuna):
    data_text.delete('1.0', END)
    data_text.insert(END, ohje_mj)
    ikkuna.destroy()

def oikeaohje(ikkuna):
    answer_text.delete('1.0', END)
    answer_text.insert(END, ohje_mj)
    ikkuna.destroy()

def tuhoa(ikkuna):
    ikkuna.destroy()

def tallenna_ohje_tiedostoon(ikkuna):
    filename = filedialog.asksaveasfilename(filetypes=(('Tekstitiedostot', '*.txt'), ('Kaikki tiedostot', '*.*')))
    if not filename:
        ikkuna.destroy()
        return None
    try:
        with open(filename, 'wt', encoding='utf-8') as k:
            print(ohje_mj, end='', file=k)
    except Exception as e:
        messagebox.showinfo('Virhe', str(type(e)) + '\n' + str(e))
    finally:
        ikkuna.destroy()

def ohje():    
    kysymysikkuna = Toplevel()
    aseta_ikoni(kysymysikkuna)
    kysymysikkuna.title("Ohje")
    topframe = Frame(kysymysikkuna)
    Label(topframe, text="Miten haluat ohjeen näytettävän?").pack()
    topframe.pack(side=TOP)
    bottomframe = Frame(kysymysikkuna)
    bottomframe.pack(side=BOTTOM)
    
    mbohje = Button(bottomframe, text="Näytä viestilaatikkona", command=lambda: messageboxohje(kysymysikkuna))
    vohje = Button(bottomframe, text="Kirjoita osallistujalistan paikalle", command=lambda: vasenohje(kysymysikkuna))
    oohje = Button(bottomframe, text="Kirjoita vastausten paikalle (oikealle)", command=lambda: oikeaohje(kysymysikkuna))
    tt = Button(bottomframe, text="Tallenna tiedostoon", command=lambda: tallenna_ohje_tiedostoon(kysymysikkuna))
    peruuta = Button(bottomframe, text="Peruuta", command=lambda: tuhoa(kysymysikkuna))

    mbohje.pack(side=LEFT)
    vohje.pack(side=LEFT)
    oohje.pack(side=LEFT)
    tt.pack(side=LEFT)
    peruuta.pack(side=LEFT)


ohje_button = Button(root, text='Ohje', command=ohje)
ohje_button.grid(row=0, column=0, sticky=W)

def laske_osallistujamaara():
    data = data_text.get("1.0","end-1c")
    try:
        if data.endswith(':'):
            data += ' '
        osallistujat = {(w.split(': ')[0][:-1], w.split(': ')[0][-1]) for w in data.splitlines()}
        todellinen = len(osallistujat)
        pituudet = []
        pituusdata = poydat_entry.get().split()
        komb = todellinen*(todellinen-1)//2
        for indeksi, luku in enumerate(pituusdata):
            if indeksi % 2 == 0:
                assert luku in {'0', '1', '2'}
                pituudet.append((int(luku), int(pituusdata[indeksi+1])))
            else:
                pass
        if ' ' in poydatkentta:
            pk = poydatkentta + ' '
        else:
            pk = poydatkentta
        kentta = sum(2*v[1]+v[0] for v in pituudet)
        messagebox.showinfo("Osallistujamäärä", 'Todellinen: {} ({} paria)\n{}-kentän mukainen: {}'.format(todellinen, komb, pk, kentta))
    except Exception as e:
        return messagebox.showinfo('Virhe', str(type(e)) + '\n' +str(e))

#lom_button = Button(root, text='Laske osallistujamäärä', command=lambda: nyk.laske_osallistujamaara(data_text.get("1.0","end-1c")))
lom_button = Button(root, text='Laske osallistujamäärä', command=laske_osallistujamaara)
lom_button.grid(row=0, column=1, sticky=E)

vastaukset = []

i = 0

def suorita():
    global nyk
    global vastaukset
    global i

    if sph_intvar.get():
        nyk = SPM
    else:
        nyk = SPT

    #juhlan_nimi, data, pituusdata_str, populaation_koko, sukupolvia, mutaatiomaara, max_ilman_edistysta, loppukiriaika

    #juhlan_nimi = juhla_entry.get()
    data = data_text.get("1.0","end-1c")
    pituusdata_str = poydat_entry.get()
    populaation_koko = populaatio_entry.get()
    sukupolvia = sukupolvet_entry.get()
    mutaatiomaara = mutaatiot_entry.get()
    max_ilman_edistysta = luovutus_entry.get()
    loppukiriaika = loppukiriaika_entry.get()

##    for i in 'juhlan_nimi, data, pituusdata_str, populaation_koko, sukupolvia, mutaatiomaara, max_ilman_edistysta, loppukiriaika'.split(', '):
##        print(i, eval(i), sep=' = ')

    try:
        vast = nyk.luo_istumajarjestyksia(data, pituusdata_str, populaation_koko, sukupolvia, mutaatiomaara, max_ilman_edistysta, loppukiriaika)
        vastaukset.clear()
        vastaukset.extend(vast)
        answer_text.delete('1.0', END)
        answer_text.insert(END, vast[0])
        i = 0
    except Exception as e:
        messagebox.showinfo('Virhe', str(type(e)) + '\n' +str(e))
        #raise
    

suorita_button = Button(root, text='Suorita', command=suorita)
suorita_button.grid(row=10, column=2, sticky=W)

poistasukupuolet_button = Button(root, text='Poista sukupuolet', command=poista_sukupuolet)
poistasukupuolet_button.grid(row=10, column=1)

def tallenna(juhla, kuvaukset):
    tm = len(os.listdir())
    numero = 0
    tallennetut = []
    for guvaus in kuvaukset:
        while True:
            try:
                ##tallennettava = '.'.join(toivetiedosto.split('.')[:-1]) + '_{}_{}.txt'.format(onnellisuus_kuvauksesta(guvaus))
                onn = onnellisuus_kuvauksesta(guvaus)
                tiedostonimi = '{}_{}_{}.txt'.format(juhla, onn, numero)
                tiedosto = open(tiedostonimi, 'xt', encoding='utf-8')
                numero += 1
                print(guvaus.encode('utf-16', 'surrogatepass').decode('utf-16'), end='', file=tiedosto)
                tiedosto.close()
                tallennetut.append(tiedostonimi)
                break
            except FileExistsError:
                numero += 1
            except PermissionError:
                if numero > tm:
                    messagebox.showinfo('Lupavirhe', 'Sinulla ei ole oikeuksia tallentaa enempää tiedostoja, tai jotain...')
                    return tallennetut
                numero += 1
    return tallennetut

def seuraava():
    global i
    
    if len(vastaukset) == 0:
        messagebox.showinfo('Virhe', 'Ei ole istumajärjestysehdotuksia, joita näyttää.')
        return None
    elif len(vastaukset) == 1:
        i = 0
        answer_text.delete('1.0', END)
        answer_text.insert(END, vastaukset[i])
        messagebox.showinfo('Vain yksi istumajärjestys', 'Ei ole enempää kuin tämä yksi istumajärjestys')
        return None

    i += 1

    try:
        if i >= len(vastaukset):
            i = len(vastaukset) - 1
            messagebox.showinfo('Virhe', 'Ei ole enempää ehdotuksia kuin {}, ja nyt ollaan viimeisessä'.format(len(vastaukset)))
            return None
        answer_text.delete('1.0', END)
        answer_text.insert(END, vastaukset[i])
    except:
        i = len(vastaukset) - 1
        messagebox.showinfo('Virhe', 'Tuntematon virhe.')
        #raise
    

def edellinen():
    global i
    if len(vastaukset) == 0:
        messagebox.showinfo('Virhe', 'Ei ole istumajärjestysehdotuksia, joita näyttää.')
        return None
    elif len(vastaukset) == 1:
        i = 0
        answer_text.delete('1.0', END)
        answer_text.insert(END, vastaukset[i])
        messagebox.showinfo('Vain yksi istumajärjestys', 'Ei ole enempää kuin tämä yksi istumajärjestys')
        return None
    
    i -= 1

    if i < 0:
        i = 0
        messagebox.showinfo('Virhe', 'Ei ole enempää ehdotuksia kuin {}, ja nyt ollaan ensimmäisessä'.format(len(vastaukset)))
    else:
        try:
            #teksti = vastaukset[i]
            answer_text.delete('1.0', END)
            answer_text.insert(END, vastaukset[i])
        except:
            i += 1
            messagebox.showinfo('Virhe', 'Tuntematon virhe.')

def path_to_list(s):
    return os.path.split(s.rstrip('/' + os.sep))

def tallennusfunktio():
    global vastaukset
    juhla = juhla_entry.get()#.replace('\\', '/')
    try:
        try:
            #juhlakansio = '/'.join(juhla.split('/')[:-1])
            #print(juhlakansio)
            #juhlakansio = os.path.dirname(os.path.abspath(juhla))
            juhlakansio = os.path.dirname(os.path.abspath(juhla))
            os.chdir(juhlakansio)
        except FileNotFoundError:
            messagebox.showinfo('Virhe', 'Nimet tulevat siitä, mitä olet syöttänyt Juhla-tekstikenttään. Kansiota {} ei löydy.'.format(juhlakansio))
            return None
        #splitslash = juhla.split('/')
        splitslash = path_to_list(juhla)
        if '.' in splitslash[-1][1:]: # poistetaan tiedostopääte, mutta jos tiedostonimi alkaa pisteellä eikä sisällä enempää pisteitä,
            # katsotaan, ettei tiedostopäätettä ole
            nimet = tallenna('/'.join(splitslash[:-1]) + '/' + '.'.join(splitslash[-1].split('.')[:-1]), vastaukset)
        else:
            nimet = tallenna(juhla, vastaukset)
        if len(nimet) > 1:
            try:
                messagebox.showinfo('Valmis', 'Tallennettiin {} tiedostoa, joista ensimmäinen oli {} ja viimeinen {}'.format(len(nimet), nimet[0], nimet[-1]))
            except UnicodeEncodeError:
                messagebox.showinfo('Valmis', 'Tallennettiin {} tiedostoa, joista ensimmäinen oli {} ja viimeinen {}'.format(len(nimet), ascii(nimet[0]), ascii(nimet[-1])))
        elif len(nimet) == 1:
            try:
                messagebox.showinfo('Valmis', 'Tallennettiin 1 tiedosto: {}'.format(nimet[0]))
            except UnicodeEncodeError:
                messagebox.showinfo('Valmis', 'Tallennettiin 1 tiedosto: {}'.format(ascii(nimet[0])))
        elif len(nimet) == 0:
            messagebox.showinfo('Valmis', 'Ei tallennettu ainuttakaan tiedostoa.')
        if len(nimet) == len(vastaukset):
            vastaukset.clear()
        else:
            messagebox.showinfo('Ei tallennettu kaikkia', 'Tallennettiin {} tiedostoa, vaikka löydettyjä istumajärjestyksiä oli {}.')
    except Exception as e:
        messagebox.showinfo(str(type(e)), str(e))
        #raise

def etsi_surulliset():
    nyk_ij = answer_text.get("1.0","end-1c")

    try:
        sur, jark = surulliset_kuvauksesta(nyk_ij)
        if not jark:
            messagebox.showinfo('Ei ole kuvaus', 'Teksti ei muistuta alkuunkaan istumajärjestyksen kuvausta, jossa olisi onnellisuudet lueteltuna.')
        elif not sur:
            messagebox.showinfo('Ei surullisia', 'Tästä istumajärjestyksestä ei löytynyt ainuttakaan surullista!')
        else:
            messagebox.showinfo('Surullisia {}'.format(len(sur)), 'Tämän istumajärjestyksen surulliset:\n{}'.format('\n'.join(sur)))
    except Exception as e:
        messagebox.showinfo(str(type(e)), str(e))

avaa_button = Button(root, text='Avaa...', command=avaa_tiedosto)
avaa_button.grid(row=0, column=1, sticky=W)

edellinen_button = Button(root, text='Edellinen', command=edellinen)
seuraava_button = Button(root, text='Seuraava', command=seuraava)
tallenna_button = Button(root, text='Tallenna kaikki', command=tallennusfunktio)
edellinen_button.grid(row=8, column=2, sticky=W)
seuraava_button.grid(row=8, column=2, sticky=E)
tallenna_button.grid(row=7, column=2)

surulliset_button = Button(root, text='Surulliset?', command=etsi_surulliset)
surulliset_button.grid(row=10, column=2, sticky=E)

root.mainloop()

