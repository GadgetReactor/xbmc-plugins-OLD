from string import *
import urllib, re, random, os
import xbmc, xbmcgui
import zipfile

try: Emulating = xbmcgui.Emulating
except: Emulating = False

ACTION_MOVE_LEFT       =  1 
ACTION_MOVE_RIGHT      =  2
ACTION_MOVE_UP         =  3
ACTION_MOVE_DOWN       =  4
ACTION_PAGE_UP         =  5
ACTION_PAGE_DOWN       =  6
ACTION_SELECT_ITEM     =  7
ACTION_HIGHLIGHT_ITEM  =  8
ACTION_PARENT_DIR      =  9
ACTION_PREVIOUS_MENU   = 10
ACTION_SHOW_INFO       = 11
ACTION_PAUSE           = 12
ACTION_STOP            = 13
ACTION_NEXT_ITEM       = 14
ACTION_PREV_ITEM       = 15


#GLOBAL VARIABLES
if Emulating:
    ROOT_DIR = "D:\\Downloads\\XBMC\\scripts\\gamesaves\\"
    SAVES_DIR = "D:\\Downloads\\XBMC\\scripts\\gamesaves\\"
    TRAINER_DIR = "D:\\Downloads\\XBMC\\scripts\\gamesaves\\trainers\\"
else:
    ROOT_DIR = "Q:\\scripts\\gamesaves\\"
    SAVES_DIR = "E:\\"
    TRAINER_DIR = "E:\\Dash\\Evox\\Trainers\\"
    
searchURL = "http://www.xbox-saves.com/pafiledb/pafiledb.php?action=search&search=do&string="
downloadURL = "http://www.xbox-saves.com/pafiledb/pafiledb.php?action=download&id="
# trainerURL = "http://www.ek-clan.vxcomputers.com/Trainers/"
trainerURL = "http://www.anime-gallore.com/Files/"

class Save:
	def __init__(self, name, id, desc):
		self.name = name
		self.id = id
		self.desc = desc


class GameSaves(xbmcgui.Window):
	def __init__(self):
		if Emulating: xbmcgui.Window.__init__(self)

		self.X = ( float(self.getWidth())  / float(720) )
		self.Y = ( float(self.getHeight()) / float(480) )
		self.saves = []
		self.status = "SAVE"

		if not os.path.exists(ROOT_DIR):
                	os.makedirs(ROOT_DIR)

		if not os.path.exists(TRAINER_DIR):
                	os.makedirs(ROOT_DIR)

		self.addControl(xbmcgui.ControlImage(0,0,int(720*self.X),int(480*self.Y), "background.png"))
		self.list = xbmcgui.ControlList(int(211*self.X), int(100*self.Y), int(450*self.X), int(350*self.Y))
                self.btnSearch  = xbmcgui.ControlButton(int(60*self.X), int(100*self.Y), int(140*self.X), int(30*self.Y), "Search")     
                self.btnRestore = xbmcgui.ControlButton(int(60*self.X), int(132*self.Y), int(140*self.X), int(30*self.Y), "Restore")     
                self.btnClear   = xbmcgui.ControlButton(int(60*self.X), int(164*self.Y), int(140*self.X), int(30*self.Y), "Clear Backup")     
                self.btnTrainer = xbmcgui.ControlButton(int(60*self.X), int(228*self.Y), int(140*self.X), int(30*self.Y), "Trainers")     
                self.btnOptions = xbmcgui.ControlButton(int(60*self.X), int(260*self.Y), int(140*self.X), int(30*self.Y), "Options")     
			
		self.addControl(self.list)
		self.addControl(self.btnSearch)
		self.addControl(self.btnRestore)
		self.addControl(self.btnClear)
		self.addControl(self.btnTrainer)
		self.addControl(self.btnOptions)

		self.list.controlLeft(self.btnSearch)
		
		self.btnSearch.controlUp(self.btnOptions)
		self.btnSearch.controlDown(self.btnRestore)
		self.btnSearch.controlRight(self.list)

		self.btnRestore.controlUp(self.btnSearch)
		self.btnRestore.controlDown(self.btnClear)
		self.btnRestore.controlRight(self.list)

		self.btnClear.controlUp(self.btnRestore)
		self.btnClear.controlDown(self.btnTrainer)
		self.btnClear.controlRight(self.list)

		self.btnTrainer.controlUp(self.btnClear)
		self.btnTrainer.controlDown(self.btnOptions)
		self.btnTrainer.controlRight(self.list)

		self.btnOptions.controlUp(self.btnTrainer)
		self.btnOptions.controlDown(self.btnSearch)
		self.btnOptions.controlRight(self.list)

		self.setFocus(self.btnSearch)

	def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()

	def onControl(self, control):

		if control == self.list:
			index = self.list.getSelectedPosition()
			if self.status == "SAVE":
        			self.downloadZip(downloadURL + self.saves[index].id)

        		elif self.status == "TRAINER":
                                self.downloadZip(self.saves[index].id)
                        zip = zipfile.ZipFile(ROOT_DIR + 'temp.zip', 'r')
                        self.unzip(zip)
                        zip.close()
			self.message ("Done. Please try the game to ensure save/trainer is working.")

		elif control == self.btnSearch:
                        self.status = "SAVE"
                        self.list.reset()
                        self.saves[:] = []
			keyboard = xbmc.Keyboard("")			
			keyboard.doModal()
			if (keyboard.isConfirmed()):
				
				self.ParseSearch(keyboard.getText())
                                for i in self.saves:
                                        self.list.addItem(i.name + " ::: " + i.desc)

                elif control == self.btnRestore:
                        self.restore()

                elif control == self.btnClear:
                        self.clear()

                elif control == self.btnTrainer:
                        self.status = "TRAINER"
                        self.list.reset()
			self.saves[:] = []
			self.ParseTrainer()
			for i in self.saves:
                        	self.list.addItem(i.name + " ::: " + i.desc)

		elif control == self.btnOptions:
                        if not Emulating:
                                self.message ("Please ensure input is accurate. Use double forward slashes")
			if os.path.exists("Q:\\scripts\\gamesaves.py"):
				f = open("Q:\\scripts\\gamesaves.py", "r")
				data = f.read()
				f.close()
				links = re.findall('TRAINER_DIR = "(.+)"', data)
				if Emulating:
                                	current = links[0]
                        	else:
                                	current = links[1]
                                
                        	keyboard = xbmc.Keyboard(current)			
				keyboard.doModal()
			
				if (keyboard.isConfirmed()):
					new = keyboard.getText()
					data = replace(data ,"TRAINER_DIR = " + current, "TRAINER_DIR = " + new)
					f = open("gamesaves.py", "w")
					f.write(data)
					f.close()
                        if not Emulating:
                                self.message ("Done")
				
	def message(self, messageText):
		dialog = xbmcgui.Dialog()
		dialog.ok(" GameSaves for XBMC", messageText)

	def unzip(self, zip):
		if not Emulating:
			progress = xbmcgui.DialogProgress()
			progress.create("GameSaves", "Unzipping + backing up...")

                if self.status == "SAVE":
                         for each in zip.namelist():
                                name = replace(each ,"/", "\\")
                                get_dir = re.search ('(.+)\\\\', name)
        		
                                if not get_dir == None:
                                        dir_name = SAVES_DIR + get_dir.group(1) + "\\"
            			
                                        if not os.path.exists(dir_name):
                                                os.makedirs(dir_name)
                			
                                        if not each.endswith("/"):
                                                if each.startswith("UDATA") or each.startswith("TDATA"):
                                                        self.createBackup (SAVES_DIR + name)
                                                        temp = open(SAVES_DIR + name, "wb")
                                                        temp.write(zip.read(each))
                                                        temp.close()

                elif self.status == "TRAINER":
                        for each in zip.namelist():
                                temp = open(TRAINER_DIR + each, "wb")
                                temp.write(zip.read(each))
                                temp.close()
                                if each.endswith(".nfo"):
                                        nfo = each
                        		self.printNFO(nfo)
	
		if not Emulating:
			progress.close()


	def downloadZip(self, source):
		if not Emulating:
			progress = xbmcgui.DialogProgress()
			progress.create("GameSaves", "Downloading save...")
		f = urllib.urlopen(source)
                real = f.geturl()
                f.close()
		real = replace (real, " ", "%20")
                dl = urllib.URLopener()
                dl.retrieve(real, ROOT_DIR + "temp.zip")
		if not Emulating:
			progress.close()

        def ParseSearch(self, search):
		if not Emulating:
			progress = xbmcgui.DialogProgress()
			progress.create("GameSaves", "Grabbing available saves...")
                search = replace(search," ", "%20")
                
		URL = searchURL + search
		f = urllib.urlopen(URL)
                data = f.read()
                f.close()

		namesRE    = re.compile ('pafiledb.php\?action=file&id=(.+?)">(.+?)<')
		descripsRE = re.compile ('<a class="smalltext">(.+)<')
		
		names = namesRE.findall(data)
		descrips = descripsRE.findall(data)
		
		for name in names:
			tmp = Save (name[1], name[0], "")
			self.saves.append (tmp)

		for i in range (0, len(descrips)):
			self.saves[i].desc = descrips[i]

		if not Emulating:
			progress.close()

	def createBackup(self, source):
                backuplog = open(ROOT_DIR + "backup.log", "a")
                backuplog.write (source)
                backuplog.write ("\n")
                
                self.fileHandler (source, source + ".bak")
                backuplog.close()

        def fileHandler (self, source, destination):
                if os.path.exists (source):
                        infile = open(source, "rb")
                        outfile = open(destination, "wb")
                        x = infile.read(10)
                        while x != "":
                                outfile.write(x)
                                x = infile.read(10)
                        infile.close()
                        outfile.close()
        
        def restore(self):
		if not Emulating:
			progress = xbmcgui.DialogProgress()
			progress.create("GameSaves", "Restoring...")
		backuplog = open(ROOT_DIR + "backup.log", "r")               
                
                data = backuplog.readline()
                while data != "":
                        data = replace (data, "\n", "")
                        if os.path.exists (data):
                                os.remove(data)
                                print "deleted " + data
                        self.fileHandler (data + ".bak", data)
                        if os.path.exists (data + ".bak"):
                                os.remove(data + ".bak")
                                print "replaced with backup"
                        data = backuplog.readline()
                backuplog.close()
                new = open(ROOT_DIR + "backup.log", "w")
		self.message ("Files restored and backups cleared")
		if not Emulating:
			progress.close()

        def clear(self):
		if not Emulating:
			progress = xbmcgui.DialogProgress()
			progress.create("GameSaves", "Deleting backups...")
                backuplog = open(ROOT_DIR + "backup.log", "r")

                data = backuplog.read()
                while data != "":
                        data = replace (data, "\n", ".bak")
                        if os.path.exists (data):
                                os.path.remove(data)
			data = backuplog.read()

                backuplog.close()
                new = open(ROOT_DIR + "backup.log", "w")
		self.message ("Backups Cleared.")
		if not Emulating:
			progress.close()

	def ParseTrainer(self):
		if not Emulating:
			progress = xbmcgui.DialogProgress()
			progress.create("GameSaves", "Grabbing available trainers...")
                
		trainerURL2 = 'http://trainers.maxconsole.com/index.php?order=mod&direction=0&directory=2.%20Upload%20your%20Evox%20Trainer%20Files'
		
		f = urllib.urlopen(trainerURL2)
                data = f.read()
		f.close()

		xRE = re.compile ('a href="javascript:popup\(\'(.+?)\'.+?\<BR\>(.+?)\<\/font\>',re.S)

		for m in xRE.finditer(data):
			tfile=m.group(1)
			tnpdesc=m.group(2)
			nc = re.compile ('[\n\t\r]')
			tdesc = nc.sub('', tnpdesc)
			tadd='http://trainers.maxconsole.com/index.php?action=downloadfile&filename=' + tfile + '&directory=2. Upload your Evox Trainer Files&'
			address = replace(tadd,"%20", " ")
			address = replace(address,"&amp;", "&")
			
			print tdesc
			tmp = Save (tfile, address, tdesc)
			self.saves.append (tmp)

		if not Emulating:
			progress.close()
	                
        def printNFO(self, filename):
                f  = open (TRAINER_DIR + filename)
                self.list.reset()
                data = f.readline()
                self.list.addItem(data)
                print data
                while data != "":
                        self.list.addItem(data)
                        data = f.readline()
                        print data
                        

w = GameSaves()
w.doModal()

del w

