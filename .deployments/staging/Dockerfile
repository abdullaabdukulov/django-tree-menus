# # # # # # # #
#             #
# BUILD STAGE #
#             #
# # # # # # # #

FROM python:3.11-slim as build-stage

ARG TEMP=/tmp

# # Install packages
RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install requirements
COPY /requirements ${TEMP}
# RUN pip install pip --upgrade && \
#     pip install wheel && \
#     pip wheel --wheel-dir /wheels -r ${TEMP}/staging.txt
# COPY /requirements ${TEMP}
RUN pip install pip --upgrade \
    && pip install --no-cache-dir -r ${TEMP}/staging.txt \
    && rm -rf /tmp


# # # # # # # #
#             #
# FINAL STAGE #
#             #
# # # # # # # #

FROM python:3.11-slim as final-stage

# ARG USERNAME=innmall
ARG APP_HOME=/code
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_HOME}

# create user
# RUN groupadd -r ${USERNAME} \
#     && useradd -r -g ${USERNAME} ${USERNAME}

# Install packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    vim \
    binutils \
    libproj-dev \
    gdal-bin \
    libpq-dev \
    postgresql-client \
    && apt-get clean \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build-stage /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=build-stage /usr/local/bin/ /usr/local/bin/
# COPY --from=build-stage /wheels  ${APP_HOME}/wheels/

# use wheels to install python dependencies
# RUN pip install pip --upgrade && \
#     pip install --no-cache-dir --no-index --find-links=${APP_HOME}/wheels/ ${APP_HOME}/wheels/* && \
#     rm -rf ${APP_HOME}/wheels/


# Add entrypoint.sh
# COPY entrypoint.sh ${APP_HOME}/entrypoint.sh
# COPY run.sh ${APP_HOME}/run.sh

# RUN chmod +x ${APP_HOME}/entrypoint.sh
# RUN chmod +x ${APP_HOME}/run.sh

# Copy project
COPY . ${APP_HOME}

# RUN mkdir -p ${APP_HOME}/static ${APP_HOME}/media \
#     && chown -R ${USERNAME}:${USERNAME} ${APP_HOME}/

# RUN chown -R ${USERNAME}:${USERNAME} ${APP_HOME}

# change to the app user
# USER ${USERNAME}:${USERNAME}

# ENTRYPOINT [ "sh", "/code/entrypoint.sh" ]