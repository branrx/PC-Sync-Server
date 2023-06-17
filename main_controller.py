import server
import threading

serverObject = server.Server()
threading.Thread(target=serverObject.connection()).start()


