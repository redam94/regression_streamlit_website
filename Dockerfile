FROM python:3.11

# Copy all the files from the folders the Dockerfile is to the container app folder streamlit cannot run from root
COPY ./app ./app
WORKDIR /app
# Install the modules specified in the requirements.txt
RUN apt-get update && apt-get install -y \
   && apt-get install -y cmake build-essential gcc gfortran libblas-dev\
   && pip install patchelf \
   && pip install ninja \
   && pip install -r requirements.txt

# The port on which a container listens for connections
EXPOSE 8501

# The command that run the app
CMD streamlit run Home.py --server.address 0.0.0.0 --server.port 8501
