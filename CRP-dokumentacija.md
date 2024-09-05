# Dokumentacija završnog praktičnog projekta
# Rješavanje problema relokacije kontejnera pomoću prioritetnih pravila i vizualizacija postupaka
Studentice: Iva Butumović, Danijela Valjak, Andrea Matasović <br/>
Mentor: dr. sc. Mateja Đumić <br/>
## Uvod
Značajan dio robe u međunarodnoj trgovini otprema se u kontejnerima, stoga su luke od velike važnosti za prijevoz robe. Kontejneri prevezeni u kontejnerski terminal pohranjuju se u skladištima tako da se postavljaju jedan uz drugi i jedan na drugi, formirajući redove.
Ako se kontejner koji nije na vrhu reda mora dohvatiti, kontejneri koji se nalaze iznad onog koji se treba dohvatiti moraju se premjestiti prije nego što se on može dohvatiti. Ova dodatna premještanja kontejnera usporavaju cijeli proces dohvaćanja.
Problem premještanja kontejnera predstavlja optimizacijski problem koji uključuje
pronalaženje optimalnog slijeda operacija za njihov dohvat iz skladišta u zadanom
redoslijedu, minimizirajući dodatna premještanja kontejnera koji blokiraju one kontejnere koje treba dohvatiti prije njih samih.
U ovom radu implementirana je simulacija koja prikazuje optimalno dohvaćanje kontejnera
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
* **Tkinter** i **ttk** koriste se za izradu grafičkog korisničkog sučelja (GUI). Omogućuju prikaz prozora aplikacije te dodavanje kontrola kao što su gumbi i izbornici na kojima korisnici mogu vizualno pratiti premještanje kontejnera.
* **Filedialog** omogućuje učitavanje podataka o luci i kontejnerima iz JSON datoteka.
* **Messagebox** prikazuje obavijesti o uspjehu ili greškama.
* **JSONDecodeError** omogućuje prepoznavanje i upravljanje greškama pri parsiranju JSON datoteka.
* **Randint i shuffle** su funkcije koje se koriste za generiranje nasumičnih brojeva i nasumično miješanje elemenata, što je korisno za simuliranje rasporeda kontejnera u luci.
## Rad aplikacije
Pokretanjem datoteke main.exe otvara se sučelje koje korisniku omogućuje odabir između ručnog dohvaćanja kontejnera (Manually Solve CRP) ili automatskog dohvaćanja (Automatically Solve CRP) korištenjem jednog od dostupnih pravila.  <br/>
![alt text](https://github.com/andreamatasovic/ZPP/blob/main/img/crp.png) <br/>
### Ručno dohvaćanje
Odabirom ručnog dohvaćanja otvara se sučelje u kojemu korisnik treba odabrati broj redaka (*tiers*) i stupaca (*stacks*) koje će imati generirana instanca problema. Pritiskom na gumb *Start*, program generira odgovarajući broj kontejnera, pri čemu su im nasumično dodijeljeni brojevi koji označavaju prioritet, odnosno redoslijed u kojem ih je potrebno dohvatiti.
![alt text](https://github.com/andreamatasovic/ZPP/blob/main/img/2.png) <br/>
![alt text](https://github.com/andreamatasovic/ZPP/blob/main/img/3.png) <br/>
Također, ako korisnik ne želi nasumično generirane kontejnere, može učitati prethodno spremljene podatke iz nekoliko JSON datoteka.  <br/>
<br/>
Ručno dohvaćanje kontejnera u aplikaciji odvija se kroz nekoliko jasno definiranih koraka. Kada korisnik klikne na kontejner u prozoru, aplikacija identificira koji kontejner je odabran, pod uvjetom da se nalazi na vrhu svog stupca. Taj kontejner označava se za premještanje. Dok korisnik povlači kontejner, aplikacija prati njegovo kretanje u prozoru i prema tome prilagođava položaj kontejnera. Kada korisnik ispusti kontejner, aplikacija utvrđuje na koji stupac je kontejner premješten, ažurira raspored stupaca i bilježi broj izvršenih premještaja. Ako se kontejneri nalaze na vrhu, a trebaju biti uklonjeni, aplikacija ih uklanja iz prikaza.  <br/>
### Automatsko dohvaćanje uz prioritetna pravila
Odabirom automatskog dohvaćanja otvara se sučelje u kojem korisnik može odabrati jedno od 3 implementirana pravila. Također, korisniku je omogućeno da odabere broj redaka i stupaca, čime se generira odgovarajući broj kontejnera s nasumično dodijeljenim redoslijedom dohvaćanja. Kao i kod ručnog dohvaćanja, korisnik može, umjesto nasumično generiranih kontejnera, učitati prethodno spremljene podatke iz JSON datoteka.
![alt text](https://github.com/andreamatasovic/ZPP/blob/main/img/4.png) <br/>
Pritiskom na gumb _Start_, aplikacija automatski premješta kontejnere prema odabranom pravilu, ažurira prikaz i prikazuje broj premještaja. Cijeli proces premještanja kontinuirano se opisuje u statusnoj traci, pružajući korisniku ažurirane informacije o trenutnom stanju.
![alt text](https://github.com/andreamatasovic/ZPP/blob/main/img/5.png) <br/>
#### *The Lowest Point* (TLP)
Pravilo TLP za rješavanje problema premještanja kontejnera funkcionira tako što prvo analizira sve stupce u skladištu i bilježi broj kontejnera u svakom stupcu. Zatim, TLP odabire stupac s najmanjim brojem kontejnera kao odredište za premještanje novih kontejnera. Ako postoji više stupaca s istim najmanjim brojem kontejnera, nsasumično se bira na koji od tih stupaca će biti premješten kontejner. Na kraju, broj kontejnera u oba stupca se ažurira i proces se može ponoviti ako je potrebno.
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
Ključna ideja je izračunati _reshuffle indeks_ za svaki stupac. _Reshuffle indeks_ definira se kao broj kontejnera u određenom stupcu koji imaju viši prioritet od blokirajućeg kontejnera, tj. kontejnera koji trenutno blokira pristup željenom kontejneru.
```python
def calculate_reshuffle_index(stack, blocking_container_id):
    reshuffle_index = 0
    for container in stack:
        if container.id < blocking_container_id:
            reshuffle_index += 1
    return reshuffle_index
```
Algoritam koristi ovaj indeks kako bi odabrao stupac s najnižim _reshuffle indeksom_ za premještanje blokirajućeg kontejnera. Odabirom stupca s _najnižim reshuffle_ indeksom minimizira vjerojatnost da će premješten kontejner ponovo blokirati pristup nekom drugom kontejneru u budućnosti.
```python
def RI(stacks):
    min_reshuffle_index = float('inf')
    target_stack = None
    current_stack = None
    blocking_container_id = None
    min_container_id = float('inf')

    for stack in stacks:
        for container in stack:
            if container.id < min_container_id:
                min_container_id = container.id
                current_stack= stack
                blocking_container_id = current_stack[-1]
    for stack in stacks:         
            current_reshuffle_index = calculate_reshuffle_index(stack, blocking_container_id)
            if current_reshuffle_index < min_reshuffle_index:
                min_reshuffle_index = current_reshuffle_index
                target_stack = stack
    return target_stack
```
#### *Reshuffle Index with Look-Ahead* (RIL)
_Reshuffle Index with Look-Ahead_ (RIL) je proširenje osnovnog _Reshuffle Index_ prioritetnog pravila koja uključuje dodatni korak *gledanja unaprijed* (look-ahead) kako bi se unaprijedilo donošenje odluka pri premještanju kontejnera. Dok standardno  _Reshuffle Index_ pravilo odabire stupac za premještanje blokirajućeg kontejnera na temelju trenutnog broja kontejnera s višim prioritetom, RIL pokušava predvidjeti buduće premještaje i izbjegavati poteze koji bi kasnije mogli uzrokovati dodatna premještanja.
RIL uzima u obzir ne samo trenutni _reshuffle indeks_, već i potencijalne posljedice premještanja na buduće poteze, što pomaže u daljnjem smanjenju ukupnog broja premještanja u cijelom procesu.

Dok standardno  _Reshuffle Index_ pravilo odabire stupac za premještanje blokirajućeg kontejnera na temelju trenutnog broja kontejnera s višim prioritetom, RIL pokušava predvidjeti buduće premještaje i izbjegavati poteze koji bi kasnije mogli uzrokovati dodatna premještanja.
Predviđanje posljedica budućih premještanja postiže tako da prilikom izračuna _reshuffle indeksa_, ocjenjuje moguće buduće scenarije u kojima bi se premješteni kontejner mogao naći u situaciji da ponovno blokira pristup nekom drugom kontejneru. Na temelju ocjena odabire stupac za premještanje koji minimizira buduća dodatna premještanja.
```python
def min(stack):
    min_id = float('inf')
    for container in stack:
        if container.id < min_id:
            min_id = container.id
    return min_id     

def RIL(stacks):
    min_reshuffle_index = float('inf')
    target_stack = None
    current_stack = None
    blocking_container_id = None
    min_container_id = float('inf')
    min_max_id= float('-inf')
    for stack in stacks:
        for container in stack:
            if container.id < min_container_id:
                min_container_id = container.id
                current_stack= stack
                blocking_container_id = current_stack[-1]
    for stack in stacks:         
            current_reshuffle_index = calculate_reshuffle_index(stack, blocking_container_id)
            min_in_stack=min(stack)
            if current_reshuffle_index < min_reshuffle_index:
                min_reshuffle_index = current_reshuffle_index
                target_stack = stack
            elif current_reshuffle_index == min_reshuffle_index:
                if min_in_stack > min_max_id:
                    min_max_id = min_in_stack
                    min_reshuffle_index = current_reshuffle_index
                    target_stack = stack
           
    return target_stack
```
