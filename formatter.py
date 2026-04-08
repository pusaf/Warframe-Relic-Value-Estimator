def build_string_format(name, status, values):
    """
    Formats the information given into a string for printing.

    Parameters:
        name (str): Relic name.
        status (str): Relic status.
        values ([float, float, float, float]): Expected values for each refinement level.

    Returns:
          str: Formatted string.
    """
    header = f"\nRelic Name: {name} ({status})\n"
    separator = "-" * 75 + "\n"
    table_contents = "Expected Plat: "
    width = len(table_contents)
    
    intact = "Intact".center(width, " ")
    exceptional = "Exceptional".center(width, " ")
    flawless = "Flawless".center(width, " ")
    radiant = "Radiant".center(width, " ")
    table_header = " " * width + intact + exceptional + flawless + radiant + "\n"

    for value in values:
        table_contents += str(value).center(width, " ")


    return header + separator + table_header + table_contents + "\n"
