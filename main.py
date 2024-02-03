import sys
sys.path.append('src')

print("")
print("----------------------------------------------------")
print("               made with ❤️  by xiduzo               ")
print("----------------------------------------------------")
print("https://github.com/xiduzo/whisper-sentiment-analysis")
print("----------------------------------------------------")
print("")

from docker import docker_check
docker_check()

# https://github.com/abdeladim-s/pywhispercpp
from pywhispercpp.examples.assistant import Assistant
from model import download_model
from processing import commands_callback

# Settings, see https://github.com/abdeladim-s/pywhispercpp for more
my_assistant = Assistant(
    commands_callback=commands_callback,
    n_threads=8,
    model=download_model())

my_assistant.start()
