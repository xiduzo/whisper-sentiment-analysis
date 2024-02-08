This is a python project using the [pywhispercpp](https://github.com/abdeladim-s/pywhispercpp.git) package to run the whisper model.

`pip install -r requirements.txt`

**on non-docker machines**

run `pip install pywhispercpp`

# Environment variables

| Variable       | Description                                                                                                                      | Default value |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `MODEL`        | The model to use. See [available models](https://github.com/ggerganov/whisper.cpp/blob/master/models/download-ggml-model.sh#L28) | `base`        |
| `PULSE_SERVER` | The IP address of the host machine. Only used when running the application in a docker container                                 | `-`           |

_Volumes (Optional)_
| Volume | Maps to | Description | Default value |
| -------------- | ---| ------------------------------------------------------------------------------------------------ | ------------- |
| `~/.config/pulse` | `/root/.config/pulse` | The pulseaudio configuration files. Only used when running the application in a docker container | `-` |

# Running the application

**on non-docker machines**

`python main.py` or `python3 main.py`

**on docker**

It is possible to run this application in a docker container. This is useful when you don't want to install the required packages on your host machine. Because we need to stream the audio from the host machine to the docker container, we need to install PulseAudio on the host machine and run the PulseAudio server.

The docker container needs to be run with the `--net=host` and `--privileged` flags to be able to connect to the PulseAudio server on the host machine.

## On a Raspberry Pi

> TODO: add instructions for running on raspberry pi

## MacOS

1. Install PulseAudio

   Requires [Homebrew](https://brew.sh/) to be installed.

   run `./install-pulseaudio-for-mac.sh` to install the pulseaudio configuration files.

2. Get IP address of the host machine (your macbook)

   `ipconfig getifaddr en0`

3. Run docker container using your IP address:

   You can either build the container yourself

   `docker build -f Dockerfile -t whisper .`

   `docker run --net=host --privileged -e PULSE_SERVER=<HOST> whisper`

   or using the pre-built container from the [Docker Hub](https://hub.docker.com/repository/docker/xiduzo/whisper-sentiment-analysis/general)

   `docker run --net=host --privileged -e PULSE_SERVER=<HOST> xiduzo/whisper-sentiment-analysis`

## validate that the connection is made

Check if there is a connection between the docker-container and the host machine by running the following command on the host machine:

`netstat -an | grep 4713`

Should say something like:

```
tcp4       0      0  <HOST>.4713      <HOST>.<PORT>    ESTABLISHED
tcp4       0      0  <HOST>.<PORT>    <HOST>.4713      ESTABLISHED
tcp4       0      0  *.4713           *.*              LISTEN
tcp6       0      0  *.4713           *.*              LISTEN
```

## Troubleshooting

### 1. Audio is not being picked up by the docker container

Read [this blog post](https://wiki.archlinux.org/title/PulseAudio/Examples) for useful examples.

| Command      | Description                |
| ------------ | -------------------------- |
| `pactl list` | List all sinks and sources |

**Configure temporary input device**

| Command                                                              | Description        |
| -------------------------------------------------------------------- | ------------------ |
| `pacmd list-sources \| grep -e 'index:' -e device.string -e 'name:'` | List input devices |
| `pacmd set-default-source <INDEX>`                                   | Set input device   |

Example output of listing input devices:

```
index: 0
    name: <Channel_1__Channel_2.monitor>
            device.string = "External screen microphone"
index: 1
    name: <Channel_1>
            device.string = "USB Audio Device"
* index: 2
    name: <Channel_1.2>
            device.string = "MacBook Pro Microphone"
```

**Configure temporary output device**

| Command                                           | Description         |
| ------------------------------------------------- | ------------------- |
| `pacmd list-sinks \| grep -e 'index:' -e 'name:'` | List output devices |
| `pacmd set-default-sink <INDEX>`                  | Set output device   |

Example output of listing output devices:

```
* index: 0
	name: <Channel_1__Channel_2>
index: 1
	name: <Front_Left__Front_Right.2>
index: 2
	name: <1__2>
```

**Validating audio streaming (docker -> host machine)**

To validate the audio streaming it is possible to play audio from the docker container --> host machine.

| Command                                 | Description                               |
| --------------------------------------- | ----------------------------------------- |
| `docker ps`                             | List running containers                   |
| `docker exec -it <CONTAINER_ID> bash`   | Get into the container                    |
| `ls /usr/share/sounds/alsa/`            | List available sounds                     |
| `paplay /usr/share/sounds/alsa/<SOUND>` | Plays sound on host machine output device |
