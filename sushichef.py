#!/usr/bin/env python
import os
import sys
from ricecooker.utils import downloader, html_writer
from ricecooker.chefs import SushiChef
from ricecooker.classes import nodes, files, questions, licenses
from ricecooker.config import LOGGER              # Use LOGGER to print messages
from ricecooker.exceptions import raise_for_invalid_channel
from le_utils.constants import exercises, content_kinds, file_formats, format_presets, languages

from ricecooker.utils.youtube import YouTubeVideoUtils, YouTubePlaylistUtils

from utils import *

# Run constants
################################################################################
CHANNEL_NAME = "AimHi"                             # Name of Kolibri channel
CHANNEL_SOURCE_ID = "aimhi"                              # Unique ID for content source
CHANNEL_DOMAIN = "www.aimhi.co"                         # Who is providing the content
CHANNEL_LANGUAGE = "en"                                     # Language of channel
CHANNEL_DESCRIPTION = 'The nature-first, curiosity-powered online school.'                                  # Description of the channel (optional)
CHANNEL_THUMBNAIL = AIMHI_THUMBNAIL_PATH                                   # Local path or url to image file (optional)
CONTENT_ARCHIVE_VERSION = 1                                 # Increment this whenever you update downloaded content


# Additional constants
################################################################################



# The chef subclass
################################################################################
class AimhiChef(SushiChef):
    """
    This class converts content from the content source into the format required by Kolibri,
    then uploads the {channel_name} channel to Kolibri Studio.
    Your command line script should call the `main` method as the entry point,
    which performs the following steps:
      - Parse command line arguments and options (run `./sushichef.py -h` for details)
      - Call the `SushiChef.run` method which in turn calls `pre_run` (optional)
        and then the ricecooker function `uploadchannel` which in turn calls this
        class' `get_channel` method to get channel info, then `construct_channel`
        to build the contentnode tree.
    For more info, see https://ricecooker.readthedocs.io
    """
    channel_info = {
        'CHANNEL_SOURCE_DOMAIN': CHANNEL_DOMAIN,
        'CHANNEL_SOURCE_ID': CHANNEL_SOURCE_ID,
        'CHANNEL_TITLE': CHANNEL_NAME,
        'CHANNEL_LANGUAGE': CHANNEL_LANGUAGE,
        'CHANNEL_THUMBNAIL': CHANNEL_THUMBNAIL,
        'CHANNEL_DESCRIPTION': CHANNEL_DESCRIPTION,
    }
    DATA_DIR = os.path.abspath('chefdata')
    DOWNLOADS_DIR = os.path.join(DATA_DIR, 'downloads')
    ARCHIVE_DIR = os.path.join(DOWNLOADS_DIR, 'archive_{}'.format(CONTENT_ARCHIVE_VERSION))

    # Your chef subclass can override/extend the following method:
    # get_channel: to create ChannelNode manually instead of using channel_info
    # pre_run: to perform preliminary tasks, e.g., crawling and scraping website
    # __init__: if need to customize functionality or add command line arguments
    def construct_channel(self, *args, **kwargs):
        """
        Creates ChannelNode and build topic tree
        Args:
          - args: arguments passed in on the command line
          - kwargs: extra options passed in as key="value" pairs on the command line
            For example, add the command line option   lang="fr"  and the value
            "fr" will be passed along to `construct_channel` as kwargs['lang'].
        Returns: ChannelNode
        """
        channel = self.get_channel(*args, **kwargs)  # Create ChannelNode from data in self.channel_info
        # Get Channel Topics
        for playlist_id in PLAYLIST_MAP:
          playlist = YouTubePlaylistUtils(id=playlist_id)
          playlist_info = playlist.get_playlist_info(use_proxy=False, use_cache=False, youtube_skip_download=False)

          # Get channel description if there is any
          playlist_description = ''
          if playlist_info["description"]:
            playlist_description = playlist_info["description"]
          else :
            playlist_description = playlist_info['title']
          print(playlist_info["title"])
          print("description "+ playlist_description)
          print(playlist_info["source_url"])
          topic_source_id = 'aimhi-child-topic-{0}'.format(playlist_info["title"])
          topic_node = nodes.TopicNode(
            title = playlist_info["title"],
            source_id = topic_source_id,
            author = "AimHi",
            provider = "AimHi",
            description = playlist_description,
            language = 'en'
          )
          channel.add_child(topic_node)
          
        # TODO: Replace next line with chef code
        # raise NotImplementedError("constuct_channel method not implemented yet...")

        return channel



# CLI
################################################################################
if __name__ == '__main__':
    # This code runs when sushichef.py is called from the command line
    chef = AimhiChef()
    chef.main()