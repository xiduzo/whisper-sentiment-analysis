# https://hub.docker.com/_/python
FROM python:3.11.7

# Get shit to make the container to work
RUN apt update && apt install -y ffmpeg alsa-utils pulseaudio pulseaudio-utils libportaudio2 libasound-dev nano && apt clean

# Install the required packages
WORKDIR /usr/src/app
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install pywhispercpp repository
RUN git clone --recurse-submodules https://github.com/abdeladim-s/pywhispercpp.git

# Build and install pywhispercpp
WORKDIR /usr/src/app/pywhispercpp
RUN python -m build --wheel
RUN pip install dist/pywhispercpp-*.whl

# Copy the main.py file
WORKDIR /usr/src/app
COPY main.py ./
COPY src ./

CMD ["python3", "-u", "main.py"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]
