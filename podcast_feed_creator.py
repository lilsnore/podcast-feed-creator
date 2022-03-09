import os
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as xml

from mutagen.mp3 import MP3


class Manager:
    def __init__(self, feed_file_path):
        self._feed_file = Path(feed_file_path)
        if self._feed_file.is_dir():
            raise ValueError('Give a path to a file')
        if not self._feed_file.exists():
            raise NotImplementedError('Initializating from non existing file still not implemented')
        self._content = xml.parse(self._feed_file)

    def export(self):
        with open(self._feed_file, "w") as f:
            self._content.write(f)

    def add_episode(self, title, link, mp3_url, mp3_file, description):
        root = self._content.getroot()
        channel = root.find('channel')
        item = xml.SubElement(channel, 'item')

        title_elem = xml.SubElement(item, 'title')
        title_elem.text = title

        link_elem = xml.SubElement(item, 'link')
        link_elem.text = link

        enclosure_elem = xml.SubElement(item, 'enclosure')
        enclosure_elem.set('url', mp3_url)
        enclosure_elem.set('type', 'audio/mpeg')
        enclosure_elem.set('length', str(os.path.getsize(mp3_file)))

        description_elem = xml.SubElement(item, 'description')
        description_elem.text = description

        pubdate_elem = xml.SubElement(item, 'pubDate')
        pubdate_elem.text = self._get_pub_date()

        duration_elem = xml.SubElement(item, 'itunes:duration')
        duration_elem.text =


        #channel.append(item)

    def _get_pub_date(self):
        now = datetime.now()
        day_name = now.strftime('%A')[:3]
        day = now.strftime('%d')
        month = now.strftime('%B')[:3]
        year = now.strftime('%Y')
        time = now.strftime('%H:%M:%S')

        return f'{day_name}, {day} {month} {year} {time} +0100'

    def _get_duration(self, mp3_path):
        audio = MP3(mp3_path)
        total_secs = int(audio.info.length)
        hours = total_secs // 3600
        mins = (total_secs - (hours * 3600)) // 60
        secs = total_secs - (hours * 3600) - (mins * 60)

        if hours >= 1:
            return f'{hours}:{mins}:{secs}'
        return f'{mins}:{secs}'