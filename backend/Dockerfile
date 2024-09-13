# configura a imagem base
FROM python:3.11.4-slim-bullseye

# impede o Python de fazer buffer de stdout e stderr
ENV PYTHONUNBUFFERED 1

# impede o Python de escrever arquivos .pyc no disco
ENV PYTHONDONTWRITEBYTECODE 1

# define o diretório de trabalho para qualquer instrução RUN, CMD, ENTRYPOINT, COPY e ADD
WORKDIR /app

# instala dependências do sistema
RUN apt-get update 

# instala dependências
RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt
