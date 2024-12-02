import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("gambling.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    telegram_id INT,
    username TEXT,
    score INT               
);  
""")

    def __del__(self):
        self.connection.close()

    def get_score(self, id: int) -> int:
        self.cursor.execute("SELECT score FROM users WHERE telegram_id=?", (id,))
        val = self.cursor.fetchone()
        if val is None:
            return None
        return tuple(val)[0]

    def get_top_five(self) -> list[tuple[str, int]]:
        self.cursor.execute(
            "SELECT username, score FROM users ORDER BY score DESC LIMIT 10"
        )
        args = self.cursor.fetchall()
        return args

    def set_score(self, id: int, value: int) -> None:
        self.cursor.execute(
            "UPDATE users SET score=?1 WHERE telegram_id=?2", (value, id)
        )
        self.connection.commit()

    def get_username(self, id: int) -> str:
        self.cursor.execute("SELECT username FROM users WHERE telegram_id=?", (id,))
        return self.cursor.fetchone()

    def create_user(self, id: int, username: str) -> None:
        self.cursor.execute("INSERT INTO users VALUES(?, ?, ?)", (id, username, 0))
        self.connection.commit()

    def __contains__(self, id: int) -> bool:
        return self.get_score(id) is not None


DATABASE = Database()
