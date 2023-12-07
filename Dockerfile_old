FROM ubuntu:22.04

# update apt and get miniconda
RUN apt-get update \
    && apt-get install -y wget \
    && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

RUN apt-get install libtiff-dev -y

COPY ./cross_environment.yml ./cross_environment.yml
# install miniconda
ENV PATH="/root/miniconda3/bin:$PATH"
RUN mkdir /root/.conda && bash Miniconda3-latest-Linux-x86_64.sh -b

# create conda environment
RUN conda init bash \
    && . ~/.bashrc \
    && conda env update -n base -f cross_environment.yml 
RUN rm cross_environment.yml

RUN mkdir ./app
COPY ./ ./app/

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["/bin/bash", "-c", "cd ./app && streamlit run Home.py --browser.gatherUsageStats false --server.port 8501 --server.address 0.0.0.0"]