import hashlib
import hmac
import json

from solstice_pivot.attendee_state_transitions import Attendee
from solstice_pivot.attendee_registry import AttendeeRegistry
from solstice_pivot.check_in_service import CheckInService
from solstice_pivot.print_queue import PrintQueue, retry_with_backoff
from solstice_pivot.webhook_handler import (
    WEBHOOK_SECRET,
    WebhookHandler,
)


def create_webhook(print_job_id, attendee_id):
    payload = json.dumps({
        "print_job_id": print_job_id,
        "attendee_id": attendee_id,
        "status": "printed"
    }, separators=(",", ":")).encode("utf-8")

    signature = hmac.new(
        WEBHOOK_SECRET,
        payload,
        hashlib.sha256
    ).hexdigest()

    return payload, signature


if __name__ == "__main__":
    registry = AttendeeRegistry()

    alice = Attendee("A001", "Alice")
    bob = Attendee("A002", "Bob")

    registry.add(alice)
    registry.add(bob)

    check_in_service = CheckInService(registry)
    webhook_handler = WebhookHandler(registry)

    print("=== 1. Attendee scans ===")

    alice_result = check_in_service.check_in("A001")
    bob_result = check_in_service.check_in("A002")

    print("Alice:", alice_result)
    print("Bob:", bob_result)

    print("\n=== 2. Publish Alice's print job ===")

    alice_queue = PrintQueue()

    alice_print_job = {
        "print_job_id": alice_result["print_job_id"],
        "attendee_id": alice_result["attendee_id"],
        "name": alice.name,
    }

    try:
        result = retry_with_backoff(
            lambda: alice_queue.publish(alice_print_job)
        )

        print("Alice publish successful:", result)

    except Exception as error:
        print("Alice publish failed:", error)

    print("\n=== 3. Publish Bob's print job ===")

    bob_queue = PrintQueue()

    bob_print_job = {
        "print_job_id": bob_result["print_job_id"],
        "attendee_id": bob_result["attendee_id"],
        "name": bob.name,
    }

    try:
        result = retry_with_backoff(
            lambda: bob_queue.publish(bob_print_job)
        )

        print("Bob publish successful:", result)

    except Exception as error:
        print("Bob publish failed:", error)

    print("\n=== 4. Out-of-order webhook confirmations ===")

    bob_payload, bob_signature = create_webhook(
        "JOB-A002",
        "A002"
    )

    alice_payload, alice_signature = create_webhook(
        "JOB-A001",
        "A001"
    )

    print("Bob webhook arrives first:")
    print(
        webhook_handler.handle(
            bob_payload,
            bob_signature
        )
    )

    print("\nAlice webhook arrives second:")
    print(
        webhook_handler.handle(
            alice_payload,
            alice_signature
        )
    )

    print("\n=== 5. Duplicate webhook ===")

    print(
        webhook_handler.handle(
            bob_payload,
            bob_signature
        )
    )

    print("\n=== 6. Final attendee states ===")

    print(
        "Alice:",
        registry.get_by_id("A001")
    )

    print(
        "Bob:",
        registry.get_by_id("A002")
    )