# Wikipedia Summary Retriever 

This program is a small microservice TCP server socket that accepts requests from TCP client sockets that contain a URL of any existing Wikipedia article and returns a UTF-8 encoded summary section of the respective article. 

## Instructions

Required: Python 3

The program runs on a TCP server socket instance assigned to a system's IP address and a hardcoded port (7634).
While the server socket is running, TCP client sockets instances can make requests to the server. Make sure the client socket is correctly configured to connect to the server's IP address and port. 

1. In a CLI navigate to this program's root directory. 
2. Execute ```pip install -r requirements.txt```
3. Execute ```python wikiSummaryServer.py```
4. The server is now listening for client connections 
5. Client sockets of Internet address family IPv4 and socket type TCP can make requests to the server using simple JSON serialized messages. Example ```{"url" : "https://en.wikipedia.org/wiki/New_York_(state)"}```
6. Try initiating a client/server connection by using testClient.py. Execute ```python testClient.py```. 
7. The client receives a simple JSON serialized response in the format: ```{"title" : "TITLE_OF_WIKIPEDIA_ARTICLE", "summary" : "SUMMARY_OF_WIKIPEDIA_ARTICLE}```
