import re


class NotInDictionaryException(Exception):
    pass

class SingleTerm(object):
    def __init__(self, match):
        self.value = match.group(0)

    def __str__(self):
        return self.value

class MultipleTerm(object):
    def __init__(self, *args):
        self.values = args

    def next(self):
        try:
            for v in self.values[0]:
                yield v
            self.values.pop(0).group(0)
        except TypeError:
            yield self.values.pop(0).group(0)
        except IndexError:
            raise StopIteration()


class Dictionary:
    def __init__(self, dictionary_file):
        with open(dictionary_file, 'r') as f:
            self.dictionary = f.read()

    def find_by_pattern(self, pattern):
        matches = re.finditer('^' + pattern + '$', self.dictionary, re.I | re.M)

        try:
            first = matches.next()
        except StopIteration:
            raise NotInDictionaryException('pattern was not found')

        try:
            second = matches.next()
        except StopIteration:
            return SingleTerm(first)

        return MultipleTerm(first, second, matches)

    def find_by_term(self, term):
        if not self.valid_term(term):
            raise NotInDictionaryException('term is not valid')

        pattern = self.term2pattern(term)

        return self.find_by_pattern(pattern)

    @staticmethod
    def valid_pattern(pattern):
        return re.search('^[a-z\.]*[a-z][a-z\.]*$', pattern, re.I) is not None

    @staticmethod
    def valid_term(term):
        return term.isalnum() and not term.isdigit()

    @staticmethod
    def pattern2term(pattern):
        term = ''
        counter = 0

        for char in pattern:
            if char.isalpha():
                if counter:
                    term += str(counter)
                    counter = 0
                term += char
            elif char == '.':
                counter += 1

        if counter:
            term += str(counter)

        return term

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

        return pattern
