# Navdih:
# https://www.khanacademy.org/computer-programming/box-it/5185240348000256
# https://www.mathsisfun.com/games/boxup-puzzle.html


def vsi_elementi_seznama_so_isti(seznam):  # pomožna funkcija
    if len(seznam) == 0:
        return True
    prvi_clen = seznam[0]
    for i in seznam[1:]:
        if i != prvi_clen:
            return False
    return True


class Matrika:

    def __init__(self, seznam_seznamov):  # notranji seznami so vrstice
        self.seznam_seznamov = seznam_seznamov  # vsi seznami so enako dolgi
        self.širina = len(self.seznam_seznamov[0])
        self.višina = len(self.seznam_seznamov)
    
    def preberi_člen(self, x_koord, y_koord):
        return self.seznam_seznamov[y_koord][x_koord]
    
    def zamenjaj_člen(self, x_koord, y_koord, člen):
        self.seznam_seznamov[y_koord][x_koord] = člen
    
    def upodobitev(self):  # predstava, predstavitev, (re)prezentacija
        string = "┌"
        string += (2 * self.širina + 1) * " "
        string += "┐\n"
        for i in self.seznam_seznamov:
            string += "│ "
            string += " ".join(i)
            string += " │"
            string += "\n"
        string += "└"
        string += (2 * self.širina + 1) * " "
        string += "┘"
        return string
    
    def __repr__():
        return self.upodobitev()
    
    def __str__():
        return self.upodobitev()



nasprotne_smeri = {"s": "j", "j": "s", "v": "z", "z": "v"}

def razberi(niz):
    if niz == "":
        return False
    znak = niz[-1]
    if znak == "-":  # pomišljaj ne bi smel biti na koncu
        return False
    if niz[:-1] == (len(niz) - 1) * "-":  # ta zadnji znak bi moral biti edini znak v nizu, ki ni pomišljaj
        return (znak, len(niz))
    else:
        return False
    

def združi(prvi_člen, drugi_člen):
    vsota = ""
    for par in itertools.zip_longest(prvi_člen, drugi_člen, fillvalue="-"):
        vsota += par[0] if par[1] == "-" else par[1]
    return vsota

class Level:  # dejansko matrika, ki se spreminja

    def __init__(self, seznam_seznamov, začetni_koord, koord_barvnih_škatel):  # leveli bodo vedno taki (tudi v level editorju ne boš mogel narediti tako), da so škatle na začetku posebej (ni dveh skupaj)
        self.matrika = Matrika(seznam_seznamov)  # se spreminja
        self.koord_igralca = začetni_koord  # nabor (x, y) (nikoli ne bomo spreminjali vsako koordinato posebej, ampak vsakič obe naenkrat. Torej lahko uporabimo nabor)
        
        # koord_barvnih_škatel  # seznam naborov (po defaultu dveh, lahko več, ne more pa bit manj kot dve)

        # od leve proti desni naraščajo velikosti
        # posodobljen format (za barvne škatle): vključili bomo še usmerjenost in velikost škatel: [seznam_koordinat, seznam_usmerjenosti, seznam_velikosti]
        # na začetku je le seznam_koordinat: tule bomo pa še dodali usmerjentosti in velikosti, ki jih preberemo iz matrike
        # v bistvu, ne bomo naredili seznama, ampak raje slovar. Vsaka velikost se pojavi največ enkrat.

        # {"1": [(x, y), usmerjenost], "2": ...} takole bo slovar izgledal
        # zdaj bomo uporabili seznam naborov koord_barvnih škatel, da ustvarimo seznam. Pomagali si bomo s self.matrika:
        # predpostavili bomo, da na začetku v matriki ni "vgnezdenih" škatel
        """
        Potrebujemo funkcijo, ki:
        - spremeni "--s" v ("s", 3)
        - spremeni "j" v ("j", 1)
        - za "" vrne error
        - če je v nizu črk več kot ena, potem prav tako vrne error

        To bo naredila funkcija razberi().
        """
        for par_koordinat in koord_barvnih_škatel:  # vrstni red v seznamu "koord_barvnih_škatel" ni pomemben. V vsakem primeru pride (oz. bi moral priti) isti rezultat
            člen_matrike = self.matrika[par_koordinat]
            smer, velikost = razberi(člen_matrike)
            if smer not in ["s", "j", "v", "z"]:
                raise ValueError("Smer ni ustrezna")
            if type(velikost) == int:
                if velikost <= 0:
                    raise ValueError("Velikost ni pozitivna!")
            else:
                raise ValueError("Velikost ni (celo) število!")
            if slovar.get(velikost, None) is None:  # če na tem naslovu v slovarju še ni ničesar 
                slovar[str(velikost)] = [par_koordinat, smer]
            else:
                raise ValueError("Ta velikost je že zasedena. Vse velikosti barvnih škatel morajo biti različne!")
        self.slovar_barvnih_škatel = slovar
        # morda lahko podatek o smeri odstranimo iz slovarja. Zaenkrat naj ostane notri

        self.velikost_igralca = 0  # velikost je odvisna od tega, koliko škatel ima igralec na svojem polju


        # barvne škatle so še vseeno shranjene v matriki, zato da poznamo usmerjenost
        """
        matrika izgleda tako:
        ┌       ┐
        │ 2 3 4 │
        │ 1 1 0 │
        │ 0 1 3 │
        └       ┘
        v pythonu pa je identiteta recimo [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        sam da niso not številke, ampak stringi:

        # "" je prazno polje
        # "-sz" 3 chari so lah sam če mamo tri nivoje, kar pa ni v izvornih igrah
        # "sj"
        # "-v"
        # "-g"
        # "d"
        # "v"
        # "!" skala

        na prvem mestu je manjša škatla, na drugem večja (minus damo uspred), vlkih črk ni več (mamo posebi spremenljivko za to)
        
        zadnji znak v nizu nikoli ne more biti pomišljaj ("-")
        """
    def __repr__(self):
        return self.matrika
    
    def __str__(self):
        return self.matrika
    
    def preveri_okolico(self, smer):  # vrne True, kadar se lahko premakne v to smer
        nasprotna_smer = nasprotne_smeri[smer]
        polje_z_igralcem = self.matrika[self.koord_igralca[1], self.koord_igralca[0]]  # člen matrike, kjer je igralec
        koord_od_drugega_polja = None
        if nasprotna_smer == "v":  # gremo v levo
            koord_od_drugega_polja = (self.koord_igralca[0] - 1, self.koord_igralca[1])
        elif nasprotna_smer == "z":
            koord_od_drugega_polja = (self.koord_igralca[0] + 1, self.koord_igralca[1])
        elif nasprotna_smer == "j":
            koord_od_drugega_polja = (self.koord_igralca[0], self.koord_igralca[1] - 1)
        elif nasprotna_smer == "s":
            koord_od_drugega_polja = (self.koord_igralca[0], self.koord_igralca[1] + 1)
        drugo_polje = self.matrika[koord_od_drugega_polja[1]][koord_od_drugega_polja[0]]  # levo, desno, gornje ...
        
        if drugo_polje == "!":
            return False  # skala

        for znak in drugo_polje:
            if znak != nasprotna_smer and znak != "-":  # če je kaka škatla v napačno smer obrnjena
                return False  # ne more se igralec premakniti v to smer
        
        # preveriti moramo še notranjo velikost škatle:
        notranja_velikost_drugega_polja = 1  # to je najmanjša možna škatla. Igralčeva velikost je 0, zato še ravno lahko gre v to škatlo
        for znak in drugo_polje:
            if znak == "-":
                notranja_velikost_drugega_polja += 1
            else:
                break
        else:
            notranja_velikost_drugega_polja = float("inf")  # če drugo polje prazno polje

        # notranja in zunanja velikost posamezne škatle je vedno ista. Če pa imamo več škatel (eno v drugi), potem pa to ni več res in je zunanja velikost večja
        # velikost igralca meri zunanjo velikost (notranja je irelevantna oz. je ni)

        # ampak najprej bomo razdelili igralčevo polje na ostanek in prenos:
        """
        Razdelili bomo igralčevo polje na del, ki se loči, in del, ki ostane. Operacija bo odvisna od smeri.

        "sjz" v smeri zahoda: "--z" ostane, "sj" gre stran
        "szz" v smeri zahoda: "-zz" ostane, "s" gre stran
        "zzz" v smeri zahoda: "zzz" ostane, "" gre stran
        "sjs" v smeri zahoda: "" ostane, "sjs" gre stran (ne loči se)
        "szs" ali"zzs" v smeri zahoda: ne loči se, oz., ostane "", vse gre stran

        To operacijo bomo opisali v funkciji razdeli()
        """
        ostanek, prenos = razdeli(polje_z_igralcem, smer)  # sprejme prvotni člen in pa smer ter vrne nabor (ostane, gre stran)
        
        

        

        zunanja_velikost_prenosa = len(prenos) # dejansko igralca (štejemo le škatle, ki grejo z njim)
        if notranja_velikost_drugega_polja > zunanja_velikost_prenosa:  # če paše not

            # če so koordinate barvnih škatel iste kot koordinate igralca, potem poglej, ali so barvne škatle v ostanku ali prenosu (saj v tem primeru v polju mora biti prava usmerjenost na pravem mestu, saj poznamo velikost škatel)
            # če je v ostanku, se nič ne spremeni. Če v prenosu, pa se.
            barvne_škatle_se_premaknejo = {}
            for ključ in self.slovar_barvnih_škatel:
                if self.slovar_barvnih_škatel[ključ][0] == self.koord_igralca:  # če so barvne škatle na istem mestu kot igralec
                    velikost = int(ključ)  # velikost barvne škatle je kar ključ
                    if len(prenos) >= velikost:
                        barvne_škatle_se_premaknejo[ključ] = True
                    else:
                        barvne_škatle_se_premaknejo[ključ] = False
                else:
                    barvne_škatle_se_premaknejo[ključ] = False

            nabor = (ostanek, prenos, drugo_polje, koord_od_drugega_polja, barvne_škatle_se_premaknejo)  # [True, False, False, ...] po vrsti barvne škatle
            # v bistvu bo to slovar: {"1": True, "2": False, ...}, ne seznam


            zunanja_velikost_drugega_polja = len(drugo_polje)

            # self.velikost_igralca = zunanja_velikost_drugega_polja  # to je samo za škatle. Če upoštevamo še prazna polja, moramo uporabiti spodnjo vrstico:
            self.velikost_igralca = max(zunanja_velikost_drugega_polja, zunanja_velikost_prenosa)  # to je zato, ker ima prazno polje zunanjo velikost 0 
            # zunanja velikost se ne spremeni, če gremo na prazno polje

            return nabor  # to je namesto True
        else:
            return False

    def premik_v_smer(self, smer):  # to bo uredilo matriko self.matrika
        # leva smer pomeni smer "z"
        if smer == "z":
            if self.koord_igralca[0] == 0:
                return False  # False vrnemo, če ni spremembe, True pa, če je
        if smer == "v":
            if self.koord_igralca[0] == self.matrika.širina - 1:
                return False
        if smer == "s":
            if self.koord_igralca[1] == 0:
                return False
        if smer == "j":
            if self.koord_igralca[1] == self.matrika.višina - 1:
                return False
        
        okolica = preveri_okolico(nasprotne_smeri[smer])  # tudi barvne škatle so notri vključene
        if okolica:  # če ni False
            ostanek, prenos, polje, koord_drugega_polja, b_škatle = okolica

            """
            Ustvarili bomo novo polje z naslednjo operacijo:

            "" + "" = ""
            "v" + "" = "v"  # operacija je tudi komutativna
            "vz" + "--j" = "vzj"
            "-j" + "-z" ne gre
            "-s" + "--j" = "-sj"

            To operacijo bomo opisali v funkciji združi()
            """

            
            novo_polje = združi(prenos, polje)
            print("Novo polje: " + novo_polje)
            self.matrika[koord_drugega_polja[1]][koord_drugega_polja[0]] = novo_polje  # posodobimo polje, kamor se je premaknil igralec
            self.matrika[self.koord_igralca[1]][self.koord_igralca[0]] = ostanek  # izpraznimo polje, kjer je bil igralec, razen če imamo ostanek
            self.koord_igralca = koord_drugega_polja  # posodobimo koordinate
            
            # tukaj posodobimo še morebitne koordinate barvnih škatel
            for ključ in b_škatle:
                if b_škatle[ključ] == True:
                    self.slovar_barvnih_škatel[ključ][0] = koord_drugega_polja

            return True
        return False


    # za vsako polje v matriki lahko definiramo največjo velikost igralca (v kok vlki škatli je lahk), da še lahk gre na tisto polje. Če je prazno polje, je največja velikost neomejena
    # igralec po premiku dobi novo velikost, ki ni nujno ista kot ravnokar definirana količina. Dobimo jo pač s primerjavo členov matrike

    def preveri_ali_na_cilju(self):
        return vsi_elementi_seznama_so_isti(self.koord_barvnih_škatel)  # pri naborih nam ni treba skrbet za kazalce


class VsiLeveli:  # v vrstnem redu - ampak ne vsi, kr lah mamo tut custom level. Torej bomo imeli slovar
    
    def __init__(self, datoteka_z_leveli):
        self.datoteka_z_leveli = datoteka_z_leveli
        # oblika: {"0": matrika, "1": ..., "custom_level": ...}

        self.število_levelov = max([int(ključ) for ključ in self.datoteka_z_leveli.keys() if ključ.isdigit()])  # vsi ključi bodo stringi

    def naslednji_level(self, trenutni_level_id):
        if type(trenutni_level_id) is int:
            if 0 <= trenutni_level_id < self.število_levelov:
                return trenutni_level_id + 1
            elif trenutni_level_id == self.število_levelov:
                return None  # to je bil zadnji level
        else:
            return None  # custom leveli niso razporejeni po vrsti



"""
TODO:
- naredi Class Koordinate?
- tam, kjer se uporablja matrika, ustrezno uporabi njene metode
- napisati funkcijo razdeli()
"""