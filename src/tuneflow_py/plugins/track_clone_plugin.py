from typing import Dict, Union, Any, Optional
from tuneflow_py import TuneflowPlugin, ParamDescriptor, Song, WidgetType, InjectSource, TuneflowPluginTriggerData
from typing import Dict, Any
from pathlib import Path
import traceback
from io import BytesIO
import soundfile as sf
from miditoolkit.midi import MidiFile

class TrackClone(TuneflowPlugin):

    @staticmethod
    def provider_id() -> str:
        return 'andantei'

    @staticmethod
    def plugin_id() -> str:
        return 'track-clone'

    @staticmethod
    def params(song: Song) -> Dict[str, ParamDescriptor]:
        return {
            "trackIds": {
                "displayName": {
                    "zh": '原轨道',
                    "en": 'Track to clone',
                },
                "defaultValue": [],
                "widget": {
                    "type": WidgetType.MultiTrackSelector.value,
                    "config": {},
                },
                "hidden": True,
            }
        }

    @staticmethod
    def run(song: Song, params: Dict[str, Any]) -> None:
        trackIds = params['trackIds']
        for trackId in trackIds:
            track = song.get_track_by_id(trackId)
            if not track:
                raise Exception(f'Track {trackId} not ready')
            song.clone_track(track)
