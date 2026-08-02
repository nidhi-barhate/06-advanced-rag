from sqlalchemy import desc
from sqlalchemy.orm import Session
from models.chat_model import Message

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, message: Message) -> Message:
        """
        Save a message into the database.
        """
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def find_all(self) -> list[Message]:
        """
        Retrieve all messages.
        """
        return self.db.query(Message).all()

    def find_by_id(self, message_id: int) -> Message | None:
        """
        Find a message by ID.
        """
        return (
            self.db.query(Message)
            .filter(Message.id == message_id)
            .first()
        )

    def delete(self, message_id: int) -> bool:
        """
        Delete a message.
        """
        message = self.find_by_id(message_id)

        if message is None:
            return False

        self.db.delete(message)
        self.db.commit()

        return True

    def delete_all(self) -> int:
        """
        Delete all messages.
        """
        deleted_count = self.db.query(Message).delete()
        self.db.commit()

        return deleted_count

    def find_last_messages(
            self,
            limit: int = 6
    ) -> list[Message]:
        messages = (
            self.db
            .query(Message)
            .order_by(desc(Message.id))
            .limit(limit)
            .all()
        )
        messages.reverse()
        return messages

    def history_as_text(
            self,
            limit: int = 6
    ) -> str:
        messages = self.find_last_messages(limit)
        history = []
        for message in messages:
            history.append(
                f"{message.role}: {message.content}"
            )
        return "\n".join(history)