# Apache Airflow image as the base
FROM apache/airflow:3.0.1 AS base

# Set workdir
WORKDIR /opt/airflow

# Install Python dependencies
COPY airflow/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY airflow/dags/ dags/
COPY airflow/pipelines/ pipelines/
COPY airflow/plugins/ plugins/
COPY alembic/ alembic/
COPY alembic.ini .

# Production stage
FROM base AS prod

EXPOSE 8080
CMD ["airflow", "webserver"]

# Development stage
FROM base AS dev

# Install dev-specific Python tools
COPY airflow/requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

EXPOSE 8080
CMD ["airflow", "webserver"]
