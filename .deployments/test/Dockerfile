FROM python:3.11-slim

WORKDIR /code
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    binutils \
    libpq-dev \
    gdal-bin \
    # Add other dependencies as needed
    && pip install --upgrade pip

# Copy requirements file
COPY /requirements /code/

# Install requirements
RUN pip install --no-cache-dir -r /code/test.txt

COPY entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# Copy the Django app code
COPY . /code/

ENTRYPOINT [ "sh", "/code/entrypoint.sh" ]