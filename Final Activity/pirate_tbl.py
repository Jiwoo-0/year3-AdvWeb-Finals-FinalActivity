from sql_connect import connecttoMysql

class Pirates:
    def __init__(self,data):
        self.id=data['id']
        self.pirate_name=data['pirate_name']
        self.pirate_img=data['pirate_img']
        self.pirate_chest=data['pirate_chest']
        self.pirate_phrase=data['pirate_phrase']
        self.pirate_position=data['pirate_position']
        self.pirate_hasPegleg=data['pirate_hasPegleg']
        self.pirate_hasEyepatch=data['pirate_hasEyepatch']
        self.pirate_hasHackhand=data['pirate_hasHackhand']
        self.date_created=data['date_created']
        self.date_updated=data['date_updated']
        
    @classmethod
    def getall_pirates(cls):
        query="SELECT * FROM piratecrew.pirate_tbl;"
        # list
        results=connecttoMysql("piratecrew").query_db(query)
        pirates=[]
        for pirate in results:
            pirates.append(cls(pirate))
        return pirates

    @classmethod
    def new_pirate(cls,data):
        query="INSERT INTO pirate_tbl (pirate_name,pirate_img,pirate_chest,pirate_phrase,pirate_position,pirate_hasPegleg,pirate_hasEyepatch,pirate_hasHackhand) VALUES(%(pirate_name)s,%(pirate_img)s,%(pirate_chest)s,%(pirate_phrase)s,%(pirate_position)s,%(pirate_hasPegleg)s,%(pirate_hasEyepatch)s,%(pirate_hasHackhand)s)"
        results=connecttoMysql("piratecrew").query_db(query,data)
        return results
    
    @classmethod
    def update_pirate(cls,data):
        query="UPDATE pirate_tbl SET pirate_name=%(pirate_name)s,pirate_img=%(pirate_img)s,pirate_chest=%(pirate_chest)s,pirate_phrase=%(pirate_phrase)s,pirate_position=%(pirate_position)s,pirate_hasPegleg=%(pirate_hasPegleg)s,pirate_hasEyepatch=%(pirate_hasEyepatch)s,pirate_hasHackhand=%(pirate_hasHackhand)s WHERE id=%(id)s"
        results=connecttoMysql("piratecrew").query_db(query,data)
        # if len(results)<1:
        #     return False
        return results
    
    @classmethod
    def getOne(cls,data):
        query="SELECT * FROM pirate_tbl WHERE id=%(id)s;"
        result=connecttoMysql("piratecrew").query_db(query,data)
        # if len(result)<1:
        #     return False
        return cls(result[0])
    
    @classmethod
    def delete_pirate(cls,data):
        query="DELETE FROM pirate_tbl WHERE id=%(id)s"
        results=connecttoMysql("piratecrew").query_db(query,data)
        # if len(results)<1:
        #     return False
        return results
    
    