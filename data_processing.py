import requests
import os
import base64

web_app = os.getenv("APP_URL")

async def get_download_url(file_id: str, bot_token: str) -> str:
    """Get the download URL for a file with the given file_id."""
    try:
        # Construct the API request URL to get file information
        file_info_url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
        
        # Send the request to get file information
        response = requests.get(file_info_url)
        response.raise_for_status()  # Raise an error for bad response status
        
        file_info = response.json()['result']  # Extract the result containing file information
        file_path = file_info['file_path']  # Get the file_path from the file information
        
        # Construct the URL for downloading the file
        download_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        return download_url
    
    except (requests.RequestException, KeyError) as e:
        raise ValueError(f"Error occurred while getting download URL: {e}")

async def download_and_encode_to_base64(url: str) -> str:
    """Download a file from the given URL and encode it to base64."""
    try:
        # Send request to download the file
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad response status
        
        # Encode the downloaded content to base64
        content_base64 = base64.b64encode(response.content).decode('utf-8')
        return content_base64
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

async def detect_faces(base64, metadata):
    data = {"image_64": base64, "metadata": str(metadata)}

    try:
        response = requests.post(web_app + '/detect_faces', json=data)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            error_message = f"Request failed with status {response.status_code} response: #{response.json()}."
            return {"error": error_message}
    except requests.RequestException as e:
        error_message = f"Error occurred during request: {e}."
        return {"error": error_message}

async def save_audio(url, metadata):
    data = {"audio_url": url, "metadata": str(metadata)}

    try:
        response = requests.post(web_app + '/save_audio', json=data)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            error_message = f"Request failed with status {response.status_code} response: #{response.json()}."
            return {"error": error_message}
    except requests.RequestException as e:
        error_message = f"Error occurred during request: {e}."
        return {"error": error_message}