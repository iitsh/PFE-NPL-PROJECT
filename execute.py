from langchain_openai import ChatOpenAI
import psycopg2
from langchain_core.prompts import ChatPromptTemplate  
from langchain_core.output_parsers import StrOutputParser 


def create_connection(): 
    try: 
        conn = psycopg2.connect(  
            dbname="YOUR_DB_NAME",  
            user="YOUR_USER_NAME",  
            password="YOUR_PASSWORD",  
            host="localhost",  
            port="5455"  
        )
    except Exception as e:
        print(e)
    return conn
        

def execute_query(sql):  
    try:
        conn = create_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        conn.commit()
        return result
    except Exception as e:
        return [] 
    finally:
        if conn:
            conn.close()

def resultat_ai_version(result,query):
    llm = ChatOpenAI(api_key="YOUR_API_KEY", model_name="gpt-3.5-turbo")  
 
    template = """  
    Give me the results of the execution of this query: {query} using OPENAI's version without showing the responses like '[()]', and I don't want the answer formula to be like that: "the response retrieved" or something like that. Rephrase the answer so as not to feel that the answer is coming from the database, don't use the query returned to not feel like the response is from the database, and don't use the meaning of 'query', give me the results in french and without talking about "database" or "data"nd respond in french and not english.
    result: {result}
    """  
 
    prompt = ChatPromptTemplate.from_template(template)  
 
    chain = prompt | llm | StrOutputParser()  
 
    response = chain.invoke({  
        "query": query,
        "result" : result
    })  
    return response
        
