from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import pymongo
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


try:
    client = pymongo.MongoClient("mongodb+srv://max:max2106@cluster0.x2kphbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["hospital_db"]
except Exception as e:
    print(f"MongoDB connection error: {str(e)}")
    
print("MongoDB connection successful")# verification de la connection a la base de donnee
#creation de variable pour mes collections
mydash = db['dashboard']
mybed = db['bed_availability']
mypatient = db['patient_vitals'] 
myclient =db['patient']
mydep = db['speciality']
mynurse = db['nurses']
myhist = db['historiques']
mydoc =  db['doctors']
myappt = db['appointments']
#---------------------------------------------------------------------
#route de test
@app.route('/')
def index():
    try:
        
        client.admin.command('ismaster')
        print("Connexion à MongoDB établie avec succès")
    except Exception as e:
        print(f"Erreur de connexion à MongoDB : {str(e)}")

    return "Hello, world!"
#------------------------------------------------------------------------------

# creer une route pour mon dashbord en convertissant les id en string
@app.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    try:
        data = list(mydash.find()) 
        for item in data:
            item['_id'] = str(item['_id']) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(data)
    
# creer une route pour retrouver les patients rechercher en convertissant les id en string
@app.route('/patients', methods=['GET'])
def get_patients():
    search_query = request.args.get('search', '') 
    if search_query:
        patients = list(myclient.find({'nom': search_query}))
        for patient in patients:
            patient['_id'] = str(patient['_id'])
        print("Patients found:", patients)
        return jsonify(patients)
    else:
        return jsonify({'message': 'No search query provided'}), 400



# creer une route pour mon patient en convertissant les id en string et en classant par ordre
@app.route('/patient', methods=['GET'])
def get_patient_data():
    try:
        data = list(myclient.find().sort('nom', 1)) 
        for item in data:
            item['_id'] = str(item['_id']) 
            print(f"Found {len(data)} records")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(data)






# creer une route pour les reservation en convertissant les id en string
@app.route('/appointments', methods=['GET'])
def get_appointments_data():
    try:
        data = list(myappt.find().sort('nom', 1)) 
        for item in data:
            item['_id'] = str(item['_id']) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(data)


# creer une route pour truver des patients en fonction de leur id en convertissant les id en string
@app.route('/patient/<string:id>', methods=['GET'])
def get_patient(id):
    try:
        patient = myclient.find_one({"_id": ObjectId(id)})
        if patient:
            patient['_id'] = str(patient['_id'])
            return jsonify(patient)
        else:
            return jsonify({"message": "Patient not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    



# Route pour récupérer les données d'une chambre par son ID
@app.route('/bed_availability/<string:id>', methods=['GET'])
def get_bed_availability(id):
    try:
        bed = mybed.find_one({"_id": ObjectId(id)})
        if bed:
            bed['_id'] = str(bed['_id']) # Conversion de l'ID en chaîne de caractères
            return jsonify(bed)
        else:
            return jsonify({"message": "Room not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Route pour récupérer toutes les données des chambres    
@app.route('/bed_availability', methods=['GET'])
def get_bed_availability_data():
    try:
        data = list(mybed.find())
        for item in data:
            item['_id'] = str(item['_id'])
        print(f"Found {len(data)} records")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
# Route pour récupérer toutes les données des médecins
@app.route('/doctors', methods=['GET'])
def get_doctors_data():
    try:
        data = list(mydoc.find())
        for item in data:
            item['_id'] = str(item['_id'])
        print(f"Found {len(data)} records")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
# Route pour récupérer toutes les données des historiques
@app.route('/historiques', methods=['GET'])
def get_historique_data():
    try:
        data = list(myhist.find())
        for item in data:
            item['_id'] = str(item['_id'])
        print(f"Found {len(data)} records")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour récupérer les historiques d'un patient par son nom
@app.route('/historiques/<string:nom>', methods=['GET'])
def get_historiques(nom):
    try:
        historiques = myhist.find({"nom": nom})
        historiques_list = list(historiques)
        for item in historiques_list:
            item['_id'] = str(item['_id'])
        return jsonify(historiques_list)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Route pour récupérer toutes les spécialités
@app.route('/speciality', methods=['GET'])
def get_speciality_data():
    try:
        data = list(mydep.find())
        for item in data:
            item['_id'] = str(item['_id'])
        print(f"Found {len(data)} records")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour récupérer toutes les données des infirmières
@app.route('/nurses', methods=['GET'])
def get_nurses_data():
    try:
        data = list(mynurse.find())
        for item in data:
            item['_id'] = str(item['_id'])
        print(f"Found {len(data)} records")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour récupérer toutes les données des constantes vitales des patients de l'hopital
@app.route('/patient_vitals', methods=['GET'])
def get_patient_vitals_data():
    try:
        data = list(mypatient.find())
        for item in data:
            item['_id'] = str(item['_id'])
        print(f"Found {len(data)} records")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#--------------------------------------------------
# Route pour ajouter des données au dashboard
@app.route('/dashboard', methods=['POST'])
def add_dashboard_data():
    try:
        data = request.get_json()
        mydash.insert_one(data)
        print(data)
        return ("Insert Succes")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour ajouter une rendez-vous
@app.route('/appointments', methods=['POST'])
def add_appointments_data():
    try:
        data = request.get_json()
        myappt.insert_one(data)
        print(data)
        return ("Insert Succes")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route pour ajouter des chambres et les lits pour les patients
@app.route('/bed_availability', methods=['POST'])
def update_collection_data():
    try:
        data = request.get_json()
        mybed.insert_one(data)
        print (data)
        return("Insert Succes")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour ajouter les constantes vitales d'un patient   
@app.route('/patient_vitals', methods=['POST'])
def add_patient_vitals_data():
    try:
        data = request.get_json()
        mypatient.insert_one(data)
        print(data)
        return ("Insert Succes")
    except Exception as e:
        return jsonify({"error": str(e)}), 500    


# Route pour ajouter un patient
@app.route('/patient', methods=['POST'])
def add_patient_data():
    try:
        data = request.get_json()
        myclient.insert_one(data)
        print(data)
        return ("Insert Succes")
    except Exception as e:
        return jsonify({"error": str(e)}), 500   

# Route pour ajouter plusieurs patients
@app.route('/patients', methods=['POST'])
def add_patients_data():
    try:
        data = request.get_json()
        if isinstance(data, list):
            result = myclient.insert_many(data)
            print(result.inserted_ids)
            return "Insert Success"
        else:
            raise ValueError("Invalid data format. Expected a list.")
    except Exception as e:
        return jsonify({"error": str(e)}), 500



#----------------------------------------------------
# Route pour mettre à jour les données du dashboard
@app.route('/dashboard/<id>', methods=['PUT'])
def update_dashboard_data(id):
    try:
        
        updated_data = request.json
        result = mydash.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        if result.modified_count == 1:
            return jsonify({"_id": id, **updated_data}), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route pour mettre à jour les données de disponibilité des lits
@app.route('/bed_availability/<id>', methods=['PUT'])
def update_bed_availability_data(id):
    try:
        updated_data = request.json
        result = mybed.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        if result.modified_count == 1:
            print("Put Succes")
            return jsonify({"_id": id, **updated_data}), 200
            
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route pour mettre à jour les données des constantes vitales d'un patient
@app.route('/patient_vitals/<id>', methods=['PUT'])
def update_patient_vitals_data(id):
    try:
        updated_data = request.json
        result = mypatient.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        if result.modified_count == 1:
            print("Put Succes")
            return jsonify({"_id": id, **updated_data}), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route pour mettre à jour les données d'un patient
@app.route('/patient/<id>', methods=['PUT'])
def update_patient_data(id):
    try:
        updated_data = request.json
        result = myclient.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        if result.modified_count == 1:
            print("Put Succes")
            return jsonify({"_id": id, **updated_data}), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
#---------------------------------------------------------------------------------------

# Route pour supprimer un document du dashboard
@app.route('/dashboard/<id>', methods=['DELETE'])
def delete_dashboard_data(id):
    try:
        
        result = mydash.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            print("Delete Succes")
            return jsonify({"message": "Document deleted"}), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour supprimer un document de disponibilité des lits
@app.route('/bed_availability/<id>', methods=['DELETE'])
def delete_bed_availability_data(id):
    try:
        result = mybed.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            print("Delete Succes")
            return jsonify({"message": "Document deleted"}), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route pour supprimer un document des constantes vitales d'un patient
@app.route('/patient_vitals/<id>', methods=['DELETE'])
def delete_patient_vitals_data(id):
    try:
        result = mypatient.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            print("Delete Succes")
            return jsonify({"message": "Document deleted"}), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route pour supprimer un document d'un patient
@app.route('/patient/<id>', methods=['DELETE'])
def delete_patient_data(id):
    try:
        result = myclient.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            print("Delete Succes")
            return jsonify({"message": "Document deleted"}), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
