import requests
import hashlib

class TXT_Send_HTTP:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "txt_content": ("STRING", {"default": "This is the transcription text."}),  # Raw text input
                "url": ("STRING", {"default": "https://your-backend.com/upload"}),  # Backend URL
                "method_type": (["post", "put"], {"default": "post"})  # No PATCH for binary data
            }
        }

    RETURN_TYPES = ("INT", "STRING", "STRING")  # status_code, response_text, debug_info
    RETURN_NAMES = ("status_code", "result_text", "debug_info")
    FUNCTION = "send_txt_content"
    OUTPUT_NODE = True
    CATEGORY = "Jornick"

    def send_txt_content(self, txt_content, url, method_type="post"):
        """
        Sends the transcription text directly as raw text data.
        """
        if not txt_content:
            error_text = "Error: No transcription text provided."
            print(error_text)
            return (0, error_text, "No text provided")

        text_size = len(txt_content.encode("utf-8"))  # Convert to bytes for size measurement
        text_hash = hashlib.sha256(txt_content.encode("utf-8")).hexdigest()

        headers = {
            "Content-Type": "text/plain"  # Sending plain text
        }

        try:
            response = requests.request(
                method=method_type.upper(),
                url=url,
                headers=headers,
                data=txt_content  # Sending the raw transcription text
            )
        except Exception as e:
            error_text = f"HTTP request failed: {str(e)}"
            print(error_text)
            return (0, error_text, f"Text size: {text_size} bytes, SHA256: {text_hash}")

        print(f"[TXT_Send_HTTP] Transcription sent: HTTP {response.status_code}")
        return (response.status_code, response.text, f"Text size: {text_size} bytes, SHA256: {text_hash}")

NODE_CLASS_MAPPINGS = {
    "TXT_Send_HTTP": TXT_Send_HTTP
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TXT_Send_HTTP": "TXT Send HTTP Node"
}
