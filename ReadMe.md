# L4D - Logging 4 dummies
<img src="src/image/l4d.png" alt="drawing" width="200"/>

# WIP PROJECT

Ever noticed how hard it is to find a Logging tool that fits your use case and isnt pain to set up?

L4D is here to try and fix this!

L4D is for 1 open source so add what you need!

And 2 trying to implement as many known standards to make it compatible with a lot of already existing Hardware/Software.

Our 2 main goals are:

1. Compatibility for known logging input/output (Fluent, AWS Firehose,...)
2. Custom input/output. This means you can add URLs with a Input schema and set how the API should response.

## L4D Parts

L4D is split up into 2 parts.

A Website to look at logs, create Inputs,...

A API to accept data.

This repository houses the API part. As this is still WIP we are not sure if we should use a known good Lib like Grafana
or create HTML pages and add everything in the API.

## Setup

1. Clone the repository
2. Create a api_config.yaml (Example exists in the /src/config/EXAMPLE-api_config.yaml)
3. Add the "DEV" environment variable. Set it to either true or false.
4. Either run start_app.py or use the Dockerfile.

## Documentation

Documentation is still WIP. But it will be available in the /docs folder.
