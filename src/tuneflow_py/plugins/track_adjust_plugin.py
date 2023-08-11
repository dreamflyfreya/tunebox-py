from typing import Dict, Union, Any, Optional
from tuneflow_py import TuneflowPlugin, ParamDescriptor, Song, WidgetType, InjectSource, TuneflowPluginTriggerData
from typing import Dict, Any
from pathlib import Path
import traceback
from io import BytesIO
import soundfile as sf
from miditoolkit.midi import MidiFile

class TrackAdjust:
    
    @staticmethod
    def provider_id() -> str:
        return 'andantei'

    @staticmethod
    def plugin_id() -> str:
        return 'track-adjust'

    def params(self) -> Dict[str, Dict[str, Any]]:
        return {
            trackId: {
                displayName: {
                zh: '轨道',
                en: 'Track',
                },
                defaultValue: undefined,
                widget: {
                type: WidgetType.TrackSelector,
                config: {} as TrackSelectorWidgetConfig,
                },
                adjustable: false,
                hidden: true,
            },
            volume: {
                displayName: {
                zh: '音量',
                en: 'Volume',
                },
                defaultValue: undefined,
                widget: {
                type: WidgetType.Slider,
                config: {
                    minValue: 0,
                    maxValue: 100,
                    step: 1,
                } as SliderWidgetConfig,
                },
                hidden: true,
                optional: true,
            },
            pan: {
                displayName: {
                zh: '声像 (Pan)',
                en: 'Pan',
                },
                defaultValue: undefined,
                widget: {
                type: WidgetType.Slider,
                config: {
                    minValue: -64,
                    maxValue: 63,
                    step: 1,
                } as SliderWidgetConfig,
                },
                hidden: true,
                optional: true,
            },
            muted: {
                displayName: {
                zh: '静音',
                en: 'Mute',
                },
                defaultValue: undefined,
                widget: {
                type: WidgetType.Switch,
                config: {} as SwitchWidgetConfig,
                },
                hidden: true,
                optional: true,
            },
            solo: {
                displayName: {
                zh: '独奏',
                en: 'Solo',
                },
                defaultValue: undefined,
                widget: {
                type: WidgetType.Switch,
                config: {} as SwitchWidgetConfig,
                },
                hidden: true,
                optional: true,
            },
            instrument: {
                displayName: {
                zh: '乐器',
                en: 'Instrument',
                },
                defaultValue: undefined,
                widget: {
                type: WidgetType.InstrumentSelector,
                config: {} as InstrumentSelectorWidgetConfig,
                },
                hidden: true,
                optional: true,
            },
        }

    def run(self, song: 'Song', params: Dict[str, Any]) -> None:
        track_id = params.get('trackId')
        volume = params.get('volume')
        pan = params.get('pan')
        mute = params.get('mute')
        solo = params.get('solo')
        instrument = params.get('instrument')
        
        track = song.get_track_by_id(track_id)
        if not track:
            raise Exception('Track not ready')
        
        if isinstance(volume, (int, float)):
            track.set_volume(volume / 100)
        if isinstance(pan, (int, float)):
            track.set_pan(pan)
        if isinstance(mute, bool):
            track.set_muted(mute)
        if isinstance(solo, bool):
            track.set_solo(solo)
        if instrument:
            track.set_instrument({
                'program': instrument['program'],
                'isDrum': instrument['isDrum']
            })