import time
from functions import rfidExists, dbQuery, cycle


delay = 3


def callBack(code):
	if rfidExists(code) == False:
		responseAdd = raw_input("L\'RFID con codice "+ code + " non e\' presente, aggiungerlo? (y/n): ")
		if responseAdd == "n":
                        cbResult = {'delay':0, 'color':"red"}
                        return cbResult
		description=raw_input("Inserisci descrizione: ")
		try:
               		active=int(raw_input("Inserisci stato (0=non attivo, 1=attivo): "))
		except:
			active = 0				
		if not ((active == 0) or (active == 1)):
	 		active = 0  
       	        data=[code,active,description]
       	        query = dbQuery('INSERT INTO rfids(code,active,description) VALUES (?,?,?)', data)
       	        if query['rowcount'] == 0:
       	                print "ERRORE: Inserimento non riuscito."
       	        else:
       	                print "Inserimento riuscito."
       	        print "\nRiavvio scansione in "+str(delay)+" secondi ..."
       	        cbResult = {'delay':delay, 'color':"green"}
		return cbResult
	else:
		responseEdit = raw_input("Modificare RFID? (y/n): ")
		if responseEdit == "n":
			cbResult = {'delay':0, 'color':"red"}
			return cbResult
		elif responseEdit == "y" or responseEdit == "Y":
			response = raw_input("\n 1)Modifica stato attivazione \n 2)Modifica descrizione \n 3)Elimina RFID\n\n")
			if response == "1":
				active = 0
				responseActive = raw_input("\nRFID attivo? (y/n): ")
				if responseActive == "y":
					active = 1
				query = dbQuery('UPDATE rfids SET ACTIVE='+str(active)+' WHERE CODE=?',[code])
				if query['rowcount'] == 0:
					print "ERRORE"
					cbResult = {'delay':0, 'color':'red'}
					return cbResult
				else:
					print "Modifica riuscita."
				cbResult = {'delay':delay, 'color':'green'}
				return cbResult
			elif response == "2":
				responseDescription = raw_input("\n Inserire la nuova descrizione: \n\n")
				print responseDescription
				query = dbQuery('UPDATE rfids SET DESCRIPTION=\"'+str(responseDescription)+'\" WHERE CODE=?',[code])
				if query['rowcount'] == 0:
					print "ERRORE"
					cbResult = {'delay':0,'color':'red'}
					return cbResult
				else:
					print "Modifica riuscita"
				cbResult = {'delay':delay,'color':'green'}
				return cbResult
			elif response == "3":
				prompt = raw_input("Procedere con l'eliminazione? (y/n): ")
       	         		if prompt == "n":
       	         	        	print "Eliminazione annullata."
       	         	        	cbResult = {'delay':0, 'color':"red"}
       	         	        	return cbResult
       	         		query = dbQuery('DELETE FROM rfids WHERE CODE=?', [code])
       	         		if query['rowcount'] == 0:
       	         	        	print "ERRORE: Eliminazione non riuscita."
       	         		else:
		                        print "ELiminazione riuscita."
       		        	print "\nRiavvio scansione in "+str(delay)+" secondi ..."
       	 	        	cbResult = {'delay':delay, 'color':"green"}
		               	return cbResult
			else:
				print "ERRORE: Selezione non valida"
		else:
			print "ERRORE: Selezione non valida"
			cbResult = {'delay':0, 'color':"red"}
                        return cbResult



print "Avviato script di gestione degli RFIDs ..."
cycle(callBack)


