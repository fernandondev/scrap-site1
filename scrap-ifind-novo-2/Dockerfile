#Monta uma imagem do python 3.9
FROM python:3.9

# instala algumas dependencias do linux do docker
RUN apt-get update \
    && apt-get -y install gcc make \
    && rm -rf /var/lib/apt/lists/*s
# instala google chrome no linux do docker
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
#Copia tudo do diretorio onde está o Dockerfile do projeto para a pasta /app do linux do docker
COPY . /app
#Muda o diretório DO DOCKER para /app
WORKDIR /app
#Instala todas as dependencias do projeto no linux do docker
RUN pip install --no-cache-dir -r requirements.txt 
#Expõe a porta 5000 para o host (minha máquina)
EXPOSE 5000
#Comando que vai ser rodado ao dar docker container run ou docker start no terminal. Comando rodado ao rodar a imagem no docker
CMD ["python", "main.py"]