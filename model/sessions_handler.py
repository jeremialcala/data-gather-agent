# -*- coding: utf-8 -*-
from utils import log, get_mongodb


# {"_id": "", "User-Agent": "", "email": "", "status": "", "creation-date": ""}

def get_session(session_id):
	try:
		db = get_mongodb()
		log("Trying to get info for this SessionId: " + session_id, "SESSIONS")
		session = db.sessions.find_one({"session-id": session_id})
		log(str(session), "SESSIONS")
		
	except Exception as e:
		log(str(e.args), 'ERROR')
		
	return session