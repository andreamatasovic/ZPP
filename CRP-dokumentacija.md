# Dokumentacija završnog praktičnog projekta
# Rješavanje problema relokacije kontejnera pomoću prioritetnih pravila i vizualizacija postupaka
Studentice: Iva Butumović, Danijela Valjak, Andrea Matasović <br/>
Mentor: izv. prof. dr. sc. Domagoj Matijević <br/>
Komentor: dr. sc. Mateja Đumić <br/>

## Uvod
Značajan dio robe u međunarodnoj trgovini otprema se u kontejnerima. Tijekom čekanja na utovar, kontejneri se u luci nalaze složeni u stupcima jedan na drugom. Kako bi se pri utovaru došli do kontejnera u predodređenom redoslijedu, suočavamo se s NP-teškim problemom. U ovom radu implementirana su tri pravila za rješavanje tog problema: pravilo najniže pozicije (*The Lowest Point* - TLP), indeks preraspodjele (*Reshuffle Index* - RI) i indeks preraspodjele s predviđanjem (*Reshuffle Index with Look-ahead* - RIL). Projekt koristi navedena pravila za simulaciju procesa utovara i omogućuje korisniku ručno dohvaćanje kontejnera, uz praćenje broja koraka. <br/>
Projekt je implementiran u Pythonu, a koristi grafičko sučelje koje omogućava korisnicima interakciju s aplikacijom.

## Biblioteke
```python
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from json import JSONDecodeError
from random import randint, shuffle
```
* **Tkinter** i **ttk** se koriste se za izradu grafičkog korisničkog sučelja (GUI). Omogućuju prikaz prozora aplikacije, kontrole kao što su gumbi i izbornici na kojima korisnici mogu vizualno pratiti premještanje kontejnera.
* **Filedialog** omogućuje učitavanje podataka o luci i kontejnerima iz JSON datoteka.
* **Messagebox** prikazuje obavijesti o uspjehu ili greškama.
* **JSONDecodeError** omogućuje prepoznavanje i upravljanje greškama pri parsiranju JSON datoteka.
* **Randint i shuffle** su funkcije koje se koriste za generiranje nasumičnih brojeva i nasumično miješanje elemenata, što je korisno za simuliranje rasporeda kontejnera u luci.









## Pokretanje
Za pokretanje projekta, potrebno je jednostavno otvoriti *CRP.exe* datoteku. Nakon toga, projekt će se automatski pokrenuti i omogućiti korisniku da započne simulaciju procesa utovara kontejnera.
