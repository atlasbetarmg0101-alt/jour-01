from django.shortcuts import render
from .models import ContactMessage


def home(request):
    return render(request, "core/home.html")


def services(request):
    return render(request, "core/services.html")


def about(request):
    return render(request, "core/about.html")


def contact(request):
    success = False

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )

            success = True

    return render(
        request,
        "core/contact.html",
        {"success": success}
    )
def projects(request):
    return render(request, "core/projects.html")