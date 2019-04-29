import pytheory

SCALE = pytheory.TonedScale(tonic='C4')['minor']


def play_from(result):
    pytheory.play(
        SCALE[1], t=result['ast_tree'].get('value', {}).get('n', 1) * 100)
