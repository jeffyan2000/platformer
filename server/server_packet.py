def assemble_packet(*args):
    result = "@"
    for arg in args:
        result += str(arg)
        result += ";"
    return result

def assemble_header(header, body):
    return header + str(body)
