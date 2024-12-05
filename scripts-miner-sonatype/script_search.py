import argparse
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import time

def fetch_categories(artefato):
    url = f"https://central.sonatype.com/search?q={artefato.replace(':', '%3A')}"
    
    # Iniciar um novo driver dentro da função
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)
        categories_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'nx-tag__text'))
        )
        return [category.text for category in categories_elements] if categories_elements else None
    except Exception as e:
        # print(f"Erro ao buscar categorias: {e}")
        return None
    finally:
        driver.quit()

def main(file_path):
    with open(file_path, 'r') as file:
        artefatos = file.readlines()

    # Utilizando ThreadPoolExecutor para processar em paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_artefato = {executor.submit(fetch_categories, artefato.strip()): artefato.strip() for artefato in artefatos if artefato.strip()}

        for future in concurrent.futures.as_completed(future_to_artefato):
            artefato = future_to_artefato[future]
            try:
                categories = future.result()
                if categories is None:
                    print(f"{artefato};#err_tag_not_found")
                else:
                    formatted_categories = ';'.join(categories)
                    print(f"{artefato}#{formatted_categories}")
                sys.stdout.flush()
            except Exception as e:
                print(f"Erro ao processar {artefato}: {e}")
                sys.stdout.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processa artefatos do arquivo CSV.')
    parser.add_argument('file_path', type=str, help='Caminho do arquivo CSV com os artefatos.')
    args = parser.parse_args()
    
    main(args.file_path)

