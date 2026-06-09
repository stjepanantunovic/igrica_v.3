import pygame
import re
import os

def napravi_putanju(naziv_datoteke):
    folder_igre = os.path.dirname(__file__)
    return os.path.join(folder_igre, naziv_datoteke)

def postavi_boje():
    CRNA = (0, 0, 0)
    CRVENA = (255, 0, 0)
    ZUTA = (255, 255, 0)
    BIJELA = (255, 255, 255)
    ZELENA = (0, 255, 0)
    LJUBICASTA = (180, 0, 255)
    return CRNA, CRVENA, ZUTA, BIJELA, ZELENA, LJUBICASTA

def postavi_igraca():
    igrac_velicina = 23
    x = 50
    y = 50
    brzina = 2
    return igrac_velicina, x, y, brzina

def nacrtaj_igraca(prozor, x, y, igrac_velicina, boja):
    pygame.draw.rect(prozor, boja, (x, y, igrac_velicina, igrac_velicina))

def provjeri_koliziju(mapa_slika, x, y, igrac_velicina, sirina, visina):
    lijevo = int(x)
    desno = int(x + igrac_velicina - 1)
    gore = int(y)
    dolje = int(y + igrac_velicina - 1)
    if lijevo < 0 or gore < 0 or desno >= sirina or dolje >= visina:
        return "ZID"

    tacke = []

    for tacka_x in range(lijevo, desno + 1):
        tacke.append((tacka_x, gore))
        tacke.append((tacka_x, dolje))

    for tacka_y in range(gore, dolje + 1):
        tacke.append((lijevo, tacka_y))
        tacke.append((desno, tacka_y))

    dodiruje_zeleno = False

    for tacka_x, tacka_y in tacke:
        boja_ispod = mapa_slika.get_at((tacka_x, tacka_y))

        if boja_ispod[0] > 200 and boja_ispod[1] < 50:
            return "CRVENA"
        elif boja_ispod[1] > 200 and boja_ispod[0] < 50:
            dodiruje_zeleno = True

    if dodiruje_zeleno == True:
        return "ZELENA"
    return "PRAZNO"

def provjeri_ime(ime):
    # Regex
    uzorak = r"^[A-Za-z]{3,10}$"
    if re.match(uzorak, ime):
        return True
    return False

def ucitaj_sliku(naziv_slike, sirina, visina, boja):
    try:
        slika = pygame.image.load(napravi_putanju(naziv_slike)).convert()
        slika = pygame.transform.scale(slika, (sirina, visina))
    except:
        slika = pygame.Surface((sirina, visina))
        slika.fill(boja)
    return slika

def ucitaj_highscore():
    rezultati = []
    try:
        with open("highscore.txt", "r") as fajl:
            for linija in fajl:
                linija = linija.strip()
                dijelovi = linija.split(";")
                if len(dijelovi) == 2 and dijelovi[1].isdigit():
                    rezultati.append((dijelovi[0], int(dijelovi[1])))
    except:
        pass
    return rezultati

def spremi_highscore(ime, vrijeme):
    rezultati = ucitaj_highscore()
    rezultati.append((ime, vrijeme))
    rezultati.sort(key=lambda rezultat: rezultat[1])

    with open("highscore.txt", "w") as fajl:
        for ime_igraca, vrijeme_igraca in rezultati:
            fajl.write(f"{ime_igraca};{vrijeme_igraca}\n")

def najbrze_vrijeme():
    rezultati = ucitaj_highscore()
    if len(rezultati) == 0:
        return None
    rezultati.sort(key=lambda rezultat: rezultat[1])
    return rezultati[0][1]
