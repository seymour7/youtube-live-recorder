import ConfigParser
import logging
import os.path
import requests
import time
import helpers

YT_API_BASE = 'https://www.googleapis.com/youtube/v3'

if __name__ == "__main__":
    
    if not helpers.package_exists("streamlink"):
        print "Error: Streamlink is not installed"
        exit(1)

    # Load configuration file
    config = ConfigParser.RawConfigParser()
    try:
        config.readfp(open('config'))
    except IOError:
        print "Error: No configuration file 'config' found"
        exit(1)
    try:
        yt_api_key    = config.get('General', 'yt-api-key')
        channel_id    = config.get('General', 'channel-id')
        download_dir  = config.get('General', 'download-dir')
        quality       = config.get('General', 'quality')
        log_file_path = config.get('Logging', 'file-path')
        log_file_size = config.get('Logging', 'max-size')
    except ConfigParser.NoOptionError, e:
        print "Error:", e
        exit(1)

    helpers.setup_logging(log_file_path, log_file_size)
    
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    while True:

        try:
            r = requests.get(YT_API_BASE+'/search?part=snippet&channelId='+channel_id+'&eventType=live&type=video&key='+yt_api_key)
            response = r.json()
        except Exception, e:
            logging.info("Error making YT request: %s", str(e))
            time.sleep(10)
            continue

        if len(response['items']) > 0:
            
            video_id = response['items'][0]['id']['videoId']
            
            video_url = "https://www.youtube.com/watch?v="+video_id
            
            today = time.strftime("%Y-%m-%d")
            
            # If more than 1 video saved today, concatenate a count
            i = 1
            while (os.path.isfile(os.path.join(download_dir, today+'-'+str(i)+'.mp4'))):
                i += 1
                
            output_fname = today+'-'+str(i)+'.mp4'

            logging.info("Downloading stream @ %s", video_url)
            
            # Invoke streamlink process to download the live video
            proc = Popen(["streamlink", "-o", os.path.join(download_dir, output_fname), video_url, quality])
            exit_code = proc.wait()

        else:
            logging.info("Channel is not live")
            time.sleep(30)
