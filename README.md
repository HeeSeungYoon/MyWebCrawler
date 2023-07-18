# MyWebCrawler
나만의 웹 크롤러

## 1. 개발 기간 및 참여 인원
* 2023.07.12 ~ 2023.07.17
* 개인 프로젝트

## 2. 기술 스택
* Python 3.11.4
* PyQt5 5.15.9 - 파이썬 플러그인으로 구현된 크로스 플랫폼 GUI 툴킷 Qt의 파이썬 바인딩
  ```
  pip install pyqt5
  ```
* Selenium 4.10.0 - 웹 애플리케이션 자동화 및 테스트를 위한 포터블 프레임워크
  ```
  pip install selenium
  ```

## 3. 핵심 기능
<details>
<summary>1. 검색

  * 검색할 키워드를 텍스트바에 입력하고 검색버튼을 누르면 크롬브라우저가 실행되어 구글 이미지 검색 사이트로 연결
  * 종료 버튼을 누르면 프로그램 종료
 </summary>

  ![검색](./image/mainwindow.PNG) 
  
  ---
  ```python
  chromeOptions = webdriver.ChromeOptions()
  chromeOptions.add_experimental_option("detach",True)
  chromeOptions.add_argument('--ignore-certificate-errors')
  chromeOptions.add_argument('--lang=ko_KR')
  chromeService = Service(executable_path=ChromeDriverManager().install())
  self.driver = webdriver.Chrome(service=chromeService,options=chromeOptions)
  self.driver.get('https://www.google.com/imghp?hl=ko&tab=ri&ogbl')
  ```

  python에서 slenium을 사용하려면 webdriver 필요 --> chrome webdriver 설치
    
  webdriver의 옵션을 설정하고 구글 이미지 사이트에 연결하는 단계
  
  ---
</details>

<details>
  <summary> 2. 크롤링

  * Chrome DOM 구조의 HTML과 CSS의 요소에 접근하여 이미지 객체 정보 추출
 </summary>
 
```python
SCROLL_PAUSE_TIME = 1
lastHeight = self.driver.execute_script("return document.body.scrollHeight")
while True:
    self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    newHeight = self.driver.execute_script("return document.body.scrollHeight")

if newHeight == lastHeight:
  """ 이하 생략 """
```

브라우저에서 스크롤의 높이를 가져옴
더이상 스크롤바를 내릴 수 없을 때까지 스크롤바를 내림  

---

```python
self.images = self.driver.find_elements(By.CSS_SELECTOR, '.rg_i.Q4LuWd')
```

css_selector와 이미지의 class 요소 id를 통해 DOM 구조에 접근하여 이미지(섬네일) 객체 정보를 저장

---

</details>

<details>
  <summary> 3. 저장
  
  * 이미지 디렉터리를 생성하고 이미지 url을 통해 원본 이미지를 저장
  * 저장 중인 상태를 progress bar에 표시
 </summary>
 
  ![크롤링](./image/crawling.gif)  

  ```python
  for image in self.images:
    try:
        image.click()
        time.sleep(1)
        imageUrl = self.driver.find_element(By.XPATH,'//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]').get_attribute('src')
        """ 이하 생략 """
  ```

  섬네일을 클릭하면 나오는 원본 이미지의 XPATH를 이용해 'src' 속성에서 원본 이미지가 저장되어 있는 url 정보를 불러옴

  ---
  
  ![저장](./image/savedImage.PNG)

  이미지 디렉터리를 생성하고 이미지 url에 접근하여 원본 이미지를 저장

  ---
  
  ![완료](./image/complete.PNG)

  저장 중인 상태를 진행바에 표시

  저장이 완료되면 총 이미지 개수와 저장에 성공한 이미지, 저장에 실패한 이미지 개수를 새 창에 표시

  ---
</details>

## 4. 오류 및 개선 사항

* 개선이 필요한 사항
  + 이미지를 저장하는 기능과 저장 중인 상태를 나타내는 UI에서 진행바가 올라가는 기능이 동시에 진행되지 않음

    이미지 저장이 완료되면 진행바가 표시됨

    --> 진행바가 올라가는 기능을 thread로 실행시켰지만 여전히 동시에 진행되지 않음

## 5. 저작권 및 라이선스
* GNU GPL v3
* Apache-2.0

  ---
Contact : <iyhs1858@gmail.com> 
