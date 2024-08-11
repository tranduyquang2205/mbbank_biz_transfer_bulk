import unidecode

def convert_to_uppercase_no_accents(text):
    # Remove accents
    no_accents = unidecode.unidecode(text)
    # Convert to uppercase
    return no_accents.upper()