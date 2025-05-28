from flask import Flask, request, render_template, redirect
import csv
from datetime import datetime
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    company = request.form['company']
    city = request.form['city']
    trigger = request.form['trigger']
    source = request.form['source']
    data_source = request.form.get('data_source', 'UNKNOWN')
    
    '''
    linkedin_url = request.form.get("linkedin_url", "")
    contact_email = request.form.get("contact_email", "")
    company_website = request.form.get("company_website", "")
    has_contact = request.form.get("has_contact", "False")
    '''


    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #file_path = os.path.join("..", "output", "submitted_leads.csv")
    
    BASE_DIR = Path(__file__).resolve().parent.parent  # goes to hni_lead_generator/
    OUTPUT_DIR = BASE_DIR / "output"
    OUTPUT_DIR.mkdir(exist_ok=True)  # creates output folder if missing
    
    '''
    file_path = OUTPUT_DIR / "submitted_leads.csv"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)   # ✅ Add this line
    '''
    
    file_path = OUTPUT_DIR / "submitted_leads.csv"
    print(f"Writing to file: {file_path.resolve()}")


    with open(file_path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            #writer.writerow(["timestamp", "name", "company", "city", "trigger", "source"])
            writer.writerow(["timestamp", "name", "company", "city", "trigger", "source", "data_source"])
            #writer.writerow(["timestamp", "name", "company", "city", "trigger", "source", "data_source", "linkedin_url", "contact_email", "company_website", "has_contact"])


        #writer.writerow([now, name, company, city, trigger, source])
        writer.writerow([now, name, company, city, trigger, source, data_source])
        #writer.writerow([now, name, company, city, trigger, source, data_source, linkedin_url, contact_email, company_website, has_contact])



    return f"<h3>Submission Successful!</h3><p>{name} from {company} submitted.</p><a href='/form'>Submit another</a>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
