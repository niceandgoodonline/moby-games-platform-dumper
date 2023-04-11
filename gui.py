from PyQt5 import QtCore, QtGui, QtWidgets
from api_walker import Api_Walker
from platform_cleaner import Platform_Cleaner
import sys
sys.path.insert(1, './modules/')
import f_util

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(386, 241)

		self.config = f_util.json_to_dict("enduser-config.json")

		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")

		self.apiGroup = QtWidgets.QGroupBox(self.centralwidget)
		self.apiGroup.setGeometry(QtCore.QRect(10, 10, 371, 81))
		self.apiGroup.setObjectName("apiGroup")

		self.formatDrop = QtWidgets.QComboBox(self.apiGroup)
		self.formatDrop.setGeometry(QtCore.QRect(60, 50, 69, 22))
		self.formatDrop.setObjectName("formatDrop")

		self.formatDropLabel = QtWidgets.QLabel(self.apiGroup)
		self.formatDropLabel.setGeometry(QtCore.QRect(10, 50, 51, 21))
		self.formatDropLabel.setObjectName("formatDropLabel")

		self.platformDropLabel = QtWidgets.QLabel(self.apiGroup)
		self.platformDropLabel.setGeometry(QtCore.QRect(10, 20, 51, 21))
		self.platformDropLabel.setObjectName("platformDropLabel")

		self.platformDrop = QtWidgets.QComboBox(self.apiGroup)
		self.platformDrop.setGeometry(QtCore.QRect(60, 20, 231, 22))
		self.platformDrop.setObjectName("platformDrop")
		self.platformDrop.currentTextChanged.connect(self.set_platform)

		self.mgpCheck = QtWidgets.QCheckBox(self.apiGroup)
		self.mgpCheck.setGeometry(QtCore.QRect(140, 50, 231, 21))
		self.mgpCheck.setObjectName("mgpCheck")
		self.mgpCheck.stateChanged.connect(self.set_normalize_for_mgp)

		self.playwrightGroup = QtWidgets.QGroupBox(self.centralwidget)
		self.playwrightGroup.setGeometry(QtCore.QRect(10, 100, 161, 91))
		self.playwrightGroup.setObjectName("playwrightGroup")

		self.scrapeScreenshotsCheck = QtWidgets.QCheckBox(self.playwrightGroup)
		self.scrapeScreenshotsCheck.setGeometry(QtCore.QRect(10, 40, 131, 17))
		self.scrapeScreenshotsCheck.setObjectName("scrapePicturesCheck")
		self.scrapeScreenshotsCheck.stateChanged.connect(self.set_scrape_screenshots)

		self.scrapeExtrasCheck = QtWidgets.QCheckBox(self.playwrightGroup)
		self.scrapeExtrasCheck.setGeometry(QtCore.QRect(10, 60, 131, 17))
		self.scrapeExtrasCheck.setObjectName("scrapeExtrasCheck")
		self.scrapeExtrasCheck.stateChanged.connect(self.set_scrape_extras)

		self.scrapeCoverCheck = QtWidgets.QCheckBox(self.playwrightGroup)
		self.scrapeCoverCheck.setGeometry(QtCore.QRect(10, 20, 141, 17))
		self.scrapeCoverCheck.setObjectName("scrapeCoverCheck")
		self.scrapeCoverCheck.stateChanged.connect(self.set_scrape_covers)

		self.runButton = QtWidgets.QPushButton(self.centralwidget)
		self.runButton.setGeometry(QtCore.QRect(180, 170, 75, 23))
		self.runButton.setObjectName("runButton")
		self.runButton.clicked.connect(self.run_scrape)

		self.cleanButton = QtWidgets.QPushButton(self.centralwidget)
		self.cleanButton.setGeometry(QtCore.QRect(270, 170, 75, 23))
		self.cleanButton.setObjectName("cleanButton")
		self.cleanButton.clicked.connect(self.run_clean)

		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setEnabled(True)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 386, 21))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setEnabled(True)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Moby Games Platform Scraper"))
		self.apiGroup.setTitle(_translate("MainWindow", "API Options"))
		self.formatDropLabel.setText(_translate("MainWindow", "Format"))
		self.platformDropLabel.setText(_translate("MainWindow", "Platform:"))
		self.mgpCheck.setText(_translate("MainWindow", "Normalize scrape for Magical Game Picker?"))
		self.playwrightGroup.setTitle(_translate("MainWindow", "Web Scraping (next version)"))
		self.scrapeScreenshotsCheck.setText(_translate("MainWindow", "Scrape Screenshots?"))
		self.scrapeExtrasCheck.setText(_translate("MainWindow", "Scrape Extras"))
		self.scrapeCoverCheck.setText(_translate("MainWindow", "Scrape Covers?"))
		self.runButton.setText(_translate("MainWindow", "Scrape"))
		self.cleanButton.setText(_translate("MainWindow", "Clean Data"))

	def populate_platform_dropdown(self, platforms: list):
		self.platformDrop.addItems(platforms)

	def populate_format_dropdown(self):
		self.formatDrop.addItems(["normal", "brief", "id"])

	def set_platform(self, platform_name: str):
		self.config['platform'] = platform_name

	def set_fromat(self, new_format: str):
		self.config['format'] = new_format

	def set_scrape_covers(self, state: bool):
		self.config['covers'] = state

	def set_scrape_extras(self, state: bool):
		self.config['extras'] = state

	def set_scrape_screenshots(self, state: bool):
		self.config['screenshots'] = state

	def set_normalize_for_mgp(self, state: bool):
		self.config['magical_game_picker_normalization'] = state

	def run_scrape(self):
		self.runButton.setEnabled(False)
		self.cleanButton.setEnabled(False)
		_walker = Api_Walker(self.config)
		_walker.main()
		self.runButton.setEnabled(True)
		self.cleanButton.setEnabled(True)

	def run_clean(self):
		if f_util.check_file_exists(f"json/{self.config['platform']}/moby-web-paths.json"):
			self.runButton.setEnabled(False)
			self.cleanButton.setEnabled(False)
			_cleaner = Platform_Cleaner(self.config)
			_cleaner.convert_genres_to_tags()
			self.runButton.setEnabled(True)
			self.cleanButton.setEnabled(True)
		else:
			print("no file")

if __name__ == "__main__":
	platforms  = f_util.json_to_dict("config/platforms.json")
	app        = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui         = Ui_MainWindow()
	ui.setupUi(MainWindow)
	ui.populate_platform_dropdown(platforms.keys())
	ui.populate_format_dropdown()
	MainWindow.show()
	sys.exit(app.exec_())