# -*- coding: utf-8 -*-
from datetime import datetime
from model.User import rollback_user, User, Password, Email
from utils import log


def create_user(user_registration):
	try:
		msg = "User created"
		result = {"rc": 201, "MSG": msg, "alt-msg": []}
		new_user = User(**user_registration['user'])
		es = 0
		rollback = {"email": [], "password": "", "user": ""}
		
		for email in user_registration['email']:
			resp = Email(new_user.user_id, email['address']).save_email()
			if resp['rc'] == 200:
				rollback['email'].append({"_id": resp['_id']})
				log(email['address'] + " Save on user " + new_user.user_id)
				es += 1
			else:
				result['alt-msg'].append(resp['MSG'])
				log(resp['MSG'], "ERROR")
				
		if len(rollback['email']) is 0:
			return resp
		
		resp = Password(new_user.user_id, user_registration['password']).save_password()
		
		if resp['rc'] != 200:
			rollback_user(rollback)
			log(resp['MSG'])
			return resp
		rollback['password'] = resp["_id"]
		resp = new_user.save_user()
		rollback['user'] = resp["_id"]
		if resp['rc'] != 200:
			rollback_user(rollback)
			log(resp['MSG'])
			return resp
	
	except Exception as e:
		log(e.args[0], "ERROR")
		result = {"rc": 500, "MSG": "something went wrong! " + e.args[0]}
	
	return result


def verify_user(user_verification):
	log("Starting: " + str(user_verification), "verify_user")
	result = {"rc": 200, "MSG": "Process OK", "alt-msg": []}
	new_email = Email("", user_verification['email'])
	# log(new_email.to_json(), "verify_user")
	resp = new_email.get_user_info()
	# log(resp['rc'], "verify_user")
	if resp['rc'] != 200:
		return resp
	
	new_email = Email(**resp['email'])
	if not new_email.status.__eq__("Active"):
		result['rc'] = 401
		result['MSG'] = "Account Unauthorized"
		return resp
	
	new_password = Password(new_email.user_id, user_verification['password'])
	log(new_password.to_json(), "verify_user")
	resp = new_password.get_user_info()
	# log(resp, "verify_user")
	if resp['rc'] != 200:
		return resp
	
	new_password = Password(**resp['password'])
	fec_exp = datetime.utcnow() - datetime.strptime(new_password.creation_date, '%Y-%m-%d %H:%M:%S')
	
	if not new_password.status.__eq__("Active"):
		if new_password.status.__eq__("Locked"):
			result['rc'] = 423
			result['MSG'] = "Account Locked"
		elif new_password.status.__eq__("Expired"):
			result['rc'] = 202
			result['MSG'] = "Password Expired"
		else:
			result['rc'] = 401
			result['MSG'] = "Account Unauthorized"
	elif fec_exp.days > 179:
		bad_result = Password(new_email.user_id, "", "", "", "Expired",
		                      datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
		bad_result.update_element()
		result['rc'] = 202
		result['MSG'] = "Password Expired"
	elif new_password.password != user_verification['password']:
		bad_result = Password(new_email.user_id, "", new_password.fail_att + 1, "", "", "")
		result['rc'] = 401
		result['MSG'] = "Invalid Password"
		
		if new_password.fail_att >= 2:
			bad_result.status = "Locked"
			bad_result.status_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
			result['rc'] = 423
			result['MSG'] = "Account Locked"
		elif new_password.fail_att + 1 is 2:
			result['alt-msg'] = "Next fail attempt will disable your account"
			
		bad_result.update_element()
	elif new_password.fail_att >= 3:
		result['rc'] = 423
		result['MSG'] = "Account Locked"
	else:
		good_result = Password(new_email.user_id, "", 0, "", "", "")
		good_result.update_element()
		user = User("", new_email.user_id, "", "", "", "").get_user_info()
		result['user'] = user.to_json()

	
	return result
