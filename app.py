from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

# load the data into a Pandas dataframe
data = pd.read_csv('colleges.csv')

# convert the "Rank Range" column to integers
data['Rank Range'] = data['Rank Range'].apply(lambda x: np.mean([int(i) for i in x.split('-')]))

# set up the homepage
@app.route('/')
def home():
    return render_template('form.html')

# set up the predict page
@app.route('/', methods=['POST'])
def predict():
    if request.method == 'POST':
        # get the form data submitted by the user
        course = request.form['course']
        gender = request.form['gender']
        caste = request.form['caste']
        rank = int(request.form['rank'])

        # filter the data based on user input
        filtered_data = data[(data['Course'] == course) & (data['Gender'] == gender) & (data['Caste'] == caste) & (data['Rank Range'] >= rank)]

        # sort the data by rank range
        sorted_data = filtered_data.sort_values('Rank Range')

        # get the top 10 college names from the sorted data
        college_list = sorted_data[['College Name', 'Course', 'Cutoff Marks']].head(10).values.tolist()

        # render the predict page with the college list
        return render_template('results.html', college_list=college_list)

if __name__ == '__main__':
    app.run(debug=True)
