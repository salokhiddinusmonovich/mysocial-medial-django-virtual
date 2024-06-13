from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from .models import ChatGroup, GroupMessage
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from .forms import ChatMessageCreateForm
from asgiref.sync import async_to_sync



@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatMessageCreateForm()


    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user
            }
            return render(request, 'a_rchat/partials/chat_message_p.html', context)

    return render(request, 'a_rchat/chat.html', {'chat_messages': chat_messages, 'form': form})




def chat_file_upload(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")

    if request.htmx and request.FILES:
        file = request.FILES['file']
        message = GroupMessage.objects.create(
            file = file,
            author=request.user,
            group=chat_group
        )
        channel_layer = get_channel_layer()
        event = {
            'type': 'message_handler',
            'message_id': message.id
        }
        async_to_sync(channel_layer.group_send)(
            chat_group, event
        )

    return HttpResponse()



