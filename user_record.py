#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Field:
    """Descriptor class to represent a data field."""

    def __init__(self, field_type, length):
        self.field_type = field_type
        self.length = length
        self.name = None  # Will be set by the metaclass


class SchemaMeta(type):
    def __new__(mcs, name, bases, attrs):
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                value.name = key  # Tell the field what its variable name is
                fields[key] = value
                del attrs[key]
        attrs["_fields"] = fields
        return super().__new__(mcs, name, bases, attrs)


class Model(metaclass=SchemaMeta):
    def __init__(self, **kwargs):
        # The metaclass prepared '_fields' for us!
        for name, value in kwargs.items():
            if name in self._fields:
                setattr(self, name, value)
            else:
                raise AttributeError(f"Invalid field: {name}")

    def serialize(self):
        """Standardize the data based on field lengths."""
        parts = []
        for name, field in self._fields.items():
            val = str(getattr(self, name, "")).ljust(field.length)
            parts.append(val)
        return "|".join(parts)


class UserRecord(Model):
    username = Field(str, length=10)
    user_id = Field(int, length=5)
    role = Field(str, length=8)


if __name__ == "__main__":
    u = UserRecord(username="jdoe", user_id=123, role="admin")
    print(u.serialize())
    # Output: 'jdoe      |123  |admin   '
