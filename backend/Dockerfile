FROM python:3.11-alpine3.19
LABEL maintainer="github.com/ojg1993"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY . ./backend
WORKDIR /backend

ARG DEV=false
# Creating venv and download dependencies as well as user setup
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # Setting up postgres dependencies[build-base postgresql-dev musl-dev]
    # Setting up image dependencies[jpeg-dev]
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    # Deleting postgre dependencies
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    # Creating static & media dirs
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    # Set the owner of the dirs & sub dirs and set the permission(r, w, e)
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts


# Setting absolute path
ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["run.sh"]