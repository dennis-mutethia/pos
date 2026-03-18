import uuid
from datetime import datetime, timedelta

class RefreshTokenManager:

    def __init__(self, db):
        self.db = db

    def create_token(self, user_id):
        token = str(uuid.uuid4())
        expiry = datetime.utcnow() + timedelta(days=7)

        self.db.execute(
            """
            INSERT INTO refresh_tokens (id, user_id, expires_at)
            VALUES (%s,%s,%s)
            """,
            (token, user_id, expiry)
        )

        return token

    def verify(self, token):
        return self.db.fetch_one(
            """
            SELECT user_id
            FROM refresh_tokens
            WHERE id=%s AND expires_at > NOW()
            """,
            (token,)
        )

    def delete(self, token):
        self.db.execute(
            "DELETE FROM refresh_tokens WHERE id=%s",
            (token,)
        )