import json
import socket 
import requests


# checks for proper JSON serialization and catches errors
def checkJSON(request):
    try:
        json.loads(request)
        return True
    except(TypeError, OverflowError, json.JSONDecodeError):
        return False


def checkRequest(request, urlComponent):
    # checks for expected parameters keys
    for key in request:
        if key == 'url':
            url = request[key]
            strIndex = url.find(urlComponent)

            # /wiki/ not found in url string; bad url
            if strIndex == -1:
               return ""

            #extracts Wikipedia article title from url
            return url[(strIndex + len(urlComponent)):]


def resolveClientRequest(conn):
    
    title = ""
    urlComponent = "/wiki/"
    payload = {"title":"", "summary":""}
    errorResponse = "Failed to scrap data. Check URL and request format."

    # decodes utf-8 encoded request
    request = conn.recv(1024).decode("utf-8")
    # checks for valid JSON serialized request
    
    validRequest = checkJSON(request)
    
    if validRequest:
        parsedRequest  = json.loads(request)
    else:
        errorResponse = json.dumps(errorResponse)
        conn.send(errorResponse.encode("utf-8"))
        return
    
    # checks for valid request body
    title = checkRequest(parsedRequest, urlComponent)
    
    # If request is valid, makes a post request to MediaWiki API 
    if title:
        payload["title"] = title
        apiUrl = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles="+title+"&exintro=&explaintext=&format=json"
        httpPostReq = requests.post(apiUrl, headers = {"Content-Type": "application/json; charset=utf-8"})

        #Receives data from MediaWiki API
        wikiData = json.loads(httpPostReq.content)
        # print(wikiData)
        
        try:
            summary =  list(wikiData['query']['pages'].values())[0]['extract']
        except:
            summary = ""

        payload["summary"] = summary
        if summary == "":
            errorResponse = json.dumps(errorResponse)
            conn.send(errorResponse.encode("utf-8"))

        else:
            response = json.dumps(payload)
            conn.send(response.encode("utf-8"))

    else:
        errorResponse = json.dumps(errorResponse)
        conn.send(errorResponse.encode("utf-8"))


# runs server and performs server-side functionality
def runServer():
    host = socket.gethostname()
    port = 7634

    # initializes socket instance
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host, port))

    # can listen for up to 4 clients
    s.listen(4)

    # server runs indefinitely
    while 1:
        # accepts and establishes connection
        conn, address = s.accept()
        print("Connection established with: "+ str(address))

        resolveClientRequest(conn)

        conn.close()
    s.close()

        
if __name__ == '__main__':
    runServer()