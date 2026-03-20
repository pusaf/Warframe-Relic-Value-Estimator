## build_string_format: Str Str [Float, Float, Float, Float] -> Str
## Formats the information given into a returned string
def build_string_format(name, type, values):
    header = f"\nRelic Name: {name} ({type})\n"
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
