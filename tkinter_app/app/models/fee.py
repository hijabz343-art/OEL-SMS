class Fee:
    def __init__(self, id=None, student_id=None, amount=0.0, paid_date="", status="Pending"):
        self.id = id
        self.student_id = student_id
        self.amount = amount
        self.paid_date = paid_date
        self.status = status
