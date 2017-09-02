# YouTube Live Recorder

Checks when a YouTube channel goes live and starts recording the stream when it is live.

## Requirements

* Python 2
* Streamlink
* Python Requests

## Installation

```
# install streamlink
pip2 install requests
git clone https://github.com/seymour7/youtube-live-recorder.git
cd youtube-live-recorder
cp config.example config
# edit config
```

## Usage

```
./run.sh
```

## Troubleshooting

### How do I get a channel id?

Run:

```
curl https://www.googleapis.com/youtube/v3/channels?part=id&forUsername=PewDiePie&key={YOUR_API_KEY}
```

Or, go to the channels url (i.e. https://www.youtube.com/user/PewDiePie), right click, view page source and search for 'channelId'

### Downloaded video will not play

Sometimes, if Streamlink ends abruptly, vlc will have problems decoding the video file. You can use `ffmpeg` to fix the encoding:

```
ffmpeg -i input.mp4 -c copy fixed.mp4
```
