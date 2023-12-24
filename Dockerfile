FROM python:3.11

# Copy all the files from the folders the Dockerfile is to the container app folder streamlit cannot run from root
COPY ./app ./app
WORKDIR /app
# Install the modules specified in the requirements.txt
RUN apt-get update && apt-get install -y \
   && apt-get install -y cmake build-essential gcc gfortran libopenblas-dev python3-h5py ca-certificates lsb-release wget \
   #&& wget https://apache.jfrog.io/artifactory/arrow/$(lsb_release --id --short | tr 'A-Z' 'a-z')/apache-arrow-apt-source-latest-$(lsb_release --codename --short).deb \
   #&& apt-get install -y ./apache-arrow-apt-source-latest-$(lsb_release --codename --short).deb \
   #&& apt-get update \
   #&& apt-get install -y libarrow-dev \
   #&& apt-get install -y libarrow-glib-dev \
   && pip3 install patchelf \
   && pip3 install ninja \
   && pip3 install -r requirements.txt

# The port on which a container listens for connections
EXPOSE 8501

# The command that run the app
CMD streamlit run Home.py --server.address 0.0.0.0 --server.port 8501
