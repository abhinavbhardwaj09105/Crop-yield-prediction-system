from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle
import logging
from sklearn.preprocessing import OneHotEncoder

# Loading model
dtr = pickle.load(open('dtr.pkl', 'rb'))
preprocessor = pickle.load(open('preprocessor.pkl', 'rb'))

app = Flask(__name__, template_folder='Template')

# Configure logging
file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

# Route for rendering the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Route for receiving predictions
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get input data from the form
            Year = request.form['Year']
            average_rain_fall_mm_per_year = request.form['average_rain_fall_mm_per_year']
            pesticides_tonnes = request.form['pesticides_tonnes']
            avg_temp = request.form['avg_temp']
            Area = request.form['Area']
            Item = request.form['Item']
            
            # Validate input data
            if not all(field.isdigit() or 
                       (field.replace('.', '', 1).isdigit() and field.count('.') <= 1) for field in [Year, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp]):
                raise ValueError("Invalid input. Please enter numeric values.")

            # Convert input data to float
            Year = float(Year)
            average_rain_fall_mm_per_year = float(average_rain_fall_mm_per_year)
            pesticides_tonnes = float(pesticides_tonnes)
            avg_temp = float(avg_temp)
            #Area = float(Area)
            
            # Prepare features array
            features = np.array([[Year, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, Area, Item]])

            # Transform categorical features using preprocessor
            transformed_features = preprocessor.transform(features)

            # Predict yield
            predicted_yield = dtr.predict(transformed_features)[0]

            # Render the index.html template with the predicted yield
            return render_template('index.html', prediction=predicted_yield)
        except ValueError as e:
            # Handle conversion errors
            error_message = str(e)
            return render_template('index.html', error=error_message)
        except Exception as ex:
            # Handle other exceptions
            error_message = f"An error occurred: {str(ex)}"
            return render_template('index.html', error=error_message)
    else:
        return render_template('index.html')




if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)




