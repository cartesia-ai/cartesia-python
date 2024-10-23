import httpx

from cartesia._types import OutputFormat
from cartesia.resource import Resource

class VoiceChanger(Resource):
    def change_voice_file(
        self,
        input_path: str,
        voice_id: str,
        output_format: OutputFormat,
        output_path: str,
    ) -> None:
        url = f"{self._http_url()}/voice-changer/bytes"
        with open(input_path, "rb") as input_file:
            headers = self.headers.copy()
            headers.pop("Content-Type", None)
            files = {"clip": input_file}
            data = {
                "voice[id]": voice_id,
                "output_format[container]": output_format["container"]
						}
            
            if "encoding" in output_format:
                data["output_format[encoding]"] = output_format["encoding"]
            if "sample_rate" in output_format:
                data["output_format[sample_rate]"] = output_format["sample_rate"]
            if "bit_rate" in output_format:
                data["output_format[bit_rate]"] = output_format["bit_rate"]

            response = httpx.post(url, headers=headers, files=files, data=data, timeout=self.timeout)
            if not response.is_success:
                raise ValueError(f"Failed to change voice in clip. Error: {response.text}")

        with open(output_path, "wb") as output_file:
            output_file.write(response.content)

    def change_voice_bytes(self, audio_blob: bytes, voice_id: str, output_format: OutputFormat) -> bytes:
        url = f"{self._http_url()}/voice-changer/bytes"
        headers = self.headers.copy()
        headers.pop("Content-Type", None)
        files = {"clip": audio_blob}
        data = {
            "voice[id]": voice_id,
            "output_format[container]": output_format["container"],
            "output_format[encoding]": output_format["encoding"],
            "output_format[sample_rate]": output_format["sample_rate"],
        }

        response = httpx.post(url, headers=headers, files=files, data=data, timeout=self.timeout)
        if not response.is_success:
            raise ValueError(f"Failed to change voice in clip. Error: {response.text}")

        return response.content
