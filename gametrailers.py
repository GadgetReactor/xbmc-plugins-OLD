# GameTrailer Script
# based on Apple Quicktime Trailers page by Darkie
# modified for gamespot by jsd (jsd@gamespot.com)
# modified for gametrailers by Sean

from string import *
import urllib, re, random, os
import xbmc, xbmcgui

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

if not Emulating:
	ROOT_DIR = "Q:\\scripts\\GameTrailers\\"
else:
	ROOT_DIR = "D:\\Downloads\\XBMC\\scripts\\GameTrailers\\"

NewestURL  = "http://www.gametrailers.com/iframe.php?p="
ComingURL  = "http://www.gametrailers.com/"
VaultURL   = "http://www.gametrailers.com/gamepage.php?id="
DownloadURL   = "http://www.gametrailers.com/player.php?type=mov&id="
PopularURL = "http://www.gametrailers.com/top20.php"

#Choose 0 to stream, 1 to download
CONTROL_DOWNLOAD = 1
SAVE_PATH = "F:\\Videos\\"

movies = []
images = []

# Movie class
class Movie:
	def __init__(self, name, url):
		self.name = name
		self.url = url

# parse the COMING INTERACTIONS page up into blocks for parsing
def ParseMovies(URL):
	if not Emulating:
		progress = xbmcgui.DialogProgress()
		progress.create("GameTrailers", "Grabbing information...")
	f = urllib.urlopen(URL)
	data = f.read()
	f.close()

	xRE = re.compile('gamepage\.php\?id=(.*?)" class="quartercontent">(.*?)</a>')

	links = xRE.findall(data)
	for link in links:
		url = VaultURL + link[0]
		tmp = Movie(link[1], url)
		movies.append(tmp)

	if not Emulating:
		progress.close()

# parse the NEWEST page up into blocks for parsing
def ParseNewest(URL):
	if not Emulating:
                progress = xbmcgui.DialogProgress()
		progress.create("GameTrailers", "Grabbing information...")
	f = urllib.urlopen(URL)
	data = f.read()
	f.close()

	xRE = re.compile('gamepage.php\?id=(.+?)">(.+?)<')
	
	links = xRE.findall(data)
	for link in links:
		test = True
		url = VaultURL + link[0]
		tmp = Movie(link[1], url)
		for i in movies:
			if i.name == link[1]:
				test = False
		if test:
			movies.append(tmp)

	if not Emulating:
		progress.close()

# parse the FEATURED page up into blocks for parsing
def ParseFeatured(URL):
	if not Emulating:
		progress = xbmcgui.DialogProgress()
		progress.create("GameTrailers", "Grabbing information...")

	f = urllib.urlopen(URL)
	data = f.read()
	f.close()

	xRE = re.compile('<a class="featured".+id=(.+)">(.+)</a>')

        url = "temp"
	links = xRE.findall(data)
	for link in links: 		
		tmp = Movie(link[1], url)
		movies.append(tmp)

	xRE2 = re.compile('player.php\?id=(.+?)&type=mov.+moses/moviesthumbs/(.+?)\.jpg')

	link2s = xRE2.findall(data)
	for i in range (0, len(link2s)):
		url1 = "http://www.gametrailers.com/moses/moviesthumbs/" + link2s[i][1] + ".jpg"
                url2 = DownloadURL + link2s[i][0]
                movies[i].url = url2
		images.append(url1)

	if not Emulating:
		progress.close()

def ParseAlphabet(alpha, num):
	if not Emulating:
		progress = xbmcgui.DialogProgress()
		progress.create("GameTrailers", "This will take some time...")
			
	URL = "http://www.gametrailers.com/vault.php?letter=" + alpha + "&p=&s=" + num
	f = urllib.urlopen(URL)
	data = f.read()
	f.close()

	xRE = re.compile('gamepage\.php\?id=(.+)" class="vaultname">(.+)</a>')

	links = xRE.findall(data)
	for link in links: 
		url = VaultURL + link[0]
		tmp = Movie(link[1], url)
		movies.append(tmp)
		
	m = re.search ('Page (\d) of (\d)', data)

	if not Emulating:
		progress.close()
				
	if m.group(1) < m.group(2):
		ParseAlphabet(alpha, str(int(num)+30))


def GrabURL (URL):
	if not Emulating:
		progress = xbmcgui.DialogProgress()
		progress.create("GameTrailers", "Grabbing information...")
	f = urllib.urlopen(URL)
	data = f.read()
	f.close

	xRE = re.compile('http://trailers.gametrailers.com/gt_vault/(.+).mov"')

	links = xRE.findall(data)
	
	url = "http://trailers.gametrailers.com/gt_vault/" + links[0] + ".mov"

	if not Emulating:
		progress.close()
	return url
					
class GameTrailer(xbmcgui.Window):
	def __init__(self):
	
		if Emulating: xbmcgui.Window.__init__(self)

		self.X = ( float(self.getWidth())  / float(720) )
		self.Y = ( float(self.getHeight()) / float(480) )
		
		self.DOWNLOAD = CONTROL_DOWNLOAD
		self.filename = ""
		
		self.addControl(xbmcgui.ControlImage(0,0,int(720*self.X),int(480*self.Y), ROOT_DIR + "background.jpg"))
		self.list = xbmcgui.ControlList(int(206*self.X), int(100*self.Y), int(446*self.X), int(350*self.Y))
                self.list2 = xbmcgui.ControlList(int(206*self.X), int(100*self.Y), int(446*self.X), int(350*self.Y))
		
                self.btnBack      = xbmcgui.ControlButton(int(60*self.X), int(100*self.Y), int(140*self.X), int(30*self.Y), "Back...     ")     
		self.btnFeatured  = xbmcgui.ControlButton(int(60*self.X), int(100*self.Y), int(140*self.X), int(30*self.Y), "Featured    ")     
		self.btnNewest    = xbmcgui.ControlButton(int(60*self.X), int(132*self.Y), int(140*self.X), int(30*self.Y), "Newest      ")
		self.btnComing    = xbmcgui.ControlButton(int(60*self.X), int(164*self.Y), int(140*self.X), int(30*self.Y), "Coming Soon ")
		self.btnPopular   = xbmcgui.ControlButton(int(60*self.X), int(196*self.Y), int(140*self.X), int(30*self.Y), "Most Popular")
		self.btnListAll   = xbmcgui.ControlButton(int(60*self.X), int(228*self.Y), int(140*self.X), int(30*self.Y), "List All    ")
		self.btnOptions   = xbmcgui.ControlButton(int(60*self.X), int(292*self.Y), int(140*self.X), int(30*self.Y), "Options     ")
		self.btnPlayback  = xbmcgui.ControlButton(int(60*self.X), int(324*self.Y), int(140*self.X), int(30*self.Y), "Playback D/L")
                self.btnSave      = xbmcgui.ControlButton(int(60*self.X), int(356*self.Y), int(140*self.X), int(30*self.Y), "Save As.... ")

		self.loadmenu()       

		ParseFeatured(ComingURL)

		if not Emulating:
			progress = xbmcgui.DialogProgress()
			progress.create("GameTrailers", "Downloading pictures...")
				
		for i in range (0,len(images)):
			self.downloadImg (images[i], ROOT_DIR + "temp" + str(i+1) + ".jpg")
	
		self.addFeat()

		self.list.reset()

		if not Emulating:
			progress.close()

		self.setFocus(self.btnFeatured)

	def loadmenu(self):
		self.addControl(self.list)
		self.addControl(self.btnFeatured)
		self.addControl(self.btnNewest)
		self.addControl(self.btnComing)
		self.addControl(self.btnPopular)
		self.addControl(self.btnListAll)
		self.addControl(self.btnOptions)
		self.addControl(self.btnPlayback)
		self.addControl(self.btnSave)

		self.list.controlLeft(self.btnFeatured)

		self.btnFeatured.controlUp(self.btnSave)
		self.btnFeatured.controlDown(self.btnNewest)    

		self.btnNewest.controlUp(self.btnFeatured)
		self.btnNewest.controlDown(self.btnComing)      

		self.btnComing.controlUp(self.btnNewest)
		self.btnComing.controlDown(self.btnPopular)     

		self.btnPopular.controlUp(self.btnComing)
		self.btnPopular.controlDown(self.btnListAll)

		self.btnListAll.controlUp(self.btnPopular)
		self.btnListAll.controlDown(self.btnOptions)    
		
		self.btnOptions.controlUp(self.btnListAll)
		self.btnOptions.controlDown(self.btnPlayback)
		
		self.btnPlayback.controlUp(self.btnOptions)
		self.btnPlayback.controlDown(self.btnSave)

		self.btnSave.controlUp(self.btnPlayback)
		self.btnSave.controlDown(self.btnFeatured) 

	def addFeat(self):
		self.pic1 = xbmcgui.ControlImage(int(225*self.X),int(130*self.Y),0,0, ROOT_DIR + "temp1.jpg")
		self.pic2 = xbmcgui.ControlImage(int(445*self.X),int(130*self.Y),0,0, ROOT_DIR + "temp2.jpg")
		self.pic3 = xbmcgui.ControlImage(int(225*self.X),int(280*self.Y),0,0, ROOT_DIR + "temp3.jpg")
		self.pic4 = xbmcgui.ControlImage(int(445*self.X),int(280*self.Y),0,0, ROOT_DIR + "temp4.jpg")

		self.addControl(self.pic1)
		self.addControl(self.pic2)
		self.addControl(self.pic3)
		self.addControl(self.pic4)

		self.Hlight1 = xbmcgui.ControlButton(int(225*self.X), int(100*self.Y), int(169*self.X), int(30*self.Y), movies[0].name)
		self.Hlight2 = xbmcgui.ControlButton(int(445*self.X), int(100*self.Y), int(169*self.X), int(30*self.Y), movies[1].name)
		self.Hlight3 = xbmcgui.ControlButton(int(225*self.X), int(250*self.Y), int(169*self.X), int(30*self.Y), movies[2].name)
		self.Hlight4 = xbmcgui.ControlButton(int(445*self.X), int(250*self.Y), int(169*self.X), int(30*self.Y), movies[3].name)

		self.addControl(self.Hlight1)
		self.addControl(self.Hlight2)
		self.addControl(self.Hlight3)
		self.addControl(self.Hlight4)

		self.btnFeatured.controlRight(self.Hlight1)
		self.btnNewest.controlRight(self.Hlight1)
		self.btnComing.controlRight(self.Hlight1)
		self.btnPopular.controlRight(self.Hlight1)
		self.btnListAll.controlRight(self.Hlight1) 
		self.btnOptions.controlRight(self.Hlight1)
		self.btnPlayback.controlRight(self.Hlight1)
		self.btnSave.controlRight(self.Hlight1)

		self.Hlight1.controlDown(self.Hlight3)
		self.Hlight1.controlLeft(self.btnFeatured)
		self.Hlight1.controlRight(self.Hlight2)

		self.Hlight2.controlDown(self.Hlight4)
		self.Hlight2.controlLeft(self.Hlight1)

		self.Hlight3.controlUp(self.Hlight1)
		self.Hlight3.controlLeft(self.btnFeatured)
		self.Hlight3.controlRight(self.Hlight4)

		self.Hlight4.controlUp(self.Hlight2)
		self.Hlight4.controlLeft(self.Hlight3)

	def removePics(self):
		if (len(images) > 0):   
			self.removeControl(self.pic1)
			self.removeControl(self.pic2)
			self.removeControl(self.pic3)
			self.removeControl(self.pic4)
			self.removeControl(self.Hlight1)
			self.removeControl(self.Hlight2)
			self.removeControl(self.Hlight3)
			self.removeControl(self.Hlight4)
			
		for i in range (0, len(images)):
			images.pop()

		self.btnFeatured.controlRight(self.list)
		self.btnNewest.controlRight(self.list)
		self.btnComing.controlRight(self.list)
		self.btnPopular.controlRight(self.list)
		self.btnListAll.controlRight(self.list)
		self.btnOptions.controlRight(self.list)
		self.btnPlayback.controlRight(self.list)
		self.btnSave.controlRight(self.list)
		
	def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()

	def onControl(self, control):

		if control == self.list:
			self.ListMedia(movies[self.list.getSelectedPosition()].url)
			self.filename = movies[self.list.getSelectedPosition()].name

		elif control == self.btnFeatured:

			self.list.reset()
			self.removePics()
			for i in range(0, len(movies)):
				movies.pop()

			ParseFeatured(ComingURL)

			if not Emulating:
				progress = xbmcgui.DialogProgress()
				progress.create("GameTrailers", "Downloading pictures...")
			
			for i in range (0,len(images)):
				self.downloadImg (images[i], ROOT_DIR + "temp" + str(i+1) + ".jpg") 

			self.addFeat()

			self.list.reset()

			if not Emulating:
				progress.close()

			self.setFocus(self.Hlight1)


		elif control == self.btnNewest:

			self.list.reset()
			self.removePics()
			for i in range(0, len(movies)):
				movies.pop()

			ParseNewest(NewestURL)

			for m in movies:
				self.list.addItem(m.name)

		elif control == self.btnComing:

			self.list.reset()
			self.removePics()
			for i in range(0, len(movies)):
				movies.pop()

			ParseMovies(ComingURL)

			for m in movies:
				self.list.addItem(m.name)

		elif control == self.btnPopular:

			self.list.reset()
			self.removePics()
			for i in range(0, len(movies)):
				movies.pop()

			ParseNewest(PopularURL)

			for m in movies:
				self.list.addItem(m.name)

		elif control == self.btnListAll:
						
			self.list.reset()
			self.removePics()
			for i in range(0, len(movies)):
				movies.pop()

			keyboard = xbmc.Keyboard("")
			keyboard.doModal()
						
			if (keyboard.isConfirmed()):
							
				temp = keyboard.getText()
							
				if 'A' <= temp[0] <= 'Z':
					key = temp[0]
				if 'a' <= temp[0] <= 'z':
					key = upper(temp[0])
				if '0' <= temp[0] <= '9':
					key = "0-9"

				ParseAlphabet(key, "0")

				for m in movies:
					self.list.addItem(m.name)

		elif control == self.btnSave:
                    
                        if os.path.exists(ROOT_DIR + "temp.mov"):
                                infile = open(ROOT_DIR + "temp.mov", "rb")

                                keyboard = xbmc.Keyboard(self.filename + " del this")			
                                keyboard.doModal()
		
                                if (keyboard.isConfirmed()):
                                        temp = keyboard.getText()

					if os.path.exists(SAVE_PATH + temp + ".mov"):
						self.message ("Filename already exists")
                                        
					else:
						if not Emulating:
							progress = xbmcgui.DialogProgress()
							progress.create("GameTrailers", "Saving...")
						outfile = open(SAVE_PATH + temp + ".mov", "wb")
                                        	x = infile.read(10)
                                        	while x != "":
                                               		outfile.write(x)
                                               		x = infile.read(10)
                                        	outfile.close()
						if not Emulating:		
							progress.close()

				else:
					self.message("weird")
					print keyboard.getText()
                                infile.close()
				
                        else:
                                self.message ("No clips were previously downloaded")


		elif control == self.btnOptions:

			dialog = xbmcgui.Dialog()
			if dialog.yesno("Download Options", "Do you wish to download the file first before playing?"):
				self.DOWNLOAD = 1
			else:
				self.DOWNLOAD = 0

		elif control == self.btnPlayback:
			if os.path.exists(ROOT_DIR + "temp.mov"):
				xbmc.Player().play(ROOT_DIR + "temp.mov")
			else:
				self.message("No clips were previously downloaded")

		elif control == self.Hlight1:
			self.Play(movies[0].url)
			self.filename = movies[0].name

		elif control == self.Hlight2:
			self.Play(movies[1].url)
			self.filename = movies[1].name

		elif control == self.Hlight3:
			self.Play(movies[2].url)
			self.filename = movies[2].name

		elif control == self.Hlight4:
			self.Play(movies[3].url)
			self.filename = movies[3].name
						
		elif control == self.list2:
			self.Play(movies[self.list2.getSelectedPosition()].url)
			self.filename = self.filename + " " + movies[self.list2.getSelectedPosition()].name    
		
                elif control == self.btnBack:
                        self.removeControl(self.list2)
			self.removeControl(self.btnBack)
			self.loadmenu()
			self.setFocus(self.btnFeatured)
                                                

	def ListMedia(self, URL):
		self.ParseGamepage(URL)
		self.removeControl(self.list)
		self.addControl(self.list2)

                self.addControl(self.btnBack)
		self.btnBack.controlRight(self.list2)
		self.list2.controlLeft(self.btnBack)
		self.setFocus(self.btnBack)
		
                self.removeControl(self.btnFeatured)
		self.removeControl(self.btnNewest)
		self.removeControl(self.btnComing)
		self.removeControl(self.btnPopular)
		self.removeControl(self.btnListAll)
		self.removeControl(self.btnOptions)
		self.removeControl(self.btnPlayback)
		self.removeControl(self.btnSave)

		for m in movies:
			self.list2.addItem(m.name)
			

	def Play(self, movie):
		temp = GrabURL (movie)
		if self.DOWNLOAD == 1:
			self.download_file(ROOT_DIR + "temp.mov", temp)
			xbmc.Player().play(ROOT_DIR + "temp.mov")
		else:
			xbmc.Player().play(temp)
		
	def downloadImg(self,source, destination):        
		try:
			loc = urllib.URLopener()
			loc.retrieve(source, destination)

		except:
			self.message("Download failed. Check your internet connection and try again later.")

	def message(self, messageText):
		dialog = xbmcgui.Dialog()
		dialog.ok(" GameTrailers for XBMC", messageText)

	def ParseGamepage (self, URL):
		if not Emulating:
			progress = xbmcgui.DialogProgress()
			progress.create("GameTrailers", "Grabbing information...")

		for i in range(0, len(movies)):
			movies.pop()

		f = urllib.urlopen(URL)
		data = f.read()
		f.close

		xRE = re.compile('<a target="_blank" href="player.php\?id=(.+)&type=mov')
		xRE2 = re.compile('gamepage"><b>(.+)</b>')
		links = xRE.findall(data)
		
		for link in links: 
			url = DownloadURL + link
			tmp = Movie("temporary", url)
			movies.append(tmp)
	
		link2s = xRE2.findall(data)
		for i in range (0, len(link2s)):
			movies[i].name = link2s[i]
			
		if not Emulating:
			progress.close()


	def download_file(self,file_path,file_url):
		if not Emulating:
			progress = xbmcgui.DialogProgress()
			progress.create("GameTrailers", "Downloading file...")
			
		outputFile = open(file_path,"wb")
		
		webPage = urllib.urlopen(file_url)
		#data = filedata.read()
		numBytes = 0
		loop = 1
		first = 1
		if webPage.headers.has_key('Content-Length') == 0:
			if not Emulating:
				error1 = xbmcgui.Dialog()
				error1.ok("iFilmBrowser", "Too many connections to the server.Please try later.")
				error1.close()
			return 0
		
		filesize = webPage.headers['Content-Length']
		while loop:
			data = webPage.read(50000)
			if first == 1:
				if find(data,'Too many connections!') != -1:
					if not Emulating:
						error2 = xbmcgui.Dialog()
						error2.ok("GameTrailers", "Too many connections to the server. Please try later.")
						error2.close()
				first = 0
			
			if not data:
				break
			
			outputFile.write(data)
			numBytes = numBytes + len(data)
				
			perc = int ((numBytes*100) / int(filesize))
			if not Emulating:
				progress.update(perc)
				
			print ('percentage complete ' + str(perc))
				
		webPage.close() 
		outputFile.close
		if not Emulating:
			progress.close()
		return 1

w = GameTrailer()
w.doModal()

del w
