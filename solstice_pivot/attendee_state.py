class Attendee:
    def __init__(self, attendee_id, name):
        self.attendee_id = attendee_id
        self.name = name
        self.status = "not_checked_in"

    def __repr__(self):
        return (
            f"Attendee("
            f"id={self.attendee_id}, "
            f"name={self.name}, "
            f"status={self.status}"
            f")"
        )


if __name__ == "__main__":
    attendee = Attendee("A001", "Alice")

    print(attendee)