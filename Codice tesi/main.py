import random
from datetime import datetime
import gig_economy, factory

#L'orario dell'ordine viene pescato rispettando il peso di proabilità delle fasce orarie
FASCE_PRANZO = [
    (12.0, 14.30, 2.0),
    (14.30, 18.30, 1.0)
]
FASCE_CENA = [
    (18.30, 22.0, 3.0),
    (22.0, 24.0, 2.0)
]

def pesca_orario_pesato(fasce_finestra):
    "Sceglie un orario casuale dentro una finestra suddivisa in sotto-fasce pesate"
    #Crea una lista per i pesi
    pesi_probabilita = []
    for fascia in fasce_finestra:
        peso = fascia[2]
        pesi_probabilita.append(peso)
    #Sceglie casualmente una fascia pesata
    risultato_scelta = random.choices(fasce_finestra, weights=pesi_probabilita, k=1)
    fascia_selezionata = risultato_scelta[0]
    orario_inizio = fascia_selezionata[0]
    orario_fine = fascia_selezionata[1]
    #estraggo un orario compreso tra orario_inizio e orario_fine
    orario_definitivo = random.uniform(orario_inizio, orario_fine)
    return orario_definitivo

def genera_flotta_factory(config_turni):
    "Crea la flotta di rider per il modello factory a partire da una lista di turni, che può essere costum o no"
    flotta_custom = {}
    lat_base = 45.46615562924043
    lon_base = 9.187673822088886
    for i, turni in enumerate(config_turni):
        nome = f"rider_custom_{i+1}"
        flotta_custom[nome] = {
            "lat_base": lat_base,
            "lon_base": lon_base,
            "v_media": 15,
            "turni": turni
        }
    return flotta_custom

def esegui_comparazione(nome_scenario, data_simulazione, fascia_oraria="tutto", meteo_brutto=False, config_turni_fac=None):
    """
    Inizialmente genera un set di ordini (36 di default), applicando le variabili dello scenario richiesto come il meteo, la fascia oraria (pranzo, cena o tutto il giorno) 
    e ordinandoli cronologicamente. Successivamente, avvia la simulazione delle consegne per entrambi i modelli gestendo le assegnazioni dei ristoranti e dei rider 
    agli ordini e tenendo conto anche dei costi relativi agli ordini persi. Infine, restituisce i risultati raggruppati in un dizionario, mostrando per ciascun modello 
    il numero di ordini evasi rispetto a quelli totali, i ricavi, i costi, il profitto netto e il dettaglio di completamento di ogni singola consegna.
    """
    #parametri fissi della simulazione
    n_ordini = 36
    gtv_medio = 25.00
    take_rate = 0.278
    #oltre quest'attesa in cucina, sia in gig_economy sia in factory, l'ordine viene considerato perso
    soglia_attesa_minuti = 50
    #genero gli ordini e condizioni meteo sia per la factory sia per la gig_economy
    random.seed(42)
    motore_ordini_gig = gig_economy.simulazione(n_ordini, gtv_medio=gtv_medio)
    lista_ordini_gig = motore_ordini_gig.genera_ordini_giornalieri()

    motore_ordini_fac = factory.simulazione(n_ordini, gtv_medio=gtv_medio)
    lista_ordini_fac = motore_ordini_fac.genera_ordini_giornalieri()

    def applica_scenario(lista_ordini):
        for o in lista_ordini:
            #guarda com'è il meteo per l'ordine
            o.brutto_tempo = meteo_brutto
            #concentra gli ordini nell'orario giusto, pescando l'orario secondo le sotto-fasce pesate
            if fascia_oraria == "pranzo":
                o.ora_generata = pesca_orario_pesato(FASCE_PRANZO)
            elif fascia_oraria == "cena":
                o.ora_generata = pesca_orario_pesato(FASCE_CENA)
        #mette in fila gli ordini dal primo all'ultimo
        lista_ordini.sort(key=lambda x: x.ora_generata)
        #riallineo numero_ordine al nuovo ordine cronologico, altrimenti resterebbe legato all'orario pre-scenario
        #e non corrisponderebbe più alla posizione nella lista ordinata
        for indice, o in enumerate(lista_ordini):
            o.numero_ordine = indice + 1

    applica_scenario(lista_ordini_gig)
    applica_scenario(lista_ordini_fac)

    #GIG ECONOMY
    azienda_gig = gig_economy.azienda(take_rate=take_rate)
    #Creiamo una lista di nomi dei ristoranti
    ristoranti_gig = []
    for nome in gig_economy.PROFILI_RISTORANTI.keys():
        nuovo_ristorante = gig_economy.ristorante(nome)
        ristoranti_gig.append(nuovo_ristorante)
    #Creiamo una lista di nome per i rider
    rider_gig = []
    for nome in gig_economy.PROFILI_RIDER.keys():
        nuovo_rider = gig_economy.rider(nome, data_simulazione)
        rider_gig.append(nuovo_rider)

    ordini_evasi_gig = 0
    dettaglio_ordini_gig = []
    tempi_consegna_gig = []

    for ord_corrente in lista_ordini_gig:
        evaso = False
        random.shuffle(ristoranti_gig)
        risto_assegnato = None
        for risto in ristoranti_gig:
        #Troviamo il ristorante da assegnare al cliente testando se è dentro i 3km. 
        #Inoltre in caso negativo non manda in crash tutto ma salta semplicemente quel ristorante e passa a valutare il prossimo ristorante casuale.
            try:
                risto.entro_raggio(ord_corrente)
                risto_assegnato = risto
                break
            except ValueError:
                continue

        if risto_assegnato:
            rider_disponibili = []
            for r in rider_gig:
                #controlliamo se il rider ha già finito la sua consegna, se la risposta è positiva lo aggiungiamo alla lista
                if r.ora_termine_consegna <= ord_corrente.ora_generata:
                    rider_disponibili.append(r)
            if rider_disponibili:
                #Attraverso il dispatching a ping sequenziale propongo l'ordine al rider migliore
                rider_assegnato = gig_economy.ping_sequenziale(risto_assegnato, rider_disponibili)

                if rider_assegnato is not None:
                    rider_assegnato.order = ord_corrente
                    t_arrivo = rider_assegnato.tempo_arrivo_ristorante(risto_assegnato)
                    t_cucina, ordine_perso_per_coda = risto_assegnato.ricevi_ordine(
                        ord_corrente, rider_assegnato,
                        t_arrivo_rider=t_arrivo,
                        soglia_attesa_minuti=soglia_attesa_minuti
                    )

                    if ordine_perso_per_coda:
                        #il ristorante è troppo in coda: il rider aspetta fino alla soglia massima e poi rinuncia.
                        #Resta comunque impegnato per quel tempo, ma la consegna non avviene e non c'è paga
                        rider_assegnato.abbandona_ordine_per_coda(risto_assegnato, t_arrivo, soglia_attesa_minuti)
                    else:
                        risto_assegnato.ordine_completo()
                        paga_rider = rider_assegnato.consegna_completa(risto_assegnato, t_cucina, t_arrivo)

                        azienda_gig.delivery_processamento(ord_corrente, paga_rider)
                        ordini_evasi_gig += 1
                        evaso = True
                        #tempo di consegna in minuti: dall'ora di generazione dell'ordine all'ora di termine consegna del rider
                        tempo_consegna_minuti = (rider_assegnato.ora_termine_consegna - ord_corrente.ora_generata) * 60
                        tempi_consegna_gig.append(tempo_consegna_minuti)

        dettaglio_ordini_gig.append({
            "numero": ord_corrente.numero_ordine,
            "ora": ord_corrente.ora_generata,
            "gtv": ord_corrente.gtv_ordine,
            "evaso": evaso
        })

    #Estraggo i dati della gig_economy
    ricavi_gig = getattr(azienda_gig, 'ricavo_totale', 0.0)
    costi_gig = getattr(azienda_gig, 'costi_totali', 0.0)
    profitto_gig = getattr(azienda_gig, 'profitto_totale', 0.0)
    #tengo conto anche degli ordini inevasi e dei raltivi ordini di mancanza
    ordini_mancati_gig = len(lista_ordini_gig) - ordini_evasi_gig
    costo_mancanza_gig = ordini_mancati_gig * 2.90
    costi_gig += costo_mancanza_gig
    profitto_gig -= costo_mancanza_gig
    #tempo medio di consegna (calcolato solo sugli ordini evasi) e tasso di evasione degli ordini
    if len(tempi_consegna_gig) > 0:
        somma_tempi = sum(tempi_consegna_gig)
        numero_ordini_evasi = len(tempi_consegna_gig)
        tempo_medio_consegna_gig = somma_tempi / numero_ordini_evasi
    else:
        tempo_medio_consegna_gig = 0.0

    numero_ordini_totali = len(lista_ordini_gig)
    if numero_ordini_totali > 0:
        proporzione_evasi = ordini_evasi_gig / numero_ordini_totali
        tasso_evasione_gig = proporzione_evasi * 100
    else:
        tasso_evasione_gig = 0.0

    #FACTORY
    random.seed(42)
    azienda_fac = factory.azienda(giorno_consegna=data_simulazione, take_rate=take_rate)
    ristoranti_fac = []
    for nome in factory.PROFILI_RISTORANTI:
        ristorante = factory.ristorante(nome)
        ristoranti_fac.append(ristorante)
    #creo la mia flotta dei rider a seconda che abbiamo una flotta custom o la flotta base
    if config_turni_fac:
        profili_custom = genera_flotta_factory(config_turni_fac)
        flotta_rider_fac = {}
        for nome, prof in profili_custom.items():
            #creo il rider usando il file factory
            nuovo_rider = factory.rider(nome, profilo_custom=prof)
            flotta_rider_fac[nome] = nuovo_rider
    else:
        flotta_rider_fac = {}
        for nome in factory.PROFILI_RIDER:
            nuovo_rider = factory.rider(nome)
            flotta_rider_fac[nome] = nuovo_rider

    ordini_evasi_fac = 0
    dettaglio_ordini_fac = []
    tempi_consegna_fac = []
    #SIMULAZIONE A CICLI DI GESTIONE DI 1 MINUTI
    #Gli ordini non vengono assegnati istantaneamente quando vengono generati, ma entrano prima in coda e poi questi, ogni
    #minuto di tempo simulato, vengono ricontrollati tutti e viene deciso quali ordini assegnare a un rider
    #e quali invece tenere ancora in pancia in attesa di una futura assegnazione, in caso ad esempio che nessun rider è conveniente momentaneamente per quell'ordine
    passo_minuti = 1
    passo_ore = passo_minuti / 60.0
    idx_prossimo_ordine = 0
    n_ordini_fac = len(lista_ordini_fac)
    tempo_simulato = 0.0
    tempo_limite = 24.0 + (soglia_attesa_minuti / 60.0)  # margine per smaltire la coda a fine giornata

    while (idx_prossimo_ordine < n_ordini_fac or azienda_fac.coda_pancia) and tempo_simulato <= tempo_limite:
        #Faccio entrare in pancia tutti gli ordini generati entro questo ciclo e gli abbino casualmente un ristorante 
        while idx_prossimo_ordine < n_ordini_fac and lista_ordini_fac[idx_prossimo_ordine].ora_generata < tempo_simulato + passo_ore:
            ord_nuovo = lista_ordini_fac[idx_prossimo_ordine]
            risto_assegnato = azienda_fac.aggiungi_in_coda(ord_nuovo, ristoranti_fac)
            if risto_assegnato is None:
                dettaglio_ordini_fac.append({
                    "numero": ord_nuovo.numero_ordine,
                    "ora": ord_nuovo.ora_generata,
                    "gtv": ord_nuovo.gtv_ordine,
                    "evaso": False
                })
            idx_prossimo_ordine += 1
        #Ricontrollo la coda assegnando gli ordini che possono essere assegnati e scartando quelli che hanno aspettato troppo in coda
        risolti = azienda_fac.elabora_coda_pancia(
            tempo_attuale=tempo_simulato,
            flotta_totale=flotta_rider_fac,
            soglia_attesa_minuti=soglia_attesa_minuti
        )

        for esito in risolti:
            ord_corrente = esito["ordine"]
            if esito["evaso"]:
                ordini_evasi_fac += 1
                #tempo di consegna in minuti: dall'ora di generazione dell'ordine all'ora di termine consegna del rider
                tempo_consegna_minuti = (esito["rider"].ora_termine_consegna - ord_corrente.ora_generata) * 60
                tempi_consegna_fac.append(tempo_consegna_minuti)
            dettaglio_ordini_fac.append({
                "numero": ord_corrente.numero_ordine,
                "ora": ord_corrente.ora_generata,
                "gtv": ord_corrente.gtv_ordine,
                "evaso": esito["evaso"]
            })

        tempo_simulato += passo_ore
    #Ordino la tabella di output per numero di ordine
    dettaglio_ordini_fac.sort(key=lambda o: o["numero"])

    if lista_ordini_fac:
        azienda_fac.calcolo_paga_rider(lista_ordini_fac[0], flotta_rider_fac)
    #Elaboro i dati di fine giornata attraverso chiusura_giornata()
    report_fac = azienda_fac.chiusura_giornata()
    ricavi_fac = report_fac.get('ricavo totale giornata', 0.0)
    costi_fac = report_fac.get('costo totale giornaliero flotta', 0.0)
    profitto_fac = report_fac.get('profitto giornaliero', 0.0)
    ordini_mancati_fac = len(lista_ordini_fac) - ordini_evasi_fac
    costo_mancanza_fac = ordini_mancati_fac * 2.90
    costi_fac += costo_mancanza_fac
    profitto_fac -= costo_mancanza_fac
    #tempo medio di consegna (calcolato solo sugli ordini evasi) e tasso di evasione degli ordini
    if len(tempi_consegna_fac) > 0:
        somma_tempi_fac = sum(tempi_consegna_fac)
        numero_ordini_evasi_fac = len(tempi_consegna_fac)
        tempo_medio_consegna_fac = somma_tempi_fac / numero_ordini_evasi_fac
    else:
        tempo_medio_consegna_fac = 0.0

    numero_ordini_totali_fac = len(lista_ordini_fac)
    if numero_ordini_totali_fac > 0:
        rapporto_evasi_fac = ordini_evasi_fac / numero_ordini_totali_fac
        tasso_evasione_fac = rapporto_evasi_fac * 100
    else:
        asso_evasione_fac = 0.0
    #Mi ritorna il risulatato finale sia per la gig_economy, sia per la factory
    return {
        "scenario": nome_scenario,
        "gig": {
            "ordini_evasi": ordini_evasi_gig,
            "ordini_totali": len(lista_ordini_gig),
            "ricavi": ricavi_gig,
            "costi": costi_gig,
            "profitto": profitto_gig,
            "tempo_medio_consegna": tempo_medio_consegna_gig,
            "tasso_evasione": tasso_evasione_gig,
            "dettaglio": dettaglio_ordini_gig
        },
        "factory": {
            "ordini_evasi": ordini_evasi_fac,
            "ordini_totali": len(lista_ordini_fac),
            "ricavi": ricavi_fac,
            "costi": costi_fac,
            "profitto": profitto_fac,
            "tempo_medio_consegna": tempo_medio_consegna_fac,
            "tasso_evasione": tasso_evasione_fac,
            "dettaglio": dettaglio_ordini_fac
        }
    }

def formatta_ora(ora_decimale):
    """Converte un'ora decimale (es. 13.75) in formato HH:MM"""
    ore = int(ora_decimale) % 24
    minuti = int(round((ora_decimale % 1) * 60))
    if minuti == 60:
        minuti = 0
        ore = (ore + 1) % 24
    return f"{ore:02d}:{minuti:02d}"

def stampa_tabella_modello(nome_modello, dati):
    "Stampa la tabella riepilogativa più il dettaglio di ogni ordine per ogni modello simulativo e per ognuna delle due politiche aziendali."
    larghezza = 55
    print("-" * larghezza)
    print(f"  {nome_modello}")
    print("-" * larghezza)
    print(f"  Ordini evasi : {dati['ordini_evasi']} / {dati['ordini_totali']}")
    print(f"  Ricavi       : £ {dati['ricavi']:.2f}")
    print(f"  Costi        : £ {dati['costi']:.2f}")
    print(f"  Profitto     : £ {dati['profitto']:.2f}")
    print(f"  Tempo medio di consegna : {dati['tempo_medio_consegna']:.2f} min")
    print(f"  Tasso di evasione       : {dati['tasso_evasione']:.2f} %")
    print("-" * larghezza)
    print(f"  {'N.ORD':<6} | {'ORA':<6} | {'GTV (£)':<9} | EVASO")
    print("  " + "-" * (larghezza - 2))
    for o in dati["dettaglio"]:
        evaso_str = "SI" if o["evaso"] else "NO"
        print(f"  {o['numero']:<6} | {formatta_ora(o['ora']):<6} | {o['gtv']:<9.2f} | {evaso_str}")
    print("-" * larghezza + "\n")

#IMPOSTAZIONE DEGLI SCENARI
if __name__ == "__main__":
    #giorni di simulazione
    domenica_festiva = datetime(2026, 1, 6)    #Festivo (Epifania)
    martedi_lavorativo = datetime(2026, 11, 3)  #Lavorativo
    #flotta costum per la simulazione
    flotta_1 = [[4],[4], [4]]
    flotta_2 = [[2],[2],[2],[3],[3]]
    flotta_3 = [[5],[2],[2],[4],[4]]

    scenari = [
        #Scenario 1: Serata festiva e piovosa
        {
            "nome": "Sera Festivo Pioggia",
            "data": domenica_festiva,
            "fascia": "cena",
            "meteo": True,
            "turni_fac": flotta_1
        },
        #Scenario 2:Pranzo lavorativo e soleggiato
        {
            "nome": "Pranzo Lavorativo Sole",
            "data": martedi_lavorativo,
            "fascia": "pranzo",
            "meteo": False,
            "turni_fac": flotta_2
        },
        #Scenario 3: Giornata intera festiva e soleggiata
        {
            "nome": "Giorno Intero Festivo Sole",
            "data": domenica_festiva,
            "fascia": "tutto",
            "meteo": False,
            "turni_fac": flotta_3
        },
       #Scenario 4: Giornata intera festiva e soleggiata
       {
           "nome": "Giorno Intero Festivo Pioggia",
           "data": domenica_festiva,
           "fascia": "tutto",
           "meteo": True,
           "turni_fac": flotta_3
       },
        #Scenario 5: Giornata intera lavorativa e piovosa
        {
            "nome": "Giorno Intero Lavorativo Pioggia",
            "data": martedi_lavorativo,
            "fascia": "tutto",
            "meteo": True,
            "turni_fac": flotta_3
        },
        #Scenario 6: Giornata intera lavorativa e soleggiata
        {
            "nome": "Giorno Intero Lavorativo Sole",
            "data": martedi_lavorativo,
            "fascia": "tutto",
            "meteo": False,
            "turni_fac": flotta_3
        },
    ]

    for config in scenari:
        res = esegui_comparazione(
            nome_scenario=config["nome"],
            data_simulazione=config["data"],
            fascia_oraria=config["fascia"],
            meteo_brutto=config["meteo"],
            config_turni_fac=config["turni_fac"]
        )

        print("=" * 55)
        print(f" SCENARIO: {res['scenario']} ".center(55, "="))
        print("=" * 55)

        stampa_tabella_modello("GIG ECONOMY", res["gig"])
        stampa_tabella_modello("FACTORY", res["factory"])