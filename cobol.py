#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
class Field:
    """Descriptor for fixed-length fields with type coercion and padding."""

    def __init__(self, field_type, length, default="", align="left", fillchar=" "):
        self.field_type = field_type
        self.length = length
        self.default = default
        self.align = align  # "left" or "right"
        self.fillchar = fillchar
        self.name = None

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f"_{self.name}", self.default)

    def __set__(self, obj, value):
        if value is None:
            value = self.default
        # Coerce type
        if self.field_type is int:
            value = int(value) if value != "" else 0
        elif self.field_type is str:
            value = str(value)
        # You can add more: date parsing, decimal, etc.
        setattr(obj, f"_{self.name}", value)


class SchemaMeta(type):
    def __new__(mcs, name, bases, attrs):
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                value.name = key
                fields[key] = value
                # Keep the descriptor in the class (don't del)
        attrs["_fields"] = fields
        return super().__new__(mcs, name, bases, attrs)


class Model(metaclass=SchemaMeta):
    def __init__(self, **kwargs):
        for name, field in self._fields.items():
            value = kwargs.get(name, field.default)
            setattr(self, name, value)  # triggers descriptor __set__

    def serialize(self) -> str:
        parts = []
        for name, field in self._fields.items():
            val = str(getattr(self, name, field.default))
            if field.align == "left":
                val = val[: field.length].ljust(field.length, field.fillchar)
            else:
                val = val[: field.length].rjust(field.length, field.fillchar)
            parts.append(val)
        return "|".join(parts)

    @classmethod
    def from_line(cls, line: str):
        """Parse a fixed-width line back into a Model instance."""
        obj = cls()
        pos = 0
        for name, field in cls._fields.items():
            # fmt: off
            chunk = line[pos:pos + field.length].strip()
            # fmt: on
            if field.field_type is int and chunk:
                chunk = int(chunk)
            setattr(obj, name, chunk)
            pos += field.length
        return obj


class UserRecord(Model):
    username = Field(str, length=10)
    user_id = Field(int, length=5)
    role = Field(str, length=8)


if __name__ == "__main__":
    # Create a single record
    u = UserRecord(username="jdoe", user_id=123, role="admin")
    print("Single record:")
    print(u.serialize())
    print("-" * 50)

    users = [
        UserRecord(username="alice", user_id=101, role="user"),
        UserRecord(
            username="bob_smith", user_id=102, role="moderator"
        ),  # will be truncated to 8 chars
        UserRecord(username="charlie", user_id=99999, role="admin"),
        UserRecord(username="dave", user_id=5, role="guest"),
    ]

    print("Multiple records (fixed-width format):")
    for user in users:
        print(user.serialize())
    print("-" * 50)

    # Example 3: Write to a fixed-width file (very common use case)
    print("Writing to fixed-width file 'users.dat'...")
    with open("users.dat", "w", encoding="utf-8") as f:
        for user in users:
            f.write(user.serialize() + "\n")  # each record on its own line

    # Example 4: Reading the file back (parsing)
    print("\nReading back from file:")
    with open("users.dat", "r", encoding="utf-8") as f:
        for line in f:
            # Simple parsing by splitting on '|' (since your serialize uses | )
            parts = line.strip().split("|")
            if len(parts) == 3:
                reconstructed = UserRecord(
                    username=parts[0].strip(),
                    user_id=int(parts[1].strip()),
                    role=parts[2].strip(),
                )
                print(reconstructed.serialize())
