import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5 import QtGui
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Creating a tab widget
        self.tabs = QTabWidget()
        # Making document mode True
        self.tabs.setDocumentMode(True)
        # Adding action when double clicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        # Adding action when tab is changed
        self.tabs.currentChanged.connect(self.current_tab_changed)
        # Making tavs closeable
        self.tabs.setTabsClosable(True)
        # Adding action when tab close is requested
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        # Making tabs as central widget
        self.setCentralWidget(self.tabs)
        # Creating a status bar
        self.status = QStatusBar()
        # Setting status bar to the main window
        self.setStatusBar(self.status)
        # Creating a tool bar for navigation
        navtb = QToolBar("Navigation")
        # Adding tool bar to the main window
        self.addToolBar(navtb)
        

        # Back button
        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Back to the previous page")
        # Adding action to the back button - make current tab to go back
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        # Add icon to the button
        back_btn.setIcon(QIcon("Icons/back.png"))
        # Add to the navegation bar
        navtb.addAction(back_btn)
        
        
        # Forward button
        forward_btn = QAction("Forward", self)
        forward_btn.setStatusTip("Forward to the next page")
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        # Add icon to the button
        forward_btn.setIcon(QIcon("Icons/forward.png"))
        navtb.addAction(forward_btn)


        # Reload button
        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        # Add icon to the button
        reload_btn.setIcon(QIcon("Icons/reload.png"))
        navtb.addAction(reload_btn)


        # Adding stop action
        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading the current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        # Add icon to the button
        stop_btn.setIcon(QIcon("Icons/stop2.png"))
        navtb.addAction(stop_btn)


        # Separator |
        navtb.addSeparator()


        # Home button
        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        home_btn.setIcon(QIcon("Icons/home.png"))
        navtb.addAction(home_btn)


        # Separator |
        navtb.addSeparator()


        # Edit search bar
        self.url_bar = QLineEdit()
        # Adding action to line edit when return key is passed
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        # Adding line edit to tool bar
        navtb.addWidget(self.url_bar)


        # Creating the first tab
        self.add_new_tab(QUrl('https://www.google.com'), 'Homepage')
        # Window Icon
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        # Window name
        self.setWindowTitle("import *")
        
        self.show()

        # Icons size (back, forward, stop...)
        self.setIconSize(QSize(20,30))
        
        # Open in full screen
        self.showMaximized()
        

    def add_new_tab(self, qurl = None, label = "Blank"):
        # If url is blank
        if qurl is None:
            # Create a google url
            qurl = QUrl('https://www.google.com')

        # Create a QWebEngineView object
        browser = QWebEngineView()
        # Setting url to browser
        browser.setUrl(qurl)
        # Setting tan index
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        # Adding action to the browser when url is changed: Update url
        browser.urlChanged.connect(lambda qurl, browser = browser:
                                    self.update_urlbar(qurl, browser)) 
        # Adding action to the browser when url is changed: Set tab title
        browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                        self.tabs.setTabText(i, browser.page().title()))


    def tab_open_doubleclick(self, i):
        # Checkin index i.e - No tab under the click
        if i == -1:
            # Creating a new tab
            self.add_new_tab()


    def current_tab_changed(self, i):
        # Get the curl
        qurl = self.tabs.currentWidget().url()
        # Update the url
        self.update_urlbar(qurl, self.tabs.currentWidget())
        # Update the title
        self.update_title(self.tabs.currentWidget())


    # When tab is closed
    def close_current_tab(self, i):
        # If there is only one tab
        if self.tabs.count() < 2:
            # Do nothing
            return
        # Else remove the tab
        self.tabs.removeTab(i)


    def update_title(self, browser):
        # If signal is not from the current tab
        if browser != self.tabs.currentWidget():
            # Do Nothing
            return
        # Get the page title
        title = self.tabs.currentWidget().page().title()
        # Set the window title
        self.setWindowTitle("% s New tab" % title)


    def navigate_home(self):
        # Go to Google
        self.tabs.currentWidget().setUrl(QUrl('https://www.google.com'))


    def navigate_to_url(self):
        # Get the lin edit text - convert it to Qurl object
        q = QUrl(self.url_bar.text())
        # If scheme is blank
        if q.scheme() == "":
            # Set scheme
            q.setScheme("http")
        # Set the url
        self.tabs.currentWidget().setUrl(q)


    def update_urlbar(self, q, browser = None):
        # If this singla is not from the current tab, ignore
        if browser != self.tabs.currentWidget():
            return
        # set text to the url bar
        self.url_bar.setText(q.toString())
        # Set cursor position
        self.url_bar.setCursorPosition(0)

    

# Creating a PyQt5 application
app = QApplication(sys.argv)
# Setting name to the application
QApplication.setApplicationName('Browser')
# Creating MainWindow boject
window = MainWindow()
# Loop
app.exec_()
