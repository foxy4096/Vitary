from .models import Feed
from .forms import FeedForm

def get_latest_feeds(request):
    feeds = Feed.latest_feeds()
    random_feed = Feed.objects.order_by("?").first()
    return {'latest_feeds': feeds, 'random_feed': random_feed}

def feed_form(request):
    feed_form = FeedForm()
    return {'feed_form': feed_form}
