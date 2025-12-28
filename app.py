from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from lexi_db.execute import execute_query
from lexi_db.generate_sql_query import generate_sql_query
from lexi_db.execute import resultat_ai_version


app = Flask(__name__)




@app.route("/whatsapp", methods=['POST'])
def lexi_db_app():
    query = request.form.get('Body').lower().strip()
    twilio_response = MessagingResponse()
    reply_message = twilio_response.message()
    sql_query = generate_sql_query(query)  
    results = execute_query(sql_query) 
    final_result = resultat_ai_version(results, sql_query)
    reply_message.body(final_result)
    return str(twilio_response)
    


if __name__ == "__main__":
    app.run(debug=True)