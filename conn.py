import psycopg2
def create_connection():  
        conn = psycopg2.connect(  
            dbname="YOUR_DB_NAME",  
            user="YOUR_USER_NAME",  
            password="YOUR_PASSWORD",  
            host="localhost",  
            port="5455"  
        )



            
        