from db_model import session, Cliente, Prodotto, Ordine, Recensione, Fornitore, Categoria, Inventario, Spedizione,Pagamento, OrdineProdotto
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime


def crea_cliente(nome, cognome, email, indirizzo, telefono):
    if not session.query(Cliente).filter_by(Email=email).first():
        cliente = Cliente(Nome=nome, Cognome=cognome, Email=email, Indirizzo=indirizzo, Telefono=telefono)
        try:
            session.add(cliente)
            session.commit()
        except IntegrityError:
            session.rollback()
            print(f"Email {email} già esistente.")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Errore durante la creazione del cliente: {str(e)}")
    else:
        print(f"Cliente con email {email} già esistente.")


def leggi_clienti():
    return session.query(Cliente).all()


def aggiorna_cliente(cliente_id, nome=None, cognome=None, email=None, indirizzo=None, telefono=None):
    try:
        cliente = session.query(Cliente).filter_by(ClienteID=cliente_id).first()
        if cliente:
            if nome:
                cliente.Nome = nome
            if cognome:
                cliente.Cognome = cognome
            if email:
                cliente.Email = email
            if indirizzo:
                cliente.Indirizzo = indirizzo
            if telefono:
                cliente.Telefono = telefono
            session.commit()
        else:
            print(f"Cliente con ID {cliente_id} non trovato.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Errore durante l'aggiornamento del cliente {cliente_id}: {str(e)}")


def cancella_cliente(cliente_id):
    try:
        cliente = session.query(Cliente).filter_by(ClienteID=cliente_id).first()
        if cliente:
            session.delete(cliente)
            session.commit()
        else:
            print(f"Cliente con ID {cliente_id} non trovato.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Errore durante la cancellazione del cliente {cliente_id}: {str(e)}")


def crea_prodotto(nome, descrizione, prezzo, quantita, categoria_id, fornitore_id):
    if not session.query(Prodotto).filter_by(Nome=nome).first():
        prodotto = Prodotto(Nome=nome, Descrizione=descrizione, Prezzo=prezzo, Quantita=quantita,
                            CategoriaID=categoria_id,
                            FornitoreID=fornitore_id)
        try:
            session.add(prodotto)
            session.commit()
        except IntegrityError:
            session.rollback()
            print(f"Errore nella creazione del prodotto {nome}.")
    else:
        print(f"Prodotto con nome {nome} già esistente.")


def leggi_prodotti():
    return session.query(Prodotto).all()


def aggiorna_prodotto(prodotto_id, nome=None, descrizione=None, prezzo=None, quantita=None, categoria_id=None,
                      fornitore_id=None):
    prodotto = session.query(Prodotto).filter_by(ProdottoID=prodotto_id).first()
    if prodotto:
        if nome:
            prodotto.Nome = nome
        if descrizione:
            prodotto.Descrizione = descrizione
        if prezzo:
            prodotto.Prezzo = prezzo
        if quantita:
            prodotto.Quantita = quantita
        if categoria_id:
            prodotto.CategoriaID = categoria_id
        if fornitore_id:
            prodotto.FornitoreID = fornitore_id
        session.commit()
    else:
        print(f"Prodotto con ID {prodotto_id} non trovato.")


def cancella_prodotto(prodotto_id):
    prodotto = session.query(Prodotto).filter_by(ProdottoID=prodotto_id).first()
    if prodotto:
        session.delete(prodotto)
        session.commit()
    else:
        print(f"Prodotto con ID {prodotto_id} non trovato.")


def crea_ordine(cliente_id, data, totale, spedizione_id, pagamento_id):
    cliente = session.query(Cliente).filter_by(ClienteID=cliente_id).first()
    spedizione = session.query(Spedizione).filter_by(SpedizioneID=spedizione_id).first()
    pagamento = session.query(Pagamento).filter_by(PagamentoID=pagamento_id).first()

    if cliente and spedizione and pagamento:
        ordine = Ordine(ClienteID=cliente_id, Data=datetime.strptime(data, '%Y-%m-%d'), Totale=totale,
                        SpedizioneID=spedizione_id, PagamentoID=pagamento_id)
        try:
            session.add(ordine)
            session.commit()

            prodotti = session.query(Prodotto).all()
            for prodotto in prodotti:
                ordine_prodotto = OrdineProdotto(OrdineID=ordine.OrdineID, ProdottoID=prodotto.ProdottoID, Quantita=1)
                ordine.ordine_prodotto.append(ordine_prodotto)

            session.commit()
        except IntegrityError:
            session.rollback()
            print(f"Errore nella creazione dell'ordine.")
    else:
        if not cliente:
            print("Errore: Cliente non esistente.")
        if not spedizione:
            print("Errore: Spedizione non esistente.")
        if not pagamento:
            print("Errore: Pagamento non esistente.")


def leggi_ordini():
    return session.query(Ordine).all()

def aggiorna_ordine(ordine_id, cliente_id=None, data=None, totale=None, spedizione_id=None, pagamento_id=None, prodotti_da_aggiungere=None):
    ordine = session.query(Ordine).filter_by(OrdineID=ordine_id).first()
    if ordine:
        try:
            if cliente_id:
                ordine.ClienteID = cliente_id
            if data:
                ordine.Data = datetime.strptime(data, '%Y-%m-%d')
            if totale:
                ordine.Totale = totale
            if spedizione_id:
                ordine.SpedizioneID = spedizione_id
            if pagamento_id:
                ordine.PagamentoID = pagamento_id
            if prodotti_da_aggiungere:
                session.query(OrdineProdotto).filter_by(OrdineID=ordine_id).delete()

                for prodotto_id, quantita in prodotti_da_aggiungere.items():
                    ordine_prodotto = OrdineProdotto(OrdineID=ordine_id, ProdottoID=prodotto_id, Quantita=quantita)
                    session.add(ordine_prodotto)

            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Errore durante l'aggiornamento dell'ordine {ordine_id}: {str(e)}")
    else:
        print(f"Ordine con ID {ordine_id} non trovato.")



def cancella_ordine(ordine_id):
    ordine = session.query(Ordine).filter_by(OrdineID=ordine_id).first()
    if ordine:
        session.delete(ordine)
        session.commit()
    else:
        print(f"Ordine con ID {ordine_id} non trovato.")


def crea_spedizione(ordine_id, metodo_spedizione, data_spedizione, data_consegna_prevista, stato):
    spedizione = Spedizione(OrdineID=ordine_id, MetodoSpedizione=metodo_spedizione,
                            DataSpedizione=datetime.strptime(data_spedizione, '%Y-%m-%d'),
                            DataConsegnaPrevista=datetime.strptime(data_consegna_prevista, '%Y-%m-%d'), Stato=stato)
    try:
        session.add(spedizione)
        session.commit()
    except IntegrityError:
        session.rollback()
        print(f"Errore nella creazione della spedizione.")


def leggi_spedizioni():
    return session.query(Spedizione).all()


def aggiorna_spedizione(spedizione_id, ordine_id=None, metodo_spedizione=None, data_spedizione=None,
                        data_consegna_prevista=None, stato=None):
    spedizione = session.query(Spedizione).filter_by(SpedizioneID=spedizione_id).first()
    if spedizione:
        if ordine_id:
            spedizione.OrdineID = ordine_id
        if metodo_spedizione:
            spedizione.MetodoSpedizione = metodo_spedizione
        if data_spedizione:
            spedizione.DataSpedizione = datetime.strptime(data_spedizione, '%Y-%m-%d')
        if data_consegna_prevista:
            spedizione.DataConsegnaPrevista = datetime.strptime(data_consegna_prevista, '%Y-%m-%d')
        if stato:
            spedizione.Stato = stato
        session.commit()
    else:
        print(f"Spedizione con ID {spedizione_id} non trovata.")


def cancella_spedizione(spedizione_id):
    spedizione = session.query(Spedizione).filter_by(SpedizioneID=spedizione_id).first()
    if spedizione:
        session.delete(spedizione)
        session.commit()
    else:
        print(f"Spedizione con ID {spedizione_id} non trovata.")


def leggi_dettagli_ordini():
    return session.query(
        Ordine.OrdineID,
        Ordine.Data,
        Ordine.Totale,
        Cliente.Nome,
        Cliente.Cognome,
        Prodotto.Nome.label('NomeProdotto'),
        OrdineProdotto.Quantita
    ).join(Cliente, Ordine.ClienteID == Cliente.ClienteID
           ).join(OrdineProdotto, Ordine.OrdineID == OrdineProdotto.OrdineID
                  ).join(Prodotto, OrdineProdotto.ProdottoID == Prodotto.ProdottoID
                         ).all()


if __name__ == "__main__":
    crea_cliente("Mario", "Rossi", "mario.rossi@gmail.com", "Via Roma 10, Milano", "+39 3331234567")
    clienti = leggi_clienti()
    for cliente in clienti:
        print(cliente.Nome, cliente.Cognome, cliente.Email)
    aggiorna_cliente(4, telefono="+39 3339876543")
    cancella_cliente(6)

    crea_prodotto("Balsamo", "Balsamo per capelli", 10.0, 50, 1, 1)
    prodotti = leggi_prodotti()
    for prodotto in prodotti:
        print(prodotto.Nome, prodotto.Descrizione, prodotto.Prezzo)

    crea_ordine(2, "2024-06-28", 100.0, 1, 1)
    ordini = leggi_ordini()
    for ordine in ordini:
        print(ordine.Data, ordine.Totale)

    dettagli_ordini = leggi_dettagli_ordini()
    for dettaglio in dettagli_ordini:
        print(dettaglio.OrdineID, dettaglio.Data, dettaglio.Totale, dettaglio.Nome, dettaglio.Cognome,
              dettaglio.NomeProdotto, dettaglio.Quantita)
