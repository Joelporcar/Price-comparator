from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def amazon(product_name):
    driver = webdriver.Chrome()
    url = "https://www.amazon.es/"
    driver.get(url)
    try:
        search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        search_bar.send_keys(product_name)
        search_bar.send_keys(Keys.RETURN)
        accept_cookie_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "a-autoid-0")))
        accept_cookie_button.click()
        nombre_producto = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-cy='title-recipe'] h2"))).text
        precio_producto = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-cy="price-recipe"]'))).text
        precio_producto_lista = re.split(r'\n', precio_producto)
        if len(precio_producto_lista) < 2:
            precio_producto_lista[0] += ',00€'
            precio_producto = precio_producto_lista[0]
        else:
            precio_producto = precio_producto_lista[0] + ',' + re.findall(r'\d+', precio_producto_lista[1])[0] + '€'
        driver.quit()
        return (nombre_producto, precio_producto, 'Amazon')
    except Exception as e:
        print("Error al extraer los datos en Amazon.")
        driver.quit()
        return ('', '', 'Amazon')

def mediamarkt(product_name):
    driver = webdriver.Chrome()
    url = "https://www.mediamarkt.es"
    driver.get(url)
    try:
        accept_cookie_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pwa-consent-layer-accept-all-button")))
        accept_cookie_button.click()
        search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search-form")))
        search_bar.send_keys(product_name)
        search_bar.send_keys(Keys.RETURN)
        nombre_producto = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="product-title"]'))).text
        precio_producto = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="product-price"]'))).text
        precio_producto_lista = re.split(r'\n', precio_producto)
        if len(precio_producto_lista) < 2:
            precio_producto_lista[0] += ',00€'
            precio_producto = precio_producto_lista[0]
        else:
            precio_producto = precio_producto_lista[1]
        driver.quit()
        return (nombre_producto, precio_producto, 'Mediamarkt')
    except Exception as e:
        print("Error al extraer los datos en Mediamarkt.")
        driver.quit()
        return ('', '', 'Mediamarkt')

def elcorteingles(product_name):
    driver = webdriver.Chrome()
    url = "https://www.elcorteingles.es"
    driver.get(url)
    try:
        accept_cookie_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        accept_cookie_button.click()
        search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchBoxBtn")))
        search_button.click()
        search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search-bar__input")))
        search_bar.send_keys(product_name)
        search_bar.send_keys(Keys.RETURN)
        nombre_producto = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.product_preview-title'))).text
        precio_producto = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.price._sale, .price._current'))).text
        precio_producto_lista = re.findall(r'\d+', precio_producto)
        if len(precio_producto_lista) < 2:
            precio_producto = precio_producto_lista[0] + ',00€'
        else:
            precio_producto = precio_producto_lista[0] + ',' + precio_producto_lista[1] + '€'
        driver.quit()
        return (nombre_producto, precio_producto, 'El Corte Inglés')
    except Exception as e:
        print("Error al extraer los datos en El Corte Inglés.")
        driver.quit()
        return ('', '', 'El Corte Inglés')

def comparar_precios(product_name):
    precios = []
    precios.append(amazon(product_name))
    precios.append(mediamarkt(product_name))
    precios.append(elcorteingles(product_name))
    opciones = []
    for producto in precios:
        if producto[1] is not None:
            precio_float = float(producto[1].replace('€', '').replace(',', '.')) if '€' in producto[1] else float('inf')
            opciones.append((producto[0], precio_float, producto[2]))
    opciones_ordenadas = []
    while opciones:
        menor = opciones[0]
        for opcion in opciones:
            if opcion[1] < menor[1]:
                menor = opcion
        opciones_ordenadas.append(menor)
        opciones.remove(menor)
    if opciones_ordenadas:
        mejor_precio = opciones_ordenadas[0][1]
        mejores_opciones = [opcion for opcion in opciones_ordenadas if opcion[1] == mejor_precio]
        if len(mejores_opciones) == 1:
            print(f"El mejor precio para el producto \"{product_name}\" es {mejor_precio} € en la siguiente tienda:")
        else:
            print(f"El mejor precio para el producto \"{product_name}\" es {mejor_precio} € en las siguientes tiendas:")
        for mejor_opcion in mejores_opciones:
            print(f"- {mejor_opcion[2]}: {mejor_opcion[0]}")
        if len(opciones_ordenadas) > len(mejores_opciones):
            print("Otras opciones disponibles:")
            for opcion in opciones_ordenadas[len(mejores_opciones):]:
                if opcion[1] != float('inf'):
                    print(f"- {opcion[2]}: {opcion[1]} € - {opcion[0]}")
    else:
        print("No se encontró información del producto en ninguna tienda.")

if __name__ == "__main__":
    product_name = input("Introduce el nombre del producto a buscar: ")
    comparar_precios(product_name)
