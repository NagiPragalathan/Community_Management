from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from base.models import MainProfile, ChapterName, Region, Chapter
from django.db.models import Q
from datetime import datetime

def profile_view(request, pk=None):
    profile = None
    if pk:
        profile = get_object_or_404(MainProfile, user=pk)

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

        # Assign the sponsor field
        sponsor_id = data.get("sponsor")
        if sponsor_id:
            profile.sponsor = User.objects.get(id=sponsor_id)

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

def profile_list_view(request):
    profiles = MainProfile.objects.all()  # Default: get all profiles
    chapters = Chapter.objects.all()
    regions = Region.objects.all()
    chapter_names = ChapterName.objects.all()

    chapter_filter = request.GET.get('chapter', None)
    region_filter = request.GET.get('region', None)
    search_query = request.GET.get('search', '').strip()

    # Apply chapter filter (manual filtering)
    if chapter_filter:
        temp = []
        for i in profiles:
            try:
                if str(i.Chapter.id) == str(chapter_filter):  # Comparing chapter id
                    temp.append(i)
            except Exception as e:
                print(f"Error while filtering chapter: {e}")
        profiles = temp
    
    # Apply region filter (filter by the region of the chapter, manual filtering)
    if region_filter:
        temp = []
        for profile in profiles:
            # Check if the chapter's region matches the selected region_filter
            try:
                chapter_name = ChapterName.objects.get(id=profile.Chapter.id)
                chapter = Chapter.objects.filter(name=chapter_name)
                for i in chapter:
                    if str(i.region.id) == str(region_filter):
                        temp.append(profile)
                        break
            except Exception as e:
                try:
                    print(profile.Chapter.chapter_name)
                    print(ChapterName.objects.get(id=profile.Chapter.id).chapter_name)
                except Exception as e:
                    print(f"Error while filtering region: {e}", profile)
        profiles = temp

    # Apply search query filter (Django ORM way)
    if search_query:
        profiles = profiles.filter(
            Q(display_name__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    # Render the filtered profiles
    return render(request, "custom_admin/chapter/profile/profile_list.html", {
        "profiles": profiles,
        "chapters": chapters,
        "chapter_names": chapter_names,
        "regions": regions,
        "search_query": search_query,
        "chapter_filter": chapter_filter,
        "region_filter": region_filter,
    })
