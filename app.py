from flask import Flask, request, jsonify
import logging
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

def scrape_function(job_role):
    search_url = "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=" + job_role
    urlclient = uReq(search_url)
    page_data = urlclient.read()
    urlclient.close()
    foundit_html = bs(page_data, 'html.parser')
    job_listings = foundit_html.find_all("li", {"class": "clearfix job-bx wht-shd-bx"})
    
    job_data_list = []  # Initialize a list to store job data
    
    if job_listings:
        for job in job_listings:
            job_data = {}  # Create a dictionary to store job details
            
            job_role_elem = job.header.h2.a
            if job_role_elem:
                job_data['Job Role'] = job_role_elem.text.strip()
            else:
                job_data['Job Role'] = "Job role not available"
            
            company_elem = job.header.find_all('h3', {"class": "joblist-comp-name"})[0]
            if company_elem:
                job_data['Company Name'] = company_elem.text.strip()
            else:
                job_data['Company Name'] = "Company name not available"
            
            job_link_elem = job_role_elem
            if job_link_elem and 'href' in job_link_elem.attrs:
                job_data['Job Link'] = job_link_elem['href']
            else:
                job_data['Job Link'] = "Link not available"
            
            # Append the job data dictionary to the list
            job_data_list.append(job_data)
    
    else:
        raise Exception("No jobs found for the given job role.")
    
    return job_data_list  # Return the list of job data dictionaries

@app.route('/')
def index():
    return "Hello"

@app.route('/scrape', methods=['POST'])
def scrape_endpoint():
    data = request.json
    job_title = data.get('job_title', '')  # Assuming the JSON payload contains a "job_title" field
    # job_title="softwaredevelopement"
    if not job_title:
        return jsonify({"error": "Job title not provided"}), 400

    result = scrape_function(job_title)
    return jsonify({"job_titles": result})

if __name__ == '__main__':
    app.run(debug=False)

