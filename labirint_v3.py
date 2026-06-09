import pygame
import sys
from moduli import provjeri_ime, ucitaj_sliku, spremi_highscore, najbrze_vrijeme
from moduli import postavi_boje, postavi_igraca, nacrtaj_igraca, provjeri_koliziju

def prikazi_best_time():
    best_time = najbrze_vrijeme()
    if best_time == None:
        tekst = font.render("Best time: --", True, ZUTA)
    else:
        tekst = font.render(f"Best time: {best_time}s", True, ZUTA)

    prozor.blit(tekst, (sirina - tekst.get_width() - 10, 10))

def trenutno_ukupno_vrijeme():
    if ukupno_pocetno_vrijeme == 0:
        return 0
    return (pygame.time.get_ticks() - ukupno_pocetno_vrijeme) // 1000

def prikazi_ukupno_vrijeme():
    tekst = font.render(f"Ukupno: {trenutno_ukupno_vrijeme()}s", True, ZUTA)
    prozor.blit(tekst, (10, visina - tekst.get_height() - 10))

def prikazi_pauzu():
    tekst = font.render("PAUSE", True, ZUTA)
    prozor.blit(tekst, ((sirina - tekst.get_width()) // 2, (visina - tekst.get_height()) // 2))

# pokretanje igrice
pygame.init()

# podesavanje prozora
sirina = 800
visina = 600
prozor = pygame.display.set_mode((sirina, visina))
pygame.display.set_caption("Labirint")

# boje
CRNA, CRVENA, ZUTA, BIJELA, ZELENA, LJUBICASTA = postavi_boje()
font = pygame.font.SysFont(None, 40)

# kockica parametri
igrac_velicina, x, y, brzina = postavi_igraca()

# mape
slika_levela = [ "lvl3.jpeg","lvl4.jpeg","lvl5.jpeg","lvl6.jpeg","lvl7.jpeg"]

# pozadine
pozadina_meni = ucitaj_sliku("startmeni.png", sirina, visina, CRNA)
pozadina_izgubio = ucitaj_sliku("izgubio.png", sirina, visina, CRVENA)
pozadina_pobjeda = ucitaj_sliku("pobjeda.png", sirina, visina, ZELENA)
pozadina_prelaz = ucitaj_sliku("prelaz.png", sirina, visina, CRNA)

trenutni_level = 0
ucitavanje = True
stanje_igre = "POCETAK"

# dodano za unos imena u pygame prozoru
ime_igraca = ""
poruka_greske = ""

vrijeme_za_level = 45  
pocetno_vrijeme = 0 
ukupno_pocetno_vrijeme = 0
ukupno_vrijeme = 0
pauza_pocetak = 0
stanje_prije_pauze = "IGRA"
pauza_slika = None
sat = pygame.time.Clock()

# glavna petlja
while True:
    for dogadaj in pygame.event.get():
        if dogadaj.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()

        if dogadaj.type == pygame.KEYDOWN and dogadaj.key == pygame.K_p:
            if stanje_igre == "IGRA" or stanje_igre == "PRELAZ":
                pauza_pocetak = pygame.time.get_ticks()
                stanje_prije_pauze = stanje_igre
                pauza_slika = prozor.copy()
                stanje_igre = "PAUZA"
            elif stanje_igre == "PAUZA":
                trajanje_pauze = pygame.time.get_ticks() - pauza_pocetak
                if stanje_prije_pauze == "IGRA":
                    pocetno_vrijeme += trajanje_pauze
                ukupno_pocetno_vrijeme += trajanje_pauze
                stanje_igre = stanje_prije_pauze

        # unos imena 
        if stanje_igre == "UNOS_IMENA":
            if dogadaj.type == pygame.KEYDOWN:
                if dogadaj.key == pygame.K_BACKSPACE:
                    ime_igraca = ime_igraca[:-1]
                    poruka_greske = ""

                elif dogadaj.key == pygame.K_RETURN:
                    if provjeri_ime(ime_igraca):
                        with open("rezultati.txt", "a") as fajl:
                            fajl.write(f"Igrac: {ime_igraca} je uspio preci igru!\n")
                        spremi_highscore(ime_igraca, ukupno_vrijeme)
                        stanje_igre = "SPREMLJENO"
                    else:
                        poruka_greske = "Ime mora imati 3-10 slova!"

                else:
                    if dogadaj.unicode.isalpha() and len(ime_igraca) < 10:
                        ime_igraca += dogadaj.unicode
                        poruka_greske = ""
            
    tipke = pygame.key.get_pressed()
    
    if stanje_igre == "POCETAK":
        prozor.blit(pozadina_meni, (0, 0)) 
        if tipke[pygame.K_s]:
            stanje_igre = "IGRA"
            trenutni_level = 0
            ucitavanje = True
            ukupno_pocetno_vrijeme = pygame.time.get_ticks()
            
    elif stanje_igre == "IGRA":
        if ucitavanje == True:
            try:
                mapa_slika = pygame.image.load(slika_levela[trenutni_level]).convert()
            except:
                mapa_slika = pygame.Surface((sirina, visina))
                mapa_slika.fill(CRNA)
            igrac_velicina, x, y, brzina = postavi_igraca()
            pocetno_vrijeme = pygame.time.get_ticks() 
            ucitavanje = False
            
        proteklo = (pygame.time.get_ticks() - pocetno_vrijeme) // 1000
        preostalo = vrijeme_za_level - proteklo
        if preostalo <= 0: stanje_igre = "IZGUBIO"
            
        novi_x, novi_y = x, y
        if tipke[pygame.K_LEFT]:  novi_x -= brzina
        if tipke[pygame.K_RIGHT]: novi_x += brzina
        if tipke[pygame.K_UP]:    novi_y -= brzina
        if tipke[pygame.K_DOWN]:  novi_y += brzina
            
        kolizija = provjeri_koliziju(mapa_slika, novi_x, novi_y, igrac_velicina, sirina, visina)
            
        if kolizija == "CRVENA": 
            stanje_igre = "IZGUBIO"
        elif kolizija == "ZELENA": 
            trenutni_level += 1
            if trenutni_level >= len(slika_levela):
                ukupno_vrijeme = trenutno_ukupno_vrijeme()
                stanje_igre = "KRAJ"
            else: 
                stanje_igre = "PRELAZ"
                ucitavanje = True
        elif kolizija == "PRAZNO":
            x, y = novi_x, novi_y
                
        prozor.blit(mapa_slika, (0, 0)) 
        nacrtaj_igraca(prozor, x, y, igrac_velicina, LJUBICASTA)
        tekst_vremena = font.render(f"Vrijeme: {preostalo}", True, ZUTA)
        prozor.blit(tekst_vremena, (10, 10))
        prikazi_best_time()
        prikazi_ukupno_vrijeme()
        
    elif stanje_igre == "PRELAZ":
        prozor.blit(pozadina_prelaz, (0, 0)) 
        
        
        prikazi_ukupno_vrijeme()        
        if tipke[pygame.K_n]: stanje_igre = "IGRA" 

    elif stanje_igre == "PAUZA":
        if pauza_slika != None:
            prozor.blit(pauza_slika, (0, 0))
        prikazi_pauzu()
            
    elif stanje_igre == "IZGUBIO":
        prozor.blit(pozadina_izgubio, (0, 0)) 
        
        if tipke[pygame.K_r]:
            trenutni_level = 0       
            ucitavanje = True       
            stanje_igre = "POCETAK"
            
    elif stanje_igre == "KRAJ":
        prozor.blit(pozadina_pobjeda, (0, 0)) 
        
        tekst_vrijeme = font.render(f"{ukupno_vrijeme} sekundi", True, LJUBICASTA)
        prozor.blit(tekst_vrijeme, (525, 460))

        

        if tipke[pygame.K_RETURN]:
            ime_igraca = ""
            poruka_greske = ""
            stanje_igre = "UNOS_IMENA"

    elif stanje_igre == "UNOS_IMENA":
        prozor.fill(CRNA)

        

        pygame.draw.rect(prozor, BIJELA, (250, 250, 300, 50), 2)

        unos = font.render(ime_igraca, True, ZELENA)
        prozor.blit(unos, (260, 260))

        uputa = font.render("ENTER spremi, BACKSPACE brise", True, BIJELA)
        prozor.blit(uputa, (160, 330))

        if poruka_greske != "":
            greska = font.render(poruka_greske, True, CRVENA)
            prozor.blit(greska, (210, 400))

    elif stanje_igre == "SPREMLJENO":
        prozor.fill(CRNA)

        tekst = font.render("Rezultat sacuvan!", True, ZELENA)
        prozor.blit(tekst, (260, 250))

        vrijeme_tekst = font.render(f"Vrijeme: {ukupno_vrijeme} sekundi", True, BIJELA)
        prozor.blit(vrijeme_tekst, (240, 285))

        izlaz = font.render("Pritisni ESC za izlaz", True, BIJELA)
        prozor.blit(izlaz, (240, 340))

        if tipke[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        
    pygame.display.update() 
    sat.tick(60)
