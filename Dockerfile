# Apache Airflow image as the base
FROM apache/airflow:2.10.2 AS base
# Switch back to airflow user
USER airflow
# Set working directory
WORKDIR /opt/airflow
# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM base AS prod

EXPOSE 8080
CMD ["airflow", "webserver"]

# Development stage
FROM base AS dev

# Install dev-specific Python tools
RUN pip install \
    pytest==8.3.3 \
    pytest-mock==3.14.0 \
    types-requests==2.32.0.20240914

EXPOSE 8080
CMD ["airflow", "webserver"]
