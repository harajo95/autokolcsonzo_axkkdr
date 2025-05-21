# -*- coding: utf-8 -*-
"""
Created on Wed May 21 09:45:16 2025

@author: Haraszti József
neptunk kód: axkkdr
szak: részismereti képzés
"""

from abc import ABC, abstractmethod
from datetime import date

class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij

    @abstractmethod
    def __str__(self):
        pass

class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, utasszam, felszereltseg):
        super().__init__(rendszam, tipus, berleti_dij)
        self.utasszam = utasszam
        self.felszereltseg = felszereltseg

    def __str__(self):
        return f"Személyautó - {self.rendszam}, {self.tipus}, {self.utasszam} fő, {self.felszereltseg} felszereltség, {self.berleti_dij} Ft/nap"

class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, teherbiras):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras = teherbiras

    def __str__(self):
        return f"Teherautó - {self.rendszam}, {self.tipus}, {self.teherbiras} kg, {self.berleti_dij} Ft/nap"

class Berles:
    def __init__(self, auto, datum):
        self.auto = auto
        self.datum = datum

    def __str__(self):
        return f"{self.auto.rendszam} bérlése {self.datum} napjára - {self.auto.berleti_dij} Ft"

class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def auto_hozzaadas(self, auto):
        self.autok.append(auto)

    def berles_hozzaadas(self, rendszam, datum):
        auto = next((a for a in self.autok if a.rendszam == rendszam), None)
        if not auto:
            return f"Nincs ilyen rendszámú autó: {rendszam}"
        for berles in self.berlesek:
            if berles.auto == auto and berles.datum == datum:
                return "Ez az autó már bérlés alatt áll ezen a napon."
        self.berlesek.append(Berles(auto, datum))
        return f"Sikeres bérlés: {auto.rendszam}, {datum} - {auto.berleti_dij} Ft"

    def berles_lemondas(self, rendszam, datum):
        for berles in self.berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                self.berlesek.remove(berles)
                return f"Bérlés lemondva: {rendszam}, {datum}"
        return "Nem található ilyen bérlés."

    def berlesek_listazasa(self):
        return [str(berles) for berles in self.berlesek]

    def elerheto_autok_listazasa(self, datum):
        foglalt_rendszamok = {berles.auto.rendszam for berles in self.berlesek if berles.datum == datum}
        return [str(auto) for auto in self.autok if auto.rendszam not in foglalt_rendszamok]

    def autok_listazasa(self):
        return [str(auto) for auto in self.autok]

def main():
    kolcsonzo = Autokolcsonzo("GDE")
    kolcsonzo.auto_hozzaadas(Szemelyauto("ABC123", "Toyota", 10000, 5, "magas"))
    kolcsonzo.auto_hozzaadas(Szemelyauto("XYZ789", "Ford", 12000, 5, "alacsony"))
    kolcsonzo.auto_hozzaadas(Teherauto("DEF456", "Mercedes", 15000, 2000))
    kolcsonzo.berles_hozzaadas("ABC123", date(2025, 6, 1))
    kolcsonzo.berles_hozzaadas("XYZ789", date(2025, 6, 2))
    kolcsonzo.berles_hozzaadas("DEF456", date(2025, 6, 3))
    kolcsonzo.berles_hozzaadas("ABC123", date(2025, 6, 4))

    while True:
        print("\n1 - Bérlés\n2 - Lemondás\n3 - Eddigi bérlések\n4 - Elérhető autók\n5 - Autóink\n6 - Kilépés")
        v = input("Válasszon menüt: ")

        if v == "1":
            rendszam = input("Rendszám: ")
            try:
                ev, ho, nap = map(int, input("Dátum (ÉÉÉÉ-HH-NN): ").split("-"))
                print(kolcsonzo.berles_hozzaadas(rendszam, date(ev, ho, nap)))
            except:
                print("Hibás dátum.")

        elif v == "2":
            rendszam = input("Rendszám: ")
            try:
                ev, ho, nap = map(int, input("Dátum (ÉÉÉÉ-HH-NN): ").split("-"))
                print(kolcsonzo.berles_lemondas(rendszam, date(ev, ho, nap)))
            except:
                print("Hibás dátum.")

        elif v == "3":
            for b in kolcsonzo.berlesek_listazasa():
                print(b)

        elif v == "4":
            try:
                ev, ho, nap = map(int, input("Dátum (ÉÉÉÉ-HH-NN): ").split("-"))
                lista = kolcsonzo.elerheto_autok_listazasa(date(ev, ho, nap))
                if lista:
                    for auto in lista:
                        print(auto)
                else:
                    print("Nincs elérhető autó ezen a napon.")
            except:
                print("Hibás dátum.")

        elif v == "5":
            autok = kolcsonzo.autok_listazasa()
            if autok:
                for auto in autok:
                    print(auto)
            else:
                print("Nincs rögzített autó.")

        elif v == "6":
            break

        else:
            print("Hibás választás.")

if __name__ == "__main__":
    main()
