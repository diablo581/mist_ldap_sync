import requests
from requests.exceptions import HTTPError

import json




def _response(resp, uri="", multi_pages_result=None):
    if resp.status_code == 200:
        if multi_pages_result == None:
            result = resp.json()
        else: 
            result = multi_pages_result
        error = ""
        #console.debug("Response Status Code: %s" % resp.status_code)
    else:
        result = ""
        error = resp.json()
        #console.debug("Response Status Code: %s" % resp.status_code)
        #console.debug("Response: %s" % error)
    return {"result": result, "status_code": resp.status_code, "error": error, "uri":uri}

def mist_get(token, url, query=None, page=1, limit=None):
    """GET HTTP Request
    Params: uri, HTTP query
    Return: HTTP response"""
    try:
        headers = {}
        final_url = url
        headers['Content-Type'] = "application/json"
        headers['Authorization'] = "Token {0}".format(token)
        html_query = []
        if query:
            for query_param in query:
                html_query.append(f"{query_param}={query[query_param]}")
        if limit:html_query.append(f"limit={limit}")
        if page: html_query.append(f"page={page}")
        if html_query: final_url += f"?{'&'.join(html_query)}"
        #print("\r\nnRequest > GET %s" % final_url)
        resp = requests.get(final_url, headers=headers)
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        print(f'HTTP error description: {resp.json()}')
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else: 
        if "X-Page-Limit" in resp.headers:
            content = resp.json()
            x_page_limit = int(resp.headers["X-Page-Limit"])
            x_page_page = int(resp.headers["X-Page-Page"])
            x_page_total = int(resp.headers["X-Page-Total"])
            if x_page_limit * x_page_page < x_page_total:
                content+=mist_get(token, url, query, page + 1, limit)["result"]
            return _response(resp, url, content)
        else:                
            return _response(resp, url)

def mist_post(token, url, body={}):
    """POST HTTP Request
    Params: uri, HTTP body
    Return: HTTP response"""
    try: 
        headers = {}
        headers['Content-Type'] = "application/json"
        headers['Authorization'] = "Token {0}".format(token)
        #console.debug("Request > POST %s" % url)
        #console.debug("Request body: \r\n%s" % body)
        if type(body) == str:
            resp = requests.post(url, data=body, headers=headers)
        else: 
            resp = requests.post(url, json=body, headers=headers)
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        print(f'HTTP error description: {resp.json()}')
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else: 
        return _response(resp, url)

def mist_put(token, url, body={}):
    """PUT HTTP Request
    Params: uri, HTTP body
    Return: HTTP response"""
    try:
        headers = {}
        headers['Content-Type'] = "application/json"
        headers['Authorization'] = "Token {0}".format(token)
        #console.debug("Request > PUT %s" % url)
        #console.debug("Request body: \r\n%s" % body)
        if type(body) == str:
            resp = requests.put(url, data=body, headers=headers)
        else: 
            resp = requests.put(url, json=body, headers=headers)
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        print(f'HTTP error description: {resp.json()}')
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else: 
        return _response(resp, url)


def mist_delete(token, url):
    """DELETE HTTP Request
    Params: uri
    Return: HTTP response"""
    try: 
        headers = {}
        headers['Content-Type'] = "application/json"
        headers['Authorization'] = "Token {0}".format(token)
        #console.debug("Request > DELETE %s" % url)
        resp = requests.delete(url, headers=headers)
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else: 
        return _response(resp, url)

