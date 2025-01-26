from django.shortcuts import render, get_object_or_404, redirect
from base.models import Chapter, ChapterName, Region, CountryData, CityData, StateData
from uuid import uuid4

def chapter_list(request):
    chapters = Chapter.objects.all()
    return render(request, 'custom_admin/chapter/chapter/chapter_list.html', {'chapters': chapters})

def chapter_create(request):
    if request.method == 'POST':
        name_id = request.POST.get('name')
        region_id = request.POST.get('region')
        country_id = request.POST.get('country')
        city_id = request.POST.get('city')
        chapter_type = request.POST.get('type')
        day = request.POST.get('day')

        name = get_object_or_404(ChapterName, id=name_id)
        region = get_object_or_404(Region, id=region_id)
        country = get_object_or_404(CountryData, id=country_id)
        city = get_object_or_404(CityData, id=city_id)

        Chapter.objects.create(
            id=uuid4(),
            name=name,
            region=region,
            country=country,
            city=city,
            type=chapter_type,
            day=day
        )
        return redirect('chapter_list')
    else:
        names = ChapterName.objects.all()
        regions = Region.objects.all()
        countries = CountryData.objects.all()
        cities = CityData.objects.all()
        return render(request, 'custom_admin/chapter/chapter/chapter_form.html', {
            'names': names, 'regions': regions, 'countries': countries, 'cities': cities
        })

def chapter_edit(request, pk):
    chapter = get_object_or_404(Chapter, id=pk)
    if request.method == 'POST':
        name_id = request.POST.get('name')
        region_id = request.POST.get('region')
        country_id = request.POST.get('country')
        city_id = request.POST.get('city')
        chapter_type = request.POST.get('type')
        day = request.POST.get('day')

        chapter.name = get_object_or_404(ChapterName, id=name_id)
        chapter.region = get_object_or_404(Region, id=region_id)
        chapter.country = get_object_or_404(CountryData, id=country_id)
        chapter.city = get_object_or_404(CityData, id=city_id)
        chapter.type = chapter_type
        chapter.day = day
        chapter.save()

        return redirect('chapter_list')
    else:
        names = ChapterName.objects.all()
        regions = Region.objects.all()
        countries = CountryData.objects.all()
        cities = CityData.objects.all()
        return render(request, 'custom_admin/chapter/chapter/chapter_form.html', {
            'chapter': chapter, 'names': names, 'regions': regions, 'countries': countries, 'cities': cities
        })

def chapter_delete(request, pk):
    chapter = get_object_or_404(Chapter, id=pk)
    if request.method == 'POST':
        chapter.delete()
        return redirect('chapter_list')  # Redirect to the list view after deletion
    return render(request, 'custom_admin/chapter/chapter/chapter_confirm_delete.html', {'chapter': chapter})