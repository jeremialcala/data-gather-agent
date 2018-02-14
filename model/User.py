# -*- coding: utf-8 -*-
from datetime import datetime
from pymongo.errors import DuplicateKeyError, WriteError
from utils import get_mongodb, log
import json
from bson.objectid import ObjectId
from flask_login import UserMixin


def rollback_user(rollback):
	try:
		log("Starting Rollback " + str(rollback))
		db = get_mongodb()
		for record in rollback['email']:
			oid = ObjectId(record['_id'])
			log(record['_id'])
			db.users_email.delete_one({"_id": ObjectId(record['_id'])})
		
		if rollback['password'] != "":
			db.users_password.delete_one({"_id": ObjectId(rollback['password'])})
		if rollback['user'] is not "":
			db.users.delete_one({"_id": ObjectId(rollback['user'])})
			
		result = {"rc": 200, "MSG": "Rollback Successful!"}
	except WriteError as e:
		log(e.args[0], "ERROR")
		result = {"rc": 500, "MSG": "something went wrong! " + e.args[0]}
	log(result)
	return result
	

def user(id):
	db = get_mongodb()
	new_user = User(str(id), "", "", "", "", "", "")
	oid = "5a834c77538a991dd0e26233"
	log("String " + oid)
	r_oid = ObjectId(oid)
	cursor = db.users.find_one({"_id": r_oid})
	log(type(cursor))
	if type(cursor) is dict:
		new_user.id = str(cursor['_id'])
		new_user.user_id = cursor['user_id']
		new_user.first_name = cursor['first_name']
		new_user.last_name = cursor['last_name']
		new_user.status = cursor['status']
	
	return new_user

	
class User(UserMixin):
		
	def __init__(self, id, user_id, first_name, last_name, dob, gender, status="Active",
	             status_date=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')):
		self.id = id
		self.user_id = user_id
		self.first_name = first_name
		self.last_name = last_name
		self.dob = dob
		self.gender = gender
		self.status = status
		self.status_date = status_date
		
	def to_json(self):
		return json.dumps(self.__dict__, sort_keys=False, indent=4, separators=(',', ': '))
			
	def save_user(self):
		db = get_mongodb()
		user_json = json.loads(self.to_json())
		try:
			cursor = db.users.insert_one(user_json)
			log("User Seved: " + str(cursor.inserted_id))
			result = {"rc": 200, "MSG": "User information saved!", "_id": str(cursor.inserted_id)}
		except DuplicateKeyError as DK:
			log(DK.args[0], "ERROR")
			result = {"rc": 409, "MSG": "Duplicate Key Error " + str(DK.args[0]).split("key:")[1]}
		
		return result
	
	def get_user_info(self):
		db = get_mongodb()
		cursor = db.users.find_one({"user_id": self.user_id})
		if type(cursor) is dict:
			self.id = str(cursor['_id'])
			self.user_id = cursor['user_id']
			self.first_name = cursor['first_name']
			self.last_name = cursor['last_name']
			self.gender = cursor['gender']
			self.dob = cursor['dob']
			self.status = cursor['status']
			self.status_date  = cursor['status_date']
		return self
	
	
class Password:
	def __init__(self, user_id,  password, fail_att=0, creation_date=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
	             status="Active", status_date=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')):
		self.user_id = user_id
		self.password = password
		self.fail_att = fail_att
		self.creation_date = creation_date
		self.status = status
		self.status_date = status_date
		
	def to_json(self):
		return json.dumps(self.__dict__, sort_keys=False, indent=4, separators=(',', ': '))
	
	def save_password(self):
		db = get_mongodb()
		password_json = json.loads(self.to_json())
		try:
			cursor = db.users_password.insert_one(password_json)
			log("Password Seved: " + str(cursor.inserted_id))
			result = {"rc": 200, "MSG": "User information saved!", "_id": str(cursor.inserted_id)}
		except DuplicateKeyError as DK:
			log(DK.args[0], "ERROR")
			result = {"rc": 409, "MSG": "Duplicate Key Error " + str(DK.args[0]).split("key:")[1]}
		return result

	def get_user_info(self):
		db = get_mongodb()
		cursor = db.users_password.find_one({"user_id":  self.user_id})
		if type(cursor) is dict:
			cursor.pop('_id')
			result = {"rc": 200, "MSG": "User information found!", "password": cursor}
		else:
			result = {"rc": 404, "MSG": "User not found!"}
		return result
	
	def update_element(self):
		db = get_mongodb()
		user_json = json.loads(self.to_json())
		update_json = {}
		for elem in user_json:
			if user_json[elem] is not "":
				update_json[elem] = user_json[elem]
		update_json.pop("user_id")
		db.users_password.update({'user_id': self.user_id},
		                         {'$set': update_json})
		

class Email:
	def __init__(self, user_id, address, creation_date=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
	             status="Active", status_date=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')):
		self.user_id = user_id
		self.address = address
		self.creation_date = creation_date
		self.status = status
		self.status_date = status_date
		
	def to_json(self):
		return json.dumps(self.__dict__, sort_keys=False, indent=4, separators=(',', ': '))
	
	def save_email(self):
		db = get_mongodb()
		email_json = json.loads(self.to_json())
		try:
			cursor = db.users_email.insert_one(email_json)
			log("Email Seved: " + str(cursor.inserted_id))
			result = {"rc": 200, "MSG": "User information saved!", "_id": str(cursor.inserted_id)}
		except DuplicateKeyError as DK:
			log(DK.args[0], "ERROR")
			result = {"rc": 409, "MSG": "Duplicate Key Error " + str(DK.args[0]).split("key:")[1]}
			
		return result
	
	def get_user_info(self):
		db = get_mongodb()
		cursor = db.users_email.find_one({"address": self.address})
		if type(cursor) is dict:
			cursor.pop('_id')
			result = {"rc": 200, "MSG": "User information found!", "email": cursor}
		else:
			result = {"rc": 404, "MSG": "User not found!"}
		return result

