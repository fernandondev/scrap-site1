import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait

class Driver:
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument('--profile-directory=Default')
        #Start em tela cheia
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-application-cache')
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        #Executa sem exibir a interface do Chrome
        #options.add_argument("--headless")
        self.driver = uc.Chrome(options=options)
        self.driver.implicitly_wait(3)
        self.usar = True
        self.wait =  WebDriverWait(self.driver, 10)
        
        