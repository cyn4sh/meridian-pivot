from solstice_pivot.attendee_state_transitions import Attendee
from solstice_pivot.attendee_registry import AttendeeRegistry


class CheckInService:
    def __init__(self, registry):
        self.registry = registry
        self._next_job_number = 1

    def check_in(self, attendee_id):
        attendee = self.registry.get_by_id(attendee_id)

        if attendee is None:
            return {
                "success": False,
                "message": "Attendee not found"
            }

        if attendee.status != "not_checked_in":
            return {
                "success": False,
                "message": f"Attendee already {attendee.status}"
            }

        print_job_id = f"JOB-{attendee.attendee_id}"

        attendee.mark_pending(print_job_id)
        self.registry.add(attendee)

        return {
            "success": True,
            "attendee_id": attendee.attendee_id,
            "print_job_id": print_job_id,
            "status": attendee.status
        }


if __name__ == "__main__":
    registry = AttendeeRegistry()

    alice = Attendee("A001", "Alice")
    bob = Attendee("A002", "Bob")

    registry.add(alice)
    registry.add(bob)

    service = CheckInService(registry)

    print("Alice first scan:")
    print(service.check_in("A001"))

    print("\nAlice duplicate scan:")
    print(service.check_in("A001"))

    print("\nUnknown attendee:")
    print(service.check_in("A999"))