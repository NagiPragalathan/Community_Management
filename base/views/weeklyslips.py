# views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from base.models import WeeklySlip

@login_required
def weekly_slips(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date and to_date:
            from_date = parse_date(from_date)
            to_date = parse_date(to_date)
            weekly_slips = WeeklySlip.objects.filter(
                user=request.user,
                from_date__gte=from_date,
                to_date__lte=to_date
            )
        else:
            weekly_slips = WeeklySlip.objects.filter(user=request.user)

        return render(request, 'weeklyslips/weeklyslips.html', {
            'weekly_slips': weekly_slips,
            'from_date': from_date,
            'to_date': to_date
        })
    else:
        return render(request, 'weeklyslips/weeklyslips.html')
