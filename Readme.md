This is a python project transforming sentiment analysis of audio to MQTT messages.

It using the [pywhispercpp](https://github.com/abdeladim-s/pywhispercpp.git) package to run the whisper model for speech-to-text and [huggingface](https://huggingface.co/models?pipeline_tag=text-classification&sort=trending) package to run the text-classification model. The output is streamed to a MQTT broker.

Before we can start we need to install [ffmpeg](https://ffmpeg.org/)

```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

# Running the application

The application is intended to be ran as a standalone application as this requires the minimal amount of effort to get started.

However, it is possible to run the application in a docker container to avoid installing the required packages on your host machine.

## On non-docker machines

Install the dependencies:

1. `pip install -r requirements.txt`
2. `pip install pywhispercpp`

Run the application:

1. `python main.py`
2. or `python3 main.py`

## On docker

It is possible to run this application in a docker container.

Because we need to stream the audio from the host machine to the docker container, we need to install PulseAudio on the host machine and run the PulseAudio server.

Below we will make the distinction between the _host machine_ and the _docker container_.

The _host machine_ is your current device (e.g. your laptop, raspberry pi, etc.) and the _docker container_ is the container that is running the sentiment analysis.

### With linux (Raspberry Pi)

> TODO: add instructions for running on raspberry pi

### With MacOS

1. Install PulseAudio on your macbook

   run `./install-pulseaudio-for-mac.sh`

2. Get your current IP address of your macbook

   `ipconfig getifaddr en0`

   The output should be something like `192.168.2.0`, and this value should be used to replace `<HOST>` below for the `PULSE_SERVER` variable.

   > ⚠️ Your IP address will be different from each network you connect to.

3. Run docker container using your IP address

   The docker container needs to be run with the `--net=host` and `--privileged` flags to be able to connect to the PulseAudio server on the host machine.

   > Make sure to always update the `PULSE_SERVER` environment variable to the correct IP address when changing locations/networks.

   1. You can either build the container yourself

      `docker build -f Dockerfile -t whisper .`

      `docker run --net=host --privileged -e PULSE_SERVER=<HOST> whisper`

   2. or using the pre-built container from the [Docker Hub](https://hub.docker.com/repository/docker/xiduzo/whisper-sentiment-analysis/general)

      `docker run --net=host --privileged -e PULSE_SERVER=<HOST> xiduzo/whisper-sentiment-analysis:latest`

## All environment variables

| Variable                    | Description                                                                                                   | Default value                                                                                                         |
| --------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `WHISPER_MODEL`             | The [whisper model](https://github.com/ggerganov/whisper.cpp/blob/master/models/download-ggml-model.sh#L28)   | `base.en`                                                                                                             |
| `PULSE_SERVER`\*            | When running in docker                                                                                        | `-`                                                                                                                   |
| `TEXT_CLASSIFICATION_MODEL` | The [text-classification model](https://huggingface.co/models?pipeline_tag=text-classification&sort=trending) | [j-hartmann/emotion-english-distilroberta-base](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base) |
| `MQTT_HOST`                 | The host of the MQTT broker                                                                                   | `test.mosquitto.org`                                                                                                  |
| `MQTT_USER`                 | When using a MQTT broker which requires authentication                                                        | `None`                                                                                                                |
| `MQTT_PWD`                  | When using a MQTT broker which requires authentication                                                        | `None`                                                                                                                |
| `MQTT_BASE_TOPIC`           | The host of the MQTT broker                                                                                   | `sentiment_analysis_base_topic`                                                                                       |

\* Required

_Volumes (Optional)_
| Volume | Maps to | Description | Default value |
| -------------- | ---| ------------------------------------------------------------------------------------------------ | ------------- |
| `~/.config/pulse` | `/root/.config/pulse` | The pulseaudio configuration files. Only used when running the application in a docker container | `-` |

## Troubleshooting

### 1. Validate that the connection is made (when running in docker)

Check if there is a connection between the docker-container and the host machine by running the following command on the host machine:

`netstat -an | grep 4713`

Should say something like:

```
tcp4       0      0  <HOST>.4713      <HOST>.<PORT>    ESTABLISHED
tcp4       0      0  <HOST>.<PORT>    <HOST>.4713      ESTABLISHED
tcp4       0      0  *.4713           *.*              LISTEN
tcp6       0      0  *.4713           *.*              LISTEN
```

### 2. Audio is not being picked up by the docker container

> ⚠️ Whenever you attach a new audio device to your host machine, you need to reconfigure the input and output devices.

> ⚠️ Whenever you restart your host machine, you need to reconfigure the input and output devices.

`PulseAudio` will stream audio from the host machine to the docker container. However, you need to manually configure which input and output devices to use.

| Command      | Description                |
| ------------ | -------------------------- |
| `pactl list` | List all sinks and sources |

#### Configure a (temporary) input device

| Command                                                              | Description                      |
| -------------------------------------------------------------------- | -------------------------------- |
| `pacmd list-sources \| grep -e 'index:' -e device.string -e 'name:'` | List all available input devices |
| `pacmd set-default-source <INDEX>`                                   | Set temporary input device       |

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

#### Configure a (temporary) output device

| Command                                           | Description                       |
| ------------------------------------------------- | --------------------------------- |
| `pacmd list-sinks \| grep -e 'index:' -e 'name:'` | List all available output devices |
| `pacmd set-default-sink <INDEX>`                  | Set temporary output device       |

Example output of listing output devices:

```
* index: 0
	name: <Channel_1__Channel_2>
index: 1
	name: <Front_Left__Front_Right.2>
index: 2
	name: <1__2>
```

Read [this blog post](https://wiki.archlinux.org/title/PulseAudio/Examples) for some more useful examples.

##### Validating audio streaming (docker -> host machine)

To validate that the audio streaming it working properly you can try to play audio from the docker container --> host machine.

Run the following commands in order:

| Command                                 | Description                                                                           |
| --------------------------------------- | ------------------------------------------------------------------------------------- |
| `docker ps`                             | List running containers, find the CONTAINER ID of one with a name including `whisper` |
| `docker exec -it <CONTAINER_ID> bash`   | Get into the sentiment analysis container                                             |
| `ls /usr/share/sounds/alsa/`            | List available sounds, should be a list of `.wav` files                               |
| `paplay /usr/share/sounds/alsa/<SOUND>` | Should play the sound on host machine output device                                   |
| `exit`                                  | Exit the container                                                                    |
