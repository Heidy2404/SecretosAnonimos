from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración del driver
driver = webdriver.Chrome()

try:
    # Abre la página de publicación
    driver.get("http://127.0.0.1:5000")

    # Espera hasta que el textarea esté disponible
    textarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "contenido"))
    )
    textarea.send_keys("Me gusta un chinito jajajj")

    # Espera hasta que el botón de enviar sea clicable
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "enviar"))
    )
    submit_button.click()

    # Espera a que la página principal cargue
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
     # Busca el botón de aprobación del último secreto
    approve_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Aprobar')]"))
    )
    approve_button.click()
     
  
    # Espera a que se procese el formulario y verifica el resultado
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "success"))
    )
    print("Prueba completada: El mensaje se publicó correctamente.")

except Exception as e:
    print("Error durante la prueba:", e)

finally:
    # Cierra el navegador
    driver.quit()