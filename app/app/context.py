from django.conf import settings
from django.utils import timezone
from dashboard.models import Tip


def insert_settings(request):
    from marketing.utils import get_stat
    try:
        num_slack = int(get_stat('slack_users'))
    except:
        num_slack = 0
    if num_slack > 1000:
        num_slack = u'{}k'.format(str(round((num_slack)/1000, 1)))
    context = {
        'mixpanel_token': settings.MIXPANEL_TOKEN,
        'STATIC_URL': settings.STATIC_URL,
        'num_slack': num_slack,
        'github_handle': request.session.get('handle', False),
        'email': request.session.get('email', False),
        'rollbar_client_token': settings.ROLLBAR_CLIENT_TOKEN,
        'env': settings.ENV,
    }
    if context['github_handle']:
        context['unclaimed_tips'] = Tip.objects.filter(
            expires_date__gte=timezone.now(),
            receive_txid='',
            username__iexact=context['github_handle']
            )

    return context
