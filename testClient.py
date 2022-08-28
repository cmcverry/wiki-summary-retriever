import socket 
import json

def runClient():
    host = socket.gethostname()
    port = 7634

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((host, port))

    message = {"url":"https://en.wikipedia.org/wiki/New_York_(state)"}
    request = json.dumps(message)

    c.send(request.encode("utf-8"))
    response = c.recv(8196).decode("utf-8")

    parsedResponse = json.loads(response)
    print(parsedResponse)

    c.close()

if __name__ == '__main__':
    runClient()

