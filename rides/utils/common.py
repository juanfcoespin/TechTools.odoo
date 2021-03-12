def remove_chars(chars_to_remove, str_in):
    for char in chars_to_remove:
        str_in = str_in.replace(char, '')
    return str_in


def show_msg(msg):
    message = {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': 'Warning!',
            'message': msg,
            'sticky': False,
        }
    }
    return message
