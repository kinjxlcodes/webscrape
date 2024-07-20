
# The ssl certificate is not verified tried bypassing the ssl certificate 
# Also tried specifying a ca bundle 
# Though the code should pretty much look like this, couldnt troubleshoot the problem
# PIP install requirements "pip install requests beautifulsoup4"
#----------------------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

# URL of the site
url = "https://hprera.nic.in/PublicDashboard"

# Make a request to the website
response = requests.get(url)
response.raise_for_status()  # Ensure we notice bad responses

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the section containing the "Registered Projects"
registered_projects_section = soup.find(div,id='tab-content')

# Extract project links 
project_links = registered_projects_section.find_all('a', limit=6)

# List to store project details
projects_details = []

# Loop through each project link
for link in project_links:
    project_url = "https://hprera.nic.in" + link.get('href')
    
    # Make a request to the project detail page
    project_response = requests.get(project_url)
    project_response.raise_for_status()  # Ensure we notice bad responses
    
    # Parse the project detail HTML content
    project_soup = BeautifulSoup(project_response.content, 'html.parser')
    
    # Extract required details
    gstin_no = project_soup.find(text='GSTIN No').find_next('td').text.strip()
    pan_no = project_soup.find(text='PAN No').find_next('td').text.strip()
    name = project_soup.find(text='Name').find_next('td').text.strip()
    permanent_address = project_soup.find(text='Permanent Address').find_next('td').text.strip()
    
    # Append the details to the list
    projects_details.append({
        'GSTIN No': gstin_no,
        'PAN No': pan_no,
        'Name': name,
        'Permanent Address': permanent_address
    })

# Print the project details
for project in projects_details:
    print(project)
