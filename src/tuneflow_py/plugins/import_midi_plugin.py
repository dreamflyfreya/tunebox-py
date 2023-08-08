from tuneflow_py import TuneflowPlugin, ParamDescriptor, Song, WidgetType, InjectSource, TuneflowPluginTriggerData
from typing import Dict, Any
from pathlib import Path
import traceback
from io import BytesIO
import soundfile as sf
from miditoolkit.midi import MidiFile


class ImportMidiPlugin(TuneflowPlugin):
    @staticmethod
    def provider_id() -> str:
        return 'ruijie'

    @staticmethod
    def plugin_id() -> str:
        return 'midi-import'
    
    @staticmethod
    def params(song: Song) -> Dict[str, ParamDescriptor]:
        return {
            "midiFile": {
                "displayName": {
                    "zh": 'MIDI文件',
                    "en": 'MIDI File',
                },
                "defaultValue": None,
                "widget": {
                    "type": WidgetType.FileSelector.value,
                    "config": {
                        "allowedExtensions": [".midi", ".mid"],
                    }
                },
                "adjustable": False,
                "hidden": False,
            },
            "selectTrackIds": {
                "displayName": {
                    "zh": '选中轨道',
                    "en": 'selected Tracks',
                },
                "defaultValue": None,
                "widget": {
                "type": WidgetType.NoWidget.value,
                },
                "adjustable": False,
                "hidden": True,
                "injectFrom": InjectSource.SelectedTrackIds.value,
            },
            "playheadTick": {
                "displayName": {
                    "zh": '播放头位置',
                    "en": 'Playhead Position',
                },
                "defaultValue": 0,
                "widget": {
                    "type": WidgetType.InputNumber.value,
                },
                "hidden": True,
                "injectFrom": InjectSource.TickAtPlayhead.value,
            },
        }
    
    @staticmethod
    def run(song: Song, params: dict[str, Any]):
        midi_files = params['midiFile']
        paste_to_track_ids = params['pasteToTrackId']
        if not midi_files or not paste_to_track_ids:
            return
        for idx, midi_file in enumerate(midi_files):
            try:
                midi_file = Path(midi_file)
                if not midi_file.exists():
                    continue
                midi = MidiFile(midi_file)
                if not midi.instruments:
                    continue
                track = song.get_track_by_id(paste_to_track_ids[idx])
                if not track:
                    continue
                for instrument in midi.instruments:
                    track.add_clip(
                        {
                            "name": instrument.name,
                            "notes": [
                                {
                                    "pitch": note.pitch,
                                    "velocity": note.velocity,
                                    "startTick": note.start,
                                    "durationTicks": note.end - note.start,
                                }
                                for note in instrument.notes
                            ],
                        }
                    )
            except Exception:
                print(traceback.format_exc())
                continue
