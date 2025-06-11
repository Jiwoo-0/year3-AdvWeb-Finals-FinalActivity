from mysqlconnection import connecttoMysql

class Customer:
    def __init__(self,data):
        self.id=data['id']
        self.customer_lastname=data['customer_lastname']
        self.customer_firstname=data['customer_firstname']
        self.customer_email=data['customer_email']
        self.customer_age=data['customer_age']
        self.created_at=data['date_created']
        self.updated_at=data['date_updated']
        
    @classmethod
    def getall_customers(cls):
        query="SELECT * FROM market_db.customer_tbl;"
        # list
        results=connecttoMysql("market_db").query_db(query)
        customers=[]
        for customer in results:
            customers.append(cls(customer))
        return customers
    
    @classmethod
    def new_customer(cls,data):
        query="INSERT INTO customer_tbl (customer_lastname,customer_firstname,customer_age,customer_email) VALUES(%(customer_lastname)s,%(customer_firstname)s,%(customer_age)s,%(customer_email)s)"
        results=connecttoMysql("market_db").query_db(query,data)
        return results
    
    @classmethod
    def update_customer(cls,data):
        query="UPDATE customer_tbl SET customer_lastname=%(customer_lastname)s,customer_firstname=%(customer_firstname)s,customer_age=%(customer_age)s,customer_email=%(customer_email)s WHERE id=%(id)s"
        results=connecttoMysql("market_db").query_db(query,data)
        # if len(results)<1:
        #     return False
        return results
    
    @classmethod
    def getOne(cls,data):
        query="SELECT * FROM customer_tbl WHERE id=%(id)s;"
        result=connecttoMysql("market_db").query_db(query,data)
        # if len(result)<1:
        #     return False
        return cls(result[0])
    
    @classmethod
    def delete_customer(cls,data):
        query="DELETE FROM customer_tbl WHERE id=%(id)s"
        results=connecttoMysql("market_db").query_db(query,data)
        # if len(results)<1:
        #     return False
        return results