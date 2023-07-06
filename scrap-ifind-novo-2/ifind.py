

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json
import random
import time
import os
from selenium.webdriver.support.ui import Select
from recapcha import Recaptcha
from time import sleep
import undetected_chromedriver as uc
import re
from driver import Driver


#----------------------------------------Variáveis básicas







class Ifind:
    def __init__(self):
        #------Driver Chrome------
        #Cada instância deverá ter seu respectivo user agent 
        #Cada instância deverá ter sua conta  
        #só poderá ser utilizada quando a variável booleana 'liberado' estiver 'true'
        self.api_key='minhaKeyCaptcha'
        self.usuario='meuUsuario'
        self.senha='minhaSenha'
        self.driver = Driver()
        self.driver.driver.get('https://www.google.com.br')

    def setDriver(self):
        self.driver = Driver()
        self.driver.driver.get('https://www.google.com.br')

        

    #-----------------------------------------Funções teste----------------------------

    def printarUserAgent(self):
        #sem setar o user agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
        #setando o user agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 
        self.driver.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})
        #self.driver.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

        print(self.driver.driver.execute_script("return navigator.userAgent;"))


    #------------------------------------------------Funções auxiliares----------------------------------------------------
    #Funções que servem apenas para reduzir as linhas do código principal

    #Interrompe a execução do código no intervalo informado
    def sleep(self,numeroMenor, numeroMaior):
        
        time.sleep(random.uniform(numeroMenor, numeroMaior))



    #----------------------------------------Funções de navegação e extração de dados------------------------------
    #Essas funções são as que navegam pelas páginas web usando o selenium

    def logar(self):
        if self.driver.driver.current_url != 'https://i-find.org/login':
            self.driver.driver.get('https://i-find.org/login')
        #Preenche o usuário
        input_usuario=self.driver.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="formLogin"]/div[1]/input')))
        self.sleep(2, 4)
        input_usuario.click()
        input_usuario.clear()
        self.sleep(1,1.2)
        letrasUsuario = [*self.usuario]
        for letra in letrasUsuario:
            input_usuario.send_keys(letra)
            self.sleep(0.1, 0.4)
        #Preenche a senha
        input_senha=self.driver.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="formLogin"]/div[2]/input')))
        self.sleep(2,4)
        letrasSenha = [*self.senha]
        input_senha.click()
        input_senha.clear()
        self.sleep(1,1.2)
        for letra in letrasSenha:
            input_senha.send_keys(letra)
            self.sleep(0.1, 0.4)
        #------------------Quebrar recaptcha
        recaptchaElement=self.driver.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'g-recaptcha')))
        siteKey = recaptchaElement.get_attribute('data-sitekey')
        resultado = Recaptcha('https://i-find.org/login', siteKey).resolver()['code']
        print(resultado)
        #Procura o nome do iframe pela tag e valor do atributo 'title'
        #soup = BeautifulSoup(html, 'html.parser')
        #nameIframe = soup.find('iframe', {'title' : 'reCAPTCHA'})['name']
        #nameIframe=self.driver.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'iframe'))).get_attribute('name')
        #self.driver.driver.switch_to.frame(nameIframe)
        comando = "document.getElementById('g-recaptcha-response').innerHTML="+ "'" +resultado+"'"
        self.driver.driver.execute_script(comando)
        #self.driver.driver.switch_to.default_content()
        botaoEntrar=self.driver.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="login"]')))
        self.sleep(2, 3.5)
        botaoEntrar.click()


#------------------------------------------Extração dos dados da consulta binfed
    def extrairDadosPlaca(self):
        #------------------------------------------Extração dos dados
        dict={}
        #Dados Básicos
        trs1=self.driver.wait.until(EC.visibility_of_all_elements_located((By.XPATH,'/html/body/div[6]/div/div/div/div[1]/table/tbody/tr')))

        for tr in trs1:
            tag=tr.find_element(By.TAG_NAME, 'th')
            valor=tr.find_element(By.TAG_NAME, 'td')
            dict.update({tag.text:valor.text})

                                                    #TABELA ESQUERDA

        #TODOS DA DIV ESQUERDA MENOS A ULTIMA, POIS FOGE DO PADRAO
        tables=self.driver.wait.until(EC.visibility_of_all_elements_located((By.XPATH,'/html/body/div[6]/div/div/div/div[2]/table/tbody')))
        titulos=self.driver.wait.until(EC.visibility_of_all_elements_located((By.XPATH,'/html/body/div[6]/div/div/div/div[2]/h1')))
        tableIndRest=tables[-1]
        tables.pop()
        #print(tables)
    
        i=0
        for table in tables:
            titulo=titulos[i]
            i= i+1
            trs=table.find_elements(By.TAG_NAME, 'tr')
            dictTrs={}

            for tr in trs:
                tag=tr.find_element(By.TAG_NAME, 'th')
                valor=tr.find_element(By.TAG_NAME, 'td')
                #print(tag.text+ ' : ' + valor.text)
                dictTrs.update({tag.text: valor.text})
            dict.update({titulo.text:dictTrs})

        #Indicador de Restrição

        titulo2=titulos[-1]
        if('ndicadore' in titulo2.text):
            dictTrs2={}
            trs = tableIndRest.find_elements(By.TAG_NAME, 'tr')
            for tr in trs:
                tds=tr.find_elements(By.TAG_NAME, 'td')
                tag=tds[0]
                valor=tds[1]
                dictTrs2.update({tag.text:valor.text})
            dict.update({titulo2.text: dictTrs2})


        

        return dict
    

#------------------------------------------Extração dos dados da consulta cnh 
    def extrairDadosCnh(self):
        dict = {}
        
        campo_texto=self.driver.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div')))

        #Itera essa string, trata e pega os campos e valores e insere no dict, que será, posteriormente, convertido em um json
        listaCampoValor = campo_texto.text.replace(': ', ':')
        listaCampoValor = re.sub('\r?\n', '*', listaCampoValor).split('*')

        
        for elemento in listaCampoValor:
            try:

                campoValor = elemento.split(':')
                dict.update({campoValor[0]:campoValor[1]})
            except:
                continue


        return dict
    
#------------------------------------------Extração dos dados da consulta de frota     
    def extrairDadosFrota(self):
        dict = {}
        campos_texto = self.driver.wait.until(EC.visibility_of_all_elements_located((By.XPATH, '/html/body/div[6]/div/div'))) 
        for index, campoTexto in enumerate(campos_texto):
            subDict = {}
            print('------------------------campoTexto.text')
            print(campoTexto.text)
            
            try:
                subSubCampoTexto = re.sub('\r?\n', '*', campoTexto.text).split('*')
                print('---------------------subSubCampoTexto')
                print(subSubCampoTexto)


                for elemento in subSubCampoTexto:
                    try:
                        subElemento = elemento.split(':')
                        subDict.update({subElemento[0]: subElemento[1]})
                    except:
                        print('caiu except 235')
                        continue
                titulo = 'veiculo' + str(index)
                dict.update({titulo: subDict})
            except:
                print('caiu except 238')
                continue

    

        return dict


    def selecionarConsulta(self,parametro, tipoParametro, tipoConsulta):
        #--------------------------------------------Tela seleção consulta-----------------------
        if tipoConsulta == 'veiculo':
            #func
            #Seleciona o card da consulta veículo
            btn_veiculos=self.driver.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[4]/div')))
            self.sleep(2, 3)
            btn_veiculos.click()
        elif tipoConsulta == 'cnh':
            #Seleciona o card da consulta cnh
            btn_habilitacao = self.driver.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[7]/div')))
            self.sleep(2, 3)
            btn_habilitacao.click()

        numeroAleatorio = random.uniform(0, 1)

        #disfarçar(Vai por caminho alternativo ao original, nesse caso, retorna para a tela do painel e retorna para a tela de seleção de consultas)
        if numeroAleatorio > 0.5:
            btn_home=self.driver.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/a[1]/span')))
            self.sleep(1.5, 2.5)
            btn_home.click()
            if tipoConsulta == 'veiculo':
                #func
                #Seleciona o card da consulta veículo
                btn_veiculos=self.driver.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[4]/div')))
                self.sleep(2, 3)
                btn_veiculos.click()
            elif tipoConsulta == 'cnh':
                #Seleciona o card da consulta cnh
                btn_habilitacao = self.driver.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[7]/div')))
                self.sleep(2, 3)
                btn_habilitacao.click()

        #func
        #Seleciona o tipo de parametro de entrada 
        select_element=self.driver.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/form/select')))
        self.sleep(2, 3)
        select = Select(select_element)
        self.sleep(1.5, 2.5)
        select.select_by_value(tipoParametro)
        #Preenche o parametro de entrada
        input_parametro = self.driver.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/form/input')))
        self.sleep(1,2)
        letrasParametro = [*parametro]
        input_parametro.click()
        input_parametro.clear()
        self.sleep(1,1.2)
        for letra in letrasParametro:
            input_parametro.send_keys(letra)
            self.sleep(0.4, 1)
        
        
        #Quebrar outro captcha aqui (Pode ser que nem sempre apareça)
        #------------------Quebrar recaptcha
        if len(self.driver.driver.find_elements(By.CLASS_NAME, 'g-recaptcha'))>0:
            recaptchaElement=self.driver.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'g-recaptcha')))
            siteKey = recaptchaElement.get_attribute('data-sitekey')
            resultado = Recaptcha('https://i-find.org/login', siteKey).resolver()['code']
            print(resultado)
            #Procura o nome do iframe pela tag e valor do atributo 'title'
            #html = self.driver.driver.page_source
            #soup = BeautifulSoup(html, 'html.parser')
            #nameIframe = soup.find('iframe', {'title' : 'reCAPTCHA'})['name']
            #nameIframe=self.driver.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'iframe'))).get_attribute('name')
            #self.driver.driver.switch_to.frame(nameIframe)
            
            comando = "document.getElementById('g-recaptcha-response').innerHTML="+ "'" +resultado+"'"
            self.driver.driver.execute_script(comando)
           # self.driver.driver.switch_to.default_content()
        botaoConsultar=self.driver.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="realizar"]')))
        self.sleep(2, 3.5)
        botaoConsultar.click()


        if tipoConsulta == 'veiculo' and (tipoParametro == 'CNPJ' or tipoParametro == 'CPF'):
            return self.extrairDadosFrota()

        if tipoConsulta == 'veiculo':
            return self.extrairDadosPlaca()
        
        elif tipoConsulta == 'cnh':
            return self.extrairDadosCnh()


   











    

