# imagem base
FROM python:3.12-alpine

# qual diretório vamos usar
WORKDIR /sgn

# melhora os logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copia todos os arquivos do projeto para dentro do container
COPY . .

# atualiza a versão do pip
RUN pip install --upgrade pip
# instala as dependências
RUN pip install -r requirements.txt

# roda as migrações pendentes
RUN python manage.py migrate

# expõe a porta 8000 do container
EXPOSE 8000

# roda a nossa aplicação
CMD python manage.py runserver 0.0.0.0:8000

