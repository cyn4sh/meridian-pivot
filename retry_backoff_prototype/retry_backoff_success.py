import time


operation_attempts = 0


def unreliable_operation():
    global operation_attempts

    operation_attempts += 1

    if operation_attempts <= 2:
        raise Exception("Temporary failure")

    return "Operation successful!"


def retry_with_backoff(max_retries=3, base_delay=1):
    attempt = 0

    while attempt <= max_retries:
        try:
            result = unreliable_operation()
            print(result)
            return result

        except Exception as error:
            print(f"Attempt {attempt + 1} failed: {error}")

            if attempt == max_retries:
                print("Maximum retries reached.")
                raise

            delay = base_delay * (2 ** attempt)

            print(f"Waiting {delay} seconds before retrying...")
            time.sleep(delay)

            attempt += 1


retry_with_backoff()