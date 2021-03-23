import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class sender:
    # Class representing a email sender object

    def __init__(self,smtp_server,sender_email, password):
        self.port = 465 # For SSL
        self.smtp_server = smtp_server
        self.sender_email = sender_email
        self.password = password

    def send_email(self, receiver_email, message,subject):

        msg = MIMEMultipart("alternative")
        msg['From'] = self.sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        
        # Create HTML version of the message
        html = """\
            <html>
                <body>
                    <p>Estimado,<br>""" \
                        + message + "<br>\
                    </p>\
                </body>\
            </html>"""

        #part1 = MIMEText(message, "plain")
        content = MIMEText(html, "html")
        msg.attach(content)

        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP_SSL(self.smtp_server, self.port, context=context)
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, msg.as_string())

            print("Successfully email sent to: {}".format(receiver_email))

        except smtplib.SMTPException:
            print("Unable to send email")
        
