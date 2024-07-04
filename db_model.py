from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root:nuova_password@localhost:3306/ecommerce_db')
Session = sessionmaker(bind=engine)
session = Session()


class Cliente(Base):
    __tablename__ = 'cliente'
    ClienteID = Column(Integer, primary_key=True)
    Nome = Column(String)
    Cognome = Column(String)
    Email = Column(String, unique=True)
    Indirizzo = Column(String)
    Telefono = Column(String)

    ordine = relationship("Ordine", back_populates="cliente", cascade="all, delete-orphan")
    recensione = relationship("Recensione", back_populates="cliente", cascade="all, delete-orphan")


class Prodotto(Base):
    __tablename__ = 'prodotto'
    ProdottoID = Column(Integer, primary_key=True)
    Nome = Column(String)
    Descrizione = Column(String)
    Prezzo = Column(Float)
    Quantita = Column(Integer)
    CategoriaID = Column(Integer, ForeignKey('categoria.CategoriaID'))
    FornitoreID = Column(Integer, ForeignKey('fornitore.FornitoreID'))

    categoria = relationship("Categoria", back_populates="prodotti")
    fornitore = relationship("Fornitore", back_populates="prodotti")
    recensione = relationship("Recensione", back_populates="prodotto", cascade="all, delete-orphan")
    ordine_prodotto = relationship("OrdineProdotto", back_populates="prodotto")
    inventario = relationship("Inventario", back_populates= "prodotto")


class Ordine(Base):
    __tablename__ = 'ordine'
    OrdineID = Column(Integer, primary_key=True)
    ClienteID = Column(Integer, ForeignKey('cliente.ClienteID'))
    Data = Column(DateTime)
    Totale = Column(Float)
    SpedizioneID = Column(Integer, ForeignKey('spedizione.SpedizioneID'))
    PagamentoID = Column(Integer, ForeignKey('pagamento.PagamentoID'))

    ordine_prodotto = relationship("OrdineProdotto", back_populates="ordine", cascade="all, delete-orphan")
    cliente = relationship("Cliente", back_populates="ordine")
    spedizione = relationship("Spedizione", back_populates="ordine",uselist=False)
    pagamento = relationship("Pagamento", back_populates="ordine",uselist=False)

class Spedizione(Base):
    __tablename__ = 'spedizione'
    SpedizioneID = Column(Integer, primary_key=True)
    MetodoSpedizione = Column(String)
    DataSpedizione = Column(DateTime)
    DataConsegnaPrevista = Column(DateTime)
    Stato = Column(String)

    ordine = relationship("Ordine", back_populates="spedizione")


class Recensione(Base):
    __tablename__ = 'recensione'
    RecensioneID = Column(Integer, primary_key=True)
    ClienteID = Column(Integer, ForeignKey('cliente.ClienteID'))
    ProdottoID = Column(Integer, ForeignKey('prodotto.ProdottoID'))
    Punteggio = Column(Integer)
    Commento = Column(String)

    cliente = relationship("Cliente", back_populates="recensione")
    prodotto = relationship("Prodotto", back_populates="recensione")


class Fornitore(Base):
    __tablename__ = 'fornitore'
    FornitoreID = Column(Integer, primary_key=True)
    Nome = Column(String)
    Contatto = Column(String)
    Indirizzo = Column(String)

    prodotti = relationship("Prodotto", back_populates="fornitore")


class Categoria(Base):
    __tablename__ = 'categoria'
    CategoriaID = Column(Integer, primary_key=True)
    Nome = Column(String)

    prodotti = relationship("Prodotto", back_populates="categoria")


class Inventario(Base):
    __tablename__ = 'inventario'
    InventarioID = Column(Integer, primary_key=True)
    ProdottoID = Column(Integer, ForeignKey('prodotto.ProdottoID'))
    Quantita = Column(Integer)
    DataAggiornamento = Column(DateTime)

    prodotto = relationship("Prodotto", back_populates="inventario")


class Pagamento(Base):
    __tablename__ = 'pagamento'
    PagamentoID = Column(Integer, primary_key=True)
    MetodoPagamento = Column(String)
    DataPagamento = Column(DateTime)
    Importo = Column(Float)

    ordine = relationship("Ordine", back_populates="pagamento")

class OrdineProdotto(Base):
    __tablename__ = 'ordine_prodotto'
    OrdineID = Column(Integer, ForeignKey('ordine.OrdineID'), primary_key=True)
    ProdottoID = Column(Integer, ForeignKey('prodotto.ProdottoID'), primary_key=True)
    Quantita = Column(Integer)

    ordine = relationship("Ordine", back_populates="ordine_prodotto")
    prodotto = relationship("Prodotto", back_populates="ordine_prodotto")


Base.metadata.create_all(engine)
