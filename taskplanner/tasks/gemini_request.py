import requests
import time

#AIzaSyC1hTHfN4xHivEP7naDtX-Xdp3HZTBmo4I

    
gemini_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyBXL2AQ5cGOOmOF0za5k_jPy6044TK_JbY'

def send_gemini_request(prompt):
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    retry_count = 0
    while retry_count < 3:
        try:
            response = requests.post(gemini_url, json=payload, headers=headers)
            response.raise_for_status()  # Raise error for bad responses
            response_json = response.json()
            if 'error' in response_json:
                print(f"Error: {response_json['error']['message']}")
                return None
            return response_json
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            retry_count += 1
            time.sleep(2 ** retry_count)

    print("Maximum retry attempts reached. Please try again later.")
    return None