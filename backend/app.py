from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from werkzeug.security import  generate_password_hash,check_password_hash
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
 role=data.get('role','user')
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
 password_hash = generate_password_hash(password)
 query="INSERT INTO utilisateur (nom, email, password,role) " \
 "VALUES (%s,%s,%s,%s)"
 values=(nom, email, password_hash,role)
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
#login
@app.route('/api/login', methods=['POST'])
def login():
    data=request.get_json() 
    if not data:
        return jsonify({
            "error": "Aucune donnée reçue"
        }), 400

    email=data.get('email') 
    password=data.get('password') 

    if not email or not password:
       return jsonify({
          "error":"Email et mot de passe obligatoires"
       }),400
    
    conn=get_db_connection()
    if conn is None:
      return jsonify({
        "error":"Erreur de connexion  à la base de données" 
      }),500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute(""" SELECT id, nom, email, password,role
      FROM utilisateur WHERE email=%s""",(email,))
    user=cursor.fetchone()

    cursor.close()
    conn.close()

    #l'orsque l'utilisateur n'existe pas
    if user is None:
       return jsonify({
          "error":"Email ou mot de passe incorrect"
       }),401

   #vérification du mot de passe
    if not check_password_hash(
      user['password'], password
    ):
       return jsonify({
          "error":"Email ou mot de passe incorrect"
       }),401
   #ne jamais renvoyer le hash
    return jsonify({
       "id": user['id'],
       "nom": user['nom'],
       "email":user['email'],
       "role":user['role']
    }),200
@app.route('/api/messages', methods=['POST'])
def envoyer_message():
   
   try:
      data=request.get_json()
      nom=data.get('nom')
      email=data.get('email')
      message= data.get('message')

      if not nom or not email or not message:
         return jsonify({
            "message":"Tous les champs sont obligatoires"
         }), 400
      conn=get_db_connection()
      cursor=conn.cursor()
      sqlquery=""" INSERT INTO messages (nom, email, message) values (%s,%s,%s)"""
      cursor.execute(sqlquery,(nom, email, message))
      conn.commit()
      cursor.close()
      conn.close()
      return jsonify({
         "message":"Message envoyé à l'administrateur "
      });201
   except Exception as e:
      print("Erreur:", e)
      return jsonify({
         "message":"Erreur serveur"
      }), 500
#recuperation des messages
@app.route('/api/messages', methods=['GET'])
def get_messages():

    try:
        conn=get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nom, email, message, date_message
            FROM messages
            ORDER BY date_message DESC
        """)

        messages = cursor.fetchall()

        cursor.close()
        conn.close()

        result = []

        for msg in messages:

            result.append({
                "id": msg[0],
                "nom": msg[1],
                "email": msg[2],
                "message": msg[3],
                "date_message": str(msg[4])
            })

        return jsonify(result), 200

    except Exception as e:

        print("Erreur :", e)

        return jsonify({
            "message": "Erreur serveur"
        }), 500
@app.route('/api/messages/<int:id>', methods=['DELETE'])
def supprimer_message(id):
   try:
    conn = get_db_connection()
    cursor = conn.cursor()
    sqlquery="""DELETE FROM messages where id=%s"""
    cursor.execute(sqlquery,(id,))
    conn.commit()
    conn.close()
    return jsonify({
       "message":"message supprimé avec succès"
    }),200
   except Exception as e:
     print("Erreur: ",e)
     return jsonify({
        "message":"erreur lors de la suppression"
     }),500

if __name__ == '__main__':
    app.run(debug=True,port=5000)