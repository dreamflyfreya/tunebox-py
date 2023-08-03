from tuneflow_py import TuneflowPlugin, ParamDescriptor, Song, WidgetType, InjectSource, TuneflowPluginTriggerData
from typing import Dict, Any
from pathlib import Path
import traceback
from io import BytesIO
import soundfile as sf
from miditoolkit.midi import MidiFile

from typing import List

class ClipMovePlugin(TuneflowPlugin):
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
            "pasteToTrackId": {
                "displayName": {
                "zh": '粘贴至轨道',
                "en": 'Track to paste to',
                },
                "defaultValue": None,
                "hidden": True,
                "widget": {
                    "type": WidgetType.NoWidget.value,
                },
                "hidden": True,
                "injectFrom": InjectSource.SelectedTrackIds,
            },
            "playheadTick": {
                "displayName": {
                    "zh": '播放头位置',
                    "en": 'Playhead Position',
                },
                "defaultValue": 0,
                "hidden": True,
                "widget": {
                    "type": WidgetType.NoWidget.value,
                },
                "hidden": True,
                "injectFrom": InjectSource.TickAtPlayheadSnappedToBeat, # type: ignore
            },
    }

@staticmethod
def run(song: Song, params: dict[str, Any]):
    selected_clip_infos = params["selectedClipInfos"]
    play_head_tick = params["playheadTick"]
    paste_to_track_id = params["pasteToTrackId"]

    # Get the source clip info
    selected_clip_info = selected_clip_infos[0]

    # Get the source track and source clip
    src_track = song.get_track_by_id(selected_clip_info["trackId"])
    if src_track is None:
        raise Exception("Cannot find source track")
    src_clip = src_track.get_clip_by_id(selected_clip_info["clipId"])
    if src_clip is None:
        raise Exception("Cannot find source clip")

    # Get the destination track
    destination_track = song.get_track_by_id(paste_to_track_id)
    if destination_track is None:
        raise Exception("Cannot find destination track")

    # Clone the source clip
    cloned_clip = src_track.clone_clip(src_clip.get_id())

    # Update the start and end ticks of the cloned clip based on the playhead position
    duration = cloned_clip.get_clip_end_tick() - cloned_clip.get_clip_start_tick()
    cloned_clip.adjust_clip_left(play_head_tick)
    cloned_clip.adjust_clip_right(play_head_tick + duration)

    # Add the cloned clip to the destination track
    destination_track.insert_clip(cloned_clip)
    src_track.delete_clip(src_clip.get_id(), True)

        

