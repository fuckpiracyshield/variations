from whois import whois

class Whois:

    def get_text(self, value):
        result = whois(value)

        return result.text
