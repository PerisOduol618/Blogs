import requests


base_url = None
def configure_request(app):
    global base_url
    base_url = app.config['QUOTE_API_BASE_URL']
def get_blogQuotes():
    """
    Function that gets the json response to our url request
    """
    get_response = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
    return get_response
