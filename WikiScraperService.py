# Author: Christian McVerry
# Course: CS 361
# Instructor: Lara Letaw
# Date: 11/09/2021
# Description: microservice that can be used to extract utf-8 encoded summaries (text before article sections) for any Wikipedia article.


from json.decoder import JSONDecodeError
import socket 
import json
import requests


# checks for proper JSON serialization and catches errors
def checkJSON(request):
    try:
        json.loads(request)
        return True
    except(TypeError, OverflowError, JSONDecodeError):
        return False


# runs server and performs server-side functionality
def runServer():
    host = socket.gethostname()
    port = 7634

    # initiates socket instance
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # binds host and port
    s.bind((host, port))

    # can listen for up to 4 clients
    s.listen(4)

    while 1:
        # accepts and establishes connection
        conn, address = s.accept()
        print("Connection established with: "+ str(address))

        while 1:
            # initializes variables and payload dict
            validRequest = False
            intro = False
            title = ""
            urlComponent = "/wiki/"
            payload = {"title":"", "summary":""}
            errorResponse = "Failed to scrap data. Check URL and request format."

            # decodes utf-8 encoded request message
            request = conn.recv(1024).decode("utf-8")

            # checks for valid JSON serialized message
            validRequest = checkJSON(request)
            
            # if valid
            if validRequest:
                # parses JSON-serialized message and returns python dict
                parsedRequest  = json.loads(request)

            # else responds with error message
            else:
                errorResponse = json.dumps(errorResponse)
                conn.send(errorResponse.encode("utf-8"))
                break

            # checks for expected parameters keys
            for key in parsedRequest:
                if key == 'url':
                    url = parsedRequest[key]
                    strIndex = url.find(urlComponent)

                    # /wiki/ not found in url string; bad url
                    if strIndex == -1:
                        break
                    #extracts Wikipedia article title from url
                    title = url[(strIndex + len(urlComponent)):]

                if key == 'summary' and parsedRequest[key] == 'true':
                    intro = True
            
            # If parsed request is valid, fills payload dict and makes a post request to MediaWiki API 
            if title and intro:
                payload["title"] = title
                apiUrl = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles="+title+"&exintro=&explaintext=&format=json"
                httpPostReq = requests.post(apiUrl, headers = {"Content-Type": "application/json; charset=utf-8"})

                #Receives data from MediaWiki API
                wikiData = json.loads(httpPostReq.content)
                # print(wikiData)
                # print(type(wikiData))
                
                # initalizes extract variable as empty string
                extract = ""

                # iterates through nested wikiData dict to extract relevant article summary data
                for k in wikiData:
                    for j in wikiData[k]:

                        # handles Wikipedia articles with '_' delineated titles
                        # otherwise would break iteration 
                        if j == "normalized":
                            continue
                        
                        for i in wikiData[k][j]:
                            for l in wikiData[k][j][i]:
                                if l == "extract":
                                    extract = wikiData[k][j][i][l]

                payload["summary"] = extract
                if extract == "":
                    errorResponse = json.dumps(errorResponse)
                    conn.send(errorResponse.encode("utf-8"))
                    break
                else:
                    response = json.dumps(payload)
                    # print(response)

                    conn.send(response.encode("utf-8"))

            else:
                errorResponse = json.dumps(errorResponse)
                conn.send(errorResponse.encode("utf-8"))
            break

        conn.close()
    s.close()

        
if __name__ == '__main__':
    runServer()