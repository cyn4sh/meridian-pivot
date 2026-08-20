import time


class TemporaryQueueError(Exception):
    pass


class PermanentQueueError(Exception):
    pass


class PrintQueue:
    def __init__(self):
        self._attempts = 0

    def publish(self, print_job):
        self._attempts += 1

        print(f"Queue publish attempt {self._attempts}")

        if self._attempts < 3:
            raise TemporaryQueueError(
                "Temporary message broker failure"
            )

        print(f"Print job published: {print_job}")
        return True


def retry_with_backoff(operation, max_retries=2, base_delay=1):
    attempt = 0

    while attempt <= max_retries:
        try:
            return operation()

        except TemporaryQueueError as error:
            print(f"Retryable failure: {error}")

            if attempt == max_retries:
                print("Maximum retry attempts reached.")
                raise

            delay = base_delay * (2 ** attempt)

            print(f"Waiting {delay} seconds before retrying...")
            time.sleep(delay)

            attempt += 1

        except PermanentQueueError as error:
            print(f"Permanent failure: {error}")
            raise


if __name__ == "__main__":
    queue = PrintQueue()

    print_job = {
        "print_job_id": "JOB-A001",
        "attendee_id": "A001",
        "name": "Alice",
    }

    print("=== Temporary failure test ===")

    try:
        result = retry_with_backoff(
            lambda: queue.publish(print_job)
        )

        print("Publish successful:", result)

    except TemporaryQueueError:
        print("Queue publish failed after retries")

    except PermanentQueueError:
        print("Queue publish permanently failed")

    print()
    print("=== Permanent failure test ===")

    def permanent_failure():
        raise PermanentQueueError(
            "Permanent message broker configuration failure"
        )

    try:
        retry_with_backoff(permanent_failure)

    except PermanentQueueError:
        print("Permanent failure handled without retry")