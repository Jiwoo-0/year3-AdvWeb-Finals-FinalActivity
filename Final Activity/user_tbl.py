from sql_connect import connecttoMysql

class Users:
    def __init__(self,data):
        self.id=data['id']
        self.user_firstname=data['user_firstname']
        self.user_lastname=data['user_lastname']
        self.user_email=data['user_email']
        self.user_password=data['user_password']
        self.date_created=data['date_created']
        self.date_updated=data['date_updated']
        
    @classmethod
    def getall_users(cls):
        query="SELECT * FROM piratecrew.user_tbl;"
        # list
        results=connecttoMysql("piratecrew").query_db(query)
        users=[]
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def new_user(cls,data):
        query="INSERT INTO user_tbl (user_firstname,user_lastname,user_email,user_password) VALUES(%(user_firstname)s,%(user_lastname)s,%(user_email)s,%(user_password)s)"
        results=connecttoMysql("piratecrew").query_db(query,data)
        return results
    
    @classmethod
    def update_user(cls,data):
        query="UPDATE user_tbl SET user_firstname=%(user_firstname)s,user_lastname=%(user_lastname)s,user_email=%(user_email)s,user_password=%(user_password)s WHERE id=%(id)s"
        results=connecttoMysql("piratecrew").query_db(query,data)
        # if len(results)<1:
        #     return False
        return results
    
    @classmethod
    def getOne(cls,data):
        query="SELECT * FROM user_tbl WHERE id=%(id)s;"
        result=connecttoMysql("piratecrew").query_db(query,data)
        # if len(result)<1:
        #     return False
        return cls(result[0])
    
    @classmethod
    def FindByEmail(cls,data):
        query="SELECT * FROM user_tbl WHERE user_email=%(user_email)s;"
        result=connecttoMysql("piratecrew").query_db(query,data)
        # if len(result)<1:
        #     return False
        return cls(result[0]) if result else None
    
    @classmethod
    def delete_user(cls,data):
        query="DELETE FROM user_tbl WHERE id=%(id)s"
        results=connecttoMysql("piratecrew").query_db(query,data)
        # if len(results)<1:
        #     return False
        return results
    
    