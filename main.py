from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def votar_varias_vezes(votos):
    url = "https://casacor.abril.com.br/ambientes/vote-banheiro-favorito-casacor-piaui-2024/"
    option_id = "PDI_answer61821523"
    vote_button_id = "pd-vote-button13862347"
    ciente_button_id = "aceitoLGPD"
    feedback_xpath = "//span[@class='pds-answer-text' and contains(text(), 'Lorena Fortes - Lavabos Sensoriais')]/following-sibling::span/span[@class='pds-feedback-per']"

    # Configurar o WebDriver para rodar em modo headless (aqui usamos o Chrome)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)  # ou o caminho completo para o ChromeDriver se não estiver no PATH
    
    for count in range(1, votos + 1):
        try:
            logging.info(f"Voto número: {count}")
            driver.get(url)
            wait = WebDriverWait(driver, 10)

            # Verificar e clicar no botão "CIENTE" se estiver presente
            try:
                ciente_button = wait.until(EC.element_to_be_clickable((By.ID, ciente_button_id)))
                ciente_button.click()
                logging.info("Botão 'CIENTE' clicado")
            except:
                logging.info("Botão 'CIENTE' não encontrado")

            # Esperar até que a opção desejada esteja disponível e clicar nela
            option = wait.until(EC.element_to_be_clickable((By.ID, option_id)))
            option.click()
            logging.info("Opção de voto clicada")

            # Clicar no botão de votar
            votar_button = wait.until(EC.element_to_be_clickable((By.ID, vote_button_id)))
            votar_button.click()
            logging.info("Botão 'Vote' clicado")

            # Esperar a confirmação de votação (ajustar conforme necessário)
            time.sleep(5)

            # Capturar a porcentagem de votos da Lorena Fortes
            feedback = driver.find_element(By.XPATH, feedback_xpath).text.strip()
            logging.info(f"Porcentagem de votos para Lorena Fortes: {feedback}")
            
            # Limpar cookies
            driver.delete_all_cookies()

            # Esperar 5 segundos antes da próxima votação
            time.sleep(2)
            
        except Exception as e:
            logging.error(f"Erro durante a votação: {e}")

    driver.quit()

# Definir o número de votos desejado
numero_de_votos = 1000  # Altere este número conforme necessário

votar_varias_vezes(numero_de_votos)
