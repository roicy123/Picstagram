from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from notification.models import Notification
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib import messages


@login_required
def ShowNotification(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')

    # Add pagination
    paginator = Paginator(notifications, 10)  # Show 10 notifications per page
    page_number = request.GET.get('page')
    notifications_page = paginator.get_page(page_number)

    context = {
        'notifications': notifications_page,
    }

    return render(request, 'notifications/notification.html', context)

@login_required
def DeleteNotification(request, noti_id):
    user = request.user

    # Securely fetch the notification or return a 404 if not found
    notification = get_object_or_404(Notification, id=noti_id, user=user)

    if request.method == "POST":
        notification.delete()
        messages.success(request, "Notification deleted successfully.")
        return redirect('show-notification')

    # Optional: Render a confirmation page for deletion
    context = {
        'notification': notification,
    }
    return render(request, 'notifications/confirm_delete.html', context)