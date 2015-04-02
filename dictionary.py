import re


class NotInDictionaryException(Exception):
    pass

class Term(object):
    def __init__(self, match):
        self.value = match.group(0)

    def __str__(self):
        return self.value

class SingleTerm(Term):
    pass

class MultipleTerm(Term):
    pass


class Dictionary:
    def __init__(self, dictionary_file):
        with open(dictionary_file, 'r') as f:
            self.dictionary = f.read()

    def find(self, term):
        if not self.valid_term(term):
            raise NotInDictionaryException()

        pattern = self.term2pattern(term)
        matches = re.finditer(pattern, self.dictionary, re.I | re.M)

        try:
            first = matches.next()
        except StopIteration:
            raise NotInDictionaryException()

        try:
            second = matches.next()
        except StopIteration:
            yield SingleTerm(first)
            return

        yield MultipleTerm(first)
        yield MultipleTerm(second)
        for match in matches:
            yield MultipleTerm(match)

    @staticmethod
    def valid_term(term):
        return term.isalnum() and not term.isdigit()

    @staticmethod
    def term2pattern(term):
        pattern = ''
        counter = 0

        for char in term:
            if char.isalpha():
                if counter:
                    pattern += '.' * counter
                    counter = 0
                pattern += char
            elif char.isdigit():
                counter *= 10
                counter += int(char)

        if counter:
            pattern += '.' * counter

        return '^' + pattern + '$'
