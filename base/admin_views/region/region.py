from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from base.models import Region, StateData, CountryData, CityData, RegionMemberPosition


# List all Regions
def region_list(request):
    regions = Region.objects.all()  # Fetch all regions from the database
    for i in regions:
        print(i.region_name, i.state.state_name, i.country.country_name, i.city.city_name)
    return render(
        request,
        "custom_admin/region/region/region_list.html",  # Replace with your actual template
        {"regions": regions},
    )


# Create a Region
def create_region(request):
    if request.method == "POST":
        region_name = request.POST.get("region_name")
        state_id = request.POST.get("state")
        country_id = request.POST.get("country")
        city_id = request.POST.get("city")

        state = get_object_or_404(StateData, id=state_id)
        country = get_object_or_404(CountryData, id=country_id)
        city = get_object_or_404(CityData, id=city_id)

        # Create a new Region without setting member_positions
        region = Region(
            region_name=region_name,
            state=state,
            country=country,
            city=city,
        )
        region.save()
        return redirect("region_list")  # Redirect to list view

    states = StateData.objects.all()
    countries = CountryData.objects.all()
    cities = CityData.objects.all()
    return render(
        request,
        "custom_admin/region/region/create_region.html",  # Replace with your actual template
        {
            "states": states,
            "countries": countries,
            "cities": cities,
        },
    )


def update_region(request, region_id):
    region = get_object_or_404(Region, id=region_id)
    if request.method == "POST":
        region.region_name = request.POST.get("region_name")
        state_id = request.POST.get("state")
        country_id = request.POST.get("country")
        city_id = request.POST.get("city")

        region.state = get_object_or_404(StateData, id=state_id)
        region.country = get_object_or_404(CountryData, id=country_id)
        region.city = get_object_or_404(CityData, id=city_id)
        # Save the region without updating member_positions
        region.save()
        return redirect("region_list")  # Redirect to list view

    # Fetch context data
    states = StateData.objects.all()
    countries = CountryData.objects.all()
    cities = CityData.objects.all()

    return render(
        request,
        "custom_admin/region/region/update_region.html",
        {
            "region": region,
            "states": states,
            "countries": countries,
            "cities": cities,
        },
    )



# Delete a Region
def delete_region(request, region_id):
    region = get_object_or_404(Region, id=region_id)
    if request.method == "POST":
        region.delete()
        return redirect("region_list")  # Redirect to list view

    return render(
        request,
        "custom_admin/region/region/delete_region.html",  # Replace with your actual template
        {"region": region},
    )
