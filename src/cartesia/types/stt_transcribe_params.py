# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, TypedDict

from .._types import FileTypes

__all__ = ["SttTranscribeParams"]


class SttTranscribeParams(TypedDict, total=False):
    encoding: Optional[Literal["pcm_s16le", "pcm_s32le", "pcm_f16le", "pcm_f32le", "pcm_mulaw", "pcm_alaw"]]
    """The encoding format to process the audio as.

    If not specified, the audio file will be decoded automatically.

    **Supported formats:**

    - `pcm_s16le` - 16-bit signed integer PCM, little-endian (recommended for best
      performance)
    - `pcm_s32le` - 32-bit signed integer PCM, little-endian
    - `pcm_f16le` - 16-bit floating point PCM, little-endian
    - `pcm_f32le` - 32-bit floating point PCM, little-endian
    - `pcm_mulaw` - 8-bit μ-law encoded PCM
    - `pcm_alaw` - 8-bit A-law encoded PCM
    """

    sample_rate: Optional[int]
    """The sample rate of the audio in Hz."""

    file: FileTypes

    language: Optional[str]
    """The language of the input audio in ISO-639-1 format. Defaults to `en`.

    <Accordion title="Supported languages">
      - `en` (English)
      - `zh` (Chinese)
      - `de` (German)
      - `es` (Spanish)
      - `ru` (Russian)
      - `ko` (Korean)
      - `fr` (French)
      - `ja` (Japanese)
      - `pt` (Portuguese)
      - `tr` (Turkish)
      - `pl` (Polish)
      - `ca` (Catalan)
      - `nl` (Dutch)
      - `ar` (Arabic)
      - `sv` (Swedish)
      - `it` (Italian)
      - `id` (Indonesian)
      - `hi` (Hindi)
      - `fi` (Finnish)
      - `vi` (Vietnamese)
      - `he` (Hebrew)
      - `uk` (Ukrainian)
      - `el` (Greek)
      - `ms` (Malay)
      - `cs` (Czech)
      - `ro` (Romanian)
      - `da` (Danish)
      - `hu` (Hungarian)
      - `ta` (Tamil)
      - `no` (Norwegian)
      - `th` (Thai)
      - `ur` (Urdu)
      - `hr` (Croatian)
      - `bg` (Bulgarian)
      - `lt` (Lithuanian)
      - `la` (Latin)
      - `mi` (Maori)
      - `ml` (Malayalam)
      - `cy` (Welsh)
      - `sk` (Slovak)
      - `te` (Telugu)
      - `fa` (Persian)
      - `lv` (Latvian)
      - `bn` (Bengali)
      - `sr` (Serbian)
      - `az` (Azerbaijani)
      - `sl` (Slovenian)
      - `kn` (Kannada)
      - `et` (Estonian)
      - `mk` (Macedonian)
      - `br` (Breton)
      - `eu` (Basque)
      - `is` (Icelandic)
      - `hy` (Armenian)
      - `ne` (Nepali)
      - `mn` (Mongolian)
      - `bs` (Bosnian)
      - `kk` (Kazakh)
      - `sq` (Albanian)
      - `sw` (Swahili)
      - `gl` (Galician)
      - `mr` (Marathi)
      - `pa` (Punjabi)
      - `si` (Sinhala)
      - `km` (Khmer)
      - `sn` (Shona)
      - `yo` (Yoruba)
      - `so` (Somali)
      - `af` (Afrikaans)
      - `oc` (Occitan)
      - `ka` (Georgian)
      - `be` (Belarusian)
      - `tg` (Tajik)
      - `sd` (Sindhi)
      - `gu` (Gujarati)
      - `am` (Amharic)
      - `yi` (Yiddish)
      - `lo` (Lao)
      - `uz` (Uzbek)
      - `fo` (Faroese)
      - `ht` (Haitian Creole)
      - `ps` (Pashto)
      - `tk` (Turkmen)
      - `nn` (Nynorsk)
      - `mt` (Maltese)
      - `sa` (Sanskrit)
      - `lb` (Luxembourgish)
      - `my` (Myanmar)
      - `bo` (Tibetan)
      - `tl` (Tagalog)
      - `mg` (Malagasy)
      - `as` (Assamese)
      - `tt` (Tatar)
      - `haw` (Hawaiian)
      - `ln` (Lingala)
      - `ha` (Hausa)
      - `ba` (Bashkir)
      - `jw` (Javanese)
      - `su` (Sundanese)
      - `yue` (Cantonese)
    </Accordion>
    """

    model: str
    """ID of the model to use for transcription.

    Use `ink-whisper` for the latest Cartesia Whisper model.
    """

    timestamp_granularities: Optional[List[Literal["word"]]]
    """The timestamp granularities to populate for this transcription.

    Currently only `word` level timestamps are supported.
    """
