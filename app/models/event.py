from sqlmodel import SQLModel, Field #importo la libreria di Python che unisce SQLAlchemy e Pydantic
from datetime import datetime  #è il tipo per rappresentare date e orari nel JSON

class Event(SQLModel, table=True): #creo la classe che rappresenterà poi la tabella nel database
                                    #table = true dice a SQLModel che è una vera tabella da creare
    id: int = Field(default=None, primary_key=True) #identifico l'evento con l'id, ed è la chiave primaria della tabella
    title: str
    description: str
    date: datetime
    location: str
