from tuneflow_py import TuneflowPlugin, ParamDescriptor, Song, WidgetType, InjectSource, TuneflowPluginTriggerData, Note
from typing import Dict, Any
from pathlib import Path
from copy import deepcopy
import traceback
from io import BytesIO
import soundfile as sf
from miditoolkit.midi import MidiFile

ClipType = song_pb2.ClipType

class MoveNotePlugin(TuneflowPlugin):
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
            "editingNotesIds": {
                "displayName": {
                    "zh": '音符',
                    "en": 'Editing Notes',
                },
                "defaultValue": [],
                "widget": {
                    "type": WidgetType.NoWidget.value,
                },
                "adjustable": False,
                "hidden": True,
                "injectFrom": InjectSource.EditingNoteIds.value,
            },
            "offsetPitch": {
                    "displayName": {
                    "zh": '移动半音数',
                    "en": 'Pitch Offset',
                },
                "defaultValue": 0,
                "widget": {
                    "type": WidgetType.NoWidget.value,
                },
                "adjustable": False,
                "hidden": True,
            },
            "offsetTick": {
                "displayName": {
                "zh": '移动量',
                "en": 'Ticks Offset',
                },
                "defaultValue": 0,
                "widget": {
                    "type": WidgetType.NoWidget.value,
                },
                "hidden": True,
            },
        }
    
    @staticmethod
    def run(song: Song, params: dict[str, Any]):
        editing_clip_infos = params["editingClipInfo"]
        editing_notes_ids = params["editingNotesIds"]
        if not editing_clip_infos:
            return
        if not editing_notes_ids:
            return
        offset_pitch = params["offsetPitch"]
        offset_tick = params["offsetTick"]
        if offset_pitch == 0 and offset_tick == 0:
            return
        track = song.get_track_by_id(editing_clip_infos[0]["trackId"])
        if not track:
            return
        clip = track.get_clip_by_id(editing_clip_infos[0]["clipId"])
        if not clip:
            return
        for note in clip.get_notes_by_ids(editing_notes_ids):
            note.move_note(offset_tick)
            note.adjust_pitch(offset_pitch)
