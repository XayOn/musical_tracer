from pyknow import KnowledgeEngine, Fact, DefFacts, Rule, MATCH, AS
from collections import Counter
import itertools
import pytheory


class Play(Fact):
    pass


class Player(KnowledgeEngine):
    """Main knowledge engine

    Plays music.

    How? TBD
    """

    @DefFacts()
    def start(self, logger=None, config=None):
        self.scales = (pytheory.TonedScale(tonic='C4')['major'],
                       pytheory.TonedScale(tonic='D4')['major'],
                       pytheory.TonedScale(tonic='E4')['major'],
                       pytheory.TonedScale(tonic='F4')['major'])
        self.logger = logger
        self.lines = Counter()
        self.config = config
        self.current_note = 0
        self.current_notes = []
        self.notes_by_event = {
            'line': 0,
            'Return': 1,
            'call': 2,
        }
        self.tempo = 4  # tempo 4/4
        # self.tempo = 0.5 # tempo crochet
        yield Fact(started=True)

    def add_note(self, result):
        """ Declare rules

        depth
        +++++

        Depth defines the scale.
        As depth in python should always come and go progressively and not with
        a lot of difference (never more than 4 steps difference, and always
        moving one step at a time, except sometimes going down)

        lineno
        ++++++

        We'll declare line numbers to count events in the same line.
        Each time a line repeats, it will sound less time.
        Also, linenumber should be used, in conjuntion with local variables
        as a way to group musical elements.

        event
        +++++

        line events are not representative
        - Maybe line events could compose accords and get them secuentially
          from a list, then, make the call event shorter or longer depending
          on the number of times the line has appeared
        - Maybe call events should stand out
        - Maybe return events should stand out in an inverse wah to call events
        - Maybe exception events should should bad? but exceptions
          can be used in a good way. Maybe just slightly bad, two scales
          difference?
        """

        notes = [
            2,  # crotchet
            4,  # black
            8  # white
            # ... TODO
        ]

        self.lines[result['line_number']] += 1
        duration = (self.lines[result['line_number']]) + len(
            result.get('source_line', '_'))
        figure = notes[duration % len(notes)]
        duration = int((figure / self.tempo) * 1000)

        self.declare(
            Fact(
                scale=result['depth'] % len(self.scales),
                duration=duration,
                figure=figure,
                note=self.notes_by_event.get(result.get('event'), 3)))

    @Rule(AS.playfact << Play())
    def play_notes(self, playfact):
        self.retract(playfact)
        for note in self.current_notes:
            pytheory.play(note['note'], t=note['t'])
        self.current_notes = []

    @Rule(
        Fact(
            scale=MATCH.scale,
            figure=MATCH.figure,
            duration=MATCH.duration,
            note=MATCH.note))
    def test_rule(self, scale, figure, duration, note):
        # TODO: add figures.
        # TODO: make this with pyknow logic
        self.current_note += figure
        if self.current_note >= self.tempo:
            self.declare(Play())
        scale = self.scales[scale]
        self.current_notes.append({
            'note': scale[note % len(scale.tones)],
            't': duration
        })
        self.current_note = 0
