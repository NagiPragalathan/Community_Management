from django.shortcuts import render

def ViewReports(request):
    return render(request, "Reports/Reportsview.html")

def Report(request):
    return render(request, "Reports/Report.html")

