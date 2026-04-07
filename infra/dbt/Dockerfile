FROM python:3.11-slim

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /opt/dbt

ENV PATH="/root/.local/bin:${PATH}" \
    DBT_PROFILES_DIR=/opt/dbt

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash git curl ca-certificates libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://public.cdn.getdbt.com/fs/install/install.sh | bash -s -- --update \
    && dbt --version

CMD ["dbt", "--version"]
