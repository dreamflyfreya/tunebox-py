from tuneflow_py import TuneflowPlugin, ParamDescriptor, Song, WidgetType, InjectSource, TuneflowPluginTriggerData
from typing import Dict, Any
from pathlib import Path
import traceback
from io import BytesIO
import soundfile as sf
from miditoolkit.midi import MidiFile

class ClipTransposePlugin(TuneflowPlugin):
    @staticmethod
    def provider_id() -> str:
        return 'ruijie'

    @staticmethod
    def plugin_id() -> str:
        return 'clip-transpose'
    
    @staticmethod
    def params(song: Song) -> Dict[str, ParamDescriptor]:
        return {
            "selectedClipInfos": {
                    "displayName": {
                        "zh": '选中片段',
                        "en": 'Selected Clips',
                    },
                    "defaultValue": None,
                    "widget": {
                        "type": WidgetType.NoWidget.value,
                    },
                    "hidden": True,
                    "injectFrom": {
                        "type": InjectSource.SelectedClipInfos.value,
                        "options": {
                            "maxNumClips": 1
                        }
                    }
            },
            "trimPosition": {
                "displayName": {
                "zh": '裁剪位置',
                "en": 'Trim Position',
                },
                "defaultValue": None,
                "widget": {
                "type": WidgetType.Select.value,
                "config": {
                    "options": [
                    {
                        "value": 'left',
                        "label": {
                        "zh": '左侧',
                        "en": 'Left',
                        },
                    },
                    {
                        "value": 'right',
                        "label": {
                        "zh": '右侧',
                        "en": 'Right',
                        },
                    },
                    ],
                }
                },
                "hidden": True,
            },
            "offsetTicks": {
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
        selected_clip_infos = params["selectedClipInfos"]
        trim_position = params["trimPosition"]
        offset_tick = params["offsetTicks"]
        if type(offset_tick) != int:
            return
        for selected_clip_info in selected_clip_infos:
            track_id, clip_id = selected_clip_info["trackId"], selected_clip_info["clipId"]
            track = song.get_track_by_id(track_id)
            clip = track.get_clip_by_id(clip_id)
            if not track or not clip:
                continue
            if trim_position == "left" and offset_tick < 0:
                selected_clip_info.adjust_clip_right(selected_clip_info.get_clip_end_tick() - offset_tick, True)
            elif trim_position == "right" and offset_tick > 0:
                selected_clip_info.adjust_clip_left(selected_clip_info.get_clip_end_tick() - offset_tick, True)

