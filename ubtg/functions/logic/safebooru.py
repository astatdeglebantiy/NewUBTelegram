import safebooru2
from ubtg import config


def _function(_vars_) -> str:
    client = safebooru2.Safebooru()
    post = safebooru2.Posts(limit=1, id=client.random_id)
    client.download(post, filename='nya', directory=config.TEMP_PATH)
    return f'{config.TEMP_PATH}nya.jpg'