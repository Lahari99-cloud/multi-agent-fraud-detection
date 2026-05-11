from __future__ import annotations


class FeedbackMemory:
    def __init__(self) -> None:
        self.memory: dict[str, str] = {}

    def add_feedback(self, transaction_id: str, label: str) -> None:
        self.memory[transaction_id] = label

    def get_feedback(self, transaction_id: str) -> str | None:
        return self.memory.get(transaction_id)


feedback_store = FeedbackMemory()
