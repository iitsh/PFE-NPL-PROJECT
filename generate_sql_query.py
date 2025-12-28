from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate  
from langchain_core.output_parsers import StrOutputParser  


def generate_sql_query(natural_language_query):  
    llm = ChatOpenAI(api_key="YOUR_API_KEY", model_name="gpt-3.5-turbo")  
 
    template = """  
    Translate the following natural language query into an SQL query for a PostgreSQL database.  
    In the database , there are 6 tables:
        1st:consultations , with 5 columns : consultationid , patientid , medecinid ,dateconsultation et description
        2nd:factures , with 5 columns :factureid , patientid , montant , dateemission ,payee
        3rd:medecins , with 6 columns:medecinid , nom , prenom , specialite , telephone , email
        4th:medications , with 7 columns:medicationid , traitementid , nommedicament ,dosage ,frequence ,datedebut ,datefin
        5th:patients , with 9 columns:patientid ,nom ,prenom , datedenaissance ,sexe ,adresse , telephone ,email , dateenregistrement 
        6ht:traitements, with 6 columns:traitementid ,consultationid ,nomtraitement ,description ,datedebut ,datefin 
        (nad you should not confuse first name and last name, you should search in both columns and know who is first name and who is last name)
        (Masculin = M and Feminin = F) 
    Natural Language Query: "{natural_language_query}"  
    SQL Query: 
    """  
 
    prompt = ChatPromptTemplate.from_template(template)  
 
    chain = prompt | llm | StrOutputParser()  
 
    query = chain.invoke({  
        "natural_language_query":natural_language_query
    })  
    return query

