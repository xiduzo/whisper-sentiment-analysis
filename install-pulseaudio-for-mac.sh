#!/bin/bash
if [ -z "$(brew -v)" ]; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

brew install pulseaudio

pulseaudio_version=$(echo "$(pulseaudio --version)" | awk '{print $2}')

file="/opt/homebrew/Cellar/pulseaudio/$pulseaudio_version/etc/pulse/default.pa.d"
if ! test -e "$file"; then
    touch "$file"
fi

echo "$(cat .config/pulse/pulseaudio.conf)" >> /opt/homebrew/Cellar/pulseaudio/$pulseaudio_version/etc/pulse/default.pa.d

brew services restart pulseaudio

sleep 5
pulseaudio --check -v # Make sure everything is working