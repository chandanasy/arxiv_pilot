FROM python:3.12-slim

RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 -ms /bin/bash appuser

# RUN \
#     --mount=type=cache,target=/var/cache/pip \
#     pip3 install --no-cache-dir --upgrade \
#     pip \
#     virtualenv

# RUN \
#     --mount=type=cache,target=/var/cache/apt \
#     apt-get update && apt-get install -y \
#     build-essential \
#     software-properties-common \
#     git


RUN pip3 install --no-cache-dir --upgrade \
    pip \
    virtualenv

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git

USER appuser
WORKDIR /home/appuser
RUN mkdir app
COPY . ./app
RUN mkdir -m u+rw app/pdfs
RUN mkdir -m u+rw app/data
RUN mkdir -m u+rw app/images

ENV VIRTUAL_ENV=/home/appuser/venv
RUN virtualenv ${VIRTUAL_ENV}
RUN \
    --mount=type=cache,target=/var/cache/pip \
    . ${VIRTUAL_ENV}/bin/activate && pip install -r app/requirements.txt

EXPOSE 8501

COPY run.sh /home/appuser
ENTRYPOINT ["/bin/bash","./run.sh"]