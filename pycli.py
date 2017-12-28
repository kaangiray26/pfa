#!/usr/bin/python
#-*- encoding:utf-8 -*-
import os
import time
import prettytable
#Condition
#0->> Failure
#1->> Success
global sitelist,siterun,siteinr,sitecond,sitepath,siterunid,tryinr,dur
sitelist=[]
siterun=({})
siteinr=({})
sitecond=({})
sitepath=({})
siterunid=({})
tryinr=0
dur=0
hours=[]
cmdlist=["help","show","add","set","exit","info","restart","save","start"]
try:
    sites=open("sites.txt","r").read().splitlines()
except:
    open("sites.txt","a")
    sites=[]
try:
    optconf=open("opt.conf","r").read().splitlines()
except:
    open("opt.conf","a")
    optconf=[]
if len(sites) != 0:
    for line in sites:
        try:
            sitepath[line.split()[0]]=line.split()[1]
            sitelist.append(line.split()[0])
            siteinr[line.split()[0]]=line.split()[2]
            sitecond[line.split()[0]]=0
            siterun[line.split()[0]]="x"
            siterunid[line.split()[0]]=0
        except:
            pass
if len(optconf) != 0:
    tryinr=int(optconf[1].split()[1])
    dur=int(optconf[2].split()[1])
    for i in range(3,len(optconf)):
        if len(optconf[i].split()) == 1:
            siterun[optconf[i].split()[0]]=""
        else:
            siterun[optconf[i].split()[0]]=optconf[i].split()[1]

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#Main process
def resetrun():
    global sitelist,siterun,siteinr,sitecond,sitepath,siterunid,tryinr,dur,hours
    for site in siterunid.keys():
        siterunid[site]=0
def main():
    global sitelist,siterun,siteinr,sitecond,sitepath,siterunid,tryinr,dur,hours
    print len(sitelist)
    if len(sitelist) == 0 or int(tryinr) == 0 or int(dur) == 0:
        raise RuntimeError("No scripts given.")
        return
    print "Starting process..."
    print "Waiting..."
    a=int(24/float(tryinr))
    if a == 0:
        a=float(24/float(tryinr))
    t=0
    for i in range(0,int(tryinr)):
        t+=a
        hrs=t*60
        if type(t) == int:
            if len(str(t)) == 1:
                hours.append("%s00" %(str(t).zfill(2)))
            else:
                hours.append("%s00" %(t))
        else:
            hours.append("%s%s" %(str(t).split(".")[0].zfill(2),str(round(60*float("0.%s" %(str(t).split(".")[1])),2)).split(".")[0].zfill(2)))
    while True:
        if time.strftime("%H%M") in hours:
            start=time.strftime("%H%M")
            while True:
                runer=0
                resetrun()
                for site in sitelist:
                    if siterun[site] != "x":
                        runer+=1
                if runer == len(sitelist):
                    break
                for site in sitelist:
                    if siterunid[site]>=siteinr[site]:
                        siterun[site] == ""
                    if siterun[site] == "x":
                        if sitecond[site]==0:
                            siterunid[site]+=int(siterunid[site])+1
                            if os.popen("python %s &" %(sitepath[site])).read() == "success":
                                sitecond[site]=1
                            else:
                                sitecond[site]=0
                    if time.strftime("%H%M") == "%s%s" %(str(int(int(str(start[0:2]))*60+int(start[2:4])+dur*60)/60).zfill(2),str(int(int(str(start[0:2]))*60+int(start[2:4])+dur*60)%60)):
                        break
def add():
    global sitelist,siterun,siteinr,sitecond,sitepath,siterunid,tryinr,dur
    print color.RED+"\nName:"+color.END
    name=raw_input("pfa> ")
    print color.RED+"\nPath:"+color.END
    path=raw_input("pfa> ")
    print color.RED+"\nTimeout_interval:"+color.END
    interval=input("pfa> ")
    sitepath[name]=path
    sitelist.append(name)
    siteinr[name]=interval
    sitecond[name]=0
    siterun[name]="x"

def varset():
    global sitelist,siterun,siteinr,sitecond,sitepath,siterunid,tryinr,dur
    print color.UNDERLINE+"Select one from these items:\n"+color.END
    for i in sitelist:
        print color.RED +"*"+color.END+color.BOLD+i+color.END
    print color.RED + "*"+color.END + color.BOLD + "Try_interval"+color.END
    print color.RED + "*"+color.END + color.BOLD + "Duration\n"+color.END
    opt=raw_input("pfa> ")
    if opt in sitelist:
        site=opt
        print color.UNDERLINE+"Select one from these items:\n"+color.END
        print color.RED + "*"+color.END+color.BOLD +"Name"+color.END
        print color.RED + "*"+color.END+color.BOLD+"Run"+color.END
        print color.RED + "*"+color.END+color.BOLD+"Timeout_interval"+color.END
        print color.RED + "*"+color.END+color.BOLD+"Path"+color.END
        opt=raw_input("pfa> ")
        if opt=="Name":
            print color.RED+"\nType new name:"+color.END
            opt=raw_input("pfa> ")
            sitepath[opt]=sitepath[site]
            sitelist.append(opt)
            siteinr[opt]=siteinr[site]
            sitecond[opt]=sitecond[site]
            siterun[opt]=sitecond[site]
            #Remove old packages
            del sitepath[site]
            sitelist.remove(site)
            del siteinr[site]
            del sitecond[site]
            del siterun[site]
        if opt=="Run":
            print color.RED+"\nType x to mark it, or"+color.END
            print "leave it blank not to run it:"
            opt=raw_input("pfa> ")
            siterun[site]=opt
        if opt=="Path":
            print color.RED+"\nType new path:"+color.END
            opt=raw_input("pfa> ")
            sitepath[site]=opt
        if opt=="Timeout_interval":
            print color.RED+"\nType new Timeout_interval:"+color.END
            opt=input("pfa> ")
            siteinr[site]=opt
    if opt=="Try_interval":
        print color.RED+"\nType new Try_interval:"+color.END
        opt=input("pfa> ")
        tryinr=opt
    if opt=="Duration":
        print color.RED+"\nType new Duration:"+color.END
        opt=input("pfa> ")
        dur=opt

def show():
    global sitelist,siterun,siteinr,sitecond,sitepath,siterunid,tryinr,dur
    x1 = prettytable.PrettyTable(["Name","Run","Timeout_interval","Result","Path"])
    for site in sitepath.keys():
        x1.add_row([site,siterun[site],siteinr[site],sitecond[site],sitepath[site]])
    x2 = prettytable.PrettyTable(["Try_interval","Duration"])
    x2.add_row([tryinr,dur])
    print x1
    print x2

def help():
    global sitelist,siterun,siteinr,sitecond,sitepath,siterunid,tryinr,dur
    print color.UNDERLINE+"Showing help"+color.END
    print color.RED + "\n1)"+color.END + color.BOLD + "help:" + color.END + "Shows this output"
    print color.RED + "2)"+color.END +color.BOLD + "show:" + color.END + "Shows scripts and options"
    print color.RED + "3)"+color.END +color.BOLD + "add:" + color.END + "Adds new script"
    print color.RED + "4)"+color.END +color.BOLD + "set:" + color.END + "Sets a value to a variable"
    print color.RED + "5)"+color.END +color.BOLD + "info:" + color.END + "Shows info about a variable"
    print color.RED + "6)"+color.END +color.BOLD + "restart:" + color.END + "Restarts the program with default options"
    print color.RED + "7)"+color.END +color.BOLD + "save:" + color.END + "Saves the current options"
    print color.RED + "8)"+color.END +color.BOLD + "exit:" + color.END + "Exits program\n"

def restart():
    os.system("python fwtxt.py")

def info():
    print color.UNDERLINE+"Showing info"+color.END
    print color.RED + "\n1)"+color.END + color.BOLD + "Name:" + color.END + "Name of the script"
    print color.RED + "2)"+color.END + color.BOLD + "Run:" + color.END + "Decides whether to run script"
    print color.RED + "3)"+color.END + color.BOLD + "Timeout_interval" + color.END + "After a while script will stop due to timeout"
    print color.RED + "4)"+color.END + color.BOLD + "Result:" + color.END + "Result of the previous run (0:Failure / 1:Success)"
    print color.RED + "5)"+color.END + color.BOLD + "Path:" + color.END + "Path of the script file"
    print color.RED + "6)"+color.END + color.BOLD + "Try_interval:" + color.END + "Decides how many times the script will run"
    print color.RED + "7)"+color.END + color.BOLD + "Duration:" + color.END + "Decides how long the script will run in period"

def save():
    global sitelist,siterun,siteinr,sitecond,sitepath,siterunid,tryinr,dur
    os.remove("sites.txt")
    file=open("sites.txt","w")
    for site in sitelist:
        file.write("\n%s %s %s" %(site,sitepath[site],siteinr[site]))
    file.close()
    file=open("opt.conf","w")
    file.write("\ntryinr %s" %(tryinr))
    file.write("\ndur %s" %(dur))
    for site in sitelist:
        file.write("\n%s %s" %(site,siterun[site]))
    file.close()
    pass
#start
os.system("clear")
print """
  _______       __   __
 |   _   .--.--|  |_|  |--.-----.-----.
 |.  1   |  |  |   _|     |  _  |     |
 |.  ____|___  |____|__|__|_____|__|__|
 |:  |   |_____|
 |::.|
 `---'
  _______                                               __               ___
 |   _   .----.---.-.--------.-----.--.--.--.-----.----|  |--.   .-----.'  _|
 |.  1___|   _|  _  |        |  -__|  |  |  |  _  |   _|    <    |  _  |   _|
 |.  __) |__| |___._|__|__|__|_____|________|_____|__| |__|__|   |_____|__|
 |:  |
 |::.|
 `---'
  _______       __                        __   __
 |   _   .--.--|  |_.-----.--------.---.-|  |_|__.-----.-----.
 |.  1   |  |  |   _|  _  |        |  _  |   _|  |  _  |     |
 |.  _   |_____|____|_____|__|__|__|___._|____|__|_____|__|__|
 |:  |   |
 |::.|:. |
 `--- ---'
"""
show()
while True:
    ui=raw_input("pfa> ")
    if ui not in cmdlist:
        print "Command not found. Try 'help' for command list"
    if ui == "help":
        help()
    if ui == "show":
        show()
    if ui == "add":
        add()
    if ui == "set":
        varset()
    if ui == "info":
        info()
    if ui == "restart":
        restart()
    if ui == "save":
        save()
    if ui == "start":
        main()
    if ui == "exit":
        print "Good bye."
        time.sleep(0.5)
        os.popen("killall python")
        exit()
