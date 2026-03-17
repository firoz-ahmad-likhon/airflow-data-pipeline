# Apache Airflow image as the base
FROM apache/airflow:3.0.1 AS base

# Set workdir
WORKDIR /opt/airflow

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY dags/ dags/
COPY alembic/ alembic/
COPY alembic.ini .

# Production stage
FROM base AS prod

EXPOSE 8080
CMD ["airflow", "webserver"]

# Development stage
FROM base AS dev

# Install dev-specific Python tools
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

EXPOSE 8080
CMD ["airflow", "webserver"]
