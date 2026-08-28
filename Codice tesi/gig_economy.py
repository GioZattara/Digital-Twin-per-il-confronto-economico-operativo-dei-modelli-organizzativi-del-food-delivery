import random 
import math
import collections

#CLIENTI
#Definisco la latitudine e la longitudine per ogni cliente
PROFILI_CLIENTI = {
    "cliente_A": {                 
        "lat_base": 45.482504000497485, 
        "lon_base": 9.144468764019887, 
    },
    "cliente_B": {
        "lat_base": 45.49261303347229,       
        "lon_base": 9.155626754595357,
    },
    "cliente_C": {
        "lat_base": 45.48081898530548,   
        "lon_base": 9.159059981972987,
    },
    "cliente_D": {
        "lat_base": 45.49453835786683,      
        "lon_base": 9.175367812016738,
    },
    "cliente_E": {
        "lat_base": 45.4887621872184,      
        "lon_base": 9.180174330345421,
    },
    "cliente_F": {                 
        "lat_base": 45.48178185730967, 
        "lon_base": 9.1757111347545, 
    },
    "cliente_G": {
        "lat_base": 45.48418896532736,       
        "lon_base": 9.197683789971343,
    },
    "cliente_H": {
        "lat_base": 45.48491107767757,     
        "lon_base": 9.211245038112988,
    },
    "cliente_I": {
        "lat_base": 45.4779595400811,       
        "lon_base": 9.188070753491553,
    },
    "cliente_L": {
        "lat_base": 45.470014815016484,      
        "lon_base": 9.190988996762542,
    },
    "cliente_M": {                 
        "lat_base": 45.470857490403695, 
        "lon_base": 9.163008193634843, 
    },
    "cliente_N": {
        "lat_base": 45.46965366447502,       
        "lon_base": 9.170732955234515,
    },
    "cliente_O": {
        "lat_base": 45.46568085648444,      
        "lon_base": 9.17880103957195,
    },
    "cliente_P": {
        "lat_base": 45.46339335516977,       
        "lon_base": 9.159574966257212,
    },
    "cliente_Q": {
        "lat_base": 45.45665070607956,    
        "lon_base": 9.158030013937278,
    },
    "cliente_R": {                 
        "lat_base": 45.456891528860154, 
        "lon_base": 9.180689314629646, 
    },
    "cliente_S": {
        "lat_base": 45.45078079257413,      
        "lon_base": 9.176252335827417,
    },
    "cliente_T": {
        "lat_base": 45.456240648083096,      
        "lon_base": 9.198520853021838,
    },
    "cliente_U": {
        "lat_base": 45.45142394146497,      
        "lon_base": 9.206073953252627,
    },
    "cliente_V": {
        "lat_base": 45.4657252352958,      
        "lon_base": 9.201133388549552,
    },
    "cliente_Z": {
        "lat_base": 45.46891412404871,     
        "lon_base": 9.204525600148207,
    },
    "cliente_X": {
        "lat_base": 45.46683883599438,      
        "lon_base": 9.214846584373907,
    }
}

#RISTORANTI
#Per ogni ristorante definisco la logintudine, la latitudine, il tempo medio di preparazione dei piatti e a seconda se sia giornata lavorativa o festiva e pranzo o cena
#definisco la coda massima nel picco orario, l'ora di inizio e di fine del picco orario e la deviazione standard di destra e sinistra della campana degli ordini
PROFILI_RISTORANTI = {
    "old_wild_west_viale_zara":{
        "lat_base": 45.49179475512985,
        "lon_base": 9.191772849567892,
        "t_medio_prep": 8,
        "lavorativo": {
            "pranzo": {
                "max_coda": 2,
                "picco_orario_i": 13.00,  
                "picco_orario_f": 14.00, 
                "dst_i": 0.3,     
                "dst_f": 0.4             
            },
            "cena": {
                "max_coda": 3,          
                "picco_orario_i": 20.00, 
                "picco_orario_f": 21.00,
                "dst_i": 0.4, 
                "dst_f": 0.7             
            }
        },
        "festivo": {
            "pranzo": {
                "max_coda": 3,
                "picco_orario_i": 13.00, 
                "picco_orario_f": 14.00, 
                "dst_i": 0.3,     
                "dst_f": 0.4             
            },
            "cena": {
                "max_coda": 4,          
                "picco_orario_i": 20.00, 
                "picco_orario_f": 21.00,
                "dst_i": 0.4, 
                "dst_f": 0.7             
            }
        }
    },
    "tow":{
        "lat_base": 45.48597421043128,
        "lon_base": 9.16356144237481, 
        "t_medio_prep": 9,
        "festivo": {
            "pranzo": {
                "max_coda": 1,
                "picco_orario_i": 13.00,  
                "picco_orario_f": 14.00, 
                "dst_i": 0.3,     
                "dst_f": 0.3             
            },
            "cena": {
                "max_coda": 2,          
                "picco_orario_i": 22.00, 
                "picco_orario_f": 23.00,
                "dst_i": 1.3, 
                "dst_f": 0.05             
            }
        },
        "lavorativo": {
            "pranzo": {
                "max_coda": 0.5,
                "picco_orario_i": 13.00, 
                "picco_orario_f": 14.00, 
                "dst_i": 0.3,     
                "dst_f": 0.3             
            },
            "cena": {
                "max_coda": 1,          
                "picco_orario_i": 20.00, 
                "picco_orario_f": 21.00,
                "dst_i": 0.7, 
                "dst_f": 1             
            }
        }
    },
    "ristorante_fresca":{
        "lat_base": 45.47423304263433,
        "lon_base": 9.205461604945162, 
        "t_medio_prep": 10,
        "lavorativo": {
            "pranzo": {
                "max_coda": 0.5,
                "picco_orario_i": 13.00, 
                "picco_orario_f": 14.00, 
                "dst_i": 0.3,     
                "dst_f": 0.6             
            },
            "cena": {
                "max_coda": 2,          
                "picco_orario_i": 20.00, 
                "picco_orario_f": 21.00,
                "dst_i": 3, 
                "dst_f": 0.6             
            }
        },
        "festivo": {
            "pranzo": {
                "max_coda": 1,
                "picco_orario_i": 13.00, 
                "picco_orario_f": 14.00, 
                "dst_i": 0.3,     
                "dst_f": 0.6             
            },
            "cena": {
                "max_coda": 1.5,          
                "picco_orario_i": 19.00, 
                "picco_orario_f": 20.00,
                "dst_i": 2.7, 
                "dst_f": 0.8             
            }
        },
    },
    "mcdonald_via_torino":{
        "lat_base": 45.4608288244417,
        "lon_base": 9.182036083888708,
        "t_medio_prep": 3,
        "lavorativo": {
            "pranzo":{
                "max_coda": 2,
                "picco_orario_i": 13.00, 
                "picco_orario_f": 14.00, 
                "dst_i": 2,     
                "dst_f": 1
            },
            "cena":{
                "max_coda": 1.5,
                "picco_orario_i": 18.00, 
                "picco_orario_f": 19.00, 
                "dst_i": 0.7,     
                "dst_f": 2
            }
        },
        "festivo": {
            "pranzo":{
                "max_coda": 2.5,
                "picco_orario_i": 12.00, 
                "picco_orario_f": 13.00, 
                "dst_i": 2.3,     
                "dst_f": 1.3
            },
            "cena":{
                "max_coda": 2.5,
                "picco_orario_i": 17.00, 
                "picco_orario_f": 19.00, 
                "dst_i": 1,     
                "dst_f": 3.3
            }
        },
    },
    "american_graffiti_san_siro":{
        "lat_base": 45.4803224999262,
        "lon_base": 9.123858979759998,
        "t_medio_prep": 7,
        "lavorativo": {
            "pranzo": {
                "max_coda": 0.5,
                "picco_orario_i": 12.00, 
                "picco_orario_f": 15.00, 
                "dst_i": 0.05,     
                "dst_f": 0.05             
            },
            "cena": {
                "max_coda": 1,          
                "picco_orario_i": 21.00, 
                "picco_orario_f": 22.00,
                "dst_i": 0.6, 
                "dst_f": 0.6             
            }
        },
        "festivo": {
            "pranzo": {
                "max_coda": 0.5,
                "picco_orario_i": 12.00, 
                "picco_orario_f": 15.00, 
                "dst_i": 0.05,     
                "dst_f": 0.05             
            },
            "cena": {
                "max_coda": 1.5,          
                "picco_orario_i": 21.00, 
                "picco_orario_f": 22.00,
                "dst_i": 0.6, 
                "dst_f": 0.6             
            }
        }
    },
    "ristorante_madama":{
        "lat_base": 45.444754364852514,
        "lon_base": 9.211869533630422,
        "t_medio_prep": 11,
        "festivo": {
            "pranzo": {
                "max_coda": 2,
                "picco_orario_i": 8.00, 
                "picco_orario_f": 9.00, 
                "dst_i": 0.3,     
                "dst_f": 2             
            },
            "cena": {
                "max_coda": 1,          
                "picco_orario_i": 22.00, 
                "picco_orario_f": 24.00,
                "dst_i": 2.3, 
                "dst_f": 0.6             
            }
        },
        "lavorativo": {
            "pranzo": {
                "max_coda": 1,
                "picco_orario_i": 12.00, 
                "picco_orario_f": 13.00, 
                "dst_i": 1.7,     
                "dst_f": 1             
            },
            "cena": {
                "max_coda": 1.8,          
                "picco_orario_i": 18.00, 
                "picco_orario_f": 20.00,
                "dst_i": 1, 
                "dst_f": 1.7            
            }
        }
    },
    "old_wild_west_corso_sempione":{
        "lat_base": 45.47775205092629,
        "lon_base": 9.170202832168302,
        "t_medio_prep": 8,
        "festivo": {
            "pranzo": {
                "max_coda": 1,
                "picco_orario_i": 13.00, 
                "picco_orario_f": 14.00, 
                "dst_i": 0.3,     
                "dst_f": 0.6             
            },
            "cena": {
                "max_coda": 2,          
                "picco_orario_i": 20.00, 
                "picco_orario_f": 22.00,
                "dst_i": 0.6, 
                "dst_f": 0.6            
            }
        },
        "lavorativo": {
            "pranzo": {
                "max_coda": 0.5,
                "picco_orario_i": 12.00, 
                "picco_orario_f": 15.00, 
                "dst_i": 0.05,     
                "dst_f": 0.05             
            },
            "cena": {
                "max_coda": 0.5,          
                "picco_orario_i": 20.00, 
                "picco_orario_f": 22.00,
                "dst_i": 0.3, 
                "dst_f": 0.05            
            }
        }
    },
    "hostaria_baita":{
        "lat_base": 45.484425015667675, 
        "lon_base": 9.204973302114295,
        "t_medio_prep": 12,
        "lavorativo": {
            "pranzo": {
                "max_coda": 1,
                "picco_orario_i": 13.00, 
                "picco_orario_f": 14.00, 
                "dst_i": 0.3,     
                "dst_f": 0.3             
            },
            "cena": {
                "max_coda": 2,          
                "picco_orario_i": 20.00, 
                "picco_orario_f": 21.00,
                "dst_i": 0.6, 
                "dst_f": 0.6            
            }
        },
        "festivo": {
            "pranzo": {
                "max_coda": 1,
                "picco_orario_i": 12.00, 
                "picco_orario_f": 15.00, 
                "dst_i": 0.05,     
                "dst_f": 0.05             
            },
            "cena": {
                "max_coda": 1.5,          
                "picco_orario_i": 21.00, 
                "picco_orario_f": 22.00,
                "dst_i": 0.3, 
                "dst_f": 1            
            }
        }
    },
    "trive_all_day":{
        "lat_base": 45.46661795741612,
        "lon_base": 9.151486122088889,
        "t_medio_prep": 5,
        "festivo": {
            "pranzo": {
                "max_coda": 2,
                "picco_orario_i": 11.00, 
                "picco_orario_f": 12.00, 
                "dst_i": 1,     
                "dst_f": 1            
            },
            "cena": {
                "max_coda": 3,          
                "picco_orario_i": 20.00, 
                "picco_orario_f": 23.00,
                "dst_i": 1.7, 
                "dst_f": 1            
            }
        },
        "lavorativo": {
            "pranzo": {
                "max_coda": 1,
                "picco_orario_i": 10.00, 
                "picco_orario_f": 11.00, 
                "dst_i": 0.6,     
                "dst_f": 1.3             
            },
            "cena": {
                "max_coda": 1,          
                "picco_orario_i": 19.00, 
                "picco_orario_f": 20.00,
                "dst_i": 1.3, 
                "dst_f": 1.7           
            }
        }
    },
    "filume_milano":{
        "lat_base": 45.45325146143019,
        "lon_base": 9.201003990705894,
        "t_medio_prep": 6,
        "lavorativo": {
            "pranzo": {
                "max_coda": 1.5,
                "picco_orario_i": 14.00, 
                "picco_orario_f": 15.00, 
                "dst_i": 1,     
                "dst_f": 0.05             
            },
            "cena": {
                "max_coda": 1.5,          
                "picco_orario_i": 23.00, 
                "picco_orario_f": 24.00,
                "dst_i": 1.7, 
                "dst_f": 0.05            
            }
        },
        "festivo": {
            "pranzo": {
                "max_coda": 2,
                "picco_orario_i": 13.00, 
                "picco_orario_f": 14.00, 
                "dst_i": 0.6,     
                "dst_f": 0.3             
            },
            "cena": {
                "max_coda": 3,          
                "picco_orario_i": 20.00, 
                "picco_orario_f": 21.00,
                "dst_i": 0.6, 
                "dst_f": 1            
            }
        }
    }
}

#RIDER
#Per ogni rider definisco la posizione (latitudine e longitudine), la velocità media e il punteggio reputazionale che va da 1 a 5.
#Questo dizionario rappresenta la configurazione base della flotta di rider.
PROFILI_RIDER = {
    "rider_1":{ 
        "lat_base": 45.46615562924043,  
        "lon_base": 9.187673822088886,
        "v_media": 15,
        "punteggio": 4.6, 
    },

    "rider_2":{ 
        "lat_base": 45.472871544279904,  
        "lon_base": 9.146742812582417,
        "v_media": 15,
        "punteggio": 3.2,
    },
    
    "rider_3":{ 
        "lat_base": 45.483463725197716,   
        "lon_base": 9.166312208634919,
        "v_media": 15,
        "punteggio": 2.3,
    },
   "rider_4":{ 
       "lat_base": 45.480214063243395, 
       "lon_base": 9.205965984846562,
       "v_media": 15,
       "punteggio": 1.9,
   },
   "rider_5":{ 
        "lat_base": 45.4714270017021,   
        "lon_base": 9.198241223246892,
        "v_media": 15,
        "punteggio": 4.8,
    },
    "rider_6":{ 
        "lat_base": 45.45312625764484,   
        "lon_base": 9.19703959366472,
        "v_media": 15,
        "punteggio": 3.7,
    },
}

#DISTANZA EUCLIDEA TRA PUNTI
def calcolo_distanza_euclidea(lat1, lon1, lat2, lon2): 
    """Calcolo la distanza in linea d'aria tra due punti mediante la formula di Haversine (risultato in km)"""
    r_terra = 6371.0 #raggio medio della terra in km
    #converto i valori della logitudine e latitudine da gradi a radianti attraverso una funzione della libreria math
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    #Formula di Haversine
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    distanza = 2 * r_terra * math.asin(math.sqrt(a))
    return distanza

#DISTANZA RETTANGOLARE TRA PUNTI
def calcolo_distanza_rettangolare(lat1, lon1, lat2, lon2):
    """Calcolo la distanza Manhattan tra due punti, ossia la distanza composta dalla somma dei due cateti tenendo conto anche della curvatura terrestre"""
    r_terra = 6371.0 
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    #Calcolo il cateto 1 che specifica la distanza est-ovest dei due punti
    delta_lon = abs(lon2_rad - lon1_rad)
    #Calcolo la lunghezza dell'arco
    cateto1 = r_terra * math.cos(lat1_rad) * delta_lon
    #Calcolo il cateto 2 che specifica la distanza nord-sud dei due punti
    delta_lat = abs(lat2_rad - lat1_rad)
    cateto2 = r_terra * delta_lat   
    distanza = cateto1 + cateto2
    return distanza

#ALGORITMO DI DISPATCHING (selezione del miglior rider a cui assegnare l'ordine)
#RANKING RIDER 
def crea_classifica_rider(risto_core, rider_disponibili, soglia_gruppo_km=0.5):
    """
    Restituisce la lista dei rider, disponibili per evadere la commessa, ordinata secondo la logica di dispatching:
    la distanza dal ristorante è il criterio primario mentre punteggio dei rider viene usato come spareggio tra rider che si trovano 
    a una distanza simile tra loro (in un intorno di 0.5km).
    """
    #calcolo la distanza di ciascun rider disponibile dal ristorante
    candidati = []
    for r in rider_disponibili:
        distanza = calcolo_distanza_rettangolare(r.lat_rider, r.lon_rider,risto_core.lat_ristorante, risto_core.lon_ristorante)
        candidati.append((r, distanza))
    #ordino prima i rider per distanza crescente, guarda solo il valore che si trova all'indice 1
    candidati.sort(key=lambda c: c[1])
    #faccio uno spareggio in base al punteggio
    classifica_finale = []
    i = 0
    while i < len(candidati):
        gruppo = [candidati[i]]
        j = i + 1
        #Un rider entra in questo gruppo se è entro la soglia 'soglia_gruppo_km' dal primo rider dei candidati
        while j < len(candidati) and (candidati[j][1] - candidati[i][1]) <= soglia_gruppo_km:
            gruppo.append(candidati[j])
            j += 1
        #con reverse ordino la lista in modo descrescente
        gruppo.sort(key=lambda c: c[0].punteggio, reverse=True)
        classifica_finale.extend(gruppo)
        #avanza l'indice principale al primo rider non compreso al gruppo appena chiuso
        i = j
    #rimuovo la distanza dalle tuple per restituire la classifica finale con solo il riferimento al rider
    solo_rider = []
    for r, distanza in classifica_finale:
        solo_rider.append(r)
    return solo_rider        

#PING SEQUENZIALE
def ping_sequenziale(ristorante_corrente, rider_disponibili, soglia_gruppo_km=0.5, prob_rifiuto=0.10):
    """
    Attraverso questa funzione simuliamo il dispatching a ping sequenziale. Viene proposto l'ordine al rider migliore
    in classifica_finale, con una probabilità del 10% quel rider rifiuta e la proposta passa al successivo
    in classifica, finche' uno non accetta o la lista non si esaurisce.
    La funzione ritorna il rider assegnato, oppure None se tutti i rider hanno rifiutato.
    """
    classifica = crea_classifica_rider(ristorante_corrente, rider_disponibili, soglia_gruppo_km)
    for rider_candidato in classifica:
        rifiuta = random.random() < prob_rifiuto
        if not rifiuta:
            return rider_candidato
    return None

#CLASSI
class ordine:
    def __init__(self, numero_ordine, lon_cliente, ora_generata, gtv_ordine, lat_cliente, brutto_tempo=False, tipo_cliente="sconosciuto"):
        self.numero_ordine = numero_ordine
        self.lat_cliente = lat_cliente
        self.lon_cliente = lon_cliente
        self.ora_generata = ora_generata
        self.gtv_ordine = gtv_ordine
        self.brutto_tempo = brutto_tempo
        self.tipo_cliente = tipo_cliente
    @classmethod
    def genera_ordine_da_profilo(cls, numero_ordine, tipo_profilo, ora_generata, gtv_medio=25.00):
        profilo = PROFILI_CLIENTI[tipo_profilo]    
        #Genero il mio gtv mediante una distribuzione gaussiana con media 25.00€. 
        #Scelgo una deviazione standard di 15€ perché so che sotto i 10€ il cliente pagherebbe una sovrattassa
        gtv_casuale = 0
        #Continuo a generare numeri finché il valore non è maggiore o uguale a 5€
        while gtv_casuale < 5.0:
            gtv_casuale = random.gauss(gtv_medio, gtv_medio-10)
        gtv = round(gtv_casuale, 2)

        lat_cliente = profilo["lat_base"]
        lon_cliente = profilo["lon_base"]

        return cls(
            numero_ordine=numero_ordine,
            lat_cliente=lat_cliente,
            lon_cliente=lon_cliente,
            ora_generata=ora_generata,
            gtv_ordine=gtv,
            tipo_cliente=tipo_profilo
        )
    def controllo_festivo(self, rider_core):
        """Verifico se la data dell'ordine cade in un giorno festivo poiché ciò implica quindi un aumento di paga per via degli indennizzi"""
        giorno = rider_core.giorno_consegna
        feste = [(1, 1), (6, 1), (25, 4), (1, 5), (2, 6), (15, 8), (1, 11), (7, 12), (8, 12), (25, 12), (26, 12)]
        control = (giorno.day, giorno.month) in feste
        return control
            
class ristorante:
    def __init__(self, tipo):
        self.tipo = tipo
        self.n_ordini = 0
        self.profilo = PROFILI_RISTORANTI[tipo]
        self.lat_ristorante = self.profilo["lat_base"]
        self.lon_ristorante = self.profilo["lon_base"]
        self.tempo_prep_medio = self.profilo["t_medio_prep"]
        self.coda_ordini = collections.deque()
        #Vado a definirmi una coda FIFO per gli ordini di ogni ristorante in modo tale da simulare un realistico aumento del tempo di preparazione dell'ordine
        self.coda_ordini = collections.deque()

    def estrai_parametri_risto(self, ordine, azienda_core):
        "estrae i parametri corretti (max_coda, picco_orario e dst) a seconda cui il giorno è lavorativo, festivo e a seconda cui siamo a pranzo o cena."
        if ordine.controllo_festivo(azienda_core) == True:
            tipo_giorno = "festivo"
        else:
            tipo_giorno = "lavorativo"
        if ordine.ora_generata < 16.00:
            fascia_oraria = "pranzo"
        else:
            fascia_oraria = "cena"
        return self.profilo[tipo_giorno][fascia_oraria]

    def entro_raggio(self, ordine):
        """Verifico che la posizione del cliente che ha effettuato l'ordine al seguente ristorante sia entro i 3Km"""
        self.d_risto_cliente_raggio = calcolo_distanza_euclidea(self.lat_ristorante, self.lon_ristorante, ordine.lat_cliente, ordine.lon_cliente)#metti apposto la classe ordine
        if self.d_risto_cliente_raggio > 3:
            raise ValueError("Non è possibile effetturare l'ordine a questo ristorante perché il cliente si trova al di fuori del raggio di 3Km") 
        self.d_risto_cliente = calcolo_distanza_rettangolare(self.lat_ristorante, self.lon_ristorante, ordine.lat_cliente, ordine.lon_cliente) 
        return self.d_risto_cliente

    def calcola_ordini_fittizi(self, ordine, azienda_core):
        """
        Calcola, usando una curva a campana, quanti ordini fittizi, precedenti a quello in esame, ci sono nella coda FIFO del ristorante tenendo conto 
        del momento della giornata e del tipo di giornata
        """
        #Viene applicata la formula della curva a campana per trovare il moltiplicatore da 0.0 a 1.0 per capire quanti ordini fittizzi ci sono a un determinato
        #orario scostato di un tot dal picco di ordini giornaliero del ristorante. Ovviamente nell'orario di picco la coda sarà massima
        parametri = self.estrai_parametri_risto(ordine, azienda_core)
        picco_orario_i = parametri["picco_orario_i"]
        picco_orario_f = parametri["picco_orario_f"]
        dst_i = parametri["dst_i"]
        dst_f = parametri["dst_f"]
        max_coda = parametri["max_coda"]

        if ordine.ora_generata < picco_orario_i:
            distanza = ordine.ora_generata - picco_orario_i
            fattore_picco = math.exp(-0.5 * (distanza / dst_i) ** 2)
            ordini_fittizzi = int(max_coda * fattore_picco)
            return ordini_fittizzi
        if ordine.ora_generata > picco_orario_f:
            distanza = ordine.ora_generata - picco_orario_f
            fattore_picco = math.exp(-0.5 * (distanza / dst_f) ** 2)
            ordini_fittizzi = int(max_coda * fattore_picco)
            return ordini_fittizzi
        else:
            ordini_fittizzi = int(max_coda)
            return ordini_fittizzi
        
    def ricevi_ordine(self, ordine_core, rider_core, t_arrivo_rider=None, soglia_attesa_minuti=50):
        """
        Simula la ricezione dell'ordine, popola la coda fittizia e calcola il tempo di preparazione totale necessario.
        Se viene passato il tempo di arrivo del rider al ristorante (t_arrivo_rider), la funzione controlla anche
        se l'attesa in cucina supera la soglia massima tollerata (soglia_attesa_minuti): in tal caso il cliente
        rinuncerebbe ad aspettare e l'ordine va considerato perso (secondo elemento della tupla ritornata = True).
        Questa perdita non ha nulla a che vedere con la paga del rider: serve solo a capire se l'ordine si perde
        e per quanto tempo il rider resta comunque impegnato prima di liberarsi.
        """
        n_fittizi = self.calcola_ordini_fittizi(ordine_core, rider_core)
        self.coda_ordini.clear()
        #Inserisco il tempo totale di preparazione per gli ordini fittizzi e infine inserisco in coda anche il tempo di preparazione del mio ordine
        for i in range(n_fittizi):
            tempo_prep = self.tempo_prep_medio
            self.coda_ordini.append(tempo_prep) 
        tempo_prep_mio_ordine = self.tempo_prep_medio
        self.coda_ordini.append(tempo_prep_mio_ordine)
        #Calcolo il tempo totale affinché la cucina smaltisca l'intera coda, ossia il tempo che passerà prima che il mio ordine sarà preparato
        tempo_totale_cucina = sum(self.coda_ordini)
        #Se conosco il tempo di arrivo del rider, verifico se l'attesa in cucina (oltre il tempo di percorrenza) è troppo lunga
        ordine_perso_per_coda = False
        if t_arrivo_rider is not None:
            attesa_in_cucina = max(0.0, tempo_totale_cucina - t_arrivo_rider)
            ordine_perso_per_coda = attesa_in_cucina > soglia_attesa_minuti

        return tempo_totale_cucina, ordine_perso_per_coda

    def ordine_completo(self):
        "Conta gli ordini preparati"
        self.n_ordini += 1

class rider:
    def __init__(self, rider_id, giorno_consegna):
        self.rider_id = rider_id
        self.order = None
        self.giorno_consegna = giorno_consegna
        profilo = PROFILI_RIDER[rider_id]
        self.lat_rider = profilo["lat_base"]
        self.lon_rider = profilo["lon_base"]
        self.velocita = profilo["v_media"]
        self.punteggio = profilo["punteggio"]
        self.ora_termine_consegna = 0.0
        self.paga_oraria = 10.0
        self.costo = 0.0
    
    def tempo_arrivo_ristorante(self, ristorante_core):
        """Mi calcolo il tempo che il rider ci mette ad arrivare al ristorante, questo tempo mi servirà successivamente per calcolare la paga del rider"""
        d_rider_risto = calcolo_distanza_rettangolare(self.lat_rider, self.lon_rider, ristorante_core.lat_ristorante, ristorante_core.lon_ristorante)
        self.t_rider_risto = (d_rider_risto/self.velocita)*60
        return self.t_rider_risto

    def calcolo_paga_rider(self, ristorante_core, ordine_core):
        """Calcolo la tariffa per ogni consegna tenendo conto anche dell'indennità"""
        #Mi calcolo la paga base usando il tempo stimato di percorrenza per evadere l'ordine
        t_lavoro = self.t_rider_risto + (ristorante_core.d_risto_cliente/self.velocita)*60
        paga_base = (t_lavoro/ 60.0)*self.paga_oraria
        #Inizializzo le circostante che mi provocano un'aumento di paga dei rider
        notte = 0 <= ordine_core.ora_generata < 7
        festa = ordine_core.controllo_festivo(self)
        meteo_avverso = ordine_core.brutto_tempo
        condizioni_lavoro = sum([notte, festa, meteo_avverso])
        moltiplicatore = 1.0
        
        if condizioni_lavoro == 1:
            moltiplicatore = 1.10
        elif condizioni_lavoro == 2:
            moltiplicatore = 1.15
        elif condizioni_lavoro == 3:
            moltiplicatore = 1.20    
        paga_finale = paga_base * moltiplicatore
        return paga_finale
    
    def consegna_completa(self, ristorante_core, t_cucina, t_rider_risto):
        """
        Assegno la posizione del mio cliente al mio rider perché sarà da lì che inizierà a fare la consegna successiva. 
        Inoltre vado a definire l'ora di termine della mia cosegna per andare a capire se il rider è disponibile o no per prendere a carico l'ordine successivo.
        """
        self.lat_rider = self.order.lat_cliente
        self.lon_rider = self.order.lon_cliente
        paga = self.calcolo_paga_rider(ristorante_core, self.order)
        self.costo += paga
        attesa_risto = max(0.0, t_cucina - t_rider_risto)
        t_risto_cliente = (ristorante_core.d_risto_cliente/self.velocita) * 60
        t_viaggio = t_rider_risto + attesa_risto + t_risto_cliente

        self.ora_termine_consegna = self.order.ora_generata + (t_viaggio / 60)

        self.order = None
        return paga

    def abbandona_ordine_per_coda(self, ristorante_core, t_rider_risto, soglia_attesa_minuti=50):
        """
        Simula il rider che, arrivato al ristorante, aspetta al massimo fino alla soglia di attesa tollerata e poi
        rinuncia alla consegna perché la cucina ha troppa coda. Il rider resta comunque impegnato per
        il tempo di andata al ristorante più l'attesa massima sostenuta, ma non riceve alcuna paga poiché la
        consegna non viene mai portata a termine. La sua posizione resta quella del ristorante, dato che è lì che
        si trova nel momento in cui il cliente rinuncia.
        """
        self.lat_rider = ristorante_core.lat_ristorante
        self.lon_rider = ristorante_core.lon_ristorante
        t_occupato = t_rider_risto + soglia_attesa_minuti
        self.ora_termine_consegna = self.order.ora_generata + (t_occupato / 60)
        self.order = None

class azienda:
    def __init__(self, nome="MyDelivery", take_rate=0.278):
        self.nome = nome
        self.take_rate = take_rate
        self.n_consegne = 0
        self.ricavo_totale = 0.0
        self.costi_totali = 0.0
        self.profitto_totale = 0.0

    def delivery_processamento(self, ordine_core, paga_singola):
        """Calcolo i ricavi, costi e utili per ogni singola spedizione e per ogni giornata aziendale. Ritorno poi un dizionario con i dati finanziari di ogni ordine effettuato"""
        ricavo = ordine_core.gtv_ordine * self.take_rate
        costi = paga_singola
        profitto = ricavo - costi
        #Aggiorno delle statistiche globali dell'azienda
        self.n_consegne += 1
        self.ricavo_totale += ricavo
        self.costi_totali += costi
        self.profitto_totale += profitto

        return {
            "ordine numero": ordine_core.numero_ordine,
            "gtv ordine": ordine_core.gtv_ordine,
            "ricavo": round(ricavo, 2),
            #il costo è dovuto alla paga del rider
            "costo": round(costi, 2), 
            "profitto": round(profitto, 2)
        }

class simulazione:

    def __init__(self, numero_ordini_desiderati, gtv_medio=25.0):
        self.numero_ordini = numero_ordini_desiderati
        self.gtv_medio=gtv_medio
        self.ordini_giornalieri = []

    def genera_ordini_giornalieri(self):
        """Genero il numero desiderato di ordini distribuendoli secondo le fasce orarie di picco"""
        tipologie_clienti = list(PROFILI_CLIENTI.keys()) 
        #Definisco le fasce orarie e i loro pesi di probabilità
        fasce_orarie = [
            (0.0, 8.0, 1.0),     #Notte fonda - bassa domanda
            (8.0, 12.0, 1.0),    #Colazione - bassa domanda
            (12.0, 14.30, 2.0),  #Pranzo - picco
            (14.30, 18.30, 1.0), #Pomeriggio - bassa domanda
            (18.30, 22.0, 3.0),  #Cena - super picco
            (22.0, 24.0, 2.0)    #Tarda sera - picco
        ]
        pesi = []
        #vado ad estrarre il terzo elemento di ogni fascia, ossia il peso
        for fascia in fasce_orarie:
            peso = fascia[2]  
            pesi.append(peso)
        
        for i in range(self.numero_ordini):
            #Scelgo la fascia oraria, naturalmente quelle con peso maggiore verranno scelte maggiormente
            fascia_scelta = random.choices(fasce_orarie, weights=pesi, k=1)[0]
            #Genero un'ora casuale all'interno di quella fascia oraria
            ora_casuale = random.uniform(fascia_scelta[0], fascia_scelta[1])
            #Scelgo casualmente un cliente
            tipo_scelto = random.choice(tipologie_clienti)
            nuovo_ordine = ordine.genera_ordine_da_profilo(i+1, tipo_scelto, ora_casuale, self.gtv_medio)
            #Per far variare un po' la posizione dei clienti, poiché ne ho definiti pochi, aggiungo un po' di rumore sulle posizioni
            nuovo_ordine.lat_cliente = random.gauss(nuovo_ordine.lat_cliente, 0.005)
            nuovo_ordine.lon_cliente = random.gauss(nuovo_ordine.lon_cliente, 0.005)
            self.ordini_giornalieri.append(nuovo_ordine) 
        #Ordino la lista in base all'orario dell'ordine
        self.ordini_giornalieri.sort(key=lambda x: x.ora_generata)
        #Ordino anche gli ID degli ordini
        for indice, o in enumerate(self.ordini_giornalieri):
            o.numero_ordine = indice + 1    
        return self.ordini_giornalieri
