from flask import jsonify, send_file, Blueprint, render_template, abort, request, g
import serverBackend.creds as creds
import os
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
adminPanel = Blueprint('adminPanel', __name__,
    template_folder=template_folder,
    static_folder=static_folder)

import serverBackend.data as data

@adminPanel.route('/',methods=['GET'])
def panel():
    return render_template("adminPanel.html")

@adminPanel.route('/addTeam',methods=['POST'])
def addTeam():
    if request.form["adminPass"] != creds.adminPass:
        abort(403)
    team = request.form["team"]
    if team not in data.teams.keys():
        abort(400)
    data.addTeam(team)
    return send_file("."+os.sep+"serverData.json")

@adminPanel.route('/rmTeam',methods=['POST'])
def removeTeam():
    if request.form["adminPass"] != creds.adminPass:
        abort(403)
    team = request.form["team"]
    if team not in data.teams.keys():
        abort("Invalid team given.",400)
    data.rmTeam(team)
    return send_file("."+os.sep+"serverData.json")

@adminPanel.route('/addUser',methods=['POST'])
def addUser():
    if request.form["adminPass"] != creds.adminPass:
        abort(403)
    user = request.form["user"]
    name = request.form["name"]
    pwd = request.form["password"]
    team = request.form["team"]
    if team not in data.teams.keys():
        abort(400)
    data.addMember(user,name,pwd,team)
    return send_file("."+os.sep+"serverData.json")

@adminPanel.route('/rmUser',methods=['POST'])
def removeUser():
    if request.form["adminPass"] != creds.adminPass:
        abort(403)
    user = request.form["user"]
    team = request.form["team"]
    if team not in data.teams.keys():
        abort("Invalid team given.",400)
    data.rmMember(user,team)
    return send_file("."+os.sep+"serverData.json")

@adminPanel.route('/launch',methods=['POST'])
def launchGame():
    if request.form["adminPass"] != creds.adminPass:
        abort(403)
    if data.gameStart:
        data.gameStart=False
        return "Game Stopped", 200
    else:
        data.gameStart=True
        return "Game Started", 200

@adminPanel.route('/leak',methods=['POST'])
def leak():
    if request.form["adminPass"] != creds.adminPass:
        abort(403)
    if request.form["device"] not in data.devices.keys():
        abort(400)
    device = request.form["device"]
    f = open("./forums.txt", "a")
    fillers = ["""
I am new in Ubuntu Linux, but when I following tutorial guide in https://www.pluralsight.com/courses/linux-network-client-management-lpic-2, I have to create a new VM by VBoxManage inside Ubuntu Server, but when I did these commands to create a new VM:
root@master:/home/master# ls VirtualBox\ VMs/ ubuntu-16.04.6-server-i386.iso ubuntu-server
root@master:/home/master# mv VirtualBox\ VMs/ubuntu-16.04.6-server-i386.iso VirtualBox\ VMs/ubuntu-server/
root@master:/home/master# ls VirtualBox\ VMs/ ubuntu-server
root@master:/home/master# ls VirtualBox\ VMs/ubuntu-server/ ubuntu-16.04.6-server-i386.iso ubuntu-server.vbox ubuntu-server.vbox-prev ubuntu-server.vdi
root@master:/home/master# VBoxManage storageattach ubuntu-server --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium /home/master/VirtualBox\ VMs/ubuntu-server/ubuntu-16.04.6-server-i386.iso
I get the following error:
VBoxManage: error: Could not find a registered machine named 'ubuntu-server' VBoxManage: error: Details: code VBOX_E_OBJECT_NOT_FOUND (0x80bb0001), component VirtualBoxWrap, interface IVirtualBox, callee nsISupports VBoxManage: error: Context: "FindMachine(Bstr(a->argv[0]).raw(), machine.asOutParam())" at line 325 of file VBoxManageStorageController.cpp root@master:/home/master#
I'm confused and I don't know how to troubleshoot, thank you for any help you can provide.""",
"""I have a dilemma of selecting between ubuntu edition for development server. I have seen that ubuntu server dosen't have a GUI(though can be installed later). My question : is there any specific difference in desktop and server edition that will help in development of web app?""",
"""I tried setting up a SVN Server on an old computer at home. I've newly installed the Ubuntu 20.04.1 LTS Server distribution and followed this guide. Everything worked pretty well but when I tried accessing the repository via my web browser (http://local-ip-adress/svn/project) I can access it directly without being asked for authentication."""]
    flavor=["When error occurs while creating PDO connection (using wrong driver like sqlsrv instead of dblib I get error in /var/log/httpd/error_log (CentOS).",
    "My server crashed... Whats going on!? I thought Ububtu was stable!",
    "Help! My server is acting all weird. I have no idea how to fix it. Can anyone help?"]
    leak = ["It says: [error] [client 10.10.103.16] PHP Fatal error:  Uncaught exception 'PDOException' with message 'could not find driver' in /var/www/html/index.php:1\nStack trace:\n#0 /var/www/html/index.php(1): PDO->__construct('sqlsrv:Server=O...', '"+data.devices[device]["username"]+"', '"+data.devices[device]["password"]+"')\n#1 {main}",
    "PHP Warning: mysqli::__construct(): (HY000/1045): Access denied for user '"+data.devices[device]["username"]+"'@'localhost' (using password: "+data.devices[device]["password"]+") in /home/[...]/mysqli.php on line 3",
    """[15-Apr-2014 11:28:17] PHP Fatal error:  Uncaught exception 'PDOException' with message 'SQLSTATE[HY000] [2002] Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)' in /opt/ZendFramework-1.10.8/library/Zend/Db/Adapter/Pdo/Abstract.php:129
Stack trace:
#0 /opt/ZendFramework-1.10.8/library/Zend/Db/Adapter/Pdo/Abstract.php(129): PDO->__construct('mysql:host=loca...', 'a_database', '"""+data.devices[device]["password"]+"""', Array)
#1 /opt/ZendFramework-1.10.8/library/Zend/Db/Adapter/Pdo/Mysql.php(96): Zend_Db_Adapter_Pdo_Abstract->_connect()"""]
    question=["Can anyone help me fix this?", "Does anyone know the source of the error?", "How to fix this!?", "Thanks in advance for the help."]
    f.write(random.choice(fillers))
    f.write("<br>-----------------------------------------------------------------<br>")
    f.write(random.choice(flavor))
    f.write("<br>")
    f.write(random.choice(leak))
    f.write("<br>")
    f.write(random.choice(question))
    f.write("<br>-----------------------------------------------------------------<br>")
    f.write(random.choice(fillers))
    f.write("<br>-----------------------------------------------------------------<br>")
    f.close()
    return "leaked", 200

@adminPanel.route('/data',methods=['POST'])
def getData():
    if request.form["adminPass"] != creds.adminPass:
        abort(403,"The admin page is not in scope, please don't attack it.")
    scorebot.save()
    return send_file("."+os.sep+"serverData.json")

@adminPanel.route("/history.log",methods=['POST'])
def logs():
    if request.form["adminPass"] != creds.adminPass:
        abort(403,"The admin page is not in scope, please don't attack it.")
    return send_file('./history.log')

@adminPanel.route("/registration.txt",methods=['POST'])
def registration():
    if request.form["adminPass"] != creds.adminPass:
        abort(403,"The admin page is not in scope, please don't attack it.")
    return send_file('./registration.txt')

@adminPanel.route('/loadData',methods=['POST'])
def loadData():
    if request.form["adminPass"] != creds.adminPass:
        abort(403,"The admin page is not in scope, please don't attack it.")
    manifest = request.form["manifest"]
    data.manifestLoad(manifest)
    scorebot.save()
    return send_file("."+os.sep+"serverData.json")
