from flask import Flask, request, jsonify
from ifind import Ifind
import logging
from datetime import datetime
from pytz import timezone
import traceback
import json

import undetected_chromedriver as uc

def main():

    app=Flask(__name__)
    
    try:
        
        ifindInstancia = Ifind()
        #Exemplo de chamada: /ifind?parametro=36349840828&tipoParametro=CPF&tipoConsulta=veiculo
        @app.route('/ifind')
        def ifind():
            try:
                brasil = timezone('America/Sao_Paulo')
                dataInicio = datetime.now(brasil).strftime('%d%m%y-%H%M%S')

                #Só faz o scrap se a instância estiver liberada
                if(ifindInstancia.driver.usar is True):
                    #Indisponibiliza a instância
                    ifindInstancia.driver.usar = False

                    parametro = request.args['parametro']
                    tipoParametro = request.args['tipoParametro']
                    tipoConsulta = request.args['tipoConsulta']
                    
                    ifindInstancia.driver.driver.get('https://i-find.org/painel')

                    #Se a url nao for a do painel, quer dizer que deslogou
                    if(ifindInstancia.driver.driver.current_url != 'https://i-find.org/painel'):
                        ifindInstancia.logar()
                    
                    
                    dict = ifindInstancia.selecionarConsulta(parametro, tipoParametro, tipoConsulta)
                    ifindInstancia.driver.usar = True
                    
                    dataFim = datetime.now(brasil).strftime('%d%m%y-%H%M%S')
                    
                    dict.update({'dataInicioConsulta': dataInicio})
                    dict.update({'dataFimConsulta': dataFim})
                    
                    json_string_cod=json.dumps(dict, ensure_ascii=False).encode('utf8')
                    jsonRetorno=json_string_cod.decode()

                    return jsonRetorno
                else:
                    return 'Fila cheia'

            except:
                #Salva o log com o trace e exclui a instancia, cria uma nova do ifind e retorna o trace do erro
                brasil = timezone('America/Sao_Paulo')
                logFilename = 'tmp/logs/'+datetime.now(brasil).strftime('%d%m%y-%H%M%S')+'.log'
                logging.basicConfig(filename=logFilename, level=logging.DEBUG)
                logging.exception('Erro ao executar o script')
                ifindInstancia.driver.driver.close()
                ifindInstancia.driver.driver.quit()
                ifindInstancia.setDriver()
            
                return traceback.format_exc(), 400
        #Método para teste
        @app.route('/teste1')
        def teste1():
            ifindInstancia.driver.driver.get('https://www.globo.com/')
       
            return '1'

        app.run(port=5000, host='0.0.0.0')
        
    except:
        return traceback.format_exc(), 400
    
        
        
    
    

if __name__ == '__main__':
    main()