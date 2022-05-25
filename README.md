# Lecture Downloader ETH

Download livestreams, watch livestreams locally (and reliably!)

## Installation

Install `downleth`:

```bash
pip install downleth
```

Make sure you have `ffmpeg` installed.

## Usage

To schedule a lecture recording based on a config:

```bash
downleth --log-level INFO exec sample-config.json
```

For structuring your configuration file, see `sample-config.json`.

## Development

`pipenv` is used. Use:

```bash
PIPENV_VENV_IN_PROJECT=1 pipenv install
```

The `vscode` task might help you get started with debugging.

## TODO

- Automatically generate configuration file per semester from myStudies, fetch room numbers, etc. automatically
- Allow spinning up local server to watch lectures without web client
- Allow configuring codecs (save storage)
- Automatically cut breaks somehow
- Consider holidays
- Use GitHub actions to publish, maybe GitVersion to version it
