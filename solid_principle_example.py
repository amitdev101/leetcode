# Single Responsibility Principle (SRP)
# Each class has a single, well-defined responsibility

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class EmailSender:
    def __init__(self):
        pass
    
    def send_email(self, user, message):
        print(f"Sending email to {user.name} at {user.email}: {message}")


# Open/Closed Principle (OCP)
# Software entities should be open for extension but closed for modification

class EmailMessage:
    def __init__(self, user, subject, body):
        self.user = user
        self.subject = subject
        self.body = body

class HTMLMessage(EmailMessage):
    def __init__(self, user, subject, body, html):
        super().__init__(user, subject, body)
        self.html = html
    
    def get_message(self):
        return self.html

class PlainTextMessage(EmailMessage):
    def __init__(self, user, subject, body):
        super().__init__(user, subject, body)
    
    def get_message(self):
        return self.body


# Liskov Substitution Principle (LSP)
# Subtypes must be substitutable for their base types

class MessageSender:
    def __init__(self):
        self.sender = EmailSender()

    def send_message(self, message):
        self.sender.send_email(message.user, message.get_message())

class CustomMessageSender(MessageSender):
    def __init__(self, sender):
        self.sender = sender

class BrokenMessageSender(MessageSender):
    def __init__(self):
        pass

    def send_message(self, message):
        # This violates LSP, as the method signature is not compatible
        # with the base class
        self.sender.send_email(message.user, message.get_message(), "extra param")


# Interface Segregation Principle (ISP)
# Clients should not be forced to depend on interfaces they do not use

class Message:
    def get_message(self):
        pass

class EmailMessageInterface:
    def get_email_message(self):
        pass

class HTMLMessageInterface(EmailMessageInterface):
    def get_html_message(self):
        pass

class PlainTextMessageInterface(EmailMessageInterface):
    def get_plain_text_message(self):
        pass


# Dependency Inversion Principle (DIP)
# Depend on abstractions, not concretions

class MessageSenderInterface:
    def send_message(self, message):
        pass

class EmailSenderInterface:
    def send_email(self, user, message):
        pass

class EmailSenderAdapter(EmailSenderInterface):
    def __init__(self):
        self.sender = EmailSender()

    def send_email(self, user, message):
        self.sender.send_email(user, message)


# Usage example
if __name__ == '__main__':
    # Create user and messages
    user = User("John Doe", "john.doe@example.com")
    message1 = HTMLMessage(user, "Test HTML message", "This is a test message in HTML format", "<html><body><h1>Test HTML message</h1><p>This is a test message in HTML format.</p></body></html>")
    message2 = PlainTextMessage(user, "Test plain text message", "This is a test message in plain text format")

    # Create sender and send messages
    sender = MessageSender()
    sender.send_message(message1)
    sender.send_message(message2)

