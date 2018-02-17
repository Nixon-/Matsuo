from textstat import textstat


def compute_haiku_coherence(haiku):
    return 0


class Haiku:

    def __init__(self, lines):
        self.lines = lines
        self.validate()

    def validate(self):
        if len(self.lines) != 3:
            raise ValueError('Not a haiku')
        constraints = [5, 7, 5]
        for idx in range(len(self.lines)):
            syllables = 0
            for word in self.lines[idx]:
                syllables += textstat.textstat.syllable_count(word)
            if syllables > constraints[idx]:
                raise ValueError('Not a haiku')

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ',\n'.join(map(lambda line: ' '.join(map(lambda word: word.capitalize(), line)), self.lines))
