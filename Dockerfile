FROM python:3.10.12-slim-buster AS base

COPY requirements.txt /app/requirements.txt
COPY entrypoint.sh /entrypoint.sh
RUN pip install -r /app/requirements.txt
COPY assets/ /app/assets
COPY migrations/ /app/migrations
COPY better_than_yesterday/ /app/better_than_yesterday
WORKDIR /app

ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["/entrypoint.sh"]


FROM base AS prod

RUN apt-get update && apt-get install default-jre -y
RUN pip install gunicorn==20.1.0

ENV FLASK_APP "better_than_yesterday:create_app"
EXPOSE 80
CMD ["-a", "api", "-t", "5", "-w", "1"]


FROM base AS worker
COPY worker.py /app
CMD ["-a", "worker", "-w", "3"]


# FROM base as worker_from_integration
# COPY worker_integration.py /app
# CMD ["-a", "worker_integration", "-t", "1"]


# FROM base as worker_from_integration_dl
# COPY worker_integration_dl.py /app
# CMD ["-a", "worker_integration_dl", "-t", "1"]


# FROM base as worker_nuvem_fiscal
# COPY worker_nuvem_fiscal.py /app
# CMD ["-a", "worker_nuvem_fiscal", "-t", "1"]


# FROM base as worker_nuvem_fiscal_dl
# COPY worker_nuvem_fiscal_dl.py /app
# CMD ["-a", "worker_nuvem_fiscal_dl", "-t", "1"]


FROM prod AS homolog
CMD ["-a", "api", "-t", "5", "-w", "2"]


FROM worker AS worker-homolog
CMD ["-a", "worker", "-w", "3"]


# FROM worker_from_integration AS worker_from_integration-homolog
# CMD ["-a", "worker_integration", "-t", "1"]


# FROM worker_from_integration_dl AS worker_from_integration_dl-homolog
# CMD ["-a", "worker_integration_dl", "-t", "1"]


# FROM worker_nuvem_fiscal AS worker_nuvem_fiscal-homolog
# CMD ["-a", "worker_nuvem_fiscal", "-t", "1"]


# FROM worker_nuvem_fiscal_dl AS worker_nuvem_fiscal_dl-homolog
# CMD ["-a", "worker_nuvem_fiscal_dl", "-t", "1"]