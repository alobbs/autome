import email.message


def to_text(msg):
    """Renders email.message to string

    This method will be added to the message objs as
    their .render() method.
    """
    assert type(msg) is email.message.Message, "Input type"

    if msg.is_multipart():
        body = msg.get_payload()[0].get_payload()
    else:
        body = msg.get_payload()

    return 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(
        msg['From'], msg['To'], msg['Subject'], body[:500])
    None


def to_html(email):
    None
