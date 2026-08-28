import random 
import math
import collections
import numpy as np
from scipy.optimize import linear_sum_assignment
#Verranno inseriti solo i commenti aggiuntivi che diversificano questo codice da 'gig_economy.py'.
#CLIENTI
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
PROFILI_RIDER = {
    "rider_1":{ 
        "lat_base": 45.46615562924043,  
        "lon_base": 9.187673822088886,
        "v_media": 15,
        "turni": [1, 3]
    },

    "rider_2":{ 
        "lat_base": 45.46615562924043,  
        "lon_base": 9.187673822088886,
        "v_media": 15, 
        "turni": [2, 4]
    },
    
    "rider_3":{ 
        "lat_base": 45.46615562924043,  
        "lon_base": 9.187673822088886,
        "v_media": 15,
        "turni": [2, 4] 
    },
   "rider_4":{ 
       "lat_base": 45.46615562924043,
       "lon_base": 9.187673822088886,
       "v_media": 15,
       "turni": [5] 
   },
   "rider_5":{ 
        "lat_base": 45.46615562924043,  
        "lon_base": 9.187673822088886,
        "v_media": 15,
        "turni": [1, 3]
    },
    "rider_6":{ 
        "lat_base": 45.46615562924043,  
        "lon_base": 9.187673822088886,
        "v_media": 15,
        "turni": [2, 4]
    },
}

#DURATA TURNI
#La paga dei rider si baserà sui turni sotto descritti. Ogni rider non eccederà nelle 8 ore di lavoro complessivo giornaliero
DURATA_TURNI = {
    1: 4.0,   #8:00-12:00 
    2: 2.5,   #12:00-14:30 
    3: 4.0,   #14:30-18:30 
    4: 5.5,   #18:30-24:00 
    5: 8.0    #00:00-08:00
}

# DISTANZA EUCLIDEA TRA PUNTI
def calcolo_distanza_euclidea(lat1, lon1, lat2, lon2): 
    """Calcolo la distanza in linea d'aria tra due punti mediante la formula di Haversine (risultato in km)"""
    r_terra = 6371.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    distanza = 2 * r_terra * math.asin(math.sqrt(a))
    return distanza

# DISTANZA RETTANGOLARE TRA PUNTI
def calcolo_distanza_rettangolare(lat1, lon1, lat2, lon2):
    """Calcolo la distanza Manhattan tra due punti"""
    r_terra = 6371.0 
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    delta_lon = abs(lon2_rad - lon1_rad)
    cateto1 = r_terra * math.cos(lat1_rad) * delta_lon
    
    delta_lat = abs(lat2_rad - lat1_rad)
    cateto2 = r_terra * delta_lat   
    distanza = cateto1 + cateto2
    return distanza

#CLASSI
class ordine:
    def __init__(self, numero_ordine, lon_cliente, ora_generata, gtv_ordine, lat_cliente, tipo_cliente="sconosciuto"):
        self.numero_ordine = numero_ordine
        self.lat_cliente = lat_cliente
        self.lon_cliente = lon_cliente
        self.ora_generata = ora_generata
        self.gtv_ordine = gtv_ordine
        self.tipo_cliente = tipo_cliente
        self.ristorante = None

    @classmethod
    def genera_ordine_da_profilo(cls, numero_ordine, tipo_profilo, ora_generata,  gtv_medio=25.00):
        profilo = PROFILI_CLIENTI[tipo_profilo]    
        gtv_casuale = 0
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

    def controllo_festivo(self, azienda_core):
        """Verifico se la data dell'ordine cade in un giorno festivo poiché ciò implica quindi un aumento di paga"""
        giorno = azienda_core.giorno_consegna
        feste = [(1, 1), (6, 1), (25, 4), (1, 5), (2, 6), (15, 8), (1, 11), (7, 12), (8, 12), (25, 12), (26, 12)]
        control = (giorno.day, giorno.month) in feste
        return control
            
class ristorante:
    def __init__(self, tipo):
        self.tipo = tipo
        self.profilo = PROFILI_RISTORANTI[tipo]
        self.lat_ristorante = self.profilo["lat_base"]
        self.lon_ristorante = self.profilo["lon_base"]
        self.tempo_prep_medio = self.profilo["t_medio_prep"]
        self.coda_ordini = collections.deque()

    def estrai_parametri_risto(self, ordine, azienda_core):
        "estrae i parametri (max_coda, picco_orario e dst) a seconda cui il giorno è lavorativo, festivo e a seconda cui siamo a pranzo o cena"
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
        self.d_risto_cliente_raggio = calcolo_distanza_euclidea(self.lat_ristorante, self.lon_ristorante, ordine.lat_cliente, ordine.lon_cliente)
        if self.d_risto_cliente_raggio > 3:
            raise ValueError("Non è possibile effetturare l'ordine a questo ristorante perché il cliente è troppo distante") 
        self.d_risto_cliente = calcolo_distanza_rettangolare(self.lat_ristorante, self.lon_ristorante, ordine.lat_cliente, ordine.lon_cliente) 
        return self.d_risto_cliente

    def calcola_ordini_fittizi(self, ordine, azienda_core): 
        """
        Calcola, usando una curva a campana, quanti ordini fittizi, precedenti a quello in esame, ci sono nella coda FIFO del ristorante tenendo conto 
        del momento della giornata e del tipo di giornata
        """
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
        
    def ricevi_ordine(self, ordine, azienda_core):
        """Simula la ricezione dell'ordine, popola la coda e calcola il tempo di preparazione totale necessario"""
        n_fittizi = self.calcola_ordini_fittizi(ordine, azienda_core)
        self.coda_ordini.clear()
        for i in range(n_fittizi):
            self.coda_ordini.append(self.tempo_prep_medio)
        tempo_prep_mio_ordine = self.tempo_prep_medio
        self.coda_ordini.append(tempo_prep_mio_ordine)
        tempo_totale_cucina = sum(self.coda_ordini)
        return tempo_totale_cucina

class rider:
    def __init__(self, rider_id, profilo_custom=None):
        self.rider_id = rider_id
        self.ora_termine_consegna = 0.0
        #Se abbiamo un profilo custom usiamo quello sennò ne prendiamo uno dal dizionario
        if profilo_custom:
            profilo = profilo_custom
        else:
            profilo = PROFILI_RIDER[rider_id]
        self.turni = profilo.get("turni", [])
        self.lat_rider = profilo["lat_base"]
        self.lon_rider = profilo["lon_base"]
        self.velocita = profilo["v_media"]

    def tempo_arrivo_ristorante(self, ristorante_core):
        """Mi calcolo il tempo che il rider ci mette ad arrivare al ristorante"""  
        self.d_rider_risto = calcolo_distanza_rettangolare(self.lat_rider, self.lon_rider, ristorante_core.lat_ristorante, ristorante_core.lon_ristorante)
        self.t_rider_risto = (self.d_rider_risto/self.velocita)*60
        return self.t_rider_risto
    
    def ordine_a_carico(self, ordine, top_tempo_tot, top_ora_inizio):   
        """Calcolo l'ora in cui l'ordine sarà stato evaso completamente e aggiorno la posizione del rider con la posizione del cliente"""
        self.ora_termine_consegna = top_ora_inizio + (top_tempo_tot / 60) 
        self.lat_rider = ordine.lat_cliente
        self.lon_rider = ordine.lon_cliente

class azienda:
    def __init__(self, giorno_consegna, nome="MyDelivery", take_rate=0.278):
        self.take_rate = take_rate
        self.n_consegne = 0
        self.ricavo_totale = 0.0
        self.costi_totali = 0.0
        self.profitto_totale = 0.0
        self.giorno_consegna = giorno_consegna
        self.paga_oraria = 8.93
        self.costo = 0.0
        self.bonus_notturni_totali = 0.0
        self.km_totali = 0.0
        self.indennizzo_km = 0.0
        #Tiene traccia di quali turni sono stati realmente attivi durante la giornata simulata
        self.turni_operativi = set()
        #Coda aziendale degli ordini generati che non ancora assegnati ad un rider. 
        #Vengono ricontrollati ad ogni ciclo di gestione (es. ogni minuto) fin tanto che non vengono assegnati
        self.coda_pancia = []
    
    def top_rider(self, ordine, risto_core, rider_core, t_cucina):
        """
        Calcolo qual è il miglior rider a cui assegnare l'ordine. La scelta del miglior rider dipenderà dal costo dei km 
        percorsi per arrivare al ristorante e dal costo dell'attesa del rider al ristorante. Il rider non verrà comunque impegnato istantaneamente; 
        ci serve solo per confrontare tra loro le coppie (ordine, rider) prima di prendere una decisione.
        Se il rider è in ritardo di oltre 50 la funzione ritorna None perché scarta la possibilità
        di affidare quell'ordine a quel rider, altrimenti (costo_totale, tempo_totale_consegna, ora_inizio_effettiva).
        """
        ora_inizio_effettiva = max(ordine.ora_generata, rider_core.ora_termine_consegna)
        ritardo_partenza_minuti = (ora_inizio_effettiva - ordine.ora_generata) * 60
        if ritardo_partenza_minuti > 50.0:
            return None

        t_viaggio_risto = rider_core.tempo_arrivo_ristorante(risto_core)
        km_viaggio = rider_core.d_rider_risto
        costo_viaggio = km_viaggio * 0.06

        ora_arrivo_rider = ora_inizio_effettiva + (t_viaggio_risto / 60)
        ora_cibo_pronto = ordine.ora_generata + (t_cucina / 60)

        t_attesa = max(0.0, (ora_cibo_pronto - ora_arrivo_rider) * 60)
        costo_attesa = t_attesa * (self.paga_oraria / 60)

        costo_totale = costo_attesa + costo_viaggio

        t_risto_cliente = (risto_core.d_risto_cliente / rider_core.velocita) * 60
        tempo_tot = t_viaggio_risto + t_attesa + t_risto_cliente

        return costo_totale, tempo_tot, ora_inizio_effettiva

    def assegna_ristorante(self, ordine, lista_ristoranti):
            "Cerca, in ordine casuale, il primo ristorante entro 3km dal cliente. Ritorna None se non trova nessun."
            ristoranti_shuffle = list(lista_ristoranti)
            random.shuffle(ristoranti_shuffle)
            for risto in ristoranti_shuffle:
                try:
                    risto.entro_raggio(ordine)
                    return risto
                except ValueError:
                    continue
            return None

    def aggiungi_in_coda(self, ordine_core, lista_ristoranti):
        """
        Quando l'ordine viene generato non viene assegnato subito a un rider, ma entra in coda per venire valutato al prossimo ciclo di gestione.
        La funzione ritorna anche il ristorante assegnato al cliente, il ristorante deve essere entro un raggio di 3km.
        Se il cliente non ha ristoranti nel raggio di 3km l'ordine non viene inserito nella coda.
        """
        risto_assegnato = self.assegna_ristorante(ordine_core, lista_ristoranti)
        ordine_core.ristorante = risto_assegnato
        if risto_assegnato is None:
            return None
        self.coda_pancia.append(ordine_core)
        return risto_assegnato
    
    #Valore "sentinella" usato nella matrice dei costi al posto delle coppie non ammissibili (es. rider troppo in ritardo).
    #Deve essere molto più grande di qualunque costo reale così l'algoritmo di ottimizzazione le eviterà sempre, se possibile.
    costo_non_ammissibile = 1e6

    def genera_candidati(self, flotta_attiva_ora):
        """
        Crea la matrice dei costi di tutte le coppie (ordine, rider) per il ciclo corrente.
        Ritorna:
        - ordini_riga: lista di ordini, una per riga della matrice
        - rider_colonna: lista di rider, uno per colonna della matrice
        - matrice_costi: matrice numpy (righe=ordini, colonne=rider) con il costo di ogni coppia
          (costo_non_ammissibile per le coppie non valide)
        - dettagli: dizionario {(numero_ordine, rider_id): (risto, tempo_tot, ora_inizio)} per recuperare
          i dati delle coppie ammissibili al momento della conferma
        """
        #ordini ancora in coda e rider attivi nell'attuale ciclo di gestione, servono per creare la matrice
        ordini_riga = list(self.coda_pancia)
        rider_colonna = list(flotta_attiva_ora.values())

        n_ordini = len(ordini_riga)
        n_rider = len(rider_colonna)
        #Creo la matrice dei costi e la riempio subito con il valore sentinella "non ammissibile", 
        #così di default nessuna coppia (ordine, rider) è valida verrà sovrascritta successivamente solo per quelle ammissibili
        matrice_costi = np.full((n_ordini, n_rider), self.costo_non_ammissibile)
        #Dizionario dove salvo i dettagli (ristorante, tempo totale, ora inizio) di ogni coppia ammissibile
        dettagli = {}

        for i, ordine in enumerate(ordini_riga):
            risto = ordine.ristorante
            t_cucina = risto.ricevi_ordine(ordine, self)
            for j, rider in enumerate(rider_colonna):
                #Calcolo i parametri di una coppia con la funzione top_rider, se la coppia non è ammissibile ritorna None
                esito = self.top_rider(ordine, risto, rider, t_cucina)
                if esito is None:
                    continue
                costo = esito[0]
                tempo_tot = esito[1]
                ora_inizio = esito[2]
                #sovrascrivo il costo sentinella con il costo reale calcolato per questa coppia
                matrice_costi[i, j] = costo
                #Costruisco la chiave del dizionario e ci associo i dettagli della coppia in questione che serviranno se più avanti la coppia verrà confermata
                chiave = (ordine.numero_ordine, rider.rider_id)
                valore = (risto, tempo_tot, ora_inizio)
                dettagli[chiave] = valore

        return ordini_riga, rider_colonna, matrice_costi, dettagli
    
    def assegna_rider_ordine(self, ordini_riga, rider_colonna, matrice_costi, dettagli):
        """
        Affida gli ordini ai rider risolvendo il problema di assegnamento a costo minimo globale
        (algoritmo ungherese, scipy.optimize.linear_sum_assignment) invece di procedere greedy
        dalla coppia più economica. In questo modo, tra tutte le combinazioni possibili di coppie
        (ordine, rider) del ciclo corrente, si sceglie quella che minimizza la somma totale dei costi,
        non semplicemente la prima coppia più economica trovata.
        """
        ordini_assegnati = set()
        risolti = []

        if matrice_costi.size == 0:
            return risolti, ordini_assegnati
        #righe_idx e colonne_idx sono gli indici delle coppie (ordine, rider) scelte dall'algoritmo
        #attraverso linear_sum_assignment trovo il modo più economico ed efficiente di accoppiare gli elementi di due gruppi diversi
        righe_idx, colonne_idx = linear_sum_assignment(matrice_costi)
        #riunisco i valori in coppie (riga, colonna) con zip, per poterli scorrere nel ciclo
        for i, j in zip(righe_idx, colonne_idx):
            #Se il costo è ancora quello "sentinella" vuol dire che quella coppia non era ammissibile e quindi va scartata
            if matrice_costi[i, j] >= self.costo_non_ammissibile:
                continue

            ordine = ordini_riga[i]
            rider = rider_colonna[j]
            #estraggo i 3 elementi dalla lista dettagli a seconda della coppia in questione
            risto, tempo_tot, ora_inizio = dettagli[(ordine.numero_ordine, rider.rider_id)]
            #Ricalcolo al volo i risultati perché ristorante e rider sono condivisi tra ordini e nel frattempo potrebbero essere cambiati
            risto.entro_raggio(ordine)
            rider.tempo_arrivo_ristorante(risto)
            rider.ordine_a_carico(ordine, tempo_tot, ora_inizio)
            dati_delivery = self.delivery_processamento(ordine, rider, risto)
            risolti.append({
                "ordine": ordine, "evaso": True,
                "rider": rider, "risto": risto, "dati": dati_delivery
            })
            ordini_assegnati.add(ordine.numero_ordine)
        return risolti, ordini_assegnati
    
    def gestisci_non_assegnati(self, ordini_assegnati, tempo_attuale, soglia_attesa_minuti):
        """Chi non ha trovato un rider resta in coda, se non ha superato la soglia temporale di 50 minuti, sennò viene dato per perso"""
        risolti = []
        ancora_in_coda = []
    
        for ordine in self.coda_pancia:
            if ordine.numero_ordine in ordini_assegnati:
                continue
            attesa_minuti = (tempo_attuale - ordine.ora_generata) * 60
            if attesa_minuti >= soglia_attesa_minuti:
                risolti.append({"ordine": ordine, "evaso": False})
            else:
                ancora_in_coda.append(ordine)
        self.coda_pancia = ancora_in_coda
        return risolti
    
    def elabora_coda_pancia(self, tempo_attuale, flotta_totale, soglia_attesa_minuti):
        """
        Ricontrolla, ad ogni ciclo di gestione, tutti gli ordini in coda e li assegna con un'ottimizzazione globale:
        1. Calcola il costo di ogni coppia (ordine, rider) ammissibile e costruisce la matrice dei costi
        2. Risolve il problema di assegnamento a costo minimo (algoritmo ungherese) su tutte le coppie del ciclo corrente,
           scegliendo la combinazione che minimizza la somma totale dei costi (non la prima coppia più economica trovata)
        3. Gli ordini che restano senza rider aspettano il prossimo ciclo, sempre se non hanno superato la soglia di attesa
        4. Ritorna la lista degli ordini "risolti" in questo ciclo (assegnati o no).
        """
        if not self.coda_pancia:
            return []
    
        flotta_attiva_ora = self.turni_flotta(tempo_attuale, flotta_totale)
        ordini_riga, rider_colonna, matrice_costi, dettagli = self.genera_candidati(flotta_attiva_ora)
        risolti, ordini_assegnati = self.assegna_rider_ordine(ordini_riga, rider_colonna, matrice_costi, dettagli)
        risolti += self.gestisci_non_assegnati(ordini_assegnati, tempo_attuale, soglia_attesa_minuti)
    
        return risolti

    def turni_flotta(self, ora, flotta_totale):
        turni_attivi = []
        if 8.00 <= ora < 12.00: 
            turni_attivi.append(1)
        if 12.00 <= ora < 14.30: 
            turni_attivi.append(2)
        if 14.30 <= ora < 18.30:
            turni_attivi.append(3)
        if 18.30 <= ora < 24.00: 
            turni_attivi.append(4)
        if len(turni_attivi) == 0: 
            turni_attivi.append(5)
        #memorizzo turni effettivamente attivi in giornata
        self.turni_operativi.update(turni_attivi)
        flotta_attiva_ora = {}
        #Controllo uno a uno i rider nel dizionario per identificare quali sono a lavoro all'ora dell'ordine. 
        #Creo una lista di rider attivi a quel preciso orario.
        for nome, rider_obj in flotta_totale.items():
            turni_del_rider = rider_obj.turni  
            for turno in turni_attivi:
                if turno in turni_del_rider:
                    flotta_attiva_ora[nome] = rider_obj
                    break      
        return flotta_attiva_ora

    def calcolo_paga_rider(self, ordine_core, flotta_totale):
        """
        Calcolo il costo totale della flotta che l'azienda deve sostenere per pagare i suoi rider. Per il calcolo tengo conto
        anche degli indennizzi per il lavoro durante festività.
        """
        ore_tot_flotta = 0.0
        # Calcola le ore iterando sui rider della flotta
        for membro in flotta_totale.values():
            for turno in membro.turni:
                if turno in self.turni_operativi:
                    ore_tot_flotta += DURATA_TURNI.get(turno, 0)
        paga_base = self.paga_oraria * ore_tot_flotta      
        #Inserisco l'indennizzo per il lavoro durante le festività
        moltiplicatore = 1.0
        if ordine_core.controllo_festivo(self):
            moltiplicatore = 1.10 
        self.paga_finale = paga_base * moltiplicatore
        return self.paga_finale
    
    def delivery_processamento(self, ordine_core, rider_core, risto_core):
        """Calcolo i ricavi, costi e utili per ogni singola spedizione. Ritorno un dizionario con i dati finanziari dell'ordine"""
        ricavo = ordine_core.gtv_ordine * self.take_rate
        bonus_notturno_ordine = 0.0
        #Indennizzo relativo al lavoro notturno
        if 23.00 <= ordine_core.ora_generata or ordine_core.ora_generata < 6.00:
            bonus_notturno_ordine = self.paga_oraria * 0.10
            self.bonus_notturni_totali += bonus_notturno_ordine

        self.n_consegne += 1
        self.ricavo_totale += ricavo
        #Indennizzo relativo ai km percorsi
        distanza_ordine = rider_core.d_rider_risto + risto_core.d_risto_cliente
        ind_km = distanza_ordine * 0.06
        self.km_totali += distanza_ordine
        self.indennizzo_km += ind_km

        return {
            "ordine numero": ordine_core.numero_ordine,
            "gtv ordine": ordine_core.gtv_ordine,
            "ricavo ordine": ricavo,
        }
    
    def chiusura_giornata(self):
        self.costi_totali = self.paga_finale + self.bonus_notturni_totali + self.indennizzo_km
        self.profitto_totale = self.ricavo_totale - self.costi_totali
        return {
            "consegne totali": self.n_consegne,
            "ricavo totale giornata": self.ricavo_totale,
            "costo totale giornaliero flotta": self.costi_totali,
            "profitto giornaliero": self.profitto_totale 
        }

class simulazione:
    def __init__(self, numero_ordini_desiderati, gtv_medio=25.00):
        self.numero_ordini = numero_ordini_desiderati
        self.gtv_medio=gtv_medio
        self.ordini_giornalieri = []

    def genera_ordini_giornalieri(self):
        """Attraverso questa funzione vado a generare il numero desiderato di ordini in un giorno, ossia 36 secondo i miei calcoli, pescando la tipologia
        di ordine dalla lista PROFILO_CLIENTI"""
        tipologie_clienti = list(PROFILI_CLIENTI.keys()) 
        fasce_orarie = [
            (0.0, 8.0, 1.0),    
            (8.0, 12.0, 1.0),  
            (12.0, 14.30, 2.0),  
            (14.30, 18.30, 1.0),  
            (18.30, 22.0, 3.0), 
            (22.0, 24.0, 2.0)
        ]
        pesi = [f[2] for f in fasce_orarie]
        
        for i in range(self.numero_ordini):
            fascia_scelta = random.choices(fasce_orarie, weights=pesi, k=1)[0]
            ora_casuale = random.uniform(fascia_scelta[0], fascia_scelta[1]) 
            tipo_scelto = random.choice(tipologie_clienti)
            nuovo_ordine = ordine.genera_ordine_da_profilo(i+1, tipo_scelto, ora_casuale, self.gtv_medio)
            nuovo_ordine.lat_cliente = random.gauss(nuovo_ordine.lat_cliente, 0.005)
            nuovo_ordine.lon_cliente = random.gauss(nuovo_ordine.lon_cliente, 0.005)
            self.ordini_giornalieri.append(nuovo_ordine)
        self.ordini_giornalieri.sort(key=lambda x: x.ora_generata)
        for indice, o in enumerate(self.ordini_giornalieri):
            o.numero_ordine = indice + 1
        return self.ordini_giornalieri
    