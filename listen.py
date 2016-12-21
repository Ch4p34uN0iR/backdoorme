import socket
import time
import sys
import os
import cmd
import pexpect
#First argument - port 
#Second argument - password
#third - if it has a prompt or not, defaults to some (meaning it has a prompt)

class Interpreter(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "# "
        self.bind()
        self.initLines = ""
        if sys.argv[2] == "none":
            if(sys.argv[3] == "some"):
                self.initLines = self.sock[0].recv(0x10000) # the lines given from the beginning
        else: #The second argument is a password; if the program requires a password.
            if(sys.argv[3] == "some"):
                self.initLines = self.sock[0].recv(0x10000)
                self.sock[0].send(sys.argv[2] + '\n')
                time.sleep(.25)
                self.initLines += self.sock[0].recv(0x10000)
            else:
                self.sock[0].send(sys.argv[2] + '\n')
                time.sleep(.25)
                self.initLines += self.sock[0].recv(0x10000)

    def bind(self): #set up a connection
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = sys.argv[1]
        self.s.bind(("0.0.0.0", int(self.port)))
        self.s.listen(5)
        self.sock = self.s.accept()
        time.sleep(.25)

    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            print("\n" + "Disconnect your shell using Ctrl+]")
            self.cmdloop()

    def specialPrint(self, lines):
        for line in lines.split('\n'):
            if(not(line[:-1] in self.initLines)): #if it's an initialization line
                print line


    def default(self, line):
        try:
            self.sock[0].send(line + '\n')
            time.sleep(.25) #fix this to make it dynamic
            self.specialPrint(self.sock[0].recv(0x10000))
        except Exception as e:
            print(e.__class__, ":", e)
            
def main():
    Interpreter().cmdloop()

if __name__ == "__main__":
    main()