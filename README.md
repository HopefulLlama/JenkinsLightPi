# JenkinsLightPi
Hit a few HTTP endpoints, and illuminate a status light on the Pi.

## Description
JenkinsLightPi is a small bundle of code which is ideally deployed on a Raspberry Pi. It's function is to report on [Jenkins](https://github.com/jenkinsci/jenkins) jobs, and illuminate an LED. For this current build, it is recommended to use three single coloured LEDs: Success, Failure and Running.

## Usage

The first step will be to create a configuration file to tell your Pi which jobs to check, how and when to report it. 

An example configuration file can be found at: `example-configs/example-configs.json`. You should note that the configuration file is written in the 'JSON' format.

### Configuration Options
`jobName <string>`: The name which it will report in the output.

`pins.success <integer>`: The GPIO pin used for the 'success' LED.

`pins.failure <integer>`: The GPIO pin used for the 'failure' LED.

`pins.running <integer>`: The GPIO pin used for the 'running' LED.

`urls <Array<string>>`: URLs which JenkinsLightPi will contact to determine job status. The script will suffix the URLs given with `/lastBuild/api/json` and `/lastCompletedBulid/api/json` when getting status information.

`frequency <integer>`: The rate in seconds, at which to repeat polling for data.

### Hardware Setup
The physical layout of the Pi is quite simple. In addition to your usual setup for a Pi, you will need three LEDs connected to the GPIO pins. Ensure you are using the correct resistor for your LED.

### Running the Script
From the terminal, all you need to do to begin running the script is:
`sudo python main.py <path/to/conf.json>`

For example:
`sudo python main.py example-configs/example-config.json`
