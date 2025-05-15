# Apache Airflow image as the base
FROM apache/airflow:3.0.1 AS base

# Install Python dependencies
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt

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

COPY pytest.ini ./

EXPOSE 8080
CMD ["airflow", "webserver"]
