

import json
import urllib2
import requests
import sys
import ui_IMDB_Thing
from PyQt4.QtGui  import *
from PyQt4.QtCore import *
from datetime import date
import webbrowser


class IMDB_Thing_Main_Window(QMainWindow,ui_IMDB_Thing.Ui_MainWindow):

	infoDict = {}
	title = ""
	windowImage = ""

	
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
	def showEverything(self):

		self.plot.show()
		self.line.show()
		self.lb_rating.show()
		self.lb_rated.show()
		self.goToWebsite.show()
		self.votes.show()
		#self.tblWd_details.show()
		self.groupBox.show()

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
		'''	
		self.tblWd_details.setItem(0,0,QTableWidgetItem('Title'))
		self.tblWd_details.setItem(0,1,QTableWidgetItem(jsonValues['Title']))
		self.tblWd_details.setItem(1,0,QTableWidgetItem('Year'))
		self.tblWd_details.setItem(1,1,QTableWidgetItem(jsonValues['Year']))
		self.tblWd_details.setItem(2,0,QTableWidgetItem('Genre'))
		self.tblWd_details.setItem(2,1,QTableWidgetItem(jsonValues['Genre']))
		self.tblWd_details.setItem(3,0,QTableWidgetItem('Runtime'))
		self.tblWd_details.setItem(3,1,QTableWidgetItem(jsonValues['Runtime']))
		self.tblWd_details.setItem(4,0,QTableWidgetItem('Actors'))
		self.tblWd_details.setItem(4,1,QTableWidgetItem(jsonValues['Actors']))
		self.tblWd_details.setItem(5,0,QTableWidgetItem('Director'))
		self.tblWd_details.setItem(5,1,QTableWidgetItem(jsonValues['Director']))
		self.tblWd_details.setItem(6,0,QTableWidgetItem('Awards'))
		self.tblWd_details.setItem(6,1,QTableWidgetItem(jsonValues['Awards']))
		self.tblWd_details.setItem(7,0,QTableWidgetItem('Movie/Serial'))
		self.tblWd_details.setItem(7,1,QTableWidgetItem(jsonValues['Type']))
		'''
	def setCBoxYear(self):
		
		self.CBoxYear.addItem('unknown')
		for year in range(1900,date.today().year):
			self.CBoxYear.addItem(str(year))
		self.CBoxYear.setMaxVisibleItems(10)		

	def updateUi(self):
		
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

	def makeConnections(self):

		self.connect(self.lEdit_movieName, SIGNAL("returnPressed()"),self.getAndUpdateData)
		self.connect(self.goToWebsite,SIGNAL("clicked()"),self.goToPage)
		self.connect(self.bt_go,SIGNAL("clicked()"),self.getAndUpdateData)

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
