from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from pathlib import Path
from constants import *

class Test_Workshop:
    
    # pytest'te her test öncesi çalıştırılan metot,  buradaki kodlar her test öncesi çalışır..
    def setup_method(self): 
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(BASE_DOMAIN_URL)  #url i al 

    # teardown_method => her test sonrası çalışır..
    def teardown_method(self): 
        # buradaki kodlar her test sonrası çalışır..
        self.driver.quit() 



    # 1- Doğru bilgilerden standard_user kullanıcı adıyla giriş yapılmanın doğru olup olmadığı kontrol edilmelidir.
        # class fonksiyonlarının ilk parametresi her zaman "self"'dir
    def test_login_success(self):
    
        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.ID, USERNAME_INFO )))
        # visibility_of_element_located => username elementini görüntüleyene kadar bekle
        # (self.driver,5) => max. 5 sn kadar
        # Usernames: standart_user, locked_out_user, problem_user, performance_glitch_user
        username= self.driver.find_element(By.ID, USERNAME_INFO )
        username.send_keys(USERNAME)

        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.ID, USERNAME_INFO )))
        # Password: secret_sauce
        password= self.driver.find_element(By.ID, PASSWORD_INFO )
        password.send_keys(PASSWORD)

        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.ID, USERNAME_INFO )))
        loginBtn= self.driver.find_element(By.ID, LGN_BUTTON)
        loginBtn.click()

        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.ID, MENU )))
        menu= self.driver.find_element(By.ID, MENU)
        menuText= menu.text

        # assert => verilen conditionu testin sonucuna bağlar (if-else bloğu yerine kullanılır)
        assert menuText == MENU_TEXT





    # 2- Yanlış bilgiler girildiğinde uyarı çıkıp çıkmadığı test edilmelidir.
    def test_login_unsuccess(self):
        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.ID, USERNAME_INFO )))
        username= self.driver.find_element(By.ID, USERNAME_INFO )
        username.send_keys(USERNAME)

        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.ID, USERNAME_INFO )))
        password= self.driver.find_element(By.ID, PASSWORD_INFO )
        password.send_keys(WRONG_PASSWORD)

        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.ID, USERNAME_INFO )))
        loginBtn= self.driver.find_element(By.ID, LGN_BUTTON)
        loginBtn.click()

        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.XPATH, ERROR)))
        error= self.driver.find_elements(By.XPATH, ERROR)
        errorLen = len(error)

        assert errorLen > 0 




        
    # 3- Yanlış bilgiler girildiğinde çıkan uyarı mesajının doğruluğu kontrol edilmelidir.  
    def test_login_error_message(self):
        self.test_login_unsuccess()

        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.XPATH, ERROR)))
        error= self.driver.find_element(By.XPATH, ERROR)
        errorText = error.text

        assert errorText == ERROR_TEXT
        # ERROR_TEXT = "Epic sadface: Username and password do not match any user in this service" 

        



    # 4- Ana sayfada 6 adet ürün listelendiği kontrol edilmelidir.
    def test_product_list(self):
        self.test_login_success()

        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.XPATH, PRODUCT_LIST)))
        productList = self.driver.find_elements(By.XPATH, PRODUCT_LIST)
        productListLen = len(productList)

        assert productListLen == 6

   
   
   
   
    # 5- Sepete Ekle butonuna tıklandığında butonun texti "REMOVE" olmalıdır.
    def test_basket(self):
        self.test_login_success()

        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.ID, ADD_TO_CARD)))
        addToCard= self.driver.find_element(By.ID, ADD_TO_CARD)
        addToCard.click()

        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.NAME, PRODUCT_REMOVE)))
        productRemove = self.driver.find_element(By.NAME, PRODUCT_REMOVE)
        removeText = productRemove.text

        assert removeText == REMOVE_TEXT
        
    
    
    
    
    # 6- Sepete 1 adet ürün eklendiğinde sağ üstteki sepet üzerinden "1" sayısı çıkmalıdır.
    def test_basket_item(self):
        self.test_login_success()

        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.ID, ADD_TO_CARD)))
        addToCard = self.driver.find_element(By.ID, ADD_TO_CARD)
        addToCard.click()

        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, BASKET_ITEM)))
        basketItem = self.driver.find_element(By.CLASS_NAME, BASKET_ITEM)
        itemText = basketItem.text

        assert itemText == ITEM_COUNT
