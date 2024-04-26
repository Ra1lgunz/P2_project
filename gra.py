import json #do zapisu slownikow w pliku
import random #do rzutu kostka
import os #do usuniecia plikow i znalezienia sciezki

#-----Slowniki na przechowywanie danych postaci---------

KP = {
    "Imie":"NULL",
    "Klasa":"NULL",
    "HP":100,
    "Mana":100,
    "Obecna_lokacja": 1,
    "Napotkani_wrogowie":0 ,
    "Zabici_wrogowie":0 ,
    }

Statystyki={
    "Sila":0,
    "Magia":0,
    "Zrecznosc":0,
    "Charyzma":0,
    "Wytrzymalosc":0,
    "Szczescie":0,
    }

#Niby mozna wcisnac Statystyki do KP, ale tak mi sie wygodniej pracuje XD

Przeciwnik ={
    "HP": 100,
    "Mercy":0,
    "Dead":0,
    }

#----funkcje do gry------

def zapis(KP, Statystyki): #funcja do zapisywania gry
    
    with open('SAVE_KP.json', 'w') as file_w: #'w' - write ->tworzy plik jesli go nie ma i umozliwia wpisywanie rzeczy do pliku
        json.dump(KP, file_w)
    with open('SAVE_STAT.json', 'w') as file_w: #no i zapisuje sie jako .json plik, wiec latwo mozna przerzucic spowrotem do slownika, bo taki sam zapis praktycznie
        json.dump(Statystyki, file_w)
        
def dice(n,bonus): #funkcja do "rzucania kostka"
    value = random.randint(0, n) #losu losu liczbe calkowita z przedzialu 0-n
    value+=bonus #uwzglednienie bonusu do rzutu
    return value
         
def ruch(action,KP,Statystyki,Przeciwnik,opponent_action): #zawiera mozliwe ruchy gracza
    
#---------Wypisywanie rzeczy----------------------------
    if action=='Akcje': #Informacje o akcjach
        with (open("AKCJE_INFO.txt") as actionfile):
            for line in actionfile:
                print (line)
                
    if action=='Stats_view': #Wypisuje statystyki
        print("Statystyki postaci: ")
        print(Statystyki)
        
    if action=='Stats_meaning': #Wypisuje na co wplywaja poszczegolne statystyki
        with (open("STATYSTYKI_INFO.txt") as statsfile):
            for line in statsfile:
                print (line)
    
    if action=='Class_info': #Wypisuje informacje o klasach postaci
    
        with (open("KLASY_INFO.txt") as classfile):
            for line in classfile:
                print (line)
#---------Akcje w pokoju----------------------------------                
    if action=='Attack': #uruchamia walke [Moze usune to albo wyifuje]
        walka(KP,Statystyki,Przeciwnik)
        
    if action=='Look': #Opis pomieszczenia, w ktorym sie znajdujemy
        if KP["Obecna_lokacja"]==1:
            with (open("1.txt") as locationfile):
                for line in locationfile:
                    print (line)
        elif KP["Obecna_lokacja"]==2:
            with (open("2.txt") as locationfile):
                for line in locationfile:
                    print (line)
        elif KP["Obecna_lokacja"]==3:
            with (open("3.txt") as locationfile):
                for line in locationfile:
                    print (line)
        elif KP["Obecna_lokacja"]==4:
            with (open("4.txt") as locationfile):
                for line in locationfile:
                    print (line)
        elif KP["Obecna_lokacja"]==5:
            with (open("5.txt") as locationfile):
                for line in locationfile:
                    print (line)
                
    if action=='Move_back': #Cofanie sie do poprzedniego pokoju [o nizszym numerze]
        now=int(KP["Obecna_lokacja"])
        if now>1 and now<=5:
            now-=1
            KP["Obecna_lokacja"]=now
        else:
            print("Nie da sie")
            
    if action=='Move_forward': #przejscie do nastepnego pokoju [o wyzszym numerze]
        now=int(KP["Obecna_lokacja"])
        if now>=1 and now<5:
            now+=1
            KP["Obecna_lokacja"]=now
        else:
            print("Nie da sie")
  
#---------Walka--------------------------------------------
    if action=='Mercy': #W pokojowy sposob wywala przeciwnika z walki
        mercy=int(Przeciwnik["Mercy"])
        if mercy>=100:
            Przeciwnik["HP"]=0
            Przeciwnik["Dead"]=-1
            print("Przeciwnik opuscil pole bitwy")
        else:
            print("Mercy przeciwnika jest niewystarczajace, aby okazac mu laske")
            
    if action=='Heal': #Leczenie sie
        mana=int(KP["Mana"])
        if mana>=10:
            mana-=10
            KP["Mana"]=mana
            x= int(Statystyki["Magia"])
            x=x/2
            luck = int(Statystyki["Szczescie"])
            powodzenie = dice(10,x)
            zycko=int(KP["HP"])
            if powodzenie<=3 and luck<5:
                zycko-=1
                KP["HP"]=zycko
                print("Krytyczne niepowodzenie: -1 HP dla gracza")
            elif powodzenie<=3 and luck>=5:
                zycko+=0
                KP["HP"]=zycko
                print("Leczenie sie nie powiodlo: +0HP dla gracza")
            elif powodzenie>3 and powodzenie<5:
                zycko+=10
                KP["HP"]=zycko
                print("Leczenie powiodlo sie: +10HP dla gracza")
            elif powodzenie>=5 and powodzenie<8:
                zycko+=20
                KP["HP"]=zycko
                print("Leczenie powiodlo sie: +20HP dla gracza")
            elif powodzenie>=8 and powodzenie<=10:
                zycko+=50
                KP["HP"]=zycko
                print("Leczenie powiodlo sie: +50HP dla gracza")
            elif powodzenie>10:
                KP["HP"]=100
                print("Krytyczne powodzenie: Cale HP zregenerowane")
        else:
            print("Za malo many; wybierz inny ruch: ")
            action=''
            while(action!='Mercy' and action!='Physical_A' and action!='Dodge' and action!='Talk' and action!='Block'):
                action=input("Podaj akcje: ");
                ruch(action,KP,Statystyki,Przeciwnik,opponent_action)
                
            print("HP Postaci: ", KP["HP"])
            print("Mana Postaci: ", KP["Mana"])
            print("HP Przeciwnika: ", Przeciwnik["HP"])
            print("Mercy Przeciwnika: ", Przeciwnik["Mercy"])
            
    if action=='Magic_A': #Atak magiczny
        mana=int(KP["Mana"])
        if mana>=10:
            mana-=10
            KP["Mana"]=mana
            x= int(Statystyki["Magia"])
            x=x/2
            luck = int(Statystyki["Szczescie"])
            zycko=int(Przeciwnik["HP"])
            powodzenie = dice(10,x)
            if opponent_action==0:
                if powodzenie<=3 and luck<5:
                    zycko+=1
                    Przeciwnik["HP"]=zycko
                    print("Krytyczne niepowodzenie: +1 HP dla przeciwnika")
                elif powodzenie<=3 and luck>=5:
                    zycko+=0
                    Przeciwnik["HP"]=zycko
                    print("Atak magiczny nie zadzialal: -0HP dla przeciwnika")
                elif powodzenie>3 and powodzenie<5:
                    zycko-=5
                    Przeciwnik["HP"]=zycko
                    print("Atak magiczny zadzialal: -5HP dla przeciwnika")
                elif powodzenie>=5 and powodzenie<8:
                    zycko-=10
                    Przeciwnik["HP"]=zycko
                    print("Atak magiczny zadzialal: -10HP dla przeciwnika")
                elif (powodzenie>=8 and powodzenie<=10) or (powodzenie>10 and luck<5):
                    zycko-=15
                    Przeciwnik["HP"]=zycko
                    print("Atak magiczny zadzialal: -15HP dla przeciwnika")
                elif powodzenie>10 and luck>=5:
                    zycko-=50
                    Przeciwnik["HP"]=zycko
                    print("Krytyczne powodzenie: -50HP dla przeciwnika")
            elif opponent_action==1:
                if powodzenie<=3 and luck<3:
                    zycko+=1
                    Przeciwnik["HP"]=zycko
                    print("W wyniku uniku przeciwnika atak magiczny wywolal odwrotny skutek do zamierzonego: +1HP dla przeciwnika")
                elif powodzenie>10 and luck>5:
                    zycko-=5
                    Przeciwnik["HP"]=zycko
                    print("W wyniku uniku pomimo niesamowitego ataku magicznego ledwo drasnales przeciwnika: -5HP dla przeciwnika")
                else:
                    print("Twoj atak magiczny nie wywolal zadnego skutku w zwiazku z unikiem przeciwnika")
        else:
            print("Za malo many; wybierz inny ruch: ")
            action=''
            while(action!='Mercy' and action!='Physical_A' and action!='Dodge' and action!='Talk' and action!='Block'):
                action=input("Podaj akcje: ");
                ruch(action,KP,Statystyki,Przeciwnik,opponent_action)
                
            print("HP Postaci: ", KP["HP"])
            print("Mana Postaci: ", KP["Mana"])
            print("HP Przeciwnika: ", Przeciwnik["HP"])
            print("Mercy Przeciwnika: ", Przeciwnik["Mercy"])
            
    if action=='Physical_A': #Atak fizyczny
        x= int(Statystyki["Sila"])
        x=x/2
        luck = int(Statystyki["Szczescie"])
        powodzenie = dice(10,x)
        zycko=int(Przeciwnik["HP"])
        if(opponent_action==0):
            if powodzenie<=3 and luck<5:
                zycko+=1
                Przeciwnik["HP"]=zycko
                print("Krytyczne niepowodzenie: +1 HP dla przeciwnika")
            elif powodzenie<=3 and luck>=5:
                zycko+=0
                Przeciwnik["HP"]=zycko
                print("Atak fizyczny nie zadzialal: -0 HP dla przeciwnika")
            elif powodzenie>3 and powodzenie<5:
                zycko-=10
                Przeciwnik["HP"]=zycko
                print("Atak fizyczny zadzialal: -10 HP dla przeciwnika")
            elif powodzenie>=5 and powodzenie<8:
                zycko-=20
                Przeciwnik["HP"]=zycko
                print("Atak fizyczny zadzialal: -20 HP dla przeciwnika")
            elif (powodzenie>=8 and powodzenie<=10) or (powodzenie>10 and luck<5):
                zycko-=50
                Przeciwnik["HP"]=zycko
                print("Atak fizyczny zadzialal: -50 HP dla przeciwnika")
            elif powodzenie>10 and luck>=5:
                Przeciwnik["HP"]=0
                print("Krytyczne powodzenie: Usmierciles wlasnie przeciwnika jednym atakiem")
        elif opponent_action==1:
            if powodzenie<=3 and luck<3:
                zycko+=1
                Przeciwnik["HP"]=zycko
                print("W wyniku uniku przeciwnika atak fizyczny wywolal odwrotny skutek do zamierzonego: +1HP dla przeciwnika")
            elif powodzenie>10 and luck>5:
                zycko-=5
                Przeciwnik["HP"]=zycko
                print("W wyniku uniku pomimo niesamowitego ataku fizycznego ledwo drasnales przeciwnika: -5HP dla przeciwnika")
            else:
                print("Twoj atak fizyczny nie wywolal zadnego skutku w zwiazku z unikiem przeciwnika")
            
    if action =='Dodge': #Unik
        x= int(Statystyki["Zrecznosc"])
        x=x/2
        luck = int(Statystyki["Szczescie"])
        powodzenie = dice(10,x)
        mercy=int(Przeciwnik["Mercy"])
        if powodzenie<=3 and luck<5:
            mercy-=1
            Przeciwnik["Mercy"]=mercy
            print("Probujesz wykonac unik: -1Mercy")
        elif powodzenie<=3 and luck>=5:
            mercy+=0
            Przeciwnik["Mercy"]=mercy
            print("Probujesz wykonac unik: +0Mercy")
        elif powodzenie>3 and powodzenie<5:
            mercy+=3
            Przeciwnik["Mercy"]=mercy
            print("Probujesz wykonac unik: +3Mercy")
        elif powodzenie>=5 and powodzenie<8:
            mercy+=5
            Przeciwnik["Mercy"]=mercy
            print("Probujesz wykonac unik: +5Mercy")
        elif (powodzenie>=8 and powodzenie<=10) or (powodzenie>10 and luck<5):
            mercy+=8
            Przeciwnik["Mercy"]=mercy
            print("Probujesz wykonac unik: +8Mercy")
        elif powodzenie>10 and luck>=5:
            mercy+=10
            Przeciwnik["Mercy"]=mercy
            print("Probujesz wykonac unik: +10Mercy")
            
    if action=='Talk': #Przegadywanie
        x= int(Statystyki["Charyzma"])
        x=x/2
        luck = int(Statystyki["Szczescie"])
        mercy=int(Przeciwnik["Mercy"])
        powodzenie = dice(10,x)
        if powodzenie<=3 and luck<5:
            mercy-=1
            Przeciwnik["Mercy"]=mercy
            print("Przeciwnikowi nie za bardzo podoba sie twoje gadanie")
        elif powodzenie<=3 and luck>=5:
            mercy+=0
            Przeciwnik["Mercy"]=mercy
            print("Twoje slowa nie wywolaly zadnego efektu na przeciwniku")
        elif powodzenie>3 and powodzenie<5:
            mercy+=10
            Przeciwnik["Mercy"]=mercy
            print("Przeciwnik stwierdzil, ze jednak jestes calkiem mila istota")
        elif powodzenie>=5 and powodzenie<8:
            mercy+=20
            Przeciwnik["Mercy"]=mercy
            print("Przeciwnikowi bardzo przypadlo do gustu to co powiedziales")
        elif powodzenie>=8 and powodzenie<=10:
            mercy+=50
            Przeciwnik["Mercy"]=mercy
            print("Przeciwnikowi zrobilo sie bardzo milo dzieki twoim slowom")
        elif powodzenie>10 and luck>=5:
            Przeciwnik["Mercy"]=100
            print("Przeciwnik przez twoje slowa stracil chec do walki i postanowil zostac twoim przyjacielem")
            
    if action=='Block': #Blok
        x= int(Statystyki["Wytrzymalosc"])
        x=x/2
        luck = int(Statystyki["Szczescie"])
        mercy=int(Przeciwnik["Mercy"])
        powodzenie = dice(10,x)
        if powodzenie<=3 and luck<5:
            mercy-=1
            Przeciwnik["Mercy"]=mercy
            print("Probujesz zablokowac atak: -1Mercy")
        elif powodzenie<=3 and luck>=5:
            mercy+=0
            Przeciwnik["Mercy"]=mercy
            print("Probujesz zablokowac atak: +0Mercy")
        elif powodzenie>3 and powodzenie<5:
            mercy+=4
            Przeciwnik["Mercy"]=mercy
            print("Probujesz zablokowac atak: +4Mercy")
        elif powodzenie>=5 and powodzenie<8:
            mercy+=6
            Przeciwnik["Mercy"]=mercy
            print("Probujesz zablokowac atak: +6Mercy")
        elif (powodzenie>=8 and powodzenie<=10) or (powodzenie>10 and luck<5):
            mercy+=9
            Przeciwnik["Mercy"]=mercy
            print("Probujesz zablokowac atak: +9Mercy")
        elif powodzenie>10 and luck>=5:
            mercy+=11
            Przeciwnik["Mercy"]=mercy
            print("Probujesz zablokowac atak: +11Mercy")

def walka(KP,Statystyki,Przeciwnik): #mechanika walki
    KP["Napotkani_wrogowie"]+=1
    fun_number=dice(4,0)
    i=1
    while True:
        mana=int(KP["Mana"])
        if i%5==0:
            print("Dostajesz mane")
            mana+=10
            if mana>=100:
                KP["Mana"]=100
            else:
                KP["Mana"]=mana
            
        zycko_g=int(KP["HP"])
        zycko_p=int(Przeciwnik["HP"])
        mercy_l=int(Przeciwnik["Mercy"])
        
        if zycko_g>=100:
            KP["HP"]=100
        if zycko_p>=100:
            Przeciwnik["HP"]=100
        if mercy_l>=100:
            Przeciwnik["Mercy"]=100
        elif mercy_l<0:
            Przeciwnik["Mercy"]=0
            
        opponent_action = dice(1,0)
        print("HP Postaci: ", KP["HP"])
        print("Mana Postaci: ", KP["Mana"])
        print("HP Przeciwnika: ", Przeciwnik["HP"])
        print("Mercy Przeciwnika: ", Przeciwnik["Mercy"])
        
        action=''
        while(action!='Mercy' and action!='Heal' and action!='Magic_A' and action!='Physical_A' and action!='Dodge' and action!='Talk' and action!='Block'):
            print("")
            print("Dostepne akcje:")
            print("Akcje/Stats_view/Stats_meaning/Class_info/Mercy/Heal/Magic_A/Physical_A/Dodge/Talk/Block")
            action=input("Podaj akcje: ");
            if action=='Attack' and action=='Look' and action=='Move_back' and action=='Move forward':
                print("Te akcje sa niedozwolone")
            elif action=='Akcje'or action=='Stats_view' or action=='Stats_meaning' or action=='Class_info'or action=='Mercy'or action=='Heal' or action=='Magic_A'or action=='Physical_A'or action=='Dodge' or action=='Talk'or action=='Block':
                ruch(action,KP,Statystyki,Przeciwnik,opponent_action)
            else:
                print("Podana akcja nie istnieje")
            
        zycko_g=int(KP["HP"])
        zycko_p=int(Przeciwnik["HP"])
        mercy_l=int(Przeciwnik["Mercy"])
        
        if zycko_p<=0:
            Przeciwnik["HP"]=0
            print("Wygrales")
            break
        if zycko_p>100:
            Przeciwnik["HP"]=100
        if zycko_g<=0:
            KP["HP"]=0
            print("Umarles")
            break
        if zycko_g>100:
            KP["HP"]=100
        if mercy_l>=100:
            Przeciwnik["Mercy"]=100
        elif mercy_l<0:
            Przeciwnik["Mercy"]=0
        
        opponent_powodzenie = dice(10,fun_number)
        zycko_g=int(KP["HP"])
        zycko_p=int(Przeciwnik["HP"])
        if opponent_action==0: #atak
            if action!="Dodge" and action!="Block":
                if opponent_powodzenie<=3:
                    zycko_p-=1
                    Przeciwnik["HP"]=zycko_p
                    zycko_g+=1
                    KP["HP"]=zycko_g
                    print("Atak przeciwnika nie zadzialal jak mial: +1HP dla gracza; -1HP dla przeciwnika")
                elif opponent_powodzenie>3 and opponent_powodzenie<=5:
                    zycko_g-=5
                    KP["HP"]=zycko_g
                    print("Atak przeciwnika ledwo cie drasnal: -5HP dla gracza")
                elif opponent_powodzenie>5 and opponent_powodzenie<=7:
                    zycko_g-=10
                    KP["HP"]=zycko_g
                    print("Atak przeciwnika zadzialal: -10HP dla gracza")
                elif opponent_powodzenie>7 and opponent_powodzenie<=10:
                    zycko_g-=15
                    KP["HP"]=zycko_g
                    print("Atak przeciwnika zadzialal: -15HP dla gracza")
                elif opponent_powodzenie>10:
                    zycko_g-=20
                    KP["HP"]=zycko_g
                    print("Atak przeciwnika zadzialal: -20HP dla gracza")
            else:
                if opponent_powodzenie<=7:
                    print("Atak przeciwnika sie nie powiodl, twoj unik sie powiodl")
                else:
                    zycko_g-=5
                    KP["HP"]=zycko_g
                    print("Pomimo desperackiej proby obrony, przeciwnik cie trafia: -5HP dla gracza")
                    
        elif opponent_action==1: #unik
            if action!="Dodge" and action!="Block":
                if opponent_powodzenie<=4:
                    zycko_p-=1
                    Przeciwnik["HP"]=zycko_p
                    zycko_g+=1
                    KP["HP"]=zycko_g
                    print("Nie wyszedl przeciwnikowi unik: +1HP dla gracza; -1HP dla przeciwnika")
                else :
                    print("Unik przeciwnika sie powiodl")
            else:
                print("Ale jak to tak? Ze oboje robicie uniki w tym samym czasie?")
                
        zycko_g=int(KP["HP"])
        zycko_p=int(Przeciwnik["HP"])
        
        if zycko_p<=0:
            Przeciwnik["HP"]=0
            print("Wygrales")
            break
        if zycko_g<=0:
            KP["HP"]=0
            print("Umarles")
            break
        
        i+=1
        
    Przeciwnik["Dead"]+=1
    if Przeciwnik["Dead"]>0:
        KP["Zabici_wrogowie"]+=1
    if KP["HP"]<=0:
        print ('game over')

def new_game(KP,Statystyki): #sekwencja poczatkowa
    with (open("INTRO.txt") as introfile): #wstepniak
        for line in introfile:
            print (line)
        
    #---------------Stworzenie KP---------------------
    name=input("Podaj imie swojej postaci: ");
    print("\n"+"Informacje o klasach: "+"\n")
    ruch('Class_info',KP,Statystyki,Przeciwnik,0)
    
    proffesion=''
    while(proffesion!='Wiedzma' and proffesion!='Wojowniczka' and proffesion!='Luczniczka'):
        print("Podaj klase swojej postaci")
        proffesion=input("Wiedzma/Wojowniczka/Luczniczka: ");
        if(proffesion!='Wiedzma' and proffesion!='Wojowniczka' and proffesion!='Luczniczka'):
            print("Nie ma takiej klasy postaci")
    
    KP.update({"Imie": name})
    KP.update({"Klasa": proffesion})
    
    #--------------Statystyki-----------------------
    print("\n"+"Informacje o statystykach: "+"\n")
    ruch('Stats_meaning',KP,Statystyki,Przeciwnik,0)
    print("\n"+"Teraz czas podac dodatkowe punkty do statystyk: "+"\n"+"Jesli punkty nie zsumuja ci sie do 10 lub podasz ujemne wartosci punktow, to bedziesz zmuszony do powtorzenia przypisywania punktow")
    
    max_points=10
    sum=0
    
    while(sum!=max_points):
        sum=0
        
        strength=input("Sila: ");
        strength=int(strength)
        sum+=strength
        
        magic=input("Magia: ");
        magic=int(magic)
        sum+=magic
        
        skill=input("Zrecznosc: ");
        skill=int(skill)
        sum+=skill
        
        charisma=input("Charyzma: ");
        charisma=int(charisma)
        sum+=charisma
        
        endurance=input("Wytrzymalosc: ");
        endurance=int(endurance)
        sum+=endurance
        
        luck=input("Szczescie: ");
        luck=int(luck)
        sum+=luck
        
        if (strength<0 or magic<0 or skill<0 or charisma<0 or endurance<0 or luck<0): #nie mozna podac ujemnych wartosci
            sum=0
            print("Zostala podana ujemna wartosc punktowa, ktora jest zakazana")
        elif sum>max_points:
            print("Podano za duzo punktow")
        elif sum<max_points:
            print("Podano za malo punktow")
        elif sum==max_points:
            print("Punkty zostaly podane wlasciwie i zostaly przypisane do postaci")
   
    #-----------Dodanie do ustalonych przez gracza statystyk, punktow klasowych----------
    
    if proffesion=='Wiedzma':
        strength+=2
        magic+=4
        skill+=3
        charisma+=3
        endurance+=1
        luck+=2
   
    elif proffesion=='Wojowniczka':
        strength+=4
        magic+=2
        skill+=3
        charisma+=1
        endurance+=3
        luck+=2
    
    elif proffesion=='Luczniczka':
        strength+=1
        magic+=2
        skill+=4
        charisma+=3
        endurance+=3
        luck+=2
    
    Statystyki.update({"Sila": strength})
    Statystyki.update({"Magia": magic})
    Statystyki.update({"Zrecznosc": skill})
    Statystyki.update({"Charyzma": charisma})
    Statystyki.update({"Wytrzymalosc": endurance})
    Statystyki.update({"Szczescie": luck})
    
    zapis(KP,Statystyki)

status=''
print("Aby wykonac akcje nalezy wpisac dokladnie wyrazenie!")
while (status!="Nowa gra" and status!="Kontynuuj"): #Wejscie gry: nowa/kontynuacja
    status=input("Nowa gra/Kontynuuj: ");
    if status=="Nowa gra": #przejscie do tworzenia nowej postaci od poczatku
        new_game(KP,Statystyki)
    elif status=="Kontynuuj": #przejscie bezposrednio do rozgrywki, jesli juz sa pliki
        with open('SAVE_KP.json') as file_r:
            KP = json.load(file_r)
        with open('SAVE_STAT.json') as file_r:
            Statystyki = json.load(file_r)
    else: #Error
        print("Nie ma takiej opcji")
        
   
encounter=int(KP["Napotkani_wrogowie"])
while(encounter!=10): #wlasciwa rozgrywka [chodzenie po pokojach i walka z wrogami dopoki nie natrafi sie na 10 wrogow]
    action=''
    while action!='Attack': #Z zalozenia nie da sie uniknac walki
        action=input("Look/Attack/Save: ");
        if action!='Save' and action!='Look' and action!='Attack':
            print("Nie ma takiej opcji")
        elif action=='Save':
            zapis(KP, Statystyki)
        else:
            ruch(action,KP,Statystyki,Przeciwnik,0)
            
    encounter=int(KP["Napotkani_wrogowie"])
    zycko=int(KP["HP"])
    if zycko<=0:
        break
    Przeciwnik["HP"]=100
    Przeciwnik["Mercy"]=0
    Przeciwnik["Dead"]=0
    KP["HP"]=100
    KP["Mana"]=100
    lokacja_p=int(KP["Obecna_lokacja"])
    lokacja_d=int(KP["Obecna_lokacja"])
    
    while lokacja_p==lokacja_d: #Trzeba zmienic pomieszczenie, zeby kontynuowac gre
        print("Gdzie idziemy?")
        action=input("Move_back/Move_forward: ")
        ruch(action, KP, Statystyki, Przeciwnik, 0)
        lokacja_d=int(KP["Obecna_lokacja"])


genocide=int(KP["Zabici_wrogowie"])
zycko=int(KP["HP"])

if genocide/10>=0.65 and zycko>0: #Jesli zabije sie ponad 65% przeciwnikow to mamy zle zakonczenie
    with (open("BAD_ENDING.txt") as endingfile):
        for line in endingfile:
            print (line)
    file='SAVE_KP.json'
    path=os.getcwd()+'\\'+file #obecna sciezka i dodajemy plik, ktory chcemy usunac
    os.remove(path) #usuwamy jeden plik z savem
    file='SAVE_STAT.json'
    path=os.getcwd()+'\\'+file #obecna sciezka i dodajemy plik, ktory chcemy usunac
    os.remove(path) #usuwamy drugi plik z savem
elif genocide/10<0.65 and zycko>0: #inaczej dobre zakonczenie
    with (open("GOOD_ENDING.txt") as endingfile):
        for line in endingfile:
            print (line)
else:
    print("Zresetuj gre, aby kontynuowac od ostatniego punktu zapisu")
    


       
