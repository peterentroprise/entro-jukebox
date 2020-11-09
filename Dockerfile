###########################
### Build Phase
###########################

FROM continuumio/miniconda3 AS build

COPY environment.yml .
RUN conda env create -f environment.yml

RUN conda install -c conda-forge conda-pack

RUN conda-pack -n jukebox -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

RUN /venv/bin/conda-unpack

###########################
### RUNTIME Phase
###########################

FROM nvidia/cuda:10.1-runtime AS runtime

RUN apt-get update && apt-get install ssh -y

COPY --from=build /venv /venv
COPY ./app /app

SHELL ["/bin/bash", "-c"]
ENTRYPOINT source /venv/bin/activate && \
           uvicorn app.main:app --reload --host 0.0.0.0 --port 8080