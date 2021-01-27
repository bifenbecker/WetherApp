import PyQt5,sys,form, WetherPredict, requests, sqlite3
from datetime import datetime
from bs4 import BeautifulSoup
from PIL import Image
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from os import listdir
from threading import Timer


class App(QtWidgets.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setGeometry(300, 300, 1050, 590)
        self.setWindowOpacity(0.95)
        self.initUi()
        self.label.setPixmap(QtGui.QPixmap("images/MainBackground1.jpeg"))
        self.pushButton_Update.clicked.connect(self.UpdatePredict)

    def UpdateTime(self):
        self.label_Date.setText(str(datetime.now()).split('.')[0])
        t = Timer(1, self.UpdateTime)
        t.start()

    def InputData(self,data):
        self.label_Temperature.setText('Temperature:' + 4*' ' + data['Temperature'])
        self.label_Clouds.setText('Clouds:' + 4 * ' ' + data['Clouds'])
        self.label_Humidity.setText('Humidity:' + 4 * ' ' + data['Humidity'])
        self.label_Wind_Speed.setText('Wind speed:' + 4 * ' ' + data['Wind_speed'])
        self.UpdateTime()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter:
            self.UpdatePredict()

    def UploadDataDB(self,obj):
        data = WetherPredict.make_prediction_db(obj)
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS  predict(
                            City TEXT,
                            Temperature TEXT,
                            Humidity TEXT,
                            Clouds TEXT,
                            Date TEXT);
            """)

        conn.commit()
        cur.execute("INSERT INTO predict VALUES(?, ?, ?, ?, ?);", data)
        conn.commit()

    def SetPicture(self,data):
        images = 'images/'
        path = images
        time = {range(8, 15): 'morning', range(8): 'night', range(15, 24): 'evening'}
        HourNow = datetime.now().hour
        for t in time:
            if HourNow in t:
                path += time[t] + '/'

        temp = float(data['Temperature'][:-1])
        clouds = float(data['Clouds'][:-1])
        humidity = float(data['Humidity'][:-1])

        if clouds > 80:
            self.label.setPixmap(QtGui.QPixmap(path + 'Clouds.jpg'))
        else:
            if temp < -1:
                self.label.setPixmap(QtGui.QPixmap(path + 'Snow.jpg'))
            elif clouds > 50 and humidity > 70:
                self.label.setPixmap(QtGui.QPixmap(path + 'Rain.jpg'))
            else:
                self.label.setPixmap(QtGui.QPixmap(path + 'Clear.jpg'))


    def UpdatePredict(self):
        CityName = self.lineEdit_CityaName.text()
        try:
            predict = WetherPredict.Prediction(CityName)
            data = WetherPredict.make_prediction2(predict)
            self.InputData(data)
            self.SetPicture(data)
            self.UploadDataDB(predict)
        except:
            self.label_Date.setText("Error")

    def initUi(self):
        self.setupUi(self)
        self.show()



def main():

    app = QtWidgets.QApplication(sys.argv)
    window = App()

    sys.exit(app.exec_())
















def CutPictures():
    img = "images/"
    path = ['evening/','morning/','nigth/']
    EvPic = [f for f in listdir(img+path[0])]
    MorPic = [f for f in listdir(img+path[1])]
    NgPic = [f for f in listdir(img+path[2])]
    scale_image(img+'MainBackground.jpeg',img+'MainBackground1.jpeg',1060)
    for p in EvPic:
        scale_image(img+path[0]+p,img+path[0]+p,1060)

    for p in MorPic:
        scale_image(img+path[1]+p,img+path[1]+p,1060)

    for p in NgPic:
        scale_image(img+path[2]+p,img+path[2]+p,1060)


def scale_image(input_image_path,
                output_image_path,
                width=None,
                height=None
                ):
    original_image = Image.open(input_image_path)
    w, h = original_image.size
    print('The original image size is {wide} wide x {height} '
          'high'.format(wide=w, height=h))

    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, h)
    elif height:
        max_size = (w, height)
    else:
        # No width or height specified
        raise RuntimeError('Width or height required!')

    original_image.thumbnail(max_size, Image.ANTIALIAS)
    original_image.save(output_image_path)

    scaled_image = Image.open(output_image_path)
    width, height = scaled_image.size
    print('The scaled image size is {wide} wide x {height} '
          'high'.format(wide=width, height=height))



if __name__ == '__main__':
    # CutPictures()
    main()