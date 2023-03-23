from tkinter import *
from socket import *
from threading import *
from tkinter.scrolledtext import ScrolledText
from MainRes import Main
    
class Client(Thread):
  def __init__(self):
    Thread.__init__(self)
    self.game : Main
    self.fin = False
    self.lancement = False

  # Activité du thread
  def run(self):
    self.client = socket()
    try:
      self.client.connect(('localhost', 3000))
      # self.client.listen(5)
      print("client connecté !")
      while True:
        message = self.client.recv(1024).decode(encoding="utf8")
        if message == "lancement":
          self.game = Main()
    except ConnectionRefusedError:
      print("Connexion au serveur échouée")
    finally: 
      self.client.close()

app = Client().start()
    