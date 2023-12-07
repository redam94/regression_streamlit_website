FROM python:3.11

# Copy all the files from the folders the Dockerfile is to the container root folder
COPY . ./app
WORKDIR /app
# Install the modules specified in the requirements.txt
RUN pip3 install -r requirements.txt

# The port on which a container listens for connections
EXPOSE 8501

# The command that run the app
CMD streamlit run Home.py --server.address 0.0.0.0 --server.port 8501