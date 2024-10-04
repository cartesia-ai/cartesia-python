from typing import Dict, List, Optional, Union

import httpx

from cartesia._types import VoiceMetadata
from cartesia.resource import Resource


class Voices(Resource):
    """This resource contains methods to list, get, clone, and create voices in your Cartesia voice library.

    Usage:
        >>> client = Cartesia(api_key="your_api_key")
        >>> voices = client.voices.list()
        >>> voice = client.voices.get(id="a0e99841-438c-4a64-b679-ae501e7d6091")
        >>> print("Voice Name:", voice["name"], "Voice Description:", voice["description"])
        >>> embedding = client.voices.clone(filepath="path/to/clip.wav")
        >>> new_voice = client.voices.create(
        ...     name="My Voice", description="A new voice", embedding=embedding
        ... )
    """

    def list(self) -> List[VoiceMetadata]:
        """List all voices in your voice library.

        Returns:
        This method returns a list of VoiceMetadata objects.
        """
        response = httpx.get(
            f"{self._http_url()}/voices",
            headers=self.headers,
            timeout=self.timeout,
        )

        if not response.is_success:
            raise ValueError(f"Failed to get voices. Error: {response.text}")

        voices = response.json()
        return voices

    def get(self, id: str) -> VoiceMetadata:
        """Get a voice by its ID.

        Args:
            id: The ID of the voice.

        Returns:
            A VoiceMetadata object containing the voice metadata.
        """
        url = f"{self._http_url()}/voices/{id}"
        response = httpx.get(url, headers=self.headers, timeout=self.timeout)

        if not response.is_success:
            raise ValueError(
                f"Failed to get voice. Status Code: {response.status_code}\n"
                f"Error: {response.text}"
            )

        return response.json()

    def clone(self, filepath: Optional[str] = None, enhance: str = True) -> List[float]:
        """Clone a voice from a clip.

        Args:
            filepath: The path to the clip file.
            enhance: Whether to enhance the clip before cloning the voice (highly recommended). Defaults to True.

        Returns:
            The embedding of the cloned voice as a list of floats.
        """
        if not filepath:
            raise ValueError("Filepath must be specified.")
        url = f"{self._http_url()}/voices/clone/clip"
        with open(filepath, "rb") as file:
            files = {"clip": file}
            files["enhance"] = str(enhance).lower()
            headers = self.headers.copy()
            headers.pop("Content-Type", None)
            response = httpx.post(url, headers=headers, files=files, timeout=self.timeout)
            if not response.is_success:
                raise ValueError(f"Failed to clone voice from clip. Error: {response.text}")

        return response.json()["embedding"]

    def create(
        self,
        name: str,
        description: str,
        embedding: List[float],
        base_voice_id: Optional[str] = None,
    ) -> VoiceMetadata:
        """Create a new voice.

        Args:
            name: The name of the voice.
            description: The description of the voice.
            embedding: The embedding of the voice. This should be generated with :meth:`clone`.
            base_voice_id: The ID of the base voice. This should be a valid voice ID if specified.

        Returns:
            A dictionary containing the voice metadata.
        """
        response = httpx.post(
            f"{self._http_url()}/voices",
            headers=self.headers,
            json={
                "name": name,
                "description": description,
                "embedding": embedding,
                "base_voice_id": base_voice_id,
            },
            timeout=self.timeout,
        )

        if not response.is_success:
            raise ValueError(f"Failed to create voice. Error: {response.text}")

        return response.json()

    def delete(self, id: str) -> bool:
        """Delete a voice by its ID.

        Args:
            id: The ID of the voice.

        Raises:
            ValueError: If the request fails.
        """
        response = httpx.delete(
            f"{self._http_url()}/voices/{id}",
            headers=self.headers,
            timeout=self.timeout,
        )

        if not response.is_success:
            raise ValueError(f"Failed to delete voice. Error: {response.text}")

    def mix(self, voices: List[Dict[str, Union[str, float]]]) -> List[float]:
        """Mix multiple voices together.

        Args:
            voices: A list of dictionaries, each containing either:
                        - 'id': The ID of an existing voice
                        - 'embedding': A voice embedding
                    AND
                        - 'weight': The weight of the voice in the mix (0.0 to 1.0)

        Returns:
            The embedding of the mixed voice as a list of floats.

        Raises:
            ValueError: If the request fails or if the input is invalid.
        """
        url = f"{self._http_url()}/voices/mix"

        if not voices or not isinstance(voices, list):
            raise ValueError("voices must be a non-empty list")

        response = httpx.post(
            url,
            headers=self.headers,
            json={"voices": voices},
            timeout=self.timeout,
        )

        if not response.is_success:
            raise ValueError(f"Failed to mix voices. Error: {response.text}")

        result = response.json()
        return result["embedding"]
