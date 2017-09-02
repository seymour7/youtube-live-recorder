import ConfigParser
import logging
from logging.handlers import RotatingFileHandler
import os.path
import requests
from subprocess import Popen, PIPE
import time

def setup_logging(file_path, max_size):
    """
    Setup handlers to log events
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create rotating file handler that logs info, warn, error & critical messages
    fh = RotatingFileHandler(file_path,
                             mode="a",
                             maxBytes=max_size*1024*1024,
                             backupCount=0)
    fh.setLevel(logging.INFO)

    # Create console handler with the same log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

def package_exists(pkg):
    """
    Checks if a given package exists on the os
    """
    proc = Popen(["which", pkg], stdout=PIPE, stderr=PIPE)
    exit_code = proc.wait()

    if exit_code == 0:
        return True

    return False


#----------------------------------------------------------------------


if __name__ == "__main__":
    
    if not package_exists("streamlink"):
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

    setup_logging(log_file_path, log_file_size)
    
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    while True:

        try:
            r = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&channelId='+channel_id+'&eventType=live&type=video&key='+yt_api_key)
            response = r.json()
        except Exception, e:
            logging.info("Error making YT request: %s", str(e))
            time.sleep(10)
            continue

        if len(response['items']) > 0:
            
            video_id = response['items'][0]['id']['videoId']
            
            video_url = "https://www.youtube.com/watch?v="+video_id
            
            today = time.strftime("%Y-%m-%d")
            
            i = 1
            while (os.path.isfile(os.path.join(download_dir, today+'-'+str(i)+'.mp4'))):
                i += 1
                
            output_fname = today+'-'+str(i)+'.mp4'

            logging.info("Downloading stream @ %s", video_url)
            
            proc = Popen(["streamlink", "-o", os.path.join(download_dir, output_fname), video_url, quality])
            exit_code = proc.wait()

        else:
            logging.info("Channel is not live")
            time.sleep(30)
