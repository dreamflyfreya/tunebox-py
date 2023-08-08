from tuneflow_py import TuneflowPlugin, ParamDescriptor, Song, WidgetType, InjectSource, TuneflowPluginTriggerData, Note
from typing import Dict, Any
from pathlib import Path
from copy import deepcopy
import traceback
from io import BytesIO
import soundfile as sf
from miditoolkit.midi import MidiFile

ClipType = song_pb2.ClipType

class SplitNotePlugin(TuneflowPlugin):
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
            "noteIds": {
                "displayName": {
                "zh": '编辑音符',
                "en": 'Editing Notes',
                },
                "defaultValue": [],
                "widget": {
                "type": WidgetType.NoWidget.value,
                },
                "adjustable": False,
                "hidden": True,
            },
            "splitAtTick": {
                "displayName": {
                "zh": '分割位置',
                "en": 'Split Position',
                },
                "defaultValue": None,
                "widget": {
                "type": WidgetType.NoWidget.value,
                },
                "adjustable": False,
                "hidden": True,
                "injectFrom": InjectSource.TickAtPlayhead.value,
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
        split_at_tick = params["splitAtTick"]
        track = song.get_track_by_id(editing_clip_infos[0]["trackId"])
        if not track:
            return
        clip = track.get_clip_by_id(editing_clip_infos[0]["clipId"])
        if not clip:
            return
        for note in clip.get_notes_by_ids(editing_notes_ids):
            if note.get_start_tick() >= split_at_tick or note.get_end_tick() <= split_at_tick:
                continue
            clip.create_note(
                note.get_pitch(),
                note.get_velocity(),
                split_at_tick,
                note.get_end_tick(),
                False,
                False,
            )
            note.adjust_right_to(split_at_tick - 1)