import requests
 
BASE_URL = 'https://demo.slashdb.com/'

 
def retrieve_data(rel_url):
    url = BASE_URL + rel_url
    response = requests.get(url)
 
    # Throw an exception on HTTP errors (404, 500, etc).
    response.raise_for_status()
 
    # Parse the response as JSON and return a Python dict.
    return response.json()
