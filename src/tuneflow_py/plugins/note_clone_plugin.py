from tuneflow_py import TuneflowPlugin, ParamDescriptor, Song, WidgetType, InjectSource, TuneflowPluginTriggerData, Note
from typing import Dict, Any
from pathlib import Path
from copy import deepcopy
import traceback
from io import BytesIO
import soundfile as sf
from miditoolkit.midi import MidiFile

from typing import List

class NoteClonePlugin(TuneflowPlugin):
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
            "cloningNotes": {
                "displayName": {
                    "zh": '待复制音符',
                    "en": 'Cloning Notes',
                },
                "defaultValue": None,
                "widget": {
                    "type": WidgetType.NoWidget.value,
                },
                "adjustable": False,
                "hidden": True,
            },
            "pasteTick": {
                "displayName": {
                "zh": '移动量',
                "en": 'Ticks Offset',
                },
                "defaultValue": 0,
                "widget": {
                    "type": WidgetType.NoWidget.value,
                },
                "hidden": True,
                "injectFrom": InjectSource.TickAtPlayhead.value,
            },
        }

    @staticmethod
    def run(song: Song, params: dict[str, Any]):
        editing_clip_infos = params['editingClipInfo']
        if editing_clip_infos is None:
            return
        cloning_notes = params['cloningNotes']
        if not cloning_notes or len(cloning_notes) == 0:
            return
        pasteTick = params['pasteTick']
        if pasteTick == 0:
            return
        track = song.get_track_by_id(editing_clip_infos[0]['trackId'])
        clip = track.get_clip_by_id(editing_clip_infos[0]['clipId'])
        if not clip or not track:
            raise Exception('Clip or track not found')
        for note in cloning_notes:
            #TODO check if note is in clip
            new_start_tick = note.get_start_tick()
            new_end_tick = note.get_end_tick()
            if not clip.is_note_in_clip(new_start_tick, new_end_tick, clip.get_clip_start_tick(), clip.get_clip_end_tick()):
                clip.create_note(note.get_pitch(), note.get_velocity(), new_start_tick, new_end_tick, note['duration'])
        