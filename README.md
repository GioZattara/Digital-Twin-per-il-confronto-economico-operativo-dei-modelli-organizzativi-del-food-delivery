Digital Twin per il confronto economico-operativo dei modelli organizzativi del food delivery  
License: MIT  
Tesi di laurea triennale in ingegneria industriale Università degli Studi di Trento-Dipartimento di ingegneria industriale  
Studente: Giovanni Zattara, mat. 247772  
Relatore: Prof. Francesco Pilati  
Anno Accademico: 2025-2026  

Descrizione progetto:  
Questo repository contiene il software di simulazione sviluppato per la mia tesi di laurea. Il progetto confronta, in termini quantitativi, due modelli organizzativi
alternativi adottati dalle piattaforme di food delivery per la gestione dei propri ordini:  
- Modello Gig Economy: i rider sono collaboratori economy e occasionali, retribuiti a cottimo e la loro assegnazione dell'ordine avviene tramite un algoritmo di dispatching
  a ping sequenziale basato sulla distanza e sul punteggio reputazionale.  
- Modello Factory: i rider sono dipendenti subordinati, retribuiti su base oraria con turni fissi pianificati e l'assegnazione degli ordini avviene tramite l'algoritmo ungherese che risolve un problema di ottimizzazione a costo minimo globale.  
Entrambi i modelli condividono le stesse condizioni al contorno (meteo, domanda, geografia e giornata) generate con seed casuale fisso. Il confronto tra i due modelli avviene
mediante 5 KPI (ricavo, costi, profitto, tasso di evasione degli ordini e tempo medio di consegna) su 6 scenari operativi che incrociano fascia oraria, festività e condizioni
meteo e che sono calibrati sull'area centrale di Milano.  
Per la descrizione completa della strutturazione del digital twin e dei suoi risultati si rimanda al testo della tesi di laurea.

Requisiti per eseguire la simulazione:
- Python 3.10 o superiore  
- librerie utilizzate: numpy e scipy nelle versioni descritte nel file di testo allegato  
Lo script genera la domanda giornaliera (36 ordini con seed fissato a 42) eseguendo la comparazione dei due modelli su 6 scenari e stampando i 5 KPI per ogni scenario.
