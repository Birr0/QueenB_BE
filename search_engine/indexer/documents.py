from collections import Counter
from dataclasses import dataclass

from . import analysis

@dataclass
class Abstract:
    ID: int
    type: str # video, notes, slides ...
    date: str
    lecturer: str
    module_code: str
    module_name: str
    url: str
    title: str
    description: str
    content: str

    @property
    def fulltext(self):
        return ' '.join([self.title, self.description, self.content, self.lecturer, self.date])

    def analyze(self):
        self.term_frequencies = Counter(analysis.analyze(self.fulltext))

    def term_frequency(self, term):
        return self.term_frequencies.get(term, 0)