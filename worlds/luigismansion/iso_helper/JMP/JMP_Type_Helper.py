from gcbrickwork.JMP import JMPEntry


def check_jmp_header_name_has_value(jmp_entry: JMPEntry, field_name: str, field_value: int | str | float) -> bool:
    """Checks if a specific JMP header has a value within the given JMPEntry."""
    return any((jmp_field, jmp_value) for (jmp_field, jmp_value) in jmp_entry.items() if
        jmp_field.field_name == field_name and jmp_entry[jmp_field] == field_value)


def get_jmp_header_name_value(jmp_entry: JMPEntry, field_name: str) -> int | str | float:
    """Returns the current value from the provided JMPEntry's field"""
    return jmp_entry[next(j_field for j_field in jmp_entry.keys() if j_field.field_name == field_name)]


def update_jmp_header_name_value(jmp_entry: JMPEntry, field_name: str, field_value: int | str | float):
    """Updates a JMP header with the provided value in the given JMPEntry"""
    jmp_field = next(j_field for j_field in jmp_entry.keys() if j_field.field_name == field_name)
    jmp_entry[jmp_field] = field_value