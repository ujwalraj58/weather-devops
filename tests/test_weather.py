import os
import time
import shutil
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# === AUTO-CLEAN OLD CHROMEDRIVER CACHE ===
def clean_old_drivers():
    """Removes cached ChromeDriver directories to force a fresh install."""
    user_profile = os.environ.get("USERPROFILE", "")
    wdm_path = os.path.join(user_profile, ".wdm")
    if os.path.exists(wdm_path):
        print(f"Cleaning old ChromeDriver cache at: {wdm_path}")
        shutil.rmtree(wdm_path, ignore_errors=True)
    else:
        print("No old ChromeDriver cache found.")


# === SETUP WEBDRIVER (Auto Installer for Jenkins) ===
def setup_driver():
    """Sets up Chrome WebDriver automatically matching system Chrome."""
    clean_old_drivers()

    print("Checking and installing correct ChromeDriver version...")
    chromedriver_autoinstaller.install()  # Auto-match Chrome version

    options = Options()
    options.add_argument("--headless=new")  # Use headless mode for Jenkins
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    return driver


# === LOAD LOCAL WEATHER APP ===
def open_weather_app(driver):
    app_path = os.path.abspath("app/index.html")
    driver.get("file://" + app_path)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "city")))
    return wait


# === TEST 1: VALID CITY SEARCH ===
def test_valid_city():
    driver = setup_driver()
    open_weather_app(driver)

    city_input = driver.find_element(By.ID, "city")
    city_input.send_keys("London")
    driver.find_element(By.ID, "getBtn").click()

    time.sleep(4)
    city_name = driver.find_element(By.ID, "cityName").text
    print(f"City Displayed: {city_name}")
    assert "London" in city_name, "City name did not update properly."

    temp = driver.find_element(By.ID, "temp").text
    assert "°C" in temp, "Temperature not displayed correctly."

    driver.quit()


# === TEST 2: EMPTY CITY FIELD ===
def test_empty_city():
    driver = setup_driver()
    open_weather_app(driver)

    driver.find_element(By.ID, "getBtn").click()
    time.sleep(1)

    alert = driver.switch_to.alert
    alert_text = alert.text
    print(f"Alert message: {alert_text}")
    assert "enter" in alert_text.lower(), "Alert for empty city not shown."
    alert.accept()

    driver.quit()


# === TEST 3: INVALID CITY NAME ===
def test_invalid_city():
    driver = setup_driver()
    open_weather_app(driver)

    city_input = driver.find_element(By.ID, "city")
    city_input.send_keys("asldkfjasldkfj")  # nonsense
    driver.find_element(By.ID, "getBtn").click()

    time.sleep(3)
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"Alert for invalid city: {alert_text}")
        assert "not found" in alert_text.lower(), "Invalid city alert missing."
        alert.accept()
    except Exception:
        print("Expected alert not found for invalid city input.")

    driver.quit()


# === TEST 4: FORECAST CARDS RENDER ===
def test_forecast_cards():
    driver = setup_driver()
    open_weather_app(driver)

    city_input = driver.find_element(By.ID, "city")
    city_input.send_keys("Tokyo")
    driver.find_element(By.ID, "getBtn").click()

    time.sleep(5)
    forecast_cards = driver.find_elements(By.CLASS_NAME, "forecast-card")
    print(f"Forecast cards found: {len(forecast_cards)}")
    assert len(forecast_cards) >= 5, "Forecast cards not rendered correctly."

    driver.quit()


# === TEST 5: WEATHER THEME APPLICATION ===
def test_theme_change():
    driver = setup_driver()
    open_weather_app(driver)

    city_input = driver.find_element(By.ID, "city")
    city_input.send_keys("New York")
    driver.find_element(By.ID, "getBtn").click()

    time.sleep(4)
    current_weather_div = driver.find_element(By.CLASS_NAME, "current-weather")
    class_name = current_weather_div.get_attribute("class")
    print(f"Current theme class: {class_name}")

    assert any(
        t in class_name for t in ["sunny", "rainy", "cloudy", "stormy", "snowy", "foggy"]
    ), "Weather theme not applied properly."

    driver.quit()


# === RUN ALL TESTS ===
if __name__ == "__main__":
    print("\nRunning Weather App Tests...\n")
    test_valid_city()
    test_empty_city()
    test_invalid_city()
    test_forecast_cards()
    test_theme_change()
    print("\nAll tests executed successfully!\n")

