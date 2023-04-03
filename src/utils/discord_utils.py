def generate_table(headers, data):

    column_widths = [len(header) for header in headers]

    for row in data:
        for index, cell in enumerate(row):
            column_widths[index] = max(column_widths[index], len(str(cell)))

    table = []

    header_row = "| " + " | ".join([header.ljust(column_widths[i])
                                   for i, header in enumerate(headers)]) + " |"
    table.append(header_row)

    separator_row = "|-" + \
        "-|-".join(["-" * column_widths[i]
                   for i in range(len(column_widths))]) + "-|"
    table.append(separator_row)

    for row in data:
        formatted_row = "| " + \
            " | ".join([str(cell).ljust(column_widths[i])
                       for i, cell in enumerate(row)]) + " |"
        table.append(formatted_row)

    return "\n".join(table)
