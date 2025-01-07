import os
import sqlite3

__all__ = [
    'SQLDBManager',
]

class SQLDBManager:
    def __init__(self):
        self.sql_db_path = os.getenv("SQL_DB_PATH")
        self.conn = sqlite3.connect(self.sql_db_path)
        self.cursor = self.conn.cursor()
        self._create_database()

    def _create_database(self):
        conn = sqlite3.connect(self.sql_db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PersonInformation (
                personID TEXT PRIMARY KEY,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                dateOfBirth TEXT,
                country TEXT,
                city TEXT,
                village TEXT,
                fatherName TEXT,
                motherName TEXT,
                address TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS FaceRelation (
                faceID TEXT PRIMARY KEY,
                personID TEXT,
                FOREIGN KEY (personID) REFERENCES PersonInformation(personID)
            )
        ''')
        self.conn.commit()

    def get_person_by_face_id(self, face_id: str):
        """
        Retrieve person information by face ID.

        Args:
            face_id (str): The face ID to search for.

        Returns:
            dict: A dictionary containing person information, or None if no match is found.
        """

        # Query to join PersonInformation and FaceRelation tables
        self.cursor.execute('''
            SELECT p.personID, p.firstName, p.lastName, p.dateOfBirth, p.country, p.city, 
                   p.village, p.fatherName, p.motherName, p.address
            FROM PersonInformation p
            JOIN FaceRelation fr ON p.personID = fr.personID
            WHERE fr.faceID = ?
        ''', (face_id,))

        result = self.cursor.fetchone()

        if result:
            return {
                "personID": result[0],
                "faceID": face_id,
                "firstName": result[1],
                "lastName": result[2],
                "dateOfBirth": result[3],
                "country": result[4],
                "city": result[5],
                "village": result[6],
                "fatherName": result[7],
                "motherName": result[8],
                "address": result[9]
            }
        return None

    def select_person(self, person_id):

        self.cursor.execute('SELECT * FROM PersonInformation WHERE personID = ?', (person_id + 1,))
        person_info = self.cursor.fetchone()
        if person_info:
            return {
                "personID": person_info[0],
                "firstName": person_info[1],
                "lastName": person_info[2],
                "dateOfBirth": person_info[3],
                "country": person_info[4],
                "city": person_info[5],
            }
        return None

    def insert_person(self, person_id, first_name, last_name, date_of_birth, country, city):
        self.cursor.execute('''
            INSERT INTO PersonInformation (personID, firstName, lastName, dateOfBirth, country, city)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (person_id, first_name, last_name, date_of_birth, country, city))
        self.conn.commit()

    def insert_face_relation(self, face_id, person_id):
        self.cursor.execute('''
            INSERT INTO FaceRelation (faceID, personID)
            VALUES (?, ?)
        ''', (face_id, person_id))
        self.conn.commit()

