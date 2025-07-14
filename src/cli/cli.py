import click
from pywebpush import webpush, WebPushException

@click.group()
def cli():
    """A simple CLI tool."""
    pass


@cli.command()
@click.option('--endpoint', prompt='Endpoint URL', help='The push service endpoint URL')
@click.option('--p256dh', prompt='User public key (p256dh)', help='User public key')
@click.option('--auth', prompt='User auth secret', help='User auth secret')
@click.option('--message', prompt='Notification message', help='Message to send')
def send_push(endpoint, p256dh, auth, message):
    """Sends a web push notification to a user."""
    VAPID_PRIVATE_KEY = "1YvkmFA5p31EK31c6GYQ79Ev__ozsoGOJNBmdMomIp8"
    VAPID_CLAIMS = {
        "sub": "mailto:admin@example.com"
    }

    subscription_info = {
        "endpoint": endpoint,
        "keys": {
            "p256dh": p256dh,
            "auth": auth
        }
    }

    try:
        webpush(
            subscription_info,
            data=message,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS
        )
        click.echo("Notification sent successfully!")
    except WebPushException as ex:
        click.echo(f"Failed to send notification: {ex}")


if __name__ == "__main__":
    cli()