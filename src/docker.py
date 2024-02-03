import os, subprocess

def is_docker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )

def docker_check():
    if(is_docker()):
        print("Running in Docker, starting PulseAudio server.")
        # Start the PulseAudio server
        subprocess.run('pulseaudio --load=module-native-protocol-tcp --exit-idle-time=-1 --daemon', shell=True, executable="/bin/bash")

        # Check if the PulseAudio server is running
        subprocess.run('pulseaudio --check', shell=True, executable="/bin/bash")
    else:
        print("Not running in Docker, skipping PulseAudio server start.")