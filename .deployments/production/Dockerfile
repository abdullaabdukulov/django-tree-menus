# # # # # # # #
#             #
# BUILD STAGE #
#             #
# # # # # # # #
# ARG PYTHON_VERSION=3.11-slim
# FROM python:${PYTHON_VERSION} as python
FROM python:3.11-slim as build-stage

ARG TEMP=/tmp

# # Install packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev

# Install requirements
COPY /requirements ${TEMP}
# RUN pip install pip --upgrade && \
#     pip install wheel && \
#     pip wheel --wheel-dir /wheels -r ${TEMP}/production.txt
# COPY /requirements ${TEMP}
RUN pip install pip --upgrade && \
    pip install --no-cache-dir -r ${TEMP}/staging.txt && \
    rm -rf /tmp


# # # # # # # #
#             #
# FINAL STAGE #
#             #
# # # # # # # #
FROM python:3.11-slim as run-stage

# ARG USERNAME=django_tree_menus
ARG APP_HOME=/code
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_HOME}

# create user
# RUN groupadd -g 10001 ${USERNAME} && \
#     useradd -u 10000 -g ${USERNAME} ${USERNAME}

# Install packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    vim \
    binutils \
    libproj-dev \
    gdal-bin \
    libpq-dev \
    postgresql-client && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build-stage /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=build-stage /usr/local/bin/ /usr/local/bin/
# COPY --from=build-stage /wheels  ${APP_HOME}/wheels/

# use wheels to install python dependencies
# RUN pip install pip --upgrade && \
#     pip install --no-cache-dir --no-deps --no-index --find-links=${APP_HOME}/wheels/ ${APP_HOME}/wheels/* && \
#     rm -rf ${APP_HOME}/wheels/


# Add entrypoint.sh
# COPY entrypoint.sh ${APP_HOME}/entrypoint.sh
# COPY run.sh ${APP_HOME}/run.sh

# RUN chmod +x ${APP_HOME}/entrypoint.sh
# RUN chmod +x ${APP_HOME}/run.sh

# Copy project
COPY . ${APP_HOME}

# RUN mkdir -p ${APP_HOME}/static && \
#     mkdir -p ${APP_HOME}/media

# RUN chown -R ${USERNAME}:${USERNAME} ${APP_HOME}

# change to the app user
# USER ${USERNAME}:${USERNAME}

# ENTRYPOINT [ "sh", "/code/entrypoint.sh" ]