from flask import Flask, request, jsonify
import pickle
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
import spacy
from fuzzywuzzy import process


def get_keywords_binaryArray(sentence, keywords):
    symptom_list = [
        "itching", "skin rash", "nodal skin eruptions", "continuous sneezing", "shivering", "chills", 
        "joint pain", "stomach pain", "acidity", "ulcers on tongue", "muscle wasting", "vomiting", 
        "burning micturition", "spotting urination", "fatigue", "weight gain", "anxiety", 
        "cold hands and feets", "mood swings", "weight loss", "restlessness", "lethargy", 
        "patches in throat", "irregular sugar level", "cough", "fever" ,"high fever", "sunken eyes", 
        "breathlessness", "sweating", "dehydration", "indigestion", "headache", "yellowish skin", 
        "dark urine", "nausea", "loss of appetite", "pain behind the eyes", "back pain", 
        "constipation", "abdominal pain", "diarrhoea", "mild fever", "yellow urine", 
        "yellowing of eyes", "acute liver failure", "fluid overload", " ", 
        "swelled lymph nodes", "malaise", "blurred and distorted vision", "phlegm", 
        "throat irritation", "redness of eyes", "sinus pressure", "runny nose", "congestion", 
        "chest pain", "weakness in limbs", "fast heart rate", "pain during bowel movements", 
        "pain in anal region", "bloody stool", "irritation in anus", "neck pain", "dizziness", 
        "cramps", "bruising", "obesity", "swollen legs", "swollen blood vessels", 
        "puffy face and eyes", "enlarged thyroid", "brittle nails", "swollen extremeties", 
        "excessive hunger", "extra marital contacts", "drying and tingling lips", 
        "slurred speech", "knee pain", "hip joint pain", "muscle weakness", "stiff neck", 
        "swelling joints", "movement stiffness", "spinning movements", "loss of balance", 
        "unsteadiness", "weakness of one body side", "loss of smell", "bladder discomfort", 
        "foul smell of urine", "continuous feel of urine", "passage of gases", "internal itching", 
        "toxic look (typhos)", "depression", "irritability", "muscle pain", "altered sensorium", 
        "red spots over body", "belly pain", "abnormal menstruation", "dischromic  patches", 
        "watering from eyes", "increased appetite", "polyuria", "family history", "mucoid sputum", 
        "rusty sputum", "lack of concentration", "visual disturbances", "receiving blood transfusion", 
        "receiving unsterile injections", "coma", "stomach bleeding", "distention of abdomen", 
        "history of alcohol consumption", "fluid overload", "blood in sputum", "prominent veins on calf", 
        "palpitations", "painful walking", "pus filled pimples", "blackheads", "scurring", 
        "skin peeling", "silver like dusting", "small dents in nails", "inflammatory nails", 
        "blister", "red sore around nose", "yellow crust ooze"]

    words = sentence.split()
    for i in range(len(words)):
        temp = ""
        for j in range(i, len(words)):
            temp += words[j]
            if(temp == "I " or temp == "i "):
                temp = ""
            for k in range(len(symptom_list)):
                keywords.add(symptom_list[k])
                break
            temp += " "

    nlp = spacy.load("en_core_web_lg")

    doc = nlp(sentence)
    phrases = [chunk.text for chunk in doc.noun_chunks]
    for phrase in phrases:
        match, score = process.extractOne(phrase, symptom_list)
        if score > 80:
            keywords.add(match.lower())
            
    print(keywords)
    
    binary_array = [0] * (len(symptom_list)-1)
    for symptom in keywords:
        if symptom in symptom_list:
            index = symptom_list.index(symptom)
            binary_array[index] = 1

    return binary_array

#-----------------------------------------------------------------------------------------------------------

model = pickle.load(open('model.pkl', 'rb'))
import warnings
warnings.filterwarnings('ignore')

def disease_prediction(matched_symptoms):
    prediction = model.predict([matched_symptoms])
    print(prediction)
    return prediction

#----------------------------------------------------------------------------------------------------------

@app.route('/predict', methods=['POST'])
@cross_origin()

def predict_disease():
    data = request.get_json()
    print(data)
    sentence = data['sentence']
    keywords = set()
    matched_symptoms = get_keywords_binaryArray(sentence, keywords)
    prediction = disease_prediction(matched_symptoms)
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)