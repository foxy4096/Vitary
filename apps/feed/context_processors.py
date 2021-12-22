from .models import Feed

def get_latest_feed(request):
    feeds = Feed.latest_feeds()
    return {'latest_feeds': feeds}