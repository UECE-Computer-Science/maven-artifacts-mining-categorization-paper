import argparse
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures


def fetch_categories(artifact):
    url = f"https://central.sonatype.com/search?q={artifact.replace(':', '%3A')}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        categories_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "nx-tag__text"))
        )
        return (
            [category.text for category in categories_elements]
            if categories_elements
            else None
        )
    except Exception as e:
        return None
    finally:
        driver.quit()


def main(file_path):
    with open(file_path, "r") as file:
        artifacts = file.readlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_artifact = {
            executor.submit(fetch_categories, artifact.strip()): artifact.strip()
            for artifact in artifacts
            if artifact.strip()
        }

        for future in concurrent.futures.as_completed(future_to_artifact):
            artifact = future_to_artifact[future]
            try:
                categories = future.result()
                if categories is None:
                    print(f"{artifact};#err_tag_not_found")
                else:
                    formatted_categories = ";".join(categories)
                    print(f"{artifact}#{formatted_categories}")
                sys.stdout.flush()
            except Exception as e:
                print(f"Erro ao processar {artifact}: {e}")
                sys.stdout.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="process artifact in file CSV.")
    parser.add_argument("file_path", type=str, help="path of file CSV with artifacts.")
    args = parser.parse_args()

    main(args.file_path)
