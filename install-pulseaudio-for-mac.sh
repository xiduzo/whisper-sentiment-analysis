#!/bin/bash

# Install pulseaudio for mac
brew install pulseaudio

# Run the command and store its output in a variable
output=$(pulseaudio --version)

# Extract the version number using awk
version=$(echo "$output" | awk '{print $2}')

file="/opt/homebrew/Cellar/pulseaudio/$version/etc/pulse/default.pa.d"
if test -e "$file"; then
    echo "File exists"
else
    # Create the file
    echo "File does not exist, creating it now..."
    touch "$file"
fi

echo "writing configuration to file..."
echo "$(cat .config/pulse/pulseaudio.conf)" >> /opt/homebrew/Cellar/pulseaudio/$version/etc/pulse/default.pa.d

echo "Configuration written to file:"
echo "$(cat /opt/homebrew/Cellar/pulseaudio/$version/etc/pulse/default.pa.d)"

# Restart pulseaudio
echo "Restarting pulseaudio..."
brew services restart pulseaudio

echo "Checking pulseaudio status..."
sleep 5
pulseaudio --check -v