## Programozás 2 ZH feladat

A feladat egy leegyszerűsített könyvtári nyilvántartó rendszer elkészítése.

A felhasználói interfészt egy Flask webapplikáció szolgáltassa.
Ehhez a megadott template-ek szabadon felhasználhatóak és módosíthatóak, de nem kötelező a megadott oldalstruktúrát követni.

### Elvárt funkciók

- Könyvek listázása, kölcsönözhetőségi információval együtt
- Új könyv adatainak felvitele
- Könyvtártagok listázása
- Új könyvtártag adatainak felvitele
- Kölcsönzés/visszahozás rögzítése
- Diagramok megjelenítése a kölcsönzésekről
  - Oszlopdiagram: melyik könyvet hányszor kölcsönözték ki
  - Oszlopdiagram: ki hány könyvet kölcsönzött ki
  - A 0 értékű oszlopok ne jelenjenek meg egyik diagramon se

Új könyv/személy felvitelénél kerüljön ellenőrzésre, hogy a megadott azonosító egyedi.

Minden könyvből 1 példány van, ha az ki van kölcsönözve, akkor visszahozásig más nem kölcsönözheti ki.
Egy személy viszont akárhány könyvet kikölcsönözhet egyszerre.

### Adatok

Az adatokat perzisztensen kell tárolni, azaz leállítás után is maradjanak meg.
Az adattároláshoz tetszőleges technológia használható.

Ahogy a template-ekből is látható, a könyvekről és a könyvtártagokról az alábbi adatokat kell tárolni:

- Könyv
  - `isbn` - egyedi azonosítószám (szöveg)
  - `author` - szerző (szöveg)
  - `title` - cím (szöveg)
  - `year` - kiadás éve (egész)
  - `publisher` - kiadó neve (szöveg)
- Személy
  - `neptun` - egyedi azonosítókód (szöveg)
  - `name` - név (szöveg)

A fenti konstans adatokon felül a kölcsönzési állapotokat és statisztikákat is követni kell, hogy a funkciók az elvárt módon működjenek.
