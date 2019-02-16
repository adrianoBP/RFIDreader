import time
import datetime
import sys

from functions import dbQuery, cycle, logAccessOffline, rfidExists, logAccessNotRecognized

successDelay = 1.5
errorDelay = 5.0

def callBack(code):
	errorResult = {'delay':errorDelay, 'color':"red"}
	successResult = {'delay':successDelay, 'color':"green"}
	rfidExistsFlag = None
	try:
		rfidExistsFlag = rfidExists(code)
		if rfidExistsFlag:
			queryRfid = dbQuery('SELECT ID, ACTIVE FROM RFIDS WHERE CODE=?',[code])
			data = queryRfid['data'][0]
			queryInsertAccess = dbQuery('INSERT INTO ACCESSES(RFIDS_ID,RFIDACTIVE) VALUES (?,?)',data)
		else:
			print "Codice non presente nel DataBase. Riavvio lettura in " +str(errorDelay)+" secondi ..."
			if not logAccessNotRecognized(code):
				print "ERRORE CRITICO: accesso non salvato."
			return errorResult
	except:
#	raise sys.exc_info()[0]
		if	logAccessOffline(code):
			print "ERRORE database: salvataggio in locale avvenuto con successo ..."
		else:
			print "ERRORE CRITICO: salvataggio in locale non riuscito."
		return errorResult

	if queryInsertAccess['rowcount'] == 0:
		print "ERRORE: Inserimento accesso non riuscito."
		print "\nRiavvio lettura in "+str(errorDelay)+" secondi ..."
	else:
		print "Inserimento accesso riuscito."
		print "\nRiavvio lettura in "+str(successDelay)+" secondi ..."

	return successResult


print "Avviato script di inserimento accessi ..."
cycle(callBack)
