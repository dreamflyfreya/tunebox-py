from tuneflow_py import TuneflowPlugin, ParamDescriptor, Song, WidgetType, InjectSource, TuneflowPluginTriggerData, Note
from typing import Dict, Any
from pathlib import Path
from copy import deepcopy
import traceback
from io import BytesIO
import soundfile as sf
from miditoolkit.midi import MidiFile

ClipType = song_pb2.ClipType

class MoveClonePlugin(TuneflowPlugin):
    @staticmethod
    def provider_id() -> str:
        return 'ruijie'

    @staticmethod
    def plugin_id() -> str:
        return 'note-clone'

    @staticmethod
    def params(song: Song) -> Dict[str, ParamDescriptor]:
        return {
            "editingClipInfo": {
                "displayName": {
                    "zh": '编辑片段',
                    "en": 'Editing Clip',
                },
                "defaultValue": None,
                "widget": {
                    "type": WidgetType.NoWidget.value,
                },
                "adjustable": False,
                "hidden": True,
                "injectFrom": InjectSource.EditingClipInfo.value,
            },
            "removeNotesIds": {
                "displayName": {
                    "zh": '音符',
                    "en": 'Cloning Notes',
                },
                "defaultValue": [],
                "widget": {
                    "type": WidgetType.NoWidget.value,
                },
                "adjustable": False,
                "hidden": True,
                "injectFrom": InjectSource.EditingNoteIds.value,
            },
        }
    
    @staticmethod
    def run(song: Song, params: dict[str, Any]):
        editing_clip_infos = params["editingClipInfo"]
        removing_notes_ids = params["removeNotesIds"]
        if not editing_clip_infos:
            return
        if not removing_notes_ids:
            return
        track = song.get_track_by_id(editing_clip_infos[0]["trackId"])
        if not track:
            return
        clip = track.get_clip_by_id(editing_clip_infos[0]["clipId"])
        for note in clip.get_notes_by_ids(removing_notes_ids):
            note.delete_from_parent()
