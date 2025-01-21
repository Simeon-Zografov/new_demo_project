import email
import imaplib


def get_last_email(email_address, password, from_email):

    server = imaplib.IMAP4_SSL('smtp.gmail.com')
    server.login(email_address, password)
    server.select('INBOX')
    email_ids = server.search(None, 'FROM', from_email)
    email_id_list = email_ids[1][0].decode('utf-8').split()
    list_len = len(email_id_list)
    latest_email_id = email_id_list[list_len-1]

    email_dict = {}
    email_data = server.fetch(str(latest_email_id), "(RFC822)")
    message_content = email_data[1][0]
    if message_content is not None:
        if isinstance(message_content, tuple) and len(message_content) == 2:
            email_headers_bytes = message_content[1]
            if isinstance(email_headers_bytes, bytes):
                message = email.message_from_bytes(email_headers_bytes)
                email_dict["From"] = message.get('From')
                email_dict["To"] = message.get('To')
                email_dict["Date"] = message.get('Date')
                email_dict["Subject"] = message.get('Subject')
                for part in message.walk():
                    if part.get_content_type() == "text/html":
                        email_dict["Content"] = part.as_string()
                return email_dict
            else:
                print("The second element of message_content is not bytes.")
        else:
            print("message_content is not a tuple of length 2.")
    else:
        print("message_content is None")

    server.logout()


def get_latest_email_subject():
    email_body = get_last_email("simeon.hhl.qa@gmail.com", "crpp cvlb oujp ansl", 'no-reply@dev.siworld.io')
    if email_body is not None:
        email_subject = email_body["Subject"]
        return email_subject
    else:
        print("Email body is None")
