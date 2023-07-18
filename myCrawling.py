import os
import sys
import time
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from saving import Worker

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle('크롤링할 이미지를 입력하세요.')
        self.resize(400, 200)
        self.center()

        self.qLE = QLineEdit(self)
        searchBtn = QPushButton('검색')
        quitBtn = QPushButton('종료',self)
        searchBtn.clicked.connect(self.search)
        quitBtn.clicked.connect(QCoreApplication.instance().quit)

        hBox1 = QHBoxLayout()
        hBox1.addStretch(1)
        hBox1.addWidget(self.qLE)
        hBox1.addWidget(searchBtn)
        hBox1.addStretch(1)

        hBox2 = QHBoxLayout()
        hBox2.addStretch(1)
        hBox2.addWidget(quitBtn)
        hBox2.addStretch(1)

        vBox = QVBoxLayout()
        vBox.addStretch(1)
        vBox.addLayout(hBox1)
        vBox.addLayout(hBox2)
        vBox.addStretch(1)
        
        self.setLayout(vBox)
        self.show()

    def center(self):
        qWindowSize = self.frameGeometry()
        monitorCenter = QDesktopWidget().availableGeometry().center()
        qWindowSize.moveCenter(monitorCenter)
        self.move(qWindowSize.topLeft())

    def search(self):
        self.text = self.qLE.text()
        if self.text == "":
            dlg = QMessageBox(self)
            dlg.warning(self, '경고', '다시 입력해주세요.')
        else:
            self.crawling()

    def crawling(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option("detach",True)
        chromeOptions.add_argument('--ignore-certificate-errors')
        chromeOptions.add_argument('--lang=ko_KR')
        chromeService = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chromeService,options=chromeOptions)
        self.driver.get('https://www.google.com/imghp?hl=ko&tab=ri&ogbl')
        self.driver.maximize_window()

        searchBar = self.driver.find_element(By.NAME, 'q')
        searchBar.send_keys(self.text)
        searchBar.send_keys(Keys.RETURN)

        SCROLL_PAUSE_TIME = 1
        lastHeight = self.driver.execute_script("return document.body.scrollHeight") # 스크롤 높이 가져옴
        while True:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            newHeight = self.driver.execute_script("return document.body.scrollHeight")

            if newHeight == lastHeight:
                try:
                    self.driver.find_element(By.CSS_SELECTOR,'.mye4qd').click()
                except:
                    break
            lastHeight = newHeight
        
        self.images = self.driver.find_elements(By.CSS_SELECTOR, '.rg_i.Q4LuWd')
        self.save()
        self.driver.close()
        self.driver.quit()

    def initSavingUI(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("저장 중입니다...")
        self.dialog.resize(360,180)

        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(self.totalImages)
        self.progressBar.setFormat("%v / %m")
        self.progressBar.setValue(0)

        # self.savingLabel = QLabel('0')
        # font1 = self.savingLabel.font()
        # font1.setPointSize(20)
        # font1.setBold(True)

        # self.totalLabel = QLabel(' / '+str(self.totalImages))
        # font2 = self.totalLabel.font()
        # font2.setPointSize(20)
        # font2.setBold(True)

        hBox = QHBoxLayout()
        hBox.addStretch(1)
        hBox.addWidget(self.progressBar)
        # hBox.addWidget(self.totalLabel)
        hBox.addStretch(1)

        vBox = QVBoxLayout()
        vBox.addStretch(1)
        vBox.addLayout(hBox)
        vBox.addStretch(1)
        self.dialog.setLayout(vBox)

        self.dlg = QMessageBox(self.dialog)

        self.dialog.show()

    def save(self):
        self.path = self.text+'/'
        if not(os.path.isdir(self.path)):
            os.mkdir(self.path)
        
        self.totalImages = len(self.images)
        self.imageNum = 1
        success = 0
        failed = 0
        self.cnt = 0

        self.initSavingUI()

        self.thread = QThread()
        self.thread.start()

        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.worker.saving.connect(self.progress)
        # coRutine = self.saving()
        # cnt = next(coRutine)
        # try:
            # while(cnt < self.totalImages):
            #     cnt += 1
            #     print(cnt)
            #     self.progressBar.setValue(cnt)
            #     cnt = coRutine.send(1)
        # except StopIteration:
        #     coRutine.close()

    # def saving(self):    
        for image in self.images:
            try:
                image.click()
                time.sleep(1)
                imageUrl = self.driver.find_element(By.XPATH,'//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]').get_attribute('src')
                fileName = self.path+self.path[:-1]+'_'+str(self.imageNum)+'.png'
                urllib.request.urlretrieve(imageUrl,fileName)
                self.imageNum+=1
                success+=1
            except:
                failed+=1
                pass      
            # yield cnt+1
            print('%dth saving... success : %d / failed : %d'%(self.cnt+1, success, failed))
            self.cnt += 1
            self.worker.run()
            if self.cnt >= self.progressBar.maximum():
                self.worker.stop()
                self.dlg.about(self.dialog, '저장 완료','총 '+str(self.totalImages)+'장 이미지\n \
                    저장 성공 : '+str(success)+'\n \
                        저장 실패 : '+str(failed))
                self.dialog.close()
    
        self.thread.exit()
            
    def progress(self, cnt):
        progress = self.progressBar.value()
        progress += cnt
        print('진행바 상태 : %d'%progress)
        self.progressBar.setValue(progress)

if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    app = MyApp()
    sys.exit(qApp.exec_())