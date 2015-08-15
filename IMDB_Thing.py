import json
import urllib2
import requests
import sys
import ui_IMDB_Thing
from PyQt4.QtGui  import *
from PyQt4.QtCore import *
from datetime import date
import webbrowser
from GoogleSuggest import GoogleSuggest


class IMDB_Thing_Main_Window(QMainWindow,ui_IMDB_Thing.Ui_MainWindow):


	infoDict = {}
	title = ""
	windowImage = ""
	completer = QCompleter()
	model = QStringListModel()
	timer = QTimer()


	def startTimer(self):
		self.timer.start()
	def __init__(self,parent=None):
		''' initializer function '''
		super(IMDB_Thing_Main_Window,self).__init__(parent)
		self.setupUi(self)
		self.updateUi()
	def hideEverything(self):
		
		self.lb_rating.hide()
		self.plot.hide()
		self.line.hide()
		self.votes.hide()
		self.goToWebsite.hide()
		self.gfxView_poster.hide()
		self.lb_rated.hide()
		self.groupBox.hide()

	def addSuggestion(self):
		print "blah"
		q = str(self.lEdit_movieName.text())
		grabber = GoogleSuggest()
		l = grabber.read(q)	
		strlist = l
		
		#self.completer = QCompleter(strlist,self.lEdit_movieName)
		#self.lEdit_movieName.setCompleter(self.completer)
		
		#model = QStringListModel(self.completer.model())
		#model  = self.completer.model()
		qstrlist = QStringList()
		for item in strlist:
			qstrlist.append(item)
		self.model.setStringList(qstrlist)
		print l
		

	def showEverything(self):

		self.plot.show()
		self.line.show()
		self.lb_rating.show()
		self.lb_rated.show()
		self.goToWebsite.show()
		self.votes.show()
		#self.tblWd_details.show()
		self.groupBox.show()


	def getSuggestions(self,initalString):
		initalString = str(initalString)
		suggest_url = "http://suggestqueries.google.com/complete/search?output=toolbar&hl=en&q="
		if ' ' in initalString:
			initalString = initalString.replace(' ','%20')
		suggest_url = suggest_url + initalString
		xmldata = urllib2.urlopen(suggest_url).read()
		
	def setDetails(self):
		print "dummy"	
			
	def updateDetails(self,jsonValues):
		color = 'black'
		self.lb_title.setText("<font color=green>" +  jsonValues['Title'] + "</font>")		
		self.year.setText('<font color=' + color + '> '+ jsonValues['Year'] + '</font>')
		self.genre.setText('<font color=' + color +'>' + jsonValues['Genre'] + '</font>')
		self.runtime.setText('<font color=' + color +'>' + jsonValues['Runtime'] + '</font>')
		self.actors.setText('<font color=' + color+ '>' + jsonValues['Actors'] + '</font>')
		self.director.setText('<font color=' + color +'>' + jsonValues['Director'] + '</font>')
		self.awards.setText('<font color=' + color +'>' + jsonValues['Awards'] + '</font>')
		self.lb_type.setText(' <font color=' + color+ '>' + jsonValues['Type'] + '</font>')
			
		self.country.setText('<font color=' + color +'>' + jsonValues['Country'] + '</font>')
		self.language.setText('<font color=' + color +'>' + jsonValues['Language'] + '</font>')
	
	
	def setCBoxYear(self):
		
		self.CBoxYear.addItem('unknown')
		for year in range(1900,date.today().year):
			self.CBoxYear.addItem(str(year))
		self.CBoxYear.setMaxVisibleItems(10)		

	def updateUi(self):
		stringList = QStringList()
		stringList.append("yeh jawaani hai deewani")
		self.model.setStringList(stringList)
		self.completer.setModel(self.model)
		self.completer.setCaseSensitivity(Qt.CaseInsensitive)
		#self.completer.setCompletionMode(QCompleter.InlineCompletion)
		self.lEdit_movieName.setCompleter(self.completer)
		self.lEdit_movieName.installEventFilter(self)
		self.setWindowTitle(self.title)
		self.setDetails()
		self.setCBoxYear()
		self.makeConnections()
		self.lEdit_movieName.setText(" Enter movie name :)")
		self.lEdit_movieName.selectAll()
		self.lb_rating.setAutoFillBackground(True)
		self.hideEverything()
		self.resize(750,600)
		self.lb_title.setText("This page is intentionally left blank!")
		self.timer.setSingleShot(True)
		self.timer.setInterval(250)

	def makeConnections(self):


		self.connect(self.lEdit_movieName, SIGNAL("returnPressed()"),self.getAndUpdateData)
		self.connect(self.goToWebsite,SIGNAL("clicked()"),self.goToPage)
		self.connect(self.bt_go,SIGNAL("clicked()"),self.getAndUpdateData)
		self.connect(self.lEdit_movieName, SIGNAL("textEdited(QString)"),self.startTimer)
		self.connect(self.timer,SIGNAL("timeout()"),self.addSuggestion)
			
	def goToPage(self):
		
		movie_url = "http://www.imdb.com/title/" + self.infoDict['imdbID']
		webbrowser.open_new_tab(movie_url)
		print self.infoDict



	def getAndUpdateData(self):
		year = str(self.CBoxYear.itemText(self.CBoxYear.currentIndex()))
		#print "year : " ,year
		name = str(self.lEdit_movieName.text())
		if " " in name:
			name = name.replace(" ","%20")
		if year!='unknown':
			url = "http://www.omdbapi.com/?t="+name+"&y="+str(year)

		else:
			url = "http://www.omdbapi.com/?t="+name
		
		response = urllib2.urlopen(url).read()
		jsonValues = json.loads(response)
		self.infoDict = jsonValues
		print jsonValues
		if jsonValues['Response'] == 'True':
			self.updateData(jsonValues)
		else:
			self.handleError()

	def handleError(self):
		self.hideEverything()
		self.lEdit_movieName.setText("Invalid movie name! Try again ")
		self.lEdit_movieName.selectAll()
		#self.lb_title.setText("A Storm is Coming Mr. Wayne")
		self.lb_title.setText("This page is intentionally left blank!")

	def updateImage(self):
		url = self.infoDict['Poster']
		if url=='N/A':
			#self.gfxView_poster.hide()
			url = "http://i.ebayimg.com/00/s/MTAwMVgxMDAx/z/cgAAAOxy3zNSoKeD/$_12.JPG"
		scene = QGraphicsScene()
		self.gfxView_poster.setScene(scene)
		image = urllib2.urlopen(url).read()
		pixmap = QPixmap()
		pixmap.loadFromData(image)
		item  = QGraphicsPixmapItem(pixmap)
		scene.addItem(item)
		#self.gfxView_poster.fitInView(scene.itemsBoundingRect(),Qt.KeepAspectRatio)
		self.gfxView_poster.show()	
		#print image
		

	def updateData(self,jsonValues):
		self.updateImage()
		self.plot.setText("<font>" + jsonValues['Plot']+ "</font>")
		self.lb_rating.setText("<font color=red> "+ jsonValues['imdbRating']+"</font>")
		self.lb_rated.setText("<font color=green>" + jsonValues['Rated'] + "</font>")
		strVotes  = jsonValues['imdbVotes']
		self.votes.setText("<font color=green>" + strVotes + " votes </font>")
		self.updateDetails(jsonValues)
		self.showEverything()
def main():

	app = QApplication(sys.argv)
	form = IMDB_Thing_Main_Window()
	xpos = QApplication.desktop().width()
	ypos = QApplication.desktop().height()
	xpos = (xpos-800)/2
	ypos = (ypos-600)/2
	form.move(xpos,ypos)
	form.show()
	app.exec_()


if __name__=="__main__":
	main()
