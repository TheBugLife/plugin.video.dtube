# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
import xbmcgui
import xbmcplugin
import sys

from resources.lib import kodiutils
from resources.lib import kodilogging
from urllib import urlencode
from urlparse import parse_qsl

import json
import requests

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]

def get_trending():
    videos = []
    trendurl = "https://api.steemjs.com/getState?path=/trending/dtube&scope=content"
    data = json.loads(requests.get(trendurl).text)
    for results in data:
        vidjson = "https://steemit.com/dtube/@" + results.split('/')[0] + "/" + results.split('/')[1] + ".json"
        viddata = json.loads(requests.get(vidjson).text)
        dtubeitem = {'name': viddata['post']['json_metadata']['video']['info']['title'],
                     'thumb': "https://ipfs.io/ipfs/" + viddata['post']['json_metadata']['video']['info']['snaphash'],
                     'video': "https://ipfs.io/ipfs/" + viddata['post']['json_metadata']['video']['content'][
                         'video480hash'],
                     'genre': 'trending'}
        videos.append(dtubeitem)

    return videos


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


@plugin.route('/')
def index():
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
        show_category, "one"), xbmcgui.ListItem("Category One"), True)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
        show_category, "two"), xbmcgui.ListItem("Category Two"), True)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(
        show_category, "trending"), xbmcgui.ListItem("Trending"), True)
    xbmcplugin.endOfDirectory(plugin.handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(plugin.handle, True, listitem=play_item)

@plugin.route('/category/<category_id>')
def show_category(category_id):
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    params = dict(parse_qsl(sys.argv[2][1:]))
    # this shit right here is stupidly hacky:
    if 'action' in params:
        play_video(params['video'])
    else:
        xbmcplugin.setPluginCategory(int(sys.argv[1]), category_id)
        if category_id == 'trending':
            # Set plugin content. It allows Kodi to select appropriate views
            # for this type of content.
            xbmcplugin.setContent(plugin.handle, 'videos')

            videos = get_trending()
            for video in videos:
                list_item = xbmcgui.ListItem(label=video['name'])
                list_item.setInfo('video', {'title': video['name'],
                                            'genre': video['genre'],
                                            'mediatype': 'video'})
                list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
                list_item.setProperty('IsPlayable', 'true')
                url = get_url(action='play', video=video['video'])
                is_folder = False
                xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, is_folder)
            xbmcplugin.endOfDirectory(plugin.handle)
        else:
            xbmcplugin.addDirectoryItem(
                plugin.handle, "", xbmcgui.ListItem("Hello category %s!" % category_id))
            xbmcplugin.endOfDirectory(plugin.handle)



def run():
    plugin.run()
