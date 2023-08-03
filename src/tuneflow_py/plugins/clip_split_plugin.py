from tuneflow_py import TuneflowPlugin, ParamDescriptor, Song, WidgetType, InjectSource, TuneflowPluginTriggerData
from typing import Dict, Any
from pathlib import Path
import traceback
from io import BytesIO
import soundfile as sf
from miditoolkit.midi import MidiFile

from typing import List

class ClipSplitPlugin(TuneflowPlugin):
    @staticmethod
    def provider_id() -> str:
        return 'ruijie'

    @staticmethod
    def plugin_id() -> str:
        return 'clip-clone'

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
                "injectFrom": InjectSource.TickAtPlayheadSnappedToBeat, # type: ignore
            },
    }

@staticmethod
def run(song: Song, params: dict[str, Any]):
    selected_clip_infos = params["selectedClipInfos"]
    play_head_tick = params["playheadTick"]
    for selected_clip_info in selected_clip_infos:
        src_track = song.get_track_by_id(selected_clip_info["trackId"])
        if src_track is None:
            raise Exception("Cannot find source track")
        src_clip = src_track.get_clip_by_id(selected_clip_info["clipId"])
        if src_clip is None:
            raise Exception("Cannot find source clip")

        # Check if split tick is within the clip's duration
        if not (src_clip.get_clip_start_tick() <= play_head_tick <= src_clip.get_clip_end_tick()):
            continue

        # Clone the source clip twice to create two new clips
        cloned_clip_1 = src_track.clone_clip(src_clip.get_id())
        cloned_clip_2 = src_track.clone_clip(src_clip.get_id())

        # Update the start and end ticks of the cloned clips based on the split tick
        cloned_clip_1.adjust_clip_right(play_head_tick)
        cloned_clip_2.adjust_clip_left(play_head_tick)

        # Add the cloned clips to the source track
        src_track.insert_clip(cloned_clip_1)
        src_track.insert_clip(cloned_clip_2)

        # Remove the original clip from the source track
        src_track.delete_clip(src_clip.get_id(), True)