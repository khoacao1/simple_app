from flask import Flask, render_template, request
import requests
from model.searched_obj import Provider 

app = Flask(__name__)

@app.route('/', methods=['GET'])
def searching():
    return render_template('index.html')

@app.route('/get-data', methods=['POST'])
def results():
    last_name = request.form['last_name']
    first_name = request.form['first_name']
    city = request.form['city']
    state = request.form['state']

    search_provider = Provider(last_name,first_name,city,state)
    
    API_URL = f'https://npiregistry.cms.hhs.gov/api/?first_name={first_name}&last_name={last_name}&city={city}&state={state}&version=2.1'
    
    counts = 0
    addresses, basics = [],[]
    
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            counts = data['result_count']
                
            for i in range (0,counts):
                if "telephone_number" in data['results'][i]['addresses'][0]:
                    addresses.append(data['results'][i]['addresses'][0])
                else:
                    addresses.append(data['results'][i]['addresses'][1])

                basics.append(data['results'][i]['basic'])

            return render_template('results.html', counts=counts, addresses=addresses, basics=basics, search_provider=search_provider)
        else:
            print('Error: API returned status code', response.status_code)
    except requests.exceptions.RequestException as e:
        print('Error:', e)


if __name__ == '__main__':
    app.run(debug=True)
