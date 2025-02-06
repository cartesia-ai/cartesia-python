from .types import OutputFormatMapping


def get_output_format(output_format_name: str):
    """Convenience method to get the output_format dictionary from a given output format name.

    Args:
        output_format_name (str): The name of the output format.

    Returns:
        OutputFormat: A dictionary containing the details of the output format to be passed into tts.sse() or tts.websocket().send()

    Raises:
        ValueError: If the output_format name is not supported
    """
    if output_format_name in OutputFormatMapping._format_mapping:
        output_format_obj = OutputFormatMapping.get_format(output_format_name)
    else:
        raise ValueError(f"Unsupported format: {output_format_name}")

    return output_format_obj
