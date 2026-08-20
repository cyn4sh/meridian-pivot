import hashlib
import hmac
import json

from solstice_pivot.attendee_registry import AttendeeRegistry


WEBHOOK_SECRET = b"my-webhook-secret"


def verify_signature(payload, received_signature):
    expected_signature = hmac.new(
        WEBHOOK_SECRET,
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        received_signature,
        expected_signature
    )


class WebhookHandler:
    def __init__(self, registry):
        self.registry = registry

    def handle(self, payload, received_signature):
        if not verify_signature(payload, received_signature):
            return {
                "success": False,
                "message": "Webhook signature invalid"
            }

        try:
            data = json.loads(payload.decode("utf-8"))
        except json.JSONDecodeError:
            return {
                "success": False,
                "message": "Invalid webhook payload"
            }

        print_job_id = data.get("print_job_id")

        if print_job_id is None:
            return {
                "success": False,
                "message": "Missing print_job_id"
            }

        attendee = self.registry.get_by_job_id(print_job_id)

        if attendee is None:
            return {
                "success": False,
                "message": "Print job not found"
            }

        if attendee.status == "checked_in":
            return {
                "success": True,
                "message": "Webhook already processed",
                "attendee_id": attendee.attendee_id,
                "status": attendee.status
            }

        if attendee.status != "pending":
            return {
                "success": False,
                "message": f"Cannot complete attendee in {attendee.status} state"
            }

        attendee.mark_checked_in()

        return {
            "success": True,
            "message": "Webhook processed successfully",
            "attendee_id": attendee.attendee_id,
            "status": attendee.status
        }


if __name__ == "__main__":
    registry = AttendeeRegistry()

    from solstice_pivot.attendee_state_transitions import Attendee

    alice = Attendee("A001", "Alice")
    alice.mark_pending("JOB-A001")
    registry.add(alice)

    payload = json.dumps({
        "print_job_id": "JOB-A001",
        "attendee_id": "A001",
        "status": "printed"
    }, separators=(",", ":")).encode("utf-8")

    signature = hmac.new(
        WEBHOOK_SECRET,
        payload,
        hashlib.sha256
    ).hexdigest()

    handler = WebhookHandler(registry)

    print("First webhook:")
    print(handler.handle(payload, signature))

    print("\nDuplicate webhook:")
    print(handler.handle(payload, signature))