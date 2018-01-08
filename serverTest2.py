import socketserver
import sched, time
import subprocess
from datetime import datetime, date

class MyTCPHandler(socketserver.StreamRequestHandler):
    
    @classmethod
    def startRecord(self,channel,duration):
        print('This is now recording')
        subprocess.run("C:\Program Files (x86)\WinTV\WinTV8\WinTVRec.exe -channel:{} -startr:pyTest2 -limit:{}".format(str(channel, "utf-8"),str(duration, "utf-8")))
        return

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.channel = self.rfile.readline().strip()
        self.timeRecord = self.rfile.readline().strip()
        self.dateRecord = self.rfile.readline().strip()
        self.duration = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        print(str(self.channel, "utf-8"))
        print("{} {}".format(str(self.dateRecord,"utf-8"), str(self.timeRecord,"utf-8")))
        print(str(self.dateRecord, "utf-8"))
        print(str(self.timeRecord, "utf-8"))
        print(str(self.duration, "utf-8"))
        cal3 = datetime.strptime("{} {}".format(str(self.dateRecord,"utf-8"), str(self.timeRecord,"utf-8")),"%Y-%m-%d %H:%M")
        print('year: %s month: %s day: %s hour: %s minute: %s second: %s' %(cal3.year, cal3.month, cal3.day, cal3.hour, cal3.minute, cal3.second))
        s = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)
        #startRecord()
        s.enterabs(cal3.timestamp(),1,MyTCPHandler.startRecord,(self.channel,self.duration))
        s.run()
        

if __name__ == "__main__":
    HOST, PORT = "192.168.43.34", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()