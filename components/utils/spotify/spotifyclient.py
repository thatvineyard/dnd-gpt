import json
import math
from multiprocessing import Process
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from components.utils.cli.cliprint import cli_print_error

# STEP 4


class Track:
    """
    Model class for spotify api track object.
    """

    album: dict
    artists: list
    available_markets: list
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: dict
    external_urls: dict
    href: str
    id: str
    is_playable: bool
    linked_from: dict
    restrictions: dict
    name: str
    popularity: int
    preview_url: str
    track_number: int
    type: str
    uri: str
    is_local: bool

    def __init__(self, **entries):
        self.__dict__.update(entries)


class Device:
    """
    Model class for spotify api device object
    """

    id: str
    is_active: bool
    is_private_session: bool
    is_restricted: bool
    name: str
    supports_volume: bool
    type: str
    volume_percent: int

    def __init__(self, **entries):
        self.__dict__.update(entries)


class SpotipyClient:
    """
    A spotipy client wrapper that keeps track of some of the details needed to set up a spotipy-client
    """

    scope = "user-library-read,user-read-playback-state,user-modify-playback-state"
    redirect_uri = "http://localhost:8000/"

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

        auth_manager = SpotifyOAuth(
            scope=self.scope,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
        )
        self.client = Spotify(auth_manager=auth_manager)
        self.device = self.__getDevice()

    def __getDevice(self):
        """Check which devices are currently available. One needs to be selected since Spotify sometimes has trouble knowing which one to choose."""

        results = self.client.devices()

        if results["devices"] is None or len(results["devices"]) == 0:
            cli_print_error(
                "No Spotify device found! Please start Spotify on a device and try again"
            )
            raise Exception("No Spotify device found")

        device = Device(**results["devices"][0])

        return device

    def searchForTrack(self, searchTerm: str) -> Track:
        """Search for a track using any search term. Will pick the first result."""

        results = self.client.search(searchTerm, 1)
        track = Track(**results["tracks"]["items"][0])
        return track

    def playTrack(self, track: Track):
        """Play the given track"""

        self.client.start_playback(uris=[track.uri], device_id=self.device.id)

    def pause(self, track: Track):
        """Pause playback"""

        self.client.pause_playback(device_id=self.device.id)

    def setVolume(self, volume: int):
        """Set playback volume"""

        volume = min(100, max(0, volume))
        self.client.volume(volume_percent=volume, device_id=self.device.id)
