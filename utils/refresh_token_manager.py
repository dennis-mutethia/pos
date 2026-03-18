import uuid
from datetime import datetime, timedelta

class RefreshTokenManager:
    def __init__(self, db):
        self.db = db

    def create_token(self, user_id):
        token = str(uuid.uuid4())
        expiry = datetime.utcnow() + timedelta(days=7)
        query = "INSERT INTO refresh_tokens (id, user_id, expires_at) VALUES (%s,%s,%s)"
        self.db.execute(query, (token, user_id, expiry))
        return token

    def verify(self, token):
        query = "SELECT user_id FROM refresh_tokens WHERE id=%s AND expires_at > NOW()"
        result = self.db.execute(query, (token,), fetchone=True)
        if result:
            return {"user_id": result[0]}
        return None

    def delete(self, token):
        query = "DELETE FROM refresh_tokens WHERE id=%s"
        self.db.execute(query, (token,))