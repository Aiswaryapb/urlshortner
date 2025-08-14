import random, string
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import ShortURL

def _generate_code(length=6):
    alphabet = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(alphabet, k=length))
        if not ShortURL.objects.filter(code=code).exists():
            return code

def home(request):
    short_url = None
    error = None

    if request.method == "POST":
        original = (request.POST.get("url") or "").strip()
        custom = (request.POST.get("custom") or "").strip()

        if not original:
            error = "Please enter a URL."
        else:
            # Make sure scheme exists so redirects work
            if not original.startswith(("http://", "https://")):
                original = "http://" + original

            # Use custom code if provided and unique
            if custom:
                if ShortURL.objects.filter(code=custom).exists():
                    error = "This custom code is already taken."
                    custom = None
                code = custom
            else:
                code = _generate_code()

            if not error:
                # If same URL exists and no custom provided, reuse it
                obj = ShortURL.objects.filter(original_url=original).first()
                if obj and not custom:
                    pass
                else:
                    obj = ShortURL.objects.create(original_url=original, code=code)

                short_url = request.build_absolute_uri(reverse("go", args=[obj.code]))

    return render(request, "home.html", {"short_url": short_url, "error": error})

def go(request, code: str):
    link = get_object_or_404(ShortURL, code=code)
    ShortURL.objects.filter(pk=link.pk).update(clicks=F("clicks") + 1)
    return redirect(link.original_url)
