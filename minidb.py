from pprint import pprint #don't worry about this this is just for making output look prettier

class Database:
    def __init__(self, dbname):
        self.dbname = dbname
        self.tables = {}

    def __str__(self):
        return f"Database: {','.join(self.tables)}"

    def __getitem__(self, tablename):
        return self.tables[tablename]

    def __setitem__(self, tablename, table: "Table"):
        self.tables[tablename] = table 

    def __delitem__(self, tablename):
        del self.tables[tablename]

    def __contains__(self, tablename):
        return tablename in self.tables

    def __len__(self):
        return len(self.tables)

    def __iter__(self):
        return iter(self.tables)

    def __eq__(self, db2):
        return (self.tables == db2.tables)

    def __call__(self, tablename):
        return self.tables[tablename]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Database closed")        
        
class Table:
    def __init__(self):
        self.records = []

    def __getitem__(self, index):
        return self.records[index]

    def __setitem__(self, index, record: dict):
        self.records[index] = record

    def __delitem__(self, index):
        del self.records[index]

    def __iter__(self):
        return iter(self.records)

    def __len__(self):
        return len(self.records)

    def __repr__(self):
        return f"{self.records}"

    def where(self, **conditions):
        result = []
        for record in self.records:
            matches = True

            for key, value in conditions.items():
                if record[key] != value:
                    matches = False
                    break

            if matches:
                result.append(record)

        return Query(result, self)

    def __getattr__(self, field):
        return Field(self, field)


class Query:
    def __init__(self, content, table):
        self.content = content
        self.table = table

    def __iter__(self):
        return iter(self.content)

    def __len__(self):
        return len(self.content)

    def __getitem__(self, index):
        return self.content[index]

    def __contains__(self, targetrecord):
        return targetrecord in self.content

    def __and__(self, other: "Query"):
        result = []
        for record in self.content:
            if record in result:
                continue
            if (record in other.content):
                result.append(record)

        return Query(result, self.table)

    def __or__(self, other: "Query"):
        result = []
        for record in self.content + other.content:
            if record in result:
                continue
            result.append(record)
        return Query(result, self.table)

    def __invert__(self):
        result = []
        for record in self.table.records: 
            if record in self.content:
                continue
            result.append(record)

        return Query(result, self.table)

class Field:
    def __init__(self, table, field):
        self.field = field
        self.table = table

    def __gt__(self, target):
        result = []
        for record in self.table.records:
            if (record[self.field] > target and record not in result):
                result.append(record)

        return Query(result, self.table)

    def __lt__(self, target):
        result = []
        for record in self.table.records:
            if (record[self.field] < target and record not in result):
                result.append(record)

        return Query(result, self.table)

    def __ge__(self, target):
        result = []
        for record in self.table.records:
            if (record[self.field] >= target and record not in result):
                result.append(record)

        return Query(result, self.table)

    def __le__(self, target):
        result = []
        for record in self.table.records:
            if (record[self.field] <= target and record not in result):
                result.append(record)

        return Query(result, self.table)

    def __eq__(self, target):
        result = []
        for record in self.table.records:
            if (record[self.field] == target and record not in result):
                result.append(record)

        return Query(result, self.table)

    def __ne__(self, target):
        result = []
        for record in self.table.records:
            if (record[self.field] != target and record not in result):
                result.append(record)

        return Query(result, self.table)


print("\n----- Checking if this works or not -----")

db = Database("school")

students = Table()
students.records = [
    {"name": "Alice", "age": 20, "grade": "A"},
    {"name": "Bob", "age": 17, "grade": "B"},
    {"name": "Charlie", "age": 20, "grade": "A"},
    {"name": "David", "age": 25, "grade": "C"}
]

teachers = Table()
teachers.records = [
    {"name": "Mr. Smith", "subject": "Math"},
    {"name": "Ms. Jones", "subject": "English"}
]

db["students"] = students
db["teachers"] = teachers


print("\n--- Database ---")

print("dbname:", db.dbname)
print("tables:", list(db))
print('db["students"]:', db["students"])
print('"students" in db:', "students" in db)
print("len(db):", len(db))
print("str(db):", db)
print('db("students"):', db("students"))

db["courses"] = Table()
print("after adding courses:", list(db))

del db["courses"]
print("after deleting courses:", list(db))


print("\n--- Database equality ---")

db1 = Database("school")
db2 = Database("school")

db1["students"] = students
db2["students"] = students

print("same tables:", db1 == db2)

db2["teachers"] = teachers

print("different tables:", db1 == db2)


print("\n--- Context manager ---")

with Database("anything") as db:
    print("inside with:", db.dbname)


print("\n--- Table ---")

print("records:", students)
print("len(table):", len(students))
print("table[0]:", students[0])
print("list(table):", list(students))

students[1] = {"name": "Bob", "age": 18, "grade": "B+"}
print("after table[1] = ...:", students[1])

del students[1]
print("after del table[1]:", students)


print("\n--- Table.where() ---")

print("age=20:", list(students.where(age=20)))
print("grade='A':", list(students.where(grade="A")))


print("\n--- Field comparisons ---")

print("age > 20 :", list(students.age > 20))
print("age < 20 :", list(students.age < 20))
print("age >= 20:", list(students.age >= 20))
print("age <= 20:", list(students.age <= 20))
print("age == 20:", list(students.age == 20))
print("age != 20:", list(students.age != 20))


print("\n--- Query operators ---")

older = students.age >= 20
grade_a = students.grade == "A"

print("older & grade_a:", list(older & grade_a))
print("older | grade_a:", list(older | grade_a))
print("~grade_a:", list(~grade_a))


print("\n--- Query indexing & membership ---")

query = students.age >= 20

print("query:", list(query))
print("query[0]:", query[0])
print("query[0] in query:", query[0] in query)


print("\n----- I guess we're done here -----")
