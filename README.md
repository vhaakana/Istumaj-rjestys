# Sitsien istumajärjestysgeneraattori (geneettinen algoritmi)

Tämä sovellus pyrkii luomaan sitseille ja muille pöytäjuhlille optimaalisia istumajärjestyksiä geneettisen algoritmin avulla. Ohjelma ottaa huomioon osallistujien toiveet, avecit, sukupuolet sekä pöytien eri muodot ja pituudet.

Projekti tarjoaa sekä graafisen Tkinter-käyttöliittymän että valmiit suoritettavat binääritiedostot Windows-ympäristöihin.

---

## Ominaisuudet

* **Kolme pöytämuotoa:** Voit määritellä pöytien koot sekä päätypaikkojen määrät (pöydän kummassakin päädyssä, vain toisessa päädyssä tai ei kummassakaan).
* **Toiveiden ja avec-parien optimointi:** Ohjelma maksimoi kokonaisonnellisuutta: avecit pyritään sijoittamaan vierekkäin ja pöytäseuratoiveet toteuttamaan. Valinnaisesti ohjelma ottaa huomioon myös sukupuolet vuorottelevilla miesten ja naisten paikoilla. Tarkemmin kohdassa [Pisteytys](#pisteytys).
* **Surulliset-työkalu:** Tunnistaa nopeasti osallistujat, joiden toiveet tai avec-ehdot eivät toteutuneet.
* **Mukautuva geneettinen algoritmi:**
  * Jokaista ratkaisuehdotusta parannetaan paikallisella haulla.
  * Mutaatiomäärää kasvatetaan automaattisesti, jos kehitys pysähtyy.
  * Vastapäisten paikkojen erillisvaihtelu paikallisten optimien murtamiseksi.
* **Laaja yhteensopivuus:** Windows 10/11, Windows XP, Linux (lähdekoodista) ja macOS (lähdekoodista, testaamatta) (ks. [Asennus](#asennus-ja-käyttö)).

---

## Asennus ja käyttö

### 1. Valmiit Windows-ohjelmat (`.exe`)

Lataamalla valmiin EXE-tiedoston projektin Releases-osiosta voit suorittaa ohjelman ilman erillistä Python-asennusta.

* **Windows 10/11:** Käytä Python 3.9:llä käännettyä tiedostoa, joka tarjoaa täyden emoji-tuen.
* **Windows XP:** Saatavilla on erillinen Python 3.4:llä käännetty `.exe`-tiedosto. Se on käännetty ja testattu Windows XP -virtuaalikoneessa. Lähdekoodista ohjelmaa on ajettu myös fyysisellä XP-koneella, tosin vain ennen `resource_path`:n ja sen kutsun lisäämistä.

### 2. Suorittaminen lähdekoodista (Linux, Windows ja macOS)

Ohjelma tarvitsee Python 3:n, `tkinter`-kirjaston ja `numpy`-kirjaston.

**Windows ja macOS:** Asenna Python ([python.org](https://www.python.org/)), jonka mukana tulee tkinter, ja asenna numpy:

```bash
pip install numpy
```

**Linux, järjestelmän Python:** Python on yleensä valmiiksi asennettuna, mutta tkinter ja numpy pitää usein asentaa erikseen. Helpoin tapa on paketinhallinta, joka toimii sekä uusissa että vanhoissa jakeluversioissa:

```bash
# Debian, Ubuntu ja niiden johdannaiset
sudo apt install python3-tk python3-numpy

# Fedora
sudo dnf install python3-tkinter python3-numpy

# Arch
sudo pacman -S tk python-numpy
```

Suorita ohjelma repositorion kansiossa:

```bash
python3 Istumajarjestys.py
```

**Linux, virtuaaliympäristö (venv):** Jos haluat asentaa numpyn pipillä, tee se virtuaaliympäristöön. Uudemmissa jakeluissa (esim. Ubuntu 23.04+, Debian 12+) pip ei suostu asentamaan suoraan järjestelmän Pythoniin, vaan antaa virheen `externally-managed-environment`. Tkinteriä ei voi asentaa pipillä, joten se asennetaan silti paketinhallinnalla. Debianissa ja Ubuntussa:

```bash
sudo apt install python3-tk python3-venv
python3 -m venv venv
source venv/bin/activate
pip install numpy
python Istumajarjestys.py
```

Myöhemmillä kerroilla riittää `source venv/bin/activate` ennen ohjelman käynnistämistä.

**Linux, Anaconda tai Miniconda:** Anacondassa tkinter ja numpy ovat valmiina. Minicondassa ne asennetaan aktiiviseen ympäristöön:

```bash
conda install numpy tk
```

Järjestelmän ikä ei vaikuta conda-asennukseen. Suorita ohjelma:

```bash
python Istumajarjestys.py
```

Mac-konetta minulla ei ole, joten Macille ei ole valmista ohjelmaa, mutta lähdekoodista ohjelman ajamisen pitäisi onnistua sielläkin.

---

## Esimerkki

Mukana on 30 osallistujan esimerkkitiedosto `esimerkki30.txt`. Kokeile ohjelmaa sillä:

1. Avaa tiedosto **Avaa**-painikkeella.
2. Syötä kenttiin:
   * Pöytien muodot ja pituudet: `1 8 1 6`
   * Populaation koko: `100`
   * Max sukupolvia: `90`
   * Mutaatioita/ratk.ehd./sukupolvi: `110`
   * Max peräkk. edistyksettömiä sukupolvia: `16`
   * Loppukiriaika: jätä arvoksi `0`
3. Rastita **Ota sukupuolet huomioon**.
4. Klikkaa **Suorita**.

Hetken kuluttua saat todennäköisesti sukupuolet huomioon ottavia istumajärjestyksiä, joiden kokonaisonnellisuus on 30 tai 29.

---

## Käyttöliittymän käyttöohjeet

### Kentät

#### Juhla

Tähän kenttään tulee osallistujalistan tiedostopolku. Voit valita tiedoston **Avaa**-painikkeella, jolloin sen polku asetetaan kenttään automaattisesti.

Kentän sisältö määrittää myös tallennettavien istumajärjestysten tiedostonimien perustan.

#### Pöytien muodot ja pituudet

Jokainen pöytä annetaan lukuparina, ja parit kirjoitetaan peräkkäin välilyönneillä erotettuina. Parin luvut ovat:

1. päätypaikkojen määrä (`0`, `1` tai `2`) ja
2. henkilöiden määrä pöydän yhdellä pitkällä sivulla.

Esimerkiksi:

```text
2 8 1 5 0 4
```

Tämä määrittää kolme pöytää:

* `2 8`: 8 henkilöä kummallakin pitkällä sivulla ja yksi kummassakin päässä, yhteensä 18 paikkaa.
* `1 5`: 5 henkilöä kummallakin pitkällä sivulla ja yksi toisessa päässä, yhteensä 11 paikkaa.
* `0 4`: 4 henkilöä kummallakin pitkällä sivulla, ei päätypaikkoja, yhteensä 8 paikkaa.

Paikkoja on yhteensä 37. **Pöytien kokonaispaikkamäärän on täsmättävä osallistujamäärään**, jotta istumajärjestysten hakeminen onnistuu.

#### Populaation koko

Määrittää, kuinka monta ratkaisuehdotusta käsitellään samanaikaisesti.

Enintään 30 osallistujan juhlissa esimerkiksi `100` voi olla sopiva arvo. Suuremmilla osallistujamäärillä kannattaa kokeilla pienempää populaatiota laskennan keventämiseksi.

#### Max sukupolvia

Suurin sallittu sukupolvien määrä. Algoritmin suoritus lopetetaan viimeistään tämän rajan täyttyessä.

#### Mutaatioita/ratk.ehd./sukupolvi

Määrittää, kuinka monta osallistujien paikkojen vaihtoa kokeillaan kutakin ratkaisuehdotusta kohden yhden sukupolven aikana.

Suurin mahdollinen arvo on osallistujien järjestämättömien parien määrä:

$$
\frac{n(n-1)}{2}
$$

Tässä $n$ tarkoittaa osallistujien määrää. Esimerkiksi 30 osallistujalla suurin arvo on 435. Jos annat tätä suuremman luvun, käytetään suurinta mahdollista arvoa, jolloin kaikki parit käydään läpi.

#### Max peräkk. edistyksettömiä sukupolvia

Kuinka monta sukupolvea algoritmi saa käsitellä peräkkäin ilman, että paras löydetty ratkaisu paranee. Kun raja täyttyy, algoritmi lopettaa, ellei loppukiri tai vastapäisten vaihtelu tuo vielä parannusta, jolloin sukupolvia jatketaan (ks. [Miten algoritmi toimii](#miten-algoritmi-toimii)).

#### Loppukiriaika

Aika sekunteina, jonka algoritmi käyttää vielä parhaan löydetyn istumajärjestyksen parantamiseen, kun edistyksettömien sukupolvien raja on täyttynyt. Aikaraja tarkistetaan vasta valmistelujen jälkeen, joten todellinen kesto voi olla hieman pidempi.

Oletusarvo on `0`, jolloin loppukiriä ei tehdä. Kenttään voi syöttää myös desimaaliluvun, esimerkiksi `2.5`. Käytä desimaalierottimena pistettä, älä pilkkua.

Loppukiriä ei suoriteta, jos maksimimäärä sukupolvia on jo täyttynyt.

#### Ota sukupuolet huomioon

Valitsee, käytetäänkö sukupuolet huomioon ottavaa versiota. Tällöin osallistujalistassa on oltava sukupuolimerkinnät, ja ilman rastia niitä ei saa olla.

#### Osallistujien tiedot

Osallistujalistan sisältö näkyy tässä tekstikentässä. Voit muokata listaa suoraan tai ladata sen tiedostosta **Avaa**-painikkeella.

Osallistujat annetaan yksi henkilö riviä kohden muodossa:

```text
Nimi: Toive1, Toive2, ..., ToiveN|Avec
```

* Toiveet kirjoitetaan kaksoispisteen ja välilyönnin jälkeen pilkulla ja välilyönnillä erotettuina.
* Avec merkitään pystyviivan (`|`) jälkeen. Jos henkilöllä on avec mutta ei toiveita, rivi on muotoa `Nimi: |Avec`.
* Jos henkilöllä ei ole toiveita eikä avecia, nimen perään on silti kirjoitettava kaksoispiste ja välilyönti.

**Sukupuolet huomiotta jättäen:**

```text
Matti Virtanen: Liisa Korhonen, Ville Vallaton|Maija Meikäläinen
Maija Meikäläinen: Matti Virtanen|Matti Virtanen
Jussi Vallakas: 
Ville Vallaton: Jussi Vallakas
Liisa Korhonen: 
```

**Sukupuolet huomioiden:** sukupuolimerkintä (`m` = mies, `n` = nainen, `o` = muu, voidaan sijoittaa sekä miehen että naisen paikalle) kirjoitetaan suoraan nimen perään ilman välilyöntiä tai sulkeita. Toiveissa ja aveceissa nimet kirjoitetaan **ilman** sukupuolimerkintää.

```text
Matti Virtanenm: Liisa Korhonen, Ville Vallaton|Maija Meikäläinen
Maija Meikäläinenn: Matti Virtanen|Matti Virtanen
Jussi Vallakasm: 
Ville Vallatonm: Jussi Vallakas
Liisa Korhonenn: 
```

Viidelle osallistujalle sopisi pöytäsyöte `1 2` (yksi päätypaikka ja kaksi henkilöä kummallakin sivulla).

Sukupuolimerkinnät voi poistaa **Poista sukupuolet** -painikkeella.

### Painikkeet

#### Avaa

Avaa tiedostonvalintaikkunan. Valitun tiedoston polku asetetaan **Juhla**-kenttään ja sisältö **Osallistujien tiedot** -kenttään.

#### Ohje

Tarjoaa pikakäyttöohjeen näyttämistä joko viestilaatikkona, osallistujalistan tai vastauskentän paikalle kirjoitettuna sekä mahdollisuuden tallentaa pikaohjeen tekstitiedostoksi.

#### Poista sukupuolet

Poistaa osallistujalistasta sukupuolimerkinnät ja ottaa pois rastin kohdasta **Ota sukupuolet huomioon**.

#### Laske osallistujamäärä

Näyttää osallistujalistan mukaisen osallistujamäärän, pöytien kokonaispaikkamäärän sekä osallistujien järjestämättömien parien määrän. Viimeksi mainittu on mutaatioiden suurin mahdollinen määrä yhtä ratkaisuehdotusta ja sukupolvea kohden.

Tarkista, että osallistujamäärä ja pöytien paikkamäärä täsmäävät.

#### Suorita

Käynnistää algoritmin annetuilla osallistujatiedoilla ja parametreilla. Ensimmäinen löydetty ratkaisu ilmestyy oikeanpuoleiseen tekstikenttään **Ehdotus**-otsikon alle. Konsolista voit seurata edistymistä.

#### Edellinen ja Seuraava

Siirtyvät edelliseen tai seuraavaan löydettyyn istumajärjestykseen. Voit selata ratkaisuja tallentamatta niitä. Kun klikkaat Edellinen-painiketta ensimmäisessä istumajärjestyksessä, saat ilmoituksen, joka kertoo, montako istumajärjestystä yhteensä on löydetty. Sama pätee, kun klikkaat Seuraava-painiketta viimeisessä istumajärjestyksessä.

#### Tallenna kaikki

Tallentaa kaikki löydetyt istumajärjestykset tiedostoiksi **Juhla**-kentän perusteella. Tämän jälkeen ratkaisuja ei voi enää selata käyttöliittymässä.

Tiedostot tallennetaan oletusarvoisesti samaan kansioon kuin osallistujalistatiedosto. Tiedostonimeen lisätään onnellisuusarvo ja järjestysnumero ennen tiedostopäätettä.

Esimerkiksi, jos Juhla-kentässä on polku

```text
C:/Users/nimi/Documents/istumajärjestys.txt
```

ja ratkaisujen kokonaisonnellisuus on `30`, tiedostot nimetään seuraavasti:

```text
istumajärjestys_30_0.txt
istumajärjestys_30_1.txt
istumajärjestys_30_2.txt
```

#### Surulliset?

Luettelee parhaillaan näkyvässä istumajärjestyksessä henkilöt, joiden onnellisuus on negatiivinen eli jotka ovat [surullisia](#termit).

---

## Termit

* **Seuralainen**, **seurassa**: Joku 2–5 henkilöstä, joka istuu vieressä, vastapäätä tai kulmittain vastapäätä. Tyypillisesti seuralaisia on viisi, mutta päätypaikoilla istuvilla niitä on kaksi ja päädyn vieressä istuvilla kolme tai neljä riippuen siitä, istuuko päätypaikalla joku.
* **Vierustoverit**: Vasemmalla ja oikealla istuva henkilö. Ohjelma ei huomioi avec-pareja sijoittaessaan sitä, kumpi istuu oikealla ja kumpi vasemmalla. Pöydän päässä istuvan kaksi seuralaista lasketaan vierustovereiksi, sillä muuten avecillisia ei voisi koskaan sijoittaa pöydän päähän.
* **Toive** eli **pöytäseuratoive**: Henkilö, jonka seurassa osallistuja haluaisi olla. Sekä avecillisilla että avecittomilla voi olla toiveita, mutta ohjelma priorisoi avecittoman toiveita silloin, kun kaikki hänen toiveensa olisivat jäämässä toteutumatta. Avecittoman ensimmäinen toteutunut toive on avecillisen vastaavaa arvokkaampi, koska se poistaa surullisuusrangaistuksen. Sen jälkeen toteutuneen toiveen arvo ei riipu siitä, onko henkilöllä avecia. Toiveiden ei tarvitse olla symmetrisiä: jos A on toivonut B:tä, B:n ei tarvitse toivoa A:ta.
* **Avec**: Henkilö, jonka viereen osallistuja on sijoitettava. Avecista erottaminen maksaa niin paljon pisteitä, että vierekkäin päätyneen avec-parin erottava vaihto ei käytännössä koskaan paranna ratkaisua. Avec-parien on oltava symmetrisiä: jos A on B:n avec, B:n on oltava A:n avec.
* **Onnellisuus**: Henkilökohtainen pistearvo, joka määräytyy sen mukaan, onko henkilö avecinsa vieressä ja kuinka monta toivetta on toteutettu. Avecittoman toiveettoman henkilön onnellisuus on aina nolla. Avecillisen toiveettoman henkilön onnellisuus on nolla, jos ja vain jos hän on avecinsa vieressä, muussa tapauksessa se on pienempi kuin avecittoman henkilön onnellisuus voi koskaan olla.
* **Surullinen**: Henkilö, jonka onnellisuus on negatiivinen. Tällainen on henkilö, joka ei istu avecinsa vieressä, tai aveciton henkilö, jolla on toiveita, mutta yksikään heistä ei ole seurassa.
* **Kokonaisonnellisuus**: Osallistujien onnellisuuksien summa, josta sukupuolet huomioivassa versiossa vähennetään rangaistukset väärän sukupuolen paikoista. Ohjelma etsii istumajärjestyksiä, jotka maksimoivat tämän arvon.
* **Muoto**: Pöydän päätypaikkojen lukumäärä (0, 1 tai 2).

---

## Miten algoritmi toimii

Ohjelma on niin sanottu memeettinen algoritmi: geneettinen algoritmi, jossa jokaista ratkaisuehdotusta parannetaan lisäksi paikallisella haulla.

**Ratkaisun esitys.** Istumajärjestys on osallistujien permutaatio, joka täytetään paikkoihin kiinteässä järjestyksessä (päätypaikka, rivien paikat vuorotellen, toinen päätypaikka).

**Alkupopulaatio.** Luodaan *Populaation koko* -kentän verran satunnaisia istumajärjestyksiä.

**Mutaatiot (paikallinen haku).** Jokaiselle ratkaisulle kokeillaan sukupolven aikana *Mutaatioita/ratk.ehd./sukupolvi* -kentän verran kahden satunnaisen paikan vaihtoa. Vaihto pidetään, jos kokonaisonnellisuus ei laske; muuten se perutaan. Jos mutaatioita pyydetään vähintään yhtä monta kuin pareja on, käydään kaikki parit läpi satunnaisessa järjestyksessä. Koska huonontavia vaihtoja ei hyväksytä, parhaan ratkaisun laatu ei koskaan laske.

**Valinta ja lisääntyminen.** Populaatio järjestetään kokonaisonnellisuuden mukaan. Parempi puolisko säilyy sellaisenaan, ja huonompi puolisko korvataan jälkeläisillä. Vanhemmat arvotaan sijoituksen mukaan painotetusti (paino ∝ (N − sija + 1)³): sadan ratkaisun populaatiossa noin 94 % vanhemmista tulee paremmasta puoliskosta ja noin 34 % parhaasta kymmenyksestä.

**Risteytys.** Jälkeläinen perii satunnaisen yhtenäisen pätkän ensimmäiseltä vanhemmalta. Loput paikat täytetään toisen vanhemman henkilöillä tämän järjestyksessä (järjestysristeytyksen muunnelma), jolloin jokainen osallistuja esiintyy tasan kerran. Pienellä todennäköisyydellä (1/populaation koko, enintään 25 %) jälkeläiselle tehdään lisäksi satunnainen vaihto, joka saa huonontaakin ratkaisua. Sukupuolet huomioivassa versiossa jälkeläiselle kokeillaan lisäksi vastapäisten vaihtoja.

***Miksi vastapäisiä vaihdellaan risteytyksen jälkeen?*** Pöydän sukupuolikuvio määräytyy sen mukaan, kuka istuu pöydän ensimmäisellä rivipaikalla. Jälkeläisessä tämä henkilö voi tulla eri vanhemmalta kuin ensimmäiseltä vanhemmalta peritty pätkä, jolloin kuvio voi osua pätkän kannalta väärinpäin: seuralaiset ovat oikeat, mutta jokainen istuu väärän sukupuolen paikalla. Vastakkain istuvien vaihtaminen siirtää molemmat vastakkaisen sukupuolen paikoille. Kun pätkä vaihdetaan näin sarake kerrallaan pöydän toiselle puolelle, syntyy peilikuva, jossa seuralaissuhteet säilyvät mutta sukupuolet osuvat oikeille paikoille. Satunnaisilla vaihdoilla sama korjaus vaatisi monta osuvaa vaihtoa peräkkäin, eikä yksittäisestä vaihdosta välttämättä olisi hyötyä. Koska pätkä alkaa ja loppuu satunnaisesta kohdasta, sen reunaan voi myös syntyä kohta, jossa samaa sukupuolta olevat joutuvat vastakkain. Tällaiset ratkaisut saavat sukupuolirangaistuksia ja karsiutuvat yleensä pian valinnassa.

**Sukupuolipaikat.** Sukupuolet huomioivassa versiossa pöydän rivipaikat ovat vuorotellen miesten ja naisten paikkoja (shakkilautakuvio): vierustoverit ja vastapäätä istuvat ovat eri sukupuolta, kulmittain vastapäätä istuvat samaa. Pöydän ensimmäiselle rivipaikalle sijoitettu henkilö määrää pöydän kuvion. Päätypaikat ovat neutraaleja, eli niille voi sijoittaa kenet tahansa ilman rangaistusta.

**Jumiutumisen purku.** Kun paras ratkaisu ei ole parantunut ¾:aan *Max peräkk. edistyksettömiä sukupolvia* -arvosta, mutaatioiden määrä kerrotaan 1,5:llä ja kaikille ratkaisuille kokeillaan vastapäätä istuvien vaihtamista. Jos tämä tai myöhempi sukupolvi tuo parannuksen, mutaatiomäärä palautetaan alkuperäiseksi.

**Lopetus ja loppukiri.** Kun edistyksettömien sukupolvien raja täyttyy:

* jos loppukiriaika > 0, parasta ratkaisua yritetään parantaa aikarajoitetusti: puolet ajasta vaihdetaan satunnaisia paikkoja, puolet keskittyen surullisiin henkilöihin ja heidän toiveidensa seuralaisiin. Jos tämä auttaa, sukupolvia jatketaan;
* sukupuolettomassa versiossa kokeillaan vielä vastapäisten vaihtoa ennen lopettamista, ja jos se auttaa, sukupolvia jatketaan.

Lopuksi palautetaan kaikki erilaiset löydetyt istumajärjestykset, joiden kokonaisonnellisuus on paras löydetty.

### Pisteytys

|                                       | Sukupuoleton versio | Sukupuolet huomioiva versio |
| ------------------------------------- | ------------------- | --------------------------- |
| Toive vieressä                        | +7                  | +1                          |
| Toive vastapäätä                      | +5                  | +1                          |
| Toive kulmittain vastapäätä           | +3                  | +1                          |
| Avec vieressä                         | 0                   | 0                           |
| Avec vastapäätä                       | −38                 | −6                          |
| Avec kulmittain vastapäätä            | −44                 | −8                          |
| Avec ei seurassa                      | −50                 | −10                         |
| Avecittoman yksikään toive ei toteudu | −25                 | −5                          |
| Ei avecia, ei toiveita                | 0                   | 0                           |

Avecilliselle lasketaan avec-rangaistuksen lisäksi toteutuneiden toiveiden pisteet. Avecittoman henkilön onnellisuus on toteutuneiden toiveiden pisteiden summa, tai jos yksikään toive ei toteudu, taulukon surullisuusarvo.

**Sukupuolirangaistukset.** Koska rivipaikat ovat vuorotellen miesten ja naisten paikkoja, kaikki eivät välttämättä mahdu oman sukupuolensa paikoille. Jos esimerkiksi miehiä on enemmän kuin miesten paikkoja, osa miehistä joutuu väistämättä naisten paikoille. Neutraalit päätypaikat vaikuttavat tähän: jokainen päätypaikalle sijoitettu henkilö vähentää omaa sukupuoltaan riveiltä.

Ohjelma laskee ennen hakua kaksi vertailulukua:

* **Luonnollinen enimmäismäärä:** päätypaikoille sijoitetaan vähemmistösukupuolen edustajia, jolloin riveille jää mahdollisimman epätasainen jakauma.
* **Luonnollinen vähimmäismäärä:** päätypaikoille sijoitetaan enemmistösukupuolen edustajia, jolloin rivien jakauma tasoittuu mahdollisimman paljon.

Esimerkki: 14 miestä, 12 naista ja pöydät `1 6 1 6`. Paikkoja on 2 päätypaikkaa ja 24 rivipaikkaa, joista 12 miesten ja 12 naisten. Jos päätypaikoille menee kaksi naista, riveille jää 14 miestä ja 10 naista, jolloin 2 miestä istuu naisten paikoilla (enimmäismäärä 2). Jos päätypaikoille menee kaksi miestä, riveille jää 12 miestä ja 12 naista, jolloin kaikki mahtuvat oman sukupuolensa paikoille (vähimmäismäärä 0).

Vähimmäismäärä tulostetaan vain konsoliin tiedoksi. Pisteytyksessä kynnyksenä on enimmäismäärä:

* **Kynnys ei ylity:** jokainen väärän sukupuolen paikalla istuva vähentää 3 pistettä. Lisäksi ratkaisu saa bonuksen 2 × enimmäismäärä.
* **Kynnys ylittyy:** bonus menetetään, ja jokainen väärän sukupuolen paikalla istuva vähentää 9 pistettä. Kynnyksen ylittäminen on siis jyrkkä pudotus, mutta kynnyksen alla jokainen vältetty väärä paikka on silti 3 pisteen arvoinen.

Lisäksi:

* Väärän sukupuolen paikalle joutunut sijoitetaan mieluiten rivin päähän, jossa seuralaisia on vähemmän: pisteitä tulee 5 − seuralaisten määrä (1 piste, jos päädyssä istuu joku, 2 pistettä, jos ei).
* Samaa sukupuolta oleva avec-pari ei tuota rangaistusta, koska toinen heistä istuu lähes aina (paitsi jos toinen istuu päätypaikalla) väärän sukupuolen paikalla. Vertailulukuja laskettaessa tällaisia pareja kohdellaan muunsukupuolisina.
* Muunsukupuoliset (`o`) eivät koskaan istu väärän sukupuolen paikalla.

#### 💡 Miksi sukupuolettomassa versiossa käytetään 7–5–3-pisteytystä?

Asteikko **7 (vieressä)**, **5 (vastapäätä)** ja **3 (kulmittain vastapäätä)** on valittu estämään toiveiden ketjuuntuminen suoraksi riviksi.

Kuvitellaan kolme henkilöä (A, B ja C), jotka ovat toivoneet kaikki toisiaan:

* **Rivimuodostelma (A — B — C):** B pystyy juttelemaan molemmille, mutta A ja C eivät toisilleen.
* **Kolmiomuodostelma:** B on A:n vieressä ja C:tä vastapäätä, A ja C ovat kulmittain vastapäätä. Kaikki pystyvät juttelemaan kaikille.

Loogiselta näyttävä 3–2–1-asteikko antaisi molemmille ryhmittymille täysin saman pistemäärän 12, jolloin algoritmi ei osaisi suosia tiiviimpää ryhmää. **7–5–3-asteikko** ratkaisee tämän:

* **Rivimuodostelma:** $7 + (7 + 7) + 7 = 28$
* **Kolmiomuodostelma:** $(7 + 3) + (7 + 5) + (5 + 3) = 30$

Näin 7–5–3-asteikko antaa tiiviille ryhmitykselle paremmat pisteet.

---

## Kehitys ja tekniset tiedot

* **Pääkoodi ja algoritmi:** Pääosa (ohjelman varsinainen toiminnallisuus lähdekoodista "normaaliolosuhteissa" Windowsilla ajettaessa) on kirjoitettu ennen ChatGPT:n julkaisua ilman tekoälyn apua. Tekoälyä on käytetty exe-paketointiin ja sen vaatimaan koodiin (`resource_path` kutsuineen) sekä tämän README:n kirjoittamisen apuna.
* **Resurssien hallinta:** Ohjelma hyödyntää `sys._MEIPASS`-mekanismia `.exe`-tiedostojen kuvakkeen ja resurssipolkujen määrittämiseen, mikä mahdollistaa yhteensopivuuden PyInstallerin kanssa.
* **Emojit:** `SurrogatePair.py` perustuu [StackOverflow-vastaukseen](http://stackoverflow.com/questions/40222971/python-find-equivalent-surrogate-pair-from-non-bmp-unicode-char/40223212#40223212) sekä samalla sivulla julkaistuun täydennykseen, jonka ansiosta emojit toimivat myös Python 3.7:ssä ja uudemmissa.
* **Emojien rajoitukset Python 3.6:ssa ja vanhemmissa** (koskee myös Windows XP -exeä):
  * Linuxissa emojit saattavat näkyä laatikoina.
  * Windowsissa Tkinter ei pysty lukemaan yksirivistä tekstikenttää, jossa on emoji. Siksi Juhla-kentässä, josta tallennettavien tiedostojen nimet muodostetaan, ei voi olla emojeita tallennushetkellä, tai tulee virheilmoitus.
  * Osallistujien nimissä emojeita saa olla järjestelmästä riippumatta: tallennus onnistuu, vaikka ne näkyisivätkin laatikoina. Kohdissa, joissa luetellaan osallistujan toivelistaukset {'tämän', 'tyylisessä', 'luettelossa', 'heitto- tai lainausmerkkien', 'välissä'} emojit muuttuvat tällöin surrogaattiparikoodeiksi, mutta virheilmoitusta ei tule. Silloin kun nimeä ei laiteta heitto- tai lainausmerkkien väliin, emojit tallentuvat oikein. Tämän rajoituksen korjaaminen vanhoille Python-versioille olisi luultavasti mahdollista, mutta silloin koodia pitäisi muuttaa niin paljon, ettei ohjelman ydin olisi enää puhtaasti ennen ChatGPT:n julkaisua kirjoitettua. Jos projektista julkaistaan joskus uusi versio, tämän korjaaminen on ensimmäisenä työlistalla.
* **Lähdekoodin ja exejen ero:** Julkaistujen exe-tiedostojen kääntämisen jälkeen lähdekoodiin on tehty kaksi muutosta. Kumpikaan ei muuta ohjelman toimintaa Windowsissa, joten exet toimivat samoin kuin nykyinen lähdekoodi:
  * Jos ikonin asettaminen ei onnistu, se ohitetaan. Ilman tätä ohjelma ei käynnistynyt lähdekoodista Linuxissa, jonka Tk ei tue `.ico`-ikoneita. Lisäksi ikoni haetaan nyt skriptin omasta kansiosta eikä käynnistyskansiosta, joten ohjelman voi käynnistää mistä kansiosta tahansa. Tämä koskee vain lähdekoodista ajamista, koska exe-tiedostot hakevat ikonin `sys._MEIPASS`-mekanismin avulla.
  * `SPMPoytaSali.py`- ja `SPTPoytaSali.py`-tiedostoihin on lisätty puuttuneet `import random` -rivit. Ne ovat tarpeen vain funktioille, jotka ovat jäänteitä hylätystä “seuraan sijoittamiseen” perustuvasta lähestymistavasta, eikä ohjelma kutsu niitä. Tekoäly huomasi puutteen `SPMPoytaSali.py`-tiedostossa, joten tarkistin myös `SPTPoytaSali.py`:n, ja puute oli siinäkin.
