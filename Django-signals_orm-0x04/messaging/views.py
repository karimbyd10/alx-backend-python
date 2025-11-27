from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout

@login_required
def delete_user(request):
    """
    Deletes the currently logged-in user.
    Related data is removed automatically by post_delete signals.
    """
    user = request.user

    # Logout user before deletion
    logout(request)

    # Delete the user (signal will run after this)
    user.delete()

    messages.success(request, "Your account and all associated data have been deleted.")
    return redirect("home")  # Redirect to a public landing page

