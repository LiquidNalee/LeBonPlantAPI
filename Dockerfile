###############################################
## Target for setting up the python-base image
## And run all the ONBUILD once.
###############################################
ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION} as python-base

ARG USER
ENV USER=${USER}
ARG USER_UID
ENV USER_UID=${USER_UID}
ARG USER_GID
ENV USER_GID=${USER_GID}

RUN useradd -rm -s /bin/bash -g root -G sudo -u ${USER_UID} ${USER}
USER ${USER}

ENV WORKDIR_PATH="/home/${USER}/app"
WORKDIR ${WORKDIR_PATH}
ENV PATH="/home/${USER}/.local/bin:${PATH}"
ENV PYTHONPATH=${WORKDIR_PATH}
ENV PIPENV_SYSTEM 1

###############################################
## Target for prod dependencies installation
###############################################
FROM python-base as prod-deps

COPY Pipfile Pipfile.lock ./

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}

RUN pip install --upgrade -q pipenv
RUN pipenv install --deploy

###############################################
## Target for test dependencies installation
###############################################
FROM prod-deps as test-deps

RUN pipenv install --deploy --dev

###############################################
## Target for production image
###############################################
FROM python-base as prod

USER root

RUN apt-get update && apt-get install -y postgresql-client

USER ${USER}

COPY --chown=${USER_UID}:${USER_GID} --from=prod-deps /home/${USER}/.local /home/${USER}/.local
ARG APP_NAME
COPY --chown=${USER_UID}:${USER_GID} ${APP_NAME} ./${APP_NAME}
COPY --chown=${USER_UID}:${USER_GID} wait-for-postgres.sh rundb.py runserver.py ./
COPY --chown=${USER_UID}:${USER_GID} instance ./instance

ENTRYPOINT ["run-program"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--worker_class", "uvicorn.workers.UvicornWorker", "runserver:app"]

###############################################
## Target for test image
###############################################
FROM python-base as test

USER root

RUN apt-get update && apt-get install -y postgresql-client

USER ${USER}

COPY --chown=${USER_UID}:${USER_GID} --from=test-deps /home/${USER}/.local /home/${USER}/.local
ARG APP_NAME
COPY --chown=${USER_UID}:${USER_GID} ${APP_NAME} ./${APP_NAME}
COPY --chown=${USER_UID}:${USER_GID} .editorconfig .flake8 wait-for-postgres.sh rundb.py runserver.py ./
COPY --chown=${USER_UID}:${USER_GID} instance ./instance
COPY --chown=${USER_UID}:${USER_GID} tests ./tests