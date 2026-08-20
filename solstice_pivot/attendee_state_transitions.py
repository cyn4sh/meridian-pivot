class Attendee:
    def __init__(self, attendee_id, name):
        self.attendee_id = attendee_id
        self.name = name
        self.status = "not_checked_in"
        self.print_job_id = None

    def mark_pending(self, print_job_id):
        if self.status != "not_checked_in":
            return False

        self.status = "pending"
        self.print_job_id = print_job_id
        return True

    def mark_checked_in(self):
        if self.status != "pending":
            return False

        self.status = "checked_in"
        return True

    def mark_failed(self):
        if self.status != "pending":
            return False

        self.status = "failed"
        return True

    def __repr__(self):
        return (
            f"Attendee("
            f"id={self.attendee_id}, "
            f"name={self.name}, "
            f"status={self.status}, "
            f"print_job_id={self.print_job_id}"
            f")"
        )


if __name__ == "__main__":
    attendee = Attendee("A001", "Alice")

    print("Initial:", attendee)

    print("Mark pending:", attendee.mark_pending("JOB-A001"))
    print("After pending:", attendee)

    print("Mark checked in:", attendee.mark_checked_in())
    print("After checked in:", attendee)

    print("Duplicate check-in:", attendee.mark_checked_in())
    print("Final:", attendee)