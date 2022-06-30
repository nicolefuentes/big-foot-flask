from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   

class Skeptic:
    db = "python_exam_schema"
    def __init__(self,data):
        self.user_skeptic_id = data['user_skeptic_id']
        self.sighting_skeptic_id = data['sighting_skeptic_id']
    
    @classmethod
    def skeptic(cls,data):
        query = "INSERT INTO skeptics (user_skeptic_id, sighting_skeptic_id) VALUES (%(user_skeptic_id)s,%(sighting_skeptic_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def not_a_skeptic(cls,data):
        query = "DELETE FROM skeptics WHERE user_skeptic_id = %(user_skeptic_id)s AND sighting_skeptic_id = %(sighting_skeptic_id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_by_sketptics(cls,data):
        query = "SELECT skeptics.* FROM sightings LEFT JOIN skeptics ON sightings.id = skeptics.sighting_skeptic_id LEFT JOIN users as users ON users.id = skeptics.user_skeptic_id WHERE skeptics.user_skeptic_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        likes = []
        for like in results:
            likes.append(cls(like))
        return likes