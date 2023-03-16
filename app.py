from flask import Flask, render_template, request
import requests

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

    
    API_URL = f'https://npiregistry.cms.hhs.gov/api/?first_name={first_name}&last_name={last_name}&city={city}&state={state}&version=2.1'
    
    counts = 0
    mailing_address, location_address, basics = [],[],[]
    othernames = []
    
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            counts = data['result_count']
                
            for i in range (0,counts):
                if data['results'][i]['addresses'][0]['address_purpose'] == "MAILING":
                    mailing_address.append(data['results'][i]['addresses'][0])
                    location_address.append(data['results'][i]['addresses'][1])
                else:
                    location_address.append(data['results'][i]['addresses'][0])
                    mailing_address.append(data['results'][i]['addresses'][1])

                basics.append(data['results'][i]['basic'])
                if len(data['results'][i]['other_names']) > 0:
                    othernames.append(data['results'][i]['other_names'][0])
                else:
                    othernames.append(data['results'][i]['other_names'])

            return render_template('results.html', counts=counts, mailing_address=mailing_address, location_address=location_address, basics=basics, othernames=othernames)
        else:
            print('Error: API returned status code', response.status_code)
    except requests.exceptions.RequestException as e:
        print('Error:', e)


if __name__ == '__main__':
    app.run(debug=True)
