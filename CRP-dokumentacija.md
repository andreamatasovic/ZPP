# Dokumentacija završnog praktičnog projekta
# Rješavanje problema relokacije kontejnera pomoću prioritetnih pravila i vizualizacija postupaka
Studentice: Iva Butumović, Danijela Valjak, Andrea Matasović <br/>
Mentor: izv. prof. dr. sc. Domagoj Matijević <br/>
Komentor: dr. sc. Mateja Đumić <br/>

## Uvod
Značajan dio robe u međunarodnoj trgovini otprema se u kontejnerima, stoga su morske
luke od velike važnosti za prijevoz robe. Kontejneri prevezeni u kontejnerski terminal pohranjuju se u skladištima tako da se postavljaju jedan uz drugi i jedan na drugi, formirajući redove.
Ako se kontejner koji nije na vrhu reda mora dohvatiti, kontejneri koji se nalaze iznad
potrebnog moraju se premjestiti prije nego što se onaj potrebni može
dohvatiti. Ova dodatna premještanja kontejnera usporavaju cijeli proces dohvaćanja.
Problem premještanja kontejnera predstavlja optimizacijski problem koji uključuje
pronalaženje optimalnog slijeda operacija za njihov dohvat iz skladišta u zadanom
redoslijedu, minimizirajući dodatna premještanja blokirajućih kontejnera.
U ovom radu implementirana je simulacija koja vizualizira optimalno dohvaćanje kontejnera
koristeći pravila prioritetnih redova. Implementirana su 3 pravila: pravilo najniže pozicije (*The Lowest Point* - TLP), indeks preraspodjele (*Reshuffle Index* - RI) i indeks preraspodjele s predviđanjem (*Reshuffle Index with Look-Ahead* - RIL). Osim vizualnog prikaza primjene ovih pravila, korisnicima je omogućeno i ručno dohvaćanje kontejnera, uz praćenje broja
potrebnih koraka. <br/>
Projekt je implementiran u Pythonu, a koristi grafičko sučelje koje omogućava korisnicima interakciju s aplikacijom.

## Biblioteke
```python
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from json import JSONDecodeError
from random import randint, shuffle
```
* **Tkinter** i **ttk** koriste se za izradu grafičkog korisničkog sučelja (GUI). Omogućuju prikaz prozora aplikacije te kontrole kao što su gumbi i izbornici na kojima korisnici mogu vizualno pratiti premještanje kontejnera.
* **Filedialog** omogućuje učitavanje podataka o luci i kontejnerima iz JSON datoteka.
* **Messagebox** prikazuje obavijesti o uspjehu ili greškama.
* **JSONDecodeError** omogućuje prepoznavanje i upravljanje greškama pri parsiranju JSON datoteka.
* **Randint i shuffle** su funkcije koje se koriste za generiranje nasumičnih brojeva i nasumično miješanje elemenata, što je korisno za simuliranje rasporeda kontejnera u luci.

## Rad aplikacije
Pokretanjem datoteke CRP.exe otvara se sučelje koje korisniku omogućuje odabir između ručnog dohvaćanja kontejnera (Manually Solve CRP) ili automatskog dohvaćanja (Automatically Solve CRP) korištenjem jednog od dostupnih pravila.  <br/>

![alt text](https://github.com/andreamatasovic/ZPP/blob/main/img/crp.png) <br/>

### Ručno dohvaćanje
Odabirom ručnog dohvaćanja otvara se sučelje u kojemu korisnik treba odabrati broj redaka (*tiers*) i stupaca (*stacks*) za simuliranu luku. Pritiskom na gumb *Start*, program generira odgovarajući broj kontejnera, pri čemu su im nasumično dodijeljeni brojevi koji označavaju prioritet redoslijeda dohvaćanja.

![alt text](https://github.com/andreamatasovic/ZPP/blob/main/img/2.png) <br/>

![alt text](https://github.com/andreamatasovic/ZPP/blob/main/img/3.png) <br/>

Također, ukoliko korisnik ne želi nasumično generirane kontejnere, može učitati prethodno spremljene podatke iz nekoliko JSON datoteka.  <br/>
<br/>
Ručno dohvaćanje kontejnera u aplikaciji odvija se kroz nekoliko jasno definiranih koraka. Kada korisnik klikne na kontejner u prozoru, aplikacija identificira koji kontejner je odabran, pod uvjetom da se nalazi na vrhu svog stoga. Taj kontejner označava se za premještanje. Dok korisnik povlači kontejner, aplikacija prati njegovo kretanje u prozoru i prema tome prilagođava položaj kontejnera. Kada korisnik ispusti kontejner, aplikacija utvrđuje na koji stog je kontejner premješten, ažurira raspored stogova i bilježi broj izvršenih premještaja. Ako se kontejneri nalaze na vrhu, a trebaju biti uklonjeni, aplikacija ih odgovarajuće briše.  <br/>

### Automatsko dohvaćanje uz prioritetna pravila
Odabirom automatskog dohvaćanja otvara se sučelje u kojem korisnik može odabrati jedno od 3 implementirana pravila. Također, korisniku je omogućeno da odabere broj redaka i stupaca za prikaz pravila, čime se generira odgovarajući broj kontejnera s nasumično dodijeljenim redoslijedom dohvaćanja. Kao i kod ručnog dohvaćanja, korisnik može, umjesto nasumično generiranih kontejnera, učitati prethodno spremljene podatke iz JSON datoteka.

![alt text](https://github.com/andreamatasovic/ZPP/blob/main/img/4.png) <br/>

Pritiskom na gumb _Start_, aplikacija automatski premješta kontejnere prema odabranom pravilu, ažurira prikaz na platnu i prikazuje broj premještaja. Cijeli proces premještanja kontinuirano se opisuje u statusnoj traci, pružajući korisniku ažurirane informacije o trenutnom stanju.

![alt text](https://github.com/andreamatasovic/ZPP/blob/main/img/5.png) <br/>

#### *The Lowest Point* (TLP)
Pravilo TLP za rješavanje problema premještanja kontejnera funkcionira tako što prvo analizira sve stogove u skladištu i bilježi broj kontejnera u svakom stogu. Zatim, TLP odabire stog s najmanjim brojem kontejnera kao odredište za premještanje novih kontejnera. Ako postoji više stogova s istim najmanjim brojem kontejnera, odredište se nasumično bira među tim stogovima. Na kraju, broj kontejnera u oba stoga se ažurira i proces se može ponoviti ako je potrebno.
```python
def TLP(stacks):
    selected_containers = []
    min_position = float('inf')

    for stack in stacks:
        if stack:
            top_container = stack[-1]
            if top_container.position < min_position:
                min_position = top_container.position
                selected_containers = [top_container]
            elif top_container.position == min_position:
                selected_containers.append(top_container)

    if len(selected_containers) > 1:
        selected_container = random.choice(selected_containers)
    
    return selected_container
```
#### *Reshuffle Index* (RI)
Ključna ideja je izračunati *reshuffle indeks* za svaki stupac, što je broj kontejnera u tom stupcu s višim prioritetom od blokirajućeg kontejnera (onog koji trenutno blokira pristup željenom). Algoritam zatim odabire stupac s najnižim _reshuffle indeksom_ za premještanje blokirajućeg kontejnera, s ciljem smanjenja budućih premještanja. 
```python
def RI(stacks):
    selected_container = None
    max_reshuffle_index = float('-inf')
    for stack in stacks:
        if stack:
            top_container = stack[-1]
            if top_container.reshuffle_index > max_reshuffle_index:
                max_reshuffle_index = top_container.reshuffle_index
                selected_container = top_container
    return selected_container
```
#### *Reshuffle Index with Look-Ahead* (RIL)
_Reshuffle Index with Look-Ahead_ (RIL) je proširenje osnovne _Reshuffle Index_ heuristike koja uključuje dodatni korak *gledanja unaprijed* (look-ahead) kako bi se unaprijedilo donošenje odluka pri premještanju kontejnera. Dok standardna _Reshuffle Index_ heuristika odabire stupac za premještanje blokirajućeg kontejnera na temelju trenutnog broja kontejnera s višim prioritetom, RIL pokušava predvidjeti buduće premještaje i izbjegavati poteze koji bi kasnije mogli uzrokovati dodatna premještanja.
RIL uzima u obzir ne samo trenutni _reshuffle indeks_, već i potencijalne posljedice premještanja na buduće poteze, što pomaže u daljnjem smanjenju ukupnog broja premještanja u cijelom procesu.
```python
def RIL(stacks):
    selected_container = None
    min_lookahead_cost = float('inf')
    for stack in stacks:
        if stack:
            top_container = stack[-1]
            if top_container.lookahead_cost < min_lookahead_cost:
                min_lookahead_cost = top_container.lookahead_cost
                selected_container = top_container
    return selected_container
```

