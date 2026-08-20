from solstice_pivot.attendee_state_transitions import Attendee


class AttendeeRegistry:
    def __init__(self):
        self._attendees_by_id = {}
        self._attendees_by_job_id = {}

    def add(self, attendee):
        self._attendees_by_id[attendee.attendee_id] = attendee

        if attendee.print_job_id is not None:
            self._attendees_by_job_id[attendee.print_job_id] = attendee

    def get_by_id(self, attendee_id):
        return self._attendees_by_id.get(attendee_id)

    def get_by_job_id(self, print_job_id):
        return self._attendees_by_job_id.get(print_job_id)


if __name__ == "__main__":
    registry = AttendeeRegistry()

    alice = Attendee("A001", "Alice")
    bob = Attendee("A002", "Bob")

    alice.mark_pending("JOB-A001")
    bob.mark_pending("JOB-B001")

    registry.add(alice)
    registry.add(bob)

    print("By attendee ID:", registry.get_by_id("A001"))
    print("By print job ID:", registry.get_by_job_id("JOB-B001"))
    print("Missing attendee:", registry.get_by_id("A999"))