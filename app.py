import pickle
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the model
model = pickle.load(open('rf_model.pkl', 'rb'))

def generate_report(prediction):
    # Logic to map prediction to attack type and recommendations
    attack_types = {
        0: {"en": "Benign", "es": "Benigno", "fr": "Bénin",
            "yo": "Alaiṣe", "ig": "Ezi uche", "ha": "Mai Kyau"},
        1: {"en": "Bot", "es": "Bot", "fr": "Bot",
            "yo": "Bot", "ig": "Bot", "ha": "Bot"},
        2: {"en": "Brute Force", "es": "Fuerza Bruta", "fr": "Force Brute",
            "yo": "Agbara Agbari", "ig": "Ike Ikpe", "ha": "Karfi Naƙi"},
        3: {"en": "DDoS", "es": "DDoS", "fr": "DDoS",
            "yo": "DDoS", "ig": "DDoS", "ha": "DDoS"},
        4: {"en": "DoS", "es": "DoS", "fr": "DoS",
            "yo": "DoS", "ig": "DoS", "ha": "DoS"},
        5: {"en": "FTP-Patator", "es": "FTP-Patator", "fr": "FTP-Patator",
            "yo": "FTP-Patator", "ig": "FTP-Patator", "ha": "FTP-Patator"},
        6: {"en": "Port Scan", "es": "Escaneo de Puertos", "fr": "Scan de Ports",
            "yo": "Ayẹwo Ibudo", "ig": "Ihe nyocha Ọdụ ụgbọ mmiri", "ha": "Binciken Tashar Jirgin Ruwa"},
        7: {"en": "SSH-Patator", "es": "SSH-Patator", "fr": "SSH-Patator",
            "yo": "SSH-Patator", "ig": "SSH-Patator", "ha": "SSH-Patator"},
        8: {"en": "XSS", "es": "XSS", "fr": "XSS",
            "yo": "XSS", "ig": "XSS", "ha": "XSS"},
    }
    recommendations = {
        0: {"en": "No action needed, the traffic is benign.",
            "es": "No se necesita ninguna acción, el tráfico es benigno.",
            "fr": "Aucune action nécessaire, le trafic est bénin.",
            "yo": "Ko si iṣe ti o nilo, ijabọ naa jẹ alaiṣe.",
            "ig": "Enweghị ihe a chọrọ, n'ihu ụgbọ njem dị mma.",
            "ha": "Babu buƙatar aiki, zirga-zirgar yana da kyau."},
        1: {"en": "Investigate the source and mitigate bot activity.",
            "es": "Investiga la fuente y mitiga la actividad de bots.",
            "fr": "Enquêter sur la source et atténuer l'activité des bots.",
            "yo": "Ṣawari orisun naa ki o dinku iṣẹ bot.",
            "ig": "Nyochaa isi iyi ma mee ka ọrụ bot dị ala.",
            "ha": "Bincika asalin kuma rage aikin bot."},
        2: {"en": "Implement account lockouts and monitor failed login attempts.",
            "es": "Implementa bloqueos de cuentas y monitorea los intentos fallidos de inicio de sesión.",
            "fr": "Mettre en œuvre des verrouillages de compte et surveiller les tentatives de connexion échouées.",
            "yo": "Ṣe ifasilẹ awọn akọọlẹ ki o ṣe abojuto awọn igbiyanju wiwọle ti kuna.",
            "ig": "Tinye igbechi akaụntụ ma soro na-agbalị ịbanye na-agaghị eme.",
            "ha": "Aiwatar da makulli asusu da kuma sa ido kan yunƙurin shiga mara kyau."},
        3: {"en": "Apply DDoS protection services and increase network resilience.",
            "es": "Aplica servicios de protección DDoS y aumenta la resiliencia de la red.",
            "fr": "Appliquez des services de protection DDoS et augmentez la résilience du réseau.",
            "yo": "Lo awọn iṣẹ aabo DDoS ki o mu agbara nẹtiwọọki pọ si.",
            "ig": "Tinye ọrụ nchebe DDoS ma melite ike netwọk.",
            "ha": "Yi amfani da ayyukan kariya na DDoS kuma kara juriyar hanyar sadarwa."},
        4: {"en": "Implement rate limiting and traffic filtering.",
            "es": "Implementa limitación de velocidad y filtrado de tráfico.",
            "fr": "Mettre en œuvre la limitation du débit et le filtrage du trafic.",
            "yo": "Ṣe agbekalẹ ifilelẹ oṣuwọn ati àlẹmọ ijabọ.",
            "ig": "Tinye na mbenata ọnụego na iju azụmaahịa.",
            "ha": "Aiwatar da iyakance ƙimar kima da tacewa zirga-zirga."},
        5: {"en": "Ensure secure FTP configurations and monitor FTP traffic.",
            "es": "Asegúrate de configuraciones FTP seguras y monitorea el tráfico FTP.",
            "fr": "Assurez-vous des configurations FTP sécurisées et surveillez le trafic FTP.",
            "yo": "Rii daju awọn iṣeto FTP ailewu ati ṣe atẹle ijabọ FTP.",
            "ig": "Jide n'aka na nchekwa FTP hazie ma soro FTP ọwara.",
            "ha": "Tabbatar da ingantattun saitunan FTP kuma saka idanu kan zirga-zirgar FTP."},
        6: {"en": "Review firewall rules and close unnecessary ports.",
            "es": "Revisar las reglas del firewall y cerrar los puertos innecesarios.",
            "fr": "Examiner les règles du pare-feu et fermer les ports inutiles.",
            "yo": "Atunwo awọn ofin ogiriina ati pa awọn ibudo ti ko wulo.",
            "ig": "Nyochaa iwu nchekwa firewall ma mechie ọdụ ụgbọ mmiri na-achọghị.",
            "ha": "Bita ƙa'idodin wuta kuma rufe tashoshi marasa mahimmanci."},
        7: {"en": "Enhance SSH security with key-based authentication and monitor SSH traffic.",
            "es": "Mejora la seguridad de SSH con autenticación basada en claves y monitorea el tráfico SSH.",
            "fr": "Renforcez la sécurité SSH avec l'authentification par clé et surveillez le trafic SSH.",
            "yo": "Mu aabo SSH pọ si pẹlu iwọle-orukọ ti orisun bọtini ki o ṣe atẹle ijabọ SSH.",
            "ig": "Mụtakwa nchekwa SSH na nhọpụta bọtịnụ na soro SSH ọwara.",
            "ha": "Haɓaka tsaron SSH tare da tabbatar da shaidar tushe kuma lura da zirga-zirgar SSH."},
        8: {"en": "Sanitize user inputs and validate data to prevent XSS.",
            "es": "Sanitiza las entradas de los usuarios y valida los datos para prevenir XSS.",
            "fr": "Assainir les entrées utilisateur et valider les données pour empêcher les XSS.",
            "yo": "Mú iṣẹgun olumulo ni mọnamọna ki o ṣe idanwo data lati yago fun XSS.",
            "ig": "Mee ka ahụ ike n'ịbanye onye ọrụ ma gosipụtara data iji gbochie XSS.",
            "ha": "Tsaftace shigarwar mai amfani kuma tabbatar da bayanai don hana XSS."},
    }

    # Get attack type and recommendations based on prediction
    attack_type = attack_types.get(prediction, {"en": "Unknown Attack", "es": "Ataque Desconocido", 
                                                "fr": "Attaque Inconnue", "yo": "Ikọlu Aimọ", 
                                                "ig": "Ọgwụgwụ Amaghị", "ha": "Hararwa Mai Sani"})
    recommendation = recommendations.get(prediction, {"en": "Further investigation required.",
                                                      "es": "Se requiere mayor investigación.",
                                                      "fr": "Une enquête plus approfondie est nécessaire.",
                                                      "yo": "Atunyẹwo siwaju sii nilo.",
                                                      "ig": "Ọchịchọ ọzọ dị mkpa.",
                                                      "ha": "Kara bincike yana bukatar."})

    # Return the report
    return {
        "attack_type": attack_type,
        "recommendation": recommendation
    }

@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)

    # Make prediction using model loaded from disk as per the data.
    prediction = model.predict([np.array(list(data.values()))])[0]

    # Generate multilingual report
    report = generate_report(prediction)

    # Return the predicted class as a JSON response
    return jsonify(report)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

