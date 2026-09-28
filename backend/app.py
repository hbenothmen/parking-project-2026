from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from werkzeug.security import  generate_password_hash,check_password_hash
import os
from dotenv import load_dotenv
load_dotenv()
print("HOST =", os.getenv("DB_HOST"))
print("PORT =", os.getenv("DB_PORT"))
print("USER =", os.getenv("DB_USER"))
print("DATABASE =", os.getenv("DB_NAME"))
app=Flask(__name__)
app.json.ensure_ascii = False
CORS(app)

#connexion a MySQL
def get_db_connection():
    try:
      #   connection=mysql.connector.connect(
      #       host='localhost',
      #       user='root',
      #       password='',
      #       database='parkingdb'
      #   )
          connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT', 3306))
          )
          return connection
    except Error as e:
      print(f"Error connecting to MySQL: {e}")
      return None
connection = get_db_connection()

if connection:
    print("✅ Connexion à Aiven réussie !")
    connection.close()
else:
    print("❌ Connexion à Aiven échouée !") 

##### Récuprer les utilisateurs ######
@app.route('/api/users',methods=['GET'])
def get_users():
   conn=get_db_connection()
   if conn is None:
      return jsonify({
         "error":"Impossible de se connexter  à la base de données"
        }), 500
   cursor=conn.cursor(dictionary=True)
   cursor.execute("SELECT id,nom, email FROM utilisateur ")
   users=cursor.fetchall()
   cursor.close()
   conn.close()
   return jsonify(users), 200

###### Ajout d'un utiliateur ########

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

 ####Supprimer utilisateur ######
@app.route('/api/users/<int:id>', methods=['DELETE']) 
def supprimer_user(id):
   try:
      conn=get_db_connection()
      if conn is None:
         return jsonify({
            "error":"Erreur lors de la connection a la base de données"
         }),500
      cursor=conn.cursor()
      sqlquery="""DELETE FROM utilisateur where id=%s"""
      cursor.execute(sqlquery,(id,))
      if cursor.rowcount==0:
         cursor.close()
         conn.close()
         return jsonify({
            "error":"Utilisateur introuvable"
         }),400
      conn.commit()
      cursor.close()
      conn.close()
      return jsonify({
         "utilisateur supprimé avec succés "
      }),200
   except Exception as e:
     print ("ERREUR:",e)
     return jsonify({
        "Erreur lors de la suppression de l'utilisateur"
     }),500
    
   

###### login #######
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
      }),201
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

@app.route('/')
def home():
    return jsonify({
        "message": "Backend Flask fonctionne !"
    })
@app.route("/api/parkings", methods=['GET'])
def get_parkings():
   connection=get_db_connection()
   if connection is None:
    return jsonify ({
       "erreur":"Erreur de connexion à la base de données"
    }),500
   cursor=connection.cursor(dictionary=True)

   try:
    cursor.execute("""SELECT id,nom, adresse, nombre_places,
                   places_disponibles, prix_heure, statut, date_creation
            FROM parking
            ORDER BY id DESC
        """)
    parkings=cursor.fetchall()
    return jsonify(parkings),200
   except Error as e:
    print("Erreur d'afficher les parkings:",e)
    return jsonify({"error": str(e)}),500
   finally:
    cursor.close()
    connection.close()
@app.route("/api/parkings", methods=['POST'])
def add_parking():

    data = request.get_json()

    nom = data.get("nom")
    adresse = data.get("adresse")
    nombre_places = data.get("nombre_places")
    prix_heure = data.get("prix_heure")

    if not nom or not adresse or nombre_places is None or prix_heure is None:
        return jsonify({
            "error": "Tous les champs sont obligatoires"
        }), 400

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "error": "Erreur au moment de la connexion"
        }), 500

    cursor = connection.cursor(dictionary=True)

    # Au départ, toutes les places sont disponibles
    places_disponibles = nombre_places

    try:

        cursor.execute("""
            INSERT INTO parking
            (nom, adresse, nombre_places, places_disponibles, prix_heure, statut)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            nom,
            adresse,
            nombre_places,
            places_disponibles,
            prix_heure,
            "disponible"
        ))

        connection.commit()

        parking_id = cursor.lastrowid

        cursor.execute("""
            SELECT id, nom, adresse, nombre_places,
                   places_disponibles, prix_heure,
                   statut, date_creation
            FROM parking
            WHERE id = %s
        """, (parking_id,))

        parking = cursor.fetchone()

        return jsonify(parking), 201

    except Error as e:

        connection.rollback()

        print("Erreur de sauvegarde du parking :", e)

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()


@app.route("/api/parkings/<int:id>", methods=["PUT"])
def modifier_parking(id):

    data = request.get_json()

    print("Data recue:", data)

    nom = data.get("nom")
    adresse = data.get("adresse")
    nombre_places = data.get("nombre_places")
    prix_heure = data.get("prix_heure")
    #######
    print("nom :", nom)
    print("adresse :", adresse)
    print("nombre_places :", nombre_places)
    print("prix_heure :", prix_heure)
    #######
    if (
       not nom
         or not adresse
           or nombre_places is None
             or prix_heure is None):
        
        return jsonify({
            "error": "Tous les champs sont obligatoires"
        }), 400

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "error": "Erreur de connexion à la base de données"
        }), 500

    cursor = connection.cursor(dictionary=True)

    try:

        # Pour l'instant, toutes les places sont disponibles
        places_disponibles = nombre_places

        statut = "disponible"

        #######
        print("places_disponibles :", places_disponibles)
        print("statut :", statut)
        #######

        cursor.execute("""
            UPDATE parking
            SET
                nom = %s,
                adresse = %s,
                nombre_places = %s,
                places_disponibles = %s,
                prix_heure = %s,
                statut = %s
            WHERE id = %s
        """, (
            nom,
            adresse,
            nombre_places,
            places_disponibles,
            prix_heure,
            statut,
            id
        ))

        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "error": "Parking introuvable"
            }), 404

        cursor.execute("""
            SELECT id, nom, adresse, nombre_places,
                   places_disponibles, prix_heure,
                   statut, date_creation
            FROM parking
            WHERE id = %s
        """, (id,))

        parking = cursor.fetchone()

        return jsonify(parking), 200

    except Error as e:

        connection.rollback()

        print("Erreur PUT parking :", e)

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        cursor.close()
        connection.close()

@app.route("/api/parkings/<int:id>", methods=["DELETE"])
def supprimer_parking(id):
    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "error": "Erreur de connexion à la base de données"
        }), 500

    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM parking WHERE id = %s",
            (id,)
        )

        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "error": "Parking introuvable"
            }), 404

        return jsonify({
            "message": "Parking supprimé avec succès"
        }), 200

    except Error as e:
        connection.rollback()
        print("Erreur DELETE parking :", e)
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()
##### Reservation ######
@app.route('/api/reservations', methods=['POST'])
def ajouter_reservation():
    try:
        data = request.get_json()

        utilisateur_id = data.get('utilisateur_id')
        parking_id = data.get('parking_id')
        date_reservation = data.get('date_reservation')
        heure_arrivee = data.get('heure_arrivee')
        duree = data.get('duree')

        # Vérification des données
        if not all([
            utilisateur_id,
            parking_id,
            date_reservation,
            heure_arrivee,
            duree
        ]):
            return jsonify({
                "error": "Toutes les informations sont obligatoires"
            }), 400

        conn = get_db_connection()

        if conn is None:
            return jsonify({
                "error": "Erreur de connexion à la base de données"
            }), 500

        cursor = conn.cursor(dictionary=True)

        # Vérifier le parking et récupérer ses informations
        cursor.execute("""
            SELECT id, places_disponibles, prix_heure
            FROM parking
            WHERE id = %s
        """, (parking_id,))

        parking = cursor.fetchone()

        if parking is None:
            cursor.close()
            conn.close()

            return jsonify({
                "error": "Parking introuvable"
            }), 404

        # Vérifier les places disponibles
        if parking['places_disponibles'] <= 0:
            cursor.close()
            conn.close()

            return jsonify({
                "error": "Aucune place disponible"
            }), 400

        # Calcul du prix côté serveur
        prix_total = float(parking['prix_heure']) * int(duree)

        # Ajouter la réservation
        cursor.execute("""
            INSERT INTO reservation
            (
                utilisateur_id,
                parking_id,
                date_reservation,
                heure_arrivee,
                duree,
                prix_total
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            utilisateur_id,
            parking_id,
            date_reservation,
            heure_arrivee,
            duree,
            prix_total
        ))

        # Diminuer le nombre de places disponibles
        cursor.execute("""
            UPDATE parking
            SET places_disponibles = places_disponibles - 1
            WHERE id = %s
        """, (parking_id,))

        conn.commit()

        reservation_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Réservation créée avec succès",
            "reservation_id": reservation_id,
            "prix_total": prix_total
        }), 201

    except Exception as e:
        print("ERREUR réservation :", e)

        if 'conn' in locals() and conn:
            conn.rollback()
            conn.close()

        return jsonify({
            "error": "Erreur lors de la création de la réservation"
        }), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=5000)