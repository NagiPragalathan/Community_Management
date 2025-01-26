from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from base.models import MainProfile, ChapterName
from datetime import datetime

def profile_view(request, pk=None):
    profile = None
    if pk:
        profile = get_object_or_404(MainProfile, pk=pk)

    if request.method == "POST":
        data = request.POST
        if profile is None:
            profile = MainProfile()

        # Assign fields
        profile.user = User.objects.get(id=data.get("user"))
        profile.title = data.get("title")
        profile.first_name = data.get("first_name")
        profile.last_name = data.get("last_name")
        profile.suffix = data.get("suffix")
        profile.display_name = data.get("display_name")
        profile.gender = data.get("gender")
        profile.company_name = data.get("company_name")
        profile.product_service_description = data.get("product_service_description")
        profile.gst_registered_state = data.get("gst_registered_state")
        profile.gst_identification_number_or_pan = data.get("gst_identification_number_or_pan")
        profile.industry = data.get("industry")
        profile.classification = data.get("classification")
        profile.requested_speciality = data.get("requested_speciality")
        profile.membership_status = data.get("membership_status")

        # Convert renewal_due_date from string to datetime.date
        renewal_due_date = data.get("renewal_due_date")
        if renewal_due_date:
            profile.renewal_due_date = datetime.strptime(renewal_due_date, "%Y-%m-%d").date()

        chapter_id = data.get("Chapter")
        if chapter_id:
            profile.Chapter = ChapterName.objects.get(id=chapter_id)

        profile.my_business = data.get("my_business")
        profile.keywords = data.get("keywords")

        profile.save()
        return redirect("profile-edit", pk=profile.pk)

    # Pass users and chapters to the template
    users = User.objects.all()
    chapters = ChapterName.objects.all()

    return render(request, "custom_admin/chapter/profile/profile_form.html", {
        "profile": profile,
        "users": users,
        "chapters": chapters,
    })
