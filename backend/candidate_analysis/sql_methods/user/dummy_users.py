from sqlalchemy import text
import hashlib

def dummy_insert_users_query():
    pattern = 'somepassword'
    passwords = { pattern + str(i): hashlib.sha3_256((pattern + str(i)).encode()).hexdigest() for i in range(1,11) }
    return text("""
        INSERT INTO users (username, email, password) VALUES
            ('sampleusername1', 'sampleusername1@gmail.com', '{somepassword1}'),
            ('sampleusername2', 'sampleusername2@gmail.com', '{somepassword2}'),
            ('sampleusername3', 'sampleusername3@gmail.com', '{somepassword3}'),
            ('sampleusername4', 'sampleusername4@gmail.com', '{somepassword4}'),
            ('sampleusername5', 'sampleusername5@gmail.com', '{somepassword5}'),
            ('sampleusername6', 'sampleusername6@gmail.com', '{somepassword6}'),
            ('sampleusername7', 'sampleusername7@gmail.com', '{somepassword7}'),
            ('sampleusername8', 'sampleusername8@gmail.com', '{somepassword8}'),
            ('sampleusername9', 'sampleusername9@gmail.com', '{somepassword9}'),
            ('sampleusername10', 'sampleusername10@gmail.com', '{somepassword10}');
    """.format(**passwords))
