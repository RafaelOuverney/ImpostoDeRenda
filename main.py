from selenium import webdriver
import time

navegador = webdriver.Chrome()
navegador.get('https://www27.receita.fazenda.gov.br/simulador-irpf/')
navegador.fullscreen_window()

valores_teste = ["1903,97", "2826,64", "3751,04", "4664,67", "4664,69"]

ano_cal = navegador.find_element("id", "mat-select-0")
ano_cal.click()
ano_cal_2022 = navegador.find_element("id", "mat-option-4")
ano_cal_2022.click()

campo_renda = navegador.find_element("id", "mat-input-0")
campo_renda.clear()
campo_renda.send_keys(valores_teste[0])

time.sleep(5)
navegador.quit()