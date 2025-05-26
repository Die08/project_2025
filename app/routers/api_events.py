from fastapi import APIRouter #serve per definire un gruppo di rotte
from sqlmodel import select   #serve per costruire le query SQL
from app.models.event import Event #importo il modello Event, per dire a FastAPI e SQLModel che tipo di dati sto trattando
from app.data.db import SessionDep #importo la sessione del database da db.py


"""Ora creo un gruppo di rotte che inizieranno tutte con http://localhost:8000/events"""
"""I due parametri sono prefix -> (tutte le rotte definite avranno events/ davanti)
e tags -> (appare nella documentazione Swagger come gruppo events)."""
router = APIRouter(prefix="/events", tags=["events"])


"""per indicare la pagina principale (root) del gruppo di rotte uso:"""
"""Quindi ora avrò http://localhost:8000/events/"""
"""Perchè prefix "/events" + route "/" = "/events/"""
"""Ma fastAPI la leggerà comunque http://localhost:8000/events"""
"""response_model=list[Event] serve per dire a fastAPI che questa rotta restituirà una lista 
di oggetti Event, che devono essere validati e convertiti in JSON secondo il modello Event"""
@router.get("/", response_model=list[Event])
def get_events(session: SessionDep): #Definisce una funzione Python che sarà eseguita quando qualcuno fa una richiesta GET /events
                                     #session è la variabile che rappresenta la connessione attiva al database
                                     #in pratica session viene creata da SessionDep,
                                     #che è un istanza della funzione get_session() che si trova nel db.py
                                     #get_session() è la funzione che crea una connessione al database
                                     #ma si trova nel db.py per organizzazione di codice.
    events = session.exec(select(Event)).all() #costruisce una query del tipo SELECT * FROM event;
    return events                    #restituisce la lista di events




