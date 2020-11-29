# Done By Ryan

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


from functools import partial
import sys

from Compiled_Store_Func import *
from Prediction_Func import *
from Data_Func import *


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #self.plot()

    def setData(self, x, y):
        self.x = x
        self.y = y

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.bar(x=self.x, height=self.y, align='edge')
        ax.get_yaxis().set_visible(False)
        ax.set_title('Popular Times')
        self.draw()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title of main window
        self.setWindowTitle("Python GUI")

        # set the size of window
        self.Width = 800
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        # set the background image 
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('backgroundimage.png'))
        self.label.setGeometry(0,0, self.Width,0.618*self.Width)

        # add all widgets   

        self.btnViewTodayStore = QPushButton("View today's store", self)

        self.btnViewTodayStore.setIcon(QtGui.QIcon('todaycolour.png'))
        self.btnViewTodayStore.setIconSize(QtCore.QSize(26,26))
        
        
        self.btnViewOtherDates = QPushButton("View other dates", self)

        self.btnViewOtherDates.setIcon(QtGui.QIcon('calendarcolour.png'))
        self.btnViewOtherDates.setIconSize(QtCore.QSize(26,26))
        
        self.btnCheckOperatingHours = QPushButton("Check operating hours", self)

        self.btnCheckOperatingHours.setIcon(QtGui.QIcon('clockcolour.png'))
        self.btnCheckOperatingHours.setIconSize(QtCore.QSize(26,26))
        
        self.btnExit = QPushButton('Exit', self)
        
        self.btnExit.setIcon(QtGui.QIcon('exitcolour.png'))
        self.btnExit.setIconSize(QtCore.QSize(22,22))

        self.btnViewTodayStore.clicked.connect(self.onClickBtnViewTodayStore)
        self.btnViewOtherDates.clicked.connect(self.onClickBtnViewOtherDates)
        self.btnCheckOperatingHours.clicked.connect(self.onClickBtnCheckingOperatingHours)
        self.btnExit.clicked.connect(self.close)

        # add tabs
        self.right_widget = QTabWidget()
        self.tab1 = self.uiViewTodayStore()
        self.tab2 = self.uiViewOtherDates()
        self.tab3 = self.uiCheckOperatingHours()
        self.tab4 = self.uiStock()
        self.tab5 = self.uiStock()
        self.tab6 = self.uiStock()
        self.tab7 = self.uiStock()
        self.tab8 = self.uiStock()

        self.initUI()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()
        # Hour, min
        self.hour = '00'
        self.min = '00'

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btnViewTodayStore)
        left_layout.addWidget(self.btnViewOtherDates)
        left_layout.addWidget(self.btnCheckOperatingHours)
        left_layout.addWidget(self.btnExit)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')
        self.right_widget.addTab(self.tab6, '')
        self.right_widget.addTab(self.tab7, '')
        self.right_widget.addTab(self.tab8, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # -----------------
    # buttons

    def onClickBtnViewTodayStore(self):
        self.right_widget.setCurrentIndex(0)

    def onClickBtnViewOtherDates(self):
        self.right_widget.setCurrentIndex(1)

    def onClickBtnCheckingOperatingHours(self):
        self.right_widget.setCurrentIndex(2)

    def button4(self):
        #self.right_widget.setCurrentIndex(3)
        print("exit");

    # -----------------
    # pages

    def uiViewTodayStore(self):
        main_layout = QVBoxLayout()
        self.lblTime = QLabel('')
        self.lblTime.setMaximumHeight(50)
        main_layout.addWidget(self.lblTime)
        groupbox = QGroupBox('Stores in operation')
        layout = QGridLayout()
        self.btnListInTodayStore = []
        btnLists = Stores_In_Operation(date_of_interest='now')
        for item in btnLists:
            self.btnListInTodayStore.append(QPushButton(item))
        

        groupbox.setLayout(layout)
        for item in self.btnListInTodayStore:
            item.setIcon(QtGui.QIcon('opencolour.png'))
            item.setIconSize(QtCore.QSize(26,26))
            
            item.clicked.connect(partial(self.onClickStoreName, item.text()))
            layout.addWidget(item)
        main_layout.addWidget(groupbox)
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def uiViewOtherDates(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('View other dates'))

        group = QGroupBox()
        layout = QVBoxLayout()
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.clicked[QtCore.QDate].connect(self.showDate)
        self.datelbl = QLabel(self)
        date = cal.selectedDate()
        self.dateInOtherDates = date
        self.datelbl.setText(date.toString())
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(cal)
        layout.addWidget(self.datelbl)
        group.setLayout(layout)
        main_layout.addWidget(group)

        group = QGroupBox()
        layout = QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.comboHour = QComboBox()
        for i in range(24):
            if i < 10:
                self.comboHour.addItem("0"+str(i))
            else:
                self.comboHour.addItem(str(i))
        self.comboHour.setMaximumWidth(80)
        self.comboHour.activated[str].connect(self.onActivatedHour)
        self.comboMin = QComboBox()
        for i in range(60):
            if i < 10:
                self.comboMin.addItem("0" + str(i))
            else :
                self.comboMin.addItem(str(i))
        self.comboMin.setMaximumWidth(80)
        self.comboMin.activated[str].connect(self.onActivatedMin)
        layout.addWidget(self.comboHour)
        lbl = QLabel(":")
        lbl.setMaximumWidth(10)
        layout.addWidget(lbl)
        layout.addWidget(self.comboMin)
        confirmButton = QPushButton("Confirm")

        confirmButton.setIcon(QtGui.QIcon('tick.png'))
        confirmButton.setIconSize(QtCore.QSize(26,26))

        confirmButton.clicked.connect(self.onClickConfirmOtherDate)
        layout.addWidget(confirmButton)
        group.setLayout(layout)
        main_layout.addWidget(group)

        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def showDate(self, date):
        self.dateInOtherDates = date
        self.datelbl.setText(date.toString())

    def onActivatedHour(self, text):
        self.hour = (text)

    def onActivatedMin(self, text):
        self.min = (text)

    def onClickConfirmOtherDate(self):
        #print(self.hour)
        #print(self.min)
        print(self.datelbl.text())
        self.right_widget.removeTab(4)
        self.tab5 = self.uiViewOtherDayStores()
        self.right_widget.insertTab(4, self.tab5, '')
        self.right_widget.setCurrentIndex(4)

    # check operating hours / main frame
    def uiCheckOperatingHours(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('Click store names for more information'))

        groupbox = QGroupBox('All Stores Available Today')
        layout = QGridLayout()
        self.btnListInCheckStore = []
        dateOfInterest = 'now'
        day = findDay(dateOfInterest)[0]
        #btnLists = Stores_In_Operation(date_of_interest=dateOfInterest)
        btnLists = Return_Store_Names()
        status = Return_All_Store_Status(dateOfInterest, 'Opening Hours')
        cnt = 0
        for item in btnLists:
            openHours = Return_Store_Hours(item, day_of_interest=day, period_of_interest='Opening Hours')
            tmpStr = 'Opening Hours : ' + openHours[0].strftime("%H:%M") + ' ~ ' + openHours[1].strftime("%H:%M")
            strStatus = "Open!" if status[cnt] else "Closed"
            if status[cnt]:
                self.btnListInCheckStore.append(QPushButton(item + '\n' + tmpStr + '\n' + strStatus))
            else:
                self.btnListInCheckStore.append(QPushButton(item  + '\n' + strStatus))
            cnt += 1

        groupbox.setLayout(layout)
        cnt = 0
        for item in self.btnListInCheckStore:
            
            item.setIcon(QtGui.QIcon('clock.png'))
            item.setIconSize(QtCore.QSize(26,26))

            item.clicked.connect(partial(self.onClickBtnCheckStoreName, btnLists[cnt]))
            layout.addWidget(item)
            cnt += 1
        main_layout.addWidget(groupbox)

        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def onClickBtnCheckStoreName(self, stockName):
        self.right_widget.removeTab(7)
        self.tab8 = self.uiStock4(stockName)
        self.right_widget.insertTab(7, self.tab8, '')
        self.right_widget.setCurrentIndex(7)

    def uiStock3(self, stockName, day):
        main_layout = QVBoxLayout()
        group = QGroupBox()
        layout = QHBoxLayout()
        self.stockNameInCheck = QLabel(stockName)
        backButton = QPushButton("Back")

        backButton.setIcon(QtGui.QIcon('backbutton.png'))
        backButton.setIconSize(QtCore.QSize(26,26))

        
        backButton.setMaximumWidth(100)
        
        backButton.clicked.connect(self.onClickBtnBackButtonInCheckOp)
        layout.addWidget(backButton)
        layout.addWidget(self.stockNameInCheck)
        group.setLayout(layout)
        main_layout.addWidget(group)
        #get plot data
        dateOfInterest = day
        data = Barplot(store_name=stockName, date_of_interest=dateOfInterest)
        if data:
            group = QGroupBox()
            layout = QHBoxLayout()
            print(data['x'])
            print(data['y'])
            m = PlotCanvas(width=5, height=4)
            m.setData(x=data['x'], y=data['y'])
            m.plot()
            layout.addWidget(m)
            group.setLayout(layout)
            main_layout.addWidget(group)
        else:
            buttonReply = QMessageBox.question(self, 'Warning', "Cannot draw graph ",
                                           QMessageBox.Ok)
        group = QGroupBox()
        self.menuLayout = QVBoxLayout()
        group.setLayout(self.menuLayout)

        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def onClickBtnBackButtonInCheckOp(self):
        self.right_widget.setCurrentIndex(7)
    # view checking oeration time / showing weekly time for each stock
    def uiStock4(self, stockName):
        main_layout = QVBoxLayout()
        group = QGroupBox()
        layout = QHBoxLayout()
        self.stockNameInCheck = QLabel(stockName)
        backButton = QPushButton("Back")

        backButton.setIcon(QtGui.QIcon('backbutton.png'))
        backButton.setIconSize(QtCore.QSize(26,26))

        
        backButton.setMaximumWidth(100)
        backButton.clicked.connect(self.onClickBtnBackButtonInWeek)
        layout.addWidget(backButton)
        layout.addWidget(self.stockNameInCheck)
        group.setLayout(layout)
        main_layout.addWidget(group)
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        group = QGroupBox()
        self.menuLayout = QVBoxLayout()
        btnList = []
        print("Open")
        for day in weekdays:
            Opening_Time, Closing_Time = Return_Store_Hours(stockName, day_of_interest=day, period_of_interest='Opening Hours')
            if (Opening_Time, Closing_Time) != (float('inf'), float('inf')):
                print(Opening_Time)
                Opening_Time, Closing_Time = (Opening_Time.strftime("%H")), (Closing_Time.strftime("%H"))
                btn = QPushButton(day + '\n Daily Opening Hours : ' + Opening_Time + ' ~ ' + Closing_Time)
                btn.clicked.connect(partial(self.onClickWeekDay, stockName, day))
                self.menuLayout.addWidget(btn)
        group.setLayout(self.menuLayout)
        main_layout.addWidget(group)
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    # back button in check op
    def onClickBtnBackButtonInWeek(self):
        self.right_widget.setCurrentIndex(2)

    def onClickWeekDay(self, stockName, day):
        self.right_widget.removeTab(6)
        self.tab7 = self.uiStock3(stockName, day)
        self.right_widget.insertTab(6, self.tab7, '')
        self.right_widget.setCurrentIndex(6)

    def uiStock(self):
        main_layout = QVBoxLayout()

        group = QGroupBox()
        layout = QHBoxLayout()
        self.stockName = QLabel('')
        backButton = QPushButton("Back")

        backButton.setIcon(QtGui.QIcon('backbutton.png'))
        backButton.setIconSize(QtCore.QSize(26,26))


        
        backButton.setMaximumWidth(100)
        backButton.clicked.connect(self.onClickBtnBackInUIStock)
        layout.addWidget(backButton)
        layout.addWidget(self.stockName)
        group.setLayout(layout)
        main_layout.addWidget(group)
        group = QGroupBox()
        self.menuLayout = QVBoxLayout()
        group.setLayout(self.menuLayout)

        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main
    # view today's stock / new frame for each stock
    def uiStock1(self, stockName):
        main_layout = QVBoxLayout()

        group = QGroupBox()
        layout = QHBoxLayout()
        self.stockName = QLabel(stockName)
        backButton = QPushButton("Back")

        backButton.setIcon(QtGui.QIcon('backbutton.png'))
        backButton.setIconSize(QtCore.QSize(26,26))


        
        backButton.setMaximumWidth(100)
        backButton.clicked.connect(self.onClickBtnBackInUIStock)
        layout.addWidget(backButton)
        layout.addWidget(self.stockName)
        group.setLayout(layout)
        main_layout.addWidget(group)

        menus = Return_Store_Menu(store_name=stockName,date_of_interest='now')
        print(menus)
        group = QGroupBox()
        menuLayout = QVBoxLayout()
        font1 = QFont("Times", 10, QFont.Bold)
        lbl = QLabel("Menu")
        lbl.setFont(font1)
        menuLayout.addWidget(lbl)
        for item in menus:
            menuLayout.addWidget(QLabel(item))
        group.setLayout(menuLayout)
        main_layout.addWidget(group)

        group = QGroupBox()
        formLayout = QVBoxLayout()
        font1 = QFont("Times", 10, QFont.Bold)
        lbl = QLabel("Estimate waiting time")
        lbl.setFont(font1)
        formLayout.addWidget(lbl)
        tmpgroup = QGroupBox()
        layout = QHBoxLayout()
        layout.addWidget(QLabel('How many people in queue?'))
        self.inpNumberOfPeople = QSpinBox()
        self.inpNumberOfPeople.setMinimum(0)
        self.inpNumberOfPeople.setMaximum(99)
        layout.addWidget(self.inpNumberOfPeople)
        tmpgroup.setLayout(layout)
        self.qtimeLabel = QLabel('Estimated Waiting Time: 0')
        confirmButton = QPushButton("Calculate")

        confirmButton.setIcon(QtGui.QIcon('calculator.png'))
        confirmButton.setIconSize(QtCore.QSize(26,26))

        
        confirmButton.clicked.connect(partial(self.onClickConfirm, stockName))
        formLayout.addWidget(tmpgroup)
        formLayout.addWidget(confirmButton)
        formLayout.addWidget(self.qtimeLabel)
        group.setLayout(formLayout)
        main_layout.addWidget(group)

        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    # view today's stock / back button on new frame
    def onClickBtnBackInUIStock(self):
        self.right_widget.setCurrentIndex(0)

    # view today's stock / show time on header (timer event)
    def showTime(self):
        time = QtCore.QTime.currentTime()
        text = time.toString('hh:mm:ss')
        self.lblTime.setText(text)

    # view today's stock / click stock name event
    def onClickStoreName(self, stockName):
        self.tab4 = self.uiStock1(stockName)
        self.right_widget.removeTab(3)
        self.right_widget.insertTab(3, self.tab4, '')
        self.right_widget.setCurrentIndex(3)

    # view todays stock / confirm button event
    def onClickConfirm(self, stockName):
        number_str = self.inpNumberOfPeople.text()
        print(number_str, stockName)
        try:
            number = int(number_str)
        except:
            buttonReply = QMessageBox.question(self, 'Warning', "Input integer",
                                               QMessageBox.Ok)
            return
        qtime = Queue_Time(store_name=stockName, number_of_people=int(number))
        Write_Average_People_Data(store_name=stockName, number_of_people=int(number))
        self.qtimeLabel.setText("Estimated Waiting Time: {}".format(qtime))
        print(qtime)

    # view other dates / new frame when click confirm button.
    def uiViewOtherDayStores(self):
        main_layout = QVBoxLayout()

        group = QGroupBox()
        layout = QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignLeft)
        backButton = QPushButton("Back")

        backButton.setIcon(QtGui.QIcon('backbutton.png'))
        backButton.setIconSize(QtCore.QSize(26,26))

        
        backButton.setMaximumWidth(100)
        backButton.clicked.connect(self.onClickBtnBackViewOtherDates)
        layout.addWidget(backButton)
        group.setLayout(layout)
        main_layout.addWidget(group)

        groupbox = QGroupBox('Stores')
        layout = QGridLayout()
        self.btnListInOtherDaysStore = []

        dateOfInterest = "{0} {1} {2} {3} {4}".format(
            self.dateInOtherDates.day(),
            self.dateInOtherDates.month(),
            self.dateInOtherDates.year(),
            self.hour,
            self.min
        )
        print(dateOfInterest)
        btnLists = Stores_In_Operation(date_of_interest=dateOfInterest)
        for item in btnLists:
            self.btnListInOtherDaysStore.append(QPushButton(item))

        groupbox.setLayout(layout)
        for item in self.btnListInOtherDaysStore:
            item.clicked.connect(partial(self.onClickStoreNameInOtherDates, item.text()))
            layout.addWidget(item)
        main_layout.addWidget(groupbox)
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    # view other dates / confirm button event
    def onClickBtnBackViewOtherDates(self):
        self.right_widget.setCurrentIndex(1)

    # view other dates tab/new frame when click stock button
    def onClickStoreNameInOtherDates(self, stockName):
        self.tab6 = self.uiStock2(stockName)
        self.right_widget.removeTab(5)
        self.right_widget.insertTab(5, self.tab6, '')
        self.right_widget.setCurrentIndex(5)

    def uiStock2(self, stockName):
        main_layout = QVBoxLayout()

        group = QGroupBox()
        layout = QHBoxLayout()
        self.stockName = QLabel(stockName)
        backButton = QPushButton("Back")

        backButton.setIcon(QtGui.QIcon('backbutton.png'))
        backButton.setIconSize(QtCore.QSize(26,26))

        
        backButton.setMaximumWidth(100)
        backButton.clicked.connect(self.onClickBtnBackInOtherDates)
        layout.addWidget(backButton)
        layout.addWidget(self.stockName)
        group.setLayout(layout)
        main_layout.addWidget(group)

        dateOfInterest = "{0} {1} {2} {3} {4}".format(
            self.dateInOtherDates.day(),
            self.dateInOtherDates.month(),
            self.dateInOtherDates.year(),
            self.hour,
            self.min
        )
        print(dateOfInterest)
        menus = Return_Store_Menu(store_name=stockName, date_of_interest=dateOfInterest)
        print(menus)
        group = QGroupBox()
        menuLayout = QVBoxLayout()
        font1 = QFont("Times", 10, QFont.Bold)
        lbl = QLabel("Menu")
        lbl.setFont(font1)
        menuLayout.addWidget(lbl)
        for item in menus:
            menuLayout.addWidget(QLabel(item))
        group.setLayout(menuLayout)
        main_layout.addWidget(group)

        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def onClickBtnBackInOtherDates(self):
        self.right_widget.setCurrentIndex(4)

if __name__ == '__main__':
    print(Stores_In_Operation())
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
