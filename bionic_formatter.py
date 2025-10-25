import re
import string

def bionic_read(text):
    """
    Processes text and returns a list of lists of (text, is_bold) tuples.
    Each inner list represents a line.
    """
    output_lines = []
    lines = text.split('\n')

    for line in lines:
        # Split the line by spaces to handle words and maintain spacing
        parts = re.split(r'(\s+)', line)
        line_chunks = []
        for part in parts:
            if not part:
                continue

            # If the part is just whitespace, add it as non-bold
            if part.isspace():
                line_chunks.append((part, False))
                continue

            # Handle words with punctuation
            leading_punct = ""
            while part and part[0] in string.punctuation:
                leading_punct += part[0]
                part = part[1:]

            trailing_punct = ""
            while part and part[-1] in string.punctuation:
                trailing_punct = part[-1] + trailing_punct
                part = part[:-1]

            if leading_punct:
                line_chunks.append((leading_punct, False))

            if part:
                split_point = (len(part) + 1) // 2
                bold_part = part[:split_point]
                normal_part = part[split_point:]
                line_chunks.append((bold_part, True))
                line_chunks.append((normal_part, False))

            if trailing_punct:
                line_chunks.append((trailing_punct, False))

        output_lines.append(line_chunks)
    return output_lines