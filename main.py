from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

service = Service(ChromeDriverManager().install())

chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.default_content_setting_values.media_stream_mic": 2, 
    "profile.default_content_setting_values.media_stream_camera": 2, 
    "profile.default_content_setting_values.notifications": 2 
}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://accounts.google.com/signin")

print("Por favor, faça o login manualmente no navegador aberto.")

while True:
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='myaccount.google.com']"))
        )
        print("Login bem-sucedido!")
        break
    except Exception as e:
        print(f"Erro ao verificar login: {e}")
    time.sleep(2)

meeting_code = input("Digite o código da reunião: ")

def join_meeting(meeting_code, driver):
    driver.get(f"https://meet.google.com/{meeting_code}")

    try:
        print("Tentando desligar a câmera e o microfone...")
        camera_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label*="Desligar câmera"]'))
        )
        if "Desligar câmera" in camera_button.get_attribute("aria-label"):
            camera_button.click()

        mic_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label*="Desligar microfone"]'))
        )
        if "Desligar microfone" in mic_button.get_attribute("aria-label"):
            mic_button.click()

        join_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label*="Participar agora"]'))
        )
        join_button.click()

        print("Você entrou na reunião com a câmera e o microfone desligados.")
    except Exception as e:
        print(f"Erro ao tentar entrar na reunião: {e}")

join_meeting(meeting_code, driver)

for i in range(1, 50):
    try:
        time.sleep(5)
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        
        join_meeting(meeting_code, driver)
        
        try:
            join_here_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@jsname="V67aGc" and contains(text(),"Participar por aqui também")]'))
            )
            join_here_button.click()
            print(f"Entrou na reunião na guia {i + 1}.")
        except Exception as e:
            print(f"Erro ao tentar participar por aqui também na guia {i}: {e}")
    except Exception as e:
        print(f"Erro ao abrir nova guia {i}: {e}")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Execução interrompida pelo usuário, mas a janela do navegador permanecerá aberta.")
