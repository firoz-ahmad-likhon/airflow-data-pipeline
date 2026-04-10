FROM python:3.11-slim

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG DBT_FUSION_VERSION=2.0.0-preview.164

WORKDIR /opt/dbt

ENV PATH="/root/.local/bin:${PATH}" \
    DBT_PROFILES_DIR=/opt/dbt

COPY dbt/ /opt/dbt/

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash git curl ca-certificates libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://public.cdn.getdbt.com/fs/install/install.sh | bash -s -- --update --version "${DBT_FUSION_VERSION}" \
    && dbt --version

CMD ["dbt", "--version"]
