import requests
import os
import hashlib

class TXT_Send_HTTP:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "txt_file": ("STRING", {"default": "./transcription.txt"}),  # Path to the TXT file
                "url": ("STRING", {"default": "https://your-backend.com/upload"}),  # Backend URL
                "method_type": (["post", "put"], {"default": "post"})  # No PATCH for binary data
            }
        }

    RETURN_TYPES = ("INT", "STRING", "STRING", "STRING")  # status_code, response_text, debug_file_path, debug_info
    RETURN_NAMES = ("status_code", "result_text", "debug_file_path", "debug_info")
    FUNCTION = "send_txt_file"
    OUTPUT_NODE = True
    CATEGORY = "Jornick"

    def send_txt_file(self, txt_file, url, method_type="post"):
        """
        Sends the TXT file as raw text data.
        """
        if not os.path.exists(txt_file):
            error_text = f"File not found: {txt_file}"
            print(error_text)
            return (0, error_text, txt_file, error_text)

        try:
            with open(txt_file, "r", encoding="utf-8") as f:
                file_content = f.read()
        except Exception as e:
            error_text = f"Failed to open TXT file at {txt_file}: {str(e)}"
            print(error_text)
            return (0, error_text, txt_file, error_text)

        file_size = len(file_content.encode("utf-8"))  # Convert to bytes for accurate size measurement
        file_hash = hashlib.sha256(file_content.encode("utf-8")).hexdigest()

        headers = {
            "Content-Type": "text/plain",  # Sending plain text
            "X-File-Name": os.path.basename(txt_file)  # Send filename as a header
        }

        try:
            response = requests.request(
                method=method_type.upper(),
                url=url,
                headers=headers,
                data=file_content  # Sending raw text data
            )
        except Exception as e:
            error_text = f"HTTP request failed: {str(e)}"
            print(error_text)
            return (0, error_text, txt_file, f"File size: {file_size} bytes, SHA256: {file_hash}")

        print(f"[TXT_Send_HTTP] File sent: HTTP {response.status_code}")
        return (response.status_code, response.text, txt_file, f"File size: {file_size} bytes, SHA256: {file_hash}")


NODE_CLASS_MAPPINGS = {
    "TXT_Send_HTTP": TXT_Send_HTTP
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TXT_Send_HTTP": "TXT Send HTTP Node"
}
