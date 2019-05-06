# -*- coding: utf-8 -*-
import os
import sys
import argparse
import logging

import cv2
import ffmpeg

from pytube import YouTube

logging.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', level=logging.DEBUG)
log = logging.getLogger(__file__)
log.addHandler(logging.StreamHandler())

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../"

class Streamer:
    DEFAULT_DOWNLOADS_PATH = ROOT_PATH+'./downloads'

    def parse_opts(self):
        parser = argparse.ArgumentParser(description='Youtube Streamer')
        return parser.parse_args()

    def parse_args(self, opt):
        values = []
        return values

    def start(self, url):
        yt = YouTube(url)
        vids = yt.streams.filter(subtype='mp4', progressive=True).all()
        vid = vids[0]
        log.info(vid)
        mp4file = self.DEFAULT_DOWNLOADS_PATH + "/" + vid.default_filename
        if not os.path.exists(mp4file):
            vid.download(self.DEFAULT_DOWNLOADS_PATH)
        else:
            log.info("Already exist mp4 file on: %s", mp4file)
        return vid.default_filename

class Parser:
    DEFAULT_FRAMES_PATH = ROOT_PATH+'./frames'

    def parse(self, path):
        log.info(path)

        # forked processing
        probe = ffmpeg.probe(path)

        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        video_frames = probe['frames']

        log.info("video_stream: %d" % len(video_stream))
        log.info("video_frames: %d" % len(video_frames))

        for frame in video_frames:
            if 'pict_type' in frame:
                log.info(frame['pict_type'])
        cap = cv2.VideoCapture(path)
        count = 0
        success = 1
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        log.info("total_frames: %s" % total_frames)

        while success:
            success, image = cap.read()
            # imagefile = (self.DEFAULT_FRAMES_PATH + "/frame%d.jpg" % count)
            # cv2.imwrite(imagefile, image)

            # fps = cap.get(cv2.CAP_PROP_FPS)
            # log.info(fps)
            # cap.retrieve()
            count += 1

        if cap.isOpened():
            cap.release()

def main():
    streamer = Streamer()
    opt = streamer.parse_opts()
    values = streamer.parse_args(opt)

    filename = streamer.start('https://www.youtube.com/watch?v=aqz-KE-bpKQ')
    log.info(filename)

    mp4file = streamer.DEFAULT_DOWNLOADS_PATH+"/"+filename
    if not os.path.exists(mp4file):
        raise FileNotFoundError
    else :
        parser = Parser()
        parser.parse(mp4file)
    return 0


if __name__ == '__main__':
    sys.exit(main())

