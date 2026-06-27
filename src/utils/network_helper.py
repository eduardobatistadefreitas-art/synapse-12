```python
import time
import random
import requests # Used for simulating requests.exceptions.HTTPError

# --- Constants ---
MAX_RETRIES = 5  # Maximum number of retry attempts
INITIAL_WAIT_SECONDS = 1  # Initial wait time in seconds before the first retry

# --- Helper for simulating requests.Response ---
class MockResponse:
    """
    A mock response object designed to simulate `requests.Response`
    for testing purposes, particularly for `raise_for_status()`.
    """
    def __init__(self, status_code: int, json_data: dict = None, text_data: str = None):
        self.status_code = status_code
        self._json_data = json_data
        # Prioritize text_data if provided, otherwise use JSON data string representation
        self.text = text_data if text_data is not None else str(json_data)

    def json(self):
        """
        Returns the JSON data if available.
        Raises ValueError if no JSON data was provided.
        """
        if self._json_data is None:
            raise ValueError("No JSON data available for this mock response.")
        return self._json_data

    def raise_for_status(self):
        """
        Simulates `requests.Response.raise_for_status()`.
        Raises `requests.exceptions.HTTPError` for status codes >= 400.
        """
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(
                f"Simulated HTTP Error: {self.status_code}",
                response=self # Attach the mock response to the exception
            )

# --- Simulated API Call Function ---
def _perform_api_call_internal(attempt: int):
    """
    Simulates an actual API call.
    This function is designed to fail with an HTTP 429 error for the first
    few attempts (e.g., 3 attempts), and then succeed.

    Args:
        attempt (int): The current attempt number.

    Returns:
        dict: A dictionary representing a successful API response.

    Raises:
        requests.exceptions.HTTPError: If the simulated API call results in
                                       an HTTP error, specifically 429.
    """
    print(f"Attempt {attempt}: Making API call...")

    # Simulate network latency or processing time
    time.sleep(0.5)

    # Simulate HTTP 429 (Quota Exceeded) error for the first 3 attempts
    if attempt <= 3:
        error_response_json = {
            "error": {
                "code": 429,
                "message": "You exceeded your current quota, please check your plan and billing details."
            }
        }
        # Create a mock response object for the 429 error
        mock_response = MockResponse(429, json_data=error_response_json)
        # Raise an HTTPError using the mock response
        mock_response.raise_for_status()

    # If we reach here, the API call is considered successful
    print(f"Attempt {attempt}: API call successful!")
    return {"status": "success", "data": f"Data retrieved successfully on attempt {attempt}"}

# --- Main Function with Retry Logic ---
def make_api_request_with_retries(api_endpoint: str = "https://api.example.com/data"):
    """
    Attempts to make an API request with built-in retry logic for HTTP 429
    (Too Many Requests) errors, using an exponential backoff strategy.

    Args:
        api_endpoint (str): The URL of the API endpoint to call.
                            (Used for context in this simulation, not an actual call).

    Returns:
        dict: The successful response from the API.

    Raises:
        requests.exceptions.HTTPError: If the API call fails with a non-429 HTTP error,
                                       or if 429 errors persist after exhausting
                                       all retry attempts.
        Exception: For any other unexpected errors during the process.
    """
    wait_time = INITIAL_WAIT_SECONDS
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Attempt the API call
            result = _perform_api_call_internal(attempt)
            print(f"API request to {api_endpoint} successful after {attempt} attempts.")
            return result
        except requests.exceptions.HTTPError as e:
            # Check if the error is specifically an HTTP 429
            if e.response is not None and e.response.status_code == 429:
                print(f"Attempt {attempt} failed with HTTP 429 (Quota Exceeded).")
                if attempt < MAX_RETRIES:
                    # If not the last attempt, wait and retry
                    print(f"Retrying in {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                    wait_time *= 2  # Exponential backoff: double the wait time
                else:
                    # Max retries reached, re-raise the 429 error
                    print(f"Max retries ({MAX_RETRIES}) reached. API call failed permanently.")
                    raise # Re-raise the last HTTP 429 error
            else:
                # Re-raise any other HTTP errors immediately
                print(f"Attempt {attempt} failed with a non-429 HTTP error: {e}")
                raise
        except Exception as e:
            # Catch any other unexpected errors
            print(f"Attempt {attempt} failed with an unexpected error: {e}")
            raise # Re-raise the unexpected error

    # This line should theoretically be unreachable if the last `raise` is always hit,
    # but it serves as a final fallback to ensure an exception is raised if all
    # retries somehow fail without explicitly re-raising.
    raise requests.exceptions.HTTPError(
        f"Failed to complete API request to {api_endpoint} after {MAX_RETRIES} attempts due to persistent 429 errors."
    )

# --- Example Usage ---
if __name__ == "__main__":
    print("--- Starting API Request with Retries ---")
    try:
        # Call the function that handles retries
        response = make_api_request_with_retries()
        print("\n--- Final API Response ---")
        print(response)
    except requests.exceptions.HTTPError as e:
        # Handle cases where the API request ultimately failed due to HTTP errors
        print(f"\n--- API Request Failed Permanently ---")
        print(f"Error: {e}")
        if e.response:
            print(f"Status Code: {e.response.status_code}")
            try:
                # Attempt to print the JSON response body if available
                print(f"Response Body (JSON): {e.response.json()}")
            except ValueError:
                # Fallback to printing raw text if JSON parsing fails
                print(f"Response Body (Text): {e.response.text}")
    except Exception as e:
        # Handle any other unexpected errors that might occur
        print(f"\n--- An unexpected error occurred ---")
        print(f"Error: {e}")
```
