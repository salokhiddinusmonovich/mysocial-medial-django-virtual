from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
from django.core.mail import EmailMessage
from .tasks import *
import threading
from django.template.loader import render_to_string

@login_required
def messageboard_view(request):
    messageboard = get_object_or_404(MessageBoard, id=1)
    form = MessageCreateForm()

    if request.method == 'POST':
        if request.user in messageboard.subscribers.all():
            form = MessageCreateForm(request.POST)
            if form.is_valid:
                message = form.save(commit=False)
                message.author = request.user
                message.messageboard = messageboard
                message.save()
                send_email(message)
        else:
            messages.warning(request, 'You need to be Subscribed!')
        return redirect('messageboard')



    context = {
        'messageboard': messageboard,
        'form': form
    }
    return render(request, 'message_board/index.html', context)


@login_required
def subscripe(request):
    messageboard = get_object_or_404(MessageBoard, id=1)

    if request.user not in messageboard.subscribers.all():
        messageboard.subscribers.add(request.user)
    else:
        messageboard.subscribers.remove(request.user)

    return redirect('messageboard')

def send_email(message):
    messageboard = message.messageboard
    subscribers = messageboard.subscribers.all()
    day = current_month_day = datetime.now().strftime('%B %d')
    subscriber_count = subscribers.count()
    for subscriber in subscribers:
        body = render_to_string('message_board/newsletter.html', {'name': subscriber.profile.name, 'sub': subscriber_count, 'day': day})
        email = EmailMessage(subscriber, body, to=[subscriber.email])
        email.content_subtype = "html"
        email.send()
    current_month = datetime.now().strftime('%B')
    subscriber_count = subscribers.count()
    return f'{current_month} Newsletter to {subscriber_count} sub! '

#         email_thread = threading.Thread(target=send_email_thread, args=(subject, body, subscribers))
#         email_thread.start()
#
# def send_email_thread(subject, body, subscriber):
#     email = EmailMessage(subject, body, to=[subscriber.email])
#     email.send()