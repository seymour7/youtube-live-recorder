# YouTube Live Recorder

Periodically checks if a YouTube channel is live and starts recording the stream when it is live.

## Requirements

* Python 2
* [pip](https://pypi.python.org/pypi/pip)
* [YouTube Data API key](https://developers.google.com/youtube/registering_an_application)

## Installation

```
pip install -r requirements.txt
git clone https://github.com/seymour7/youtube-live-recorder.git
cd youtube-live-recorder
cp config.example config
```

## Configuration

To configure the app, edit the file `config`

## Usage

```
./run.sh
```

## Troubleshooting

### How do I get a channel's id?

Run:

```
curl https://www.googleapis.com/youtube/v3/channels?part=id&forUsername=PewDiePie&key={YOUR_API_KEY}
```

Or, visit the channel's url (i.e. https://www.youtube.com/user/PewDiePie), right click, view page source and search for 'channelId'.

### Downloaded video will not play

Sometimes, if Streamlink ends abruptly, vlc will have problems decoding the video file. You can use `ffmpeg` to fix the encoding:

```
ffmpeg -i input.mp4 -c copy fixed.mp4
```
