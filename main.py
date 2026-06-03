from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv 
from valores_teste import valores

navegador = webdriver.Chrome()
navegador.get('https://www27.receita.fazenda.gov.br/simulador-irpf/')
navegador.fullscreen_window()

valores_teste = valores

resultados_finais = []

espera = WebDriverWait(navegador, 10)

ano_cal = espera.until(EC.element_to_be_clickable((By.ID, "mat-select-0")))
ano_cal.click()
ano_cal_2022 = espera.until(EC.element_to_be_clickable((By.ID, "mat-option-4")))
ano_cal_2022.click()

campo_renda = espera.until(EC.presence_of_element_located((By.ID, "mat-input-0")))

print("Iniciando a coleta de dados...")

for valor in valores_teste:
    campo_renda.click()
    campo_renda.send_keys(Keys.CONTROL + "a")
    campo_renda.send_keys(Keys.BACKSPACE)
    
    campo_renda.send_keys(valor)
    campo_renda.send_keys(Keys.TAB)

    time.sleep(1.5)
    
    try:
        aliquota = navegador.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div/div/div/app-root/p/mat-tab-group/div/mat-tab-body[1]/div/calculo-mensal/div/form/mat-card[4]/div[2]/label/span[1]").text
        valor_imposto = navegador.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div/div/div/app-root/p/mat-tab-group/div/mat-tab-body[1]/div/calculo-mensal/div/form/mat-accordion[2]/mat-expansion-panel/mat-expansion-panel-header/span[1]/mat-panel-title/label[2]").text
        aliquota_efetiva = navegador.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div/div/div/app-root/p/mat-tab-group/div/mat-tab-body[1]/div/calculo-mensal/div/form/mat-card[4]/div[1]/label[2]").text
    except Exception:
        print(f"Erro ao capturar os dados para o valor: R$ {valor}. Verifique o XPath ou a estrutura do site.")
        continue  

    dados_rodada = {
        "Base de Cálculo": valor,
        "Alíquota": aliquota,
        "Valor do Imposto": valor_imposto,
        "Alíquota Efetiva": aliquota_efetiva
    }
    
    resultados_finais.append(dados_rodada)
    print(f"Dados coletados com sucesso para o valor: R$ {valor}")

navegador.quit()

nome_planilha = "simulacao_irpf_resultados.csv"

with open(nome_planilha, mode="w", newline="", encoding="utf-8-sig") as arquivo:
    colunas = ["Base de Cálculo", "Alíquota", "Valor do Imposto", "Alíquota Efetiva"]
    config_csv = csv.DictWriter(arquivo, fieldnames=colunas)
    config_csv.writeheader()
    config_csv.writerows(resultados_finais)

print(f"\nA planilha '{nome_planilha}' foi gerada no diretório.")