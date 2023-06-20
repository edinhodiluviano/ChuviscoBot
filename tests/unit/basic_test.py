import itertools

from chuvisco import main


def test_should_always_pass():
    ...


def test_app_has_save_handler():
    app = main.create_app()
    all_callbacks = {
        h.callback
        for h in itertools.chain.from_iterable(app.handlers.values())
    }
    assert main.save in all_callbacks
