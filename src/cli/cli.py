import click
from . import notify

@click.group()
def enso():
    """A simple CLI tool."""
    pass


@enso.command()
@click.argument('message')
def push(message):
    subscription = {
        'endpoint': 'https://fcm.googleapis.com/fcm/send/cfzwE1V4jlM:APA91bEuOi4Bv_W4Ahg3713nfqJ06VHRkf5ktrnyog5PCYXW3Fs1efiML5EF2pBi0Kne41raeNrNtAPoksxTYGRmbu4GY0-B8fZSn1eE7Cv30r3pOJVq4OPgObvJyxiujywvCndMUiNP',
        'expirationTime': None,
        'keys': {
            'p256dh': 'BM9QAEApa_vRxebni7Ok8WnZmCA_WChADMx45OL_46v7BZYRBmT4rQjxOxnAFEH1ZGMm1YBfD4nQr97e4gfdYpM',
            'auth': 'l-Db4nt0J6mewzFjBEq0NQ'
        }
    }

    notify.push_message(subscription, message)


if __name__ == "__main__":
    enso()