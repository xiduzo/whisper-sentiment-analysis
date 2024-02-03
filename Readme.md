This is a python project using the [pywhispercpp](https://github.com/abdeladim-s/pywhispercpp.git) package to run the whisper model.

To get started, install the required packages and run the application.

`pip install -r requirements.txt`

**on non-docker machines**

run `pip install pywhispercpp`

## Running the application

`python main.py` or `python3 main.py`

## Install the python whisper package

This project relies on the `base` model from the [whisper repo](https://github.com/ggerganov/whisper.cpp).

In order to get the model follow the instructions below:

1. Clone the repository (git clone --recurse-submodules https://github.com/abdeladim-s/pywhispercpp.git)
2. Install the model (./pywhispercpp/whisper.cpp/models/download-ggml-model.sh base)

It is possible to use other, move advanced, models:

1. Clone the repository (git clone --recurse-submodules https://github.com/abdeladim-s/pywhispercpp.git)
2. Install the model (./pywhispercpp/whisper.cpp/models/download-ggml-model.sh `<MODEL>`)
3. Set the model path in `main.py` (model = 'pywhispercpp/whisper.cpp/models/ggml-`<MODEL>`.bin')

See [this file](https://github.com/ggerganov/whisper.cpp/blob/master/models/download-ggml-model.sh#L28) for all available models.

# Docker

It is possible to run this application in a docker container. This is useful when you don't want to install the required packages on your host machine.

## Building docker container

You can use this repository to build the docker container. Alternatively, you can use the pre-built container from the [Docker Hub](https://hub.docker.com/repository/docker/xiduzo/whisper-sentiment-analysis/general).

`docker build -f Dockerfile -t whisper .`

## Running docker container

### On a MacBook

Because we need to stream the audio from the host machine to the docker container, we need to install PulseAudio on the host machine and run the PulseAudio server. Then we need to run the docker container with the `--net=host` flag and set the `PULSE_SERVER` environment variable to the IP address of the host machine.

1. Install PulseAudio

`brew install pulseaudio`

2. Run PulseAudio Server (on your MacBook)

`pulseaudio --load=module-native-protocol-tcp --exit-idle-time=-1 --daemon`

**Stopping**

Sometimes the server needs to be stopped and restarted. To stop the server, run the following command:

`pulseaudio --kill`

Then run the start command again.

3. Get IP address of the host machine (your macbook)

`ipconfig getifaddr en0`

4. Run docker container using your IP address:

`docker run --net=host --privileged -e PULSE_SERVER=<HOST> -v ~/.config/pulse:/root/.config/pulse whisper`

or using the pre-built container:

`docker run --net=host --privileged -e PULSE_SERVER=<HOST> -v ~/.config/pulse:/root/.config/pulse xiduzo/whisper-sentiment-analysis`

**validate that the connection is made**

Check if the server is running by running the following command:

`netstat -an | grep 4713`

Should say something like:

```
tcp4       0      0  <HOST>.4713      <HOST>0.49349    ESTABLISHED
tcp4       0      0  <HOST>.49349     <HOST>.4713      ESTABLISHED
tcp4       0      0  *.4713           *.*              LISTEN
tcp6       0      0  *.4713           *.*              LISTEN
```

### On a Raspberry Pi

TODO: add instructions for running on raspberry pi

### Troubleshooting

#### Audio is not being picked up by the docker container

## Configure PulseAudio input- and output devices on host machine

Read useful [Examples](https://wiki.archlinux.org/title/PulseAudio/Examples)

| Command              | Description                |
| -------------------- | -------------------------- |
| `pactl list`         | List all sinks and sources |
| `pacmd info`         | List input devices         |
| `pacmd list-sources` | List input devices         |

**Configure temporary input device**

| Command                                                              | Description        |
| -------------------------------------------------------------------- | ------------------ |
| `pacmd list-sources \| grep -e 'index:' -e device.string -e 'name:'` | List input devices |
| `pacmd set-default-source <INDEX>`                                   | Set input device   |

Example output:

```
index: 0
    name: <Channel_1__Channel_2.monitor>
            device.string = "C49RG9x"
index: 1
    name: <Channel_1>
            device.string = "FHD Webcam"
index: 2
    name: <Front_Left__Front_Right>
            device.string = "HyperX 7.1 Audio"
index: 3
    name: <Front_Left__Front_Right.2.monitor>
            device.string = "HyperX 7.1 Audio"
* index: 4
    name: <Channel_1.2>
            device.string = "MacBook Pro Microphone"
```

**Configure temporary output device**

| Command                                           | Description         |
| ------------------------------------------------- | ------------------- |
| `pacmd list-sinks \| grep -e 'index:' -e 'name:'` | List output devices |
| `pacmd set-default-sink <INDEX>`                  | Set output device   |

Example output:

```
* index: 0
	name: <Channel_1__Channel_2>
index: 1
	name: <Front_Left__Front_Right.2>
index: 2
	name: <1__2>
index: 3
	name: <Channel_1__Channel_2.2>
```

<!-- TODO: add instructions for running on raspberry pi -->

## Validating audio streaming (docker -> mac)

To validate the audio streaming it is possible to play audio from the docker container --> host machine.

| Command                                 | Description                |
| --------------------------------------- | -------------------------- |
| `docker ps`                             | List running containers    |
| `docker exec -it <CONTAINER_ID> bash`   | Get into the container     |
| `ls /usr/share/sounds/alsa/`            | List available sounds      |
| `paplay /usr/share/sounds/alsa/<SOUND>` | Play sound on host machine |
