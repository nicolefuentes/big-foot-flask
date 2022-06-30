from pydoc import describe
from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Sighting:
    db = "python_exam_schema"
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date = data['date']
        self.sasquatch_num = data['sasquatch_num']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_reported_id = data['user_reported_id']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO sightings (location, description, date, sasquatch_num, created_at, updated_at, user_reported_id) VALUES (%(location)s,%(description)s,%(date)s,%(sasquatch_num)s,NOW(),NOW(),%(user_reported_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings LEFT JOIN users ON users.id = sightings.user_reported_id;"
        results = connectToMySQL(cls.db).query_db(query)
        sightings = []
        for row in results:
            sightings.append( cls(row))
        return sightings

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM sightings WHERE id = %(sighting_id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_by_id_except(cls,data):
        query = "SELECT * FROM sightings WHERE id != %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        users = []
        for row in results:
            users.append( cls(row))
        return users
    
    @classmethod
    def update(cls,data):
        query = "UPDATE sightings SET location=%(location)s,description=%(description)s,date=%(date)s,sasquatch_num=%(sasquatch_num)s,updated_at=NOW() WHERE id = %(sighting_id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_user_who_added(cls,data):
        query = "SELECT users.first_name, users.last_name, sightings.* FROM sightings LEFT JOIN users ON users.id = sightings.user_reported_id WHERE sightings.id = %(sighting_id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        added_by = []
        for row in result:
            added_by.append(cls(row))
        return added_by

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM sightings WHERE id = %(sighting_id)s;"
        return connectToMySQL(cls.db).query_db(query,data)