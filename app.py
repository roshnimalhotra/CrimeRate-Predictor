from flask import Flask, request, render_template
import joblib
import math

# Load the trained KNN model and the feature scaler
model = joblib.load('knn_model.joblib')
scaler_X = joblib.load('scaler_X.joblib')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict_result():
    # City, crime and population dictionaries
    city_names = {
        '0': 'Ahmedabad', '1': 'Bengaluru', '2': 'Chennai', '3': 'Coimbatore', '4': 'Delhi',
        '5': 'Ghaziabad', '6': 'Hyderabad', '7': 'Indore', '8': 'Jaipur', '9': 'Kanpur',
        '10': 'Kochi', '11': 'Kolkata', '12': 'Kozhikode', '13': 'Lucknow', '14': 'Mumbai',
        '15': 'Nagpur', '16': 'Patna', '17': 'Pune', '18': 'Surat'
    }

    crimes_names = {
        '0': 'Crime Committed by Juveniles', '1': 'Crime against SC', '2': 'Crime against ST',
        '3': 'Crime against Senior Citizen', '4': 'Crime against children', '5': 'Crime against women',
        '6': 'Cyber Crimes', '7': 'Economic Offences', '8': 'Kidnapping', '9': 'Murder'
    }

    population = {
        '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10, '5': 23.60,
        '6': 77.50, '7': 21.70, '8': 30.70, '9': 29.20, '10': 21.20, '11': 141.10,
        '12': 20.30, '13': 29.00, '14': 184.10, '15': 25.00, '16': 20.50, '17': 50.50, '18': 45.80
    }

    # Get and convert form input
    city_code = int(request.form["city"])
    crime_code = int(request.form['crime'])
    year = int(request.form['year'])

    # Get and update population
    pop = population[str(city_code)]
    year_diff = year - 2011
    pop = pop + 0.01 * year_diff * pop  # 1% growth per year

    # Scale the inputs
    scaled_input = scaler_X.transform([[year, city_code, pop, crime_code]])

    # Predict
    crime_rate = model.predict(scaled_input)[0]

    # Get names from dictionaries
    city_name = city_names[str(city_code)]
    crime_type = crimes_names[str(crime_code)]

    # Crime risk classification and safety suggestion
    if crime_rate <= 1:
        crime_status = "Very Low Crime Area"
        safety_tip = "This area is considered very safe. Continue following standard precautions."
    elif crime_rate <= 5:
        crime_status = "Low Crime Area"
        safety_tip = "Relatively safe, but always be cautious, especially at night or in less crowded areas."
    elif crime_rate <= 15:
        crime_status = "High Crime Area"
        safety_tip = "Avoid traveling alone, especially after dark. Stay in well-lit and populated areas."
    else:
        crime_status = "Very High Crime Area"
        safety_tip = "This area is considered unsafe. Stay alert, avoid late-night outings, and keep emergency numbers handy."

    # Number of predicted cases
    cases = math.ceil(crime_rate * pop)

    # Radar chart dummy data (can be customized later)
    crime_data = {
        "crime_murder": 3,
        "crime_kidnapping": 2,
        "crime_economic": 1,
        "crime_cybercrime": 4,
        "crime_women": 6,
        "crime_children": 2,
        "crime_seniorcitizens": 5,
        "crime_juveniles": 1
    }

    police_stations = {
    'Ahmedabad': ["Ellis Bridge Police Station", "Navrangpura Police Station", "Maninagar Police Station"],
    'Bengaluru': ["Cubbon Park Police Station", "Koramangala Police Station", "Whitefield Police Station"],
    'Chennai': ["T. Nagar Police Station", "Adyar Police Station", "Anna Nagar Police Station"],
    'Coimbatore': ["Race Course Police Station", "Gandhipuram Police Station", "RS Puram Police Station"],
    'Delhi': ["Connaught Place Police Station", "Chanakyapuri Police Station", "Kalkaji Police Station"],
    'Ghaziabad': ["Kavi Nagar Police Station", "Indirapuram Police Station", "Vijay Nagar Police Station"],
    'Hyderabad': ["Banjara Hills Police Station", "Gachibowli Police Station", "Madhapur Police Station"],
    'Indore': ["MG Road Police Station", "Vijay Nagar Police Station", "Palasia Police Station"],
    'Jaipur': ["Mansarovar Police Station", "Vaishali Nagar Police Station", "Jhotwara Police Station"],
    'Kanpur': ["Swaroop Nagar Police Station", "Kalyanpur Police Station", "Govind Nagar Police Station"],
    'Kochi': ["Ernakulam Town Police Station", "Palarivattom Police Station", "Fort Kochi Police Station"],
    'Kolkata': ["Lalbazar Police HQ", "Tollygunge Police Station", "Salt Lake Police Station"],
    'Kozhikode': ["Medical College Police Station", "Vadakara Police Station", "Nadakkavu Police Station"],
    'Lucknow': ["Hazratganj Police Station", "Gomti Nagar Police Station", "Alambagh Police Station"],
    'Mumbai': ["Colaba Police Station", "Dadar Police Station", "Andheri Police Station"],
    'Nagpur': ["Sitabuldi Police Station", "Sadar Police Station", "Dhantoli Police Station"],
    'Patna': ["Kankarbagh Police Station", "Patna City Police Station", "Gandhi Maidan Police Station"],
    'Pune': ["Shivaji Nagar Police Station", "Hadapsar Police Station", "Deccan Police Station"],
    'Surat': ["Athwa Police Station", "Adajan Police Station", "Varachha Police Station"]
}


    recommended_stations = police_stations.get(city_name, ["No station data available."])

    return render_template('result.html',
                           city_name=city_name,
                           crime_type=crime_type,
                           year=year,
                           crime_status=crime_status,
                           crime_rate=crime_rate,
                           cases=cases,
                           population=round(pop, 2),
                           safety_tip=safety_tip,
                           recommended_stations=recommended_stations,
                           crime_murder=crime_data["crime_murder"],
                           crime_kidnapping=crime_data["crime_kidnapping"],
                           crime_economic=crime_data["crime_economic"],
                           crime_cybercrime=crime_data["crime_cybercrime"],
                           crime_women=crime_data["crime_women"],
                           crime_children=crime_data["crime_children"],
                           crime_seniorcitizens=crime_data["crime_seniorcitizens"],
                           crime_juveniles=crime_data["crime_juveniles"])

if __name__ == '__main__':
    app.run(debug=True)
