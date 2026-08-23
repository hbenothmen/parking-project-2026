from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
app=Flask(__name__)
CORS(app)
#connexion a MySQL
def get_db_connection():
    try:
        connection=mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='parkingdb'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
#recuperer les utilisateurs
@app.route('/api/users',methods=['GET'])
def get_users():
   conn=get_db_connection()
   if conn is None:
      return jsonify({
         "error":"Impossible de se connexter  à la base de données"
        }), 500
   cursor=conn.cursor(dictionary=True)
   cursor.execute("SELECT nom, email FROM utilisateur")
   users=cursor.fetchall()
   cursor.close()
   conn.close()
   return jsonify(users), 200

#ajout d'un utiliateur
@app.route('/api/users', methods=['POST'])
def add_user():
 data=request.get_json()
 if not data:
    return jsonify({
       "error":"Aucune donnée reçue"
       
    }),400
 
 nom=data.get('nom')
 email=data.get('email')
 password=data.get('password')
 #verification du nom
 if not nom :
    return jsonify({
       "error":"le nom est obligatoire"}), 400
 
#verification de l'email
 if not email:
    return jsonify({
       "error":"L'email est obligatoire"
    }), 400
 
#verification le mot de passe
 if not password:
    return jsonify({
       "error":"Le mot de passe est obligatoire"
    }),400
 
 conn=get_db_connection()
 if conn is None:
    return ({
       "error":"Impossible de connecter à la base de données"
        }), 500 
    
 cursor=conn.cursor(dictionary=True)
 query="INSERT INTO utilisateur (nom, email, password) " \
 "VALUES (%s,%s,%s)"
 values=(nom, email, password)
 try:

   cursor.execute(query,values)
   conn.commit()
 #recuperer le nouvel utilisateur
 # pour l'envoyer au Frontend
   new_user_id=cursor.lastrowid #id du nouvel utilisateur
   cursor.execute("SELECT * FROM utilisateur WHERE id=%s",(new_user_id,))
   new_user=cursor.fetchone() 
   cursor.close()  
   conn.close() 
   return jsonify(new_user), 201 
 except Error as e:
    conn.rollback()
    cursor.close() 
    conn.close()
    print(f"Erreur MySQL : {e}")   
    return jsonify({
       "error":"Erreur lors de l'ajout de l'utilisateur"
    }),500 
      
if __name__ == '__main__':
    app.run(debug=True,port=5000)