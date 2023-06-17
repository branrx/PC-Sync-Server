import client
import threading

clientObject = client.Client()
threading.Thread(target=clientObject.pullRequest()).start()