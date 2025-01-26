from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from base.models import ChapterPosition
from django.utils.timezone import now

# List all ChapterPosition entries
def chapter_position_list(request):
    chapter_positions = ChapterPosition.objects.all()
    return render(request, 'custom_admin/chapter/chapter_position/chapter_position_list.html', {'chapter_positions': chapter_positions})

# Create a new ChapterPosition entry
def chapter_position_create(request):
    if request.method == "POST":
        chapter_position = request.POST.get('Chapterposition')
        is_chapter = request.POST.get('is_chapter') == 'on'
        ChapterPosition.objects.create(Chapterposition=chapter_position, is_chapter=is_chapter, lastupdateddate=now())
        return redirect('chapter_position_list')
    return render(request, 'custom_admin/chapter/chapter_position/chapter_position_form.html')

# Edit an existing ChapterPosition entry
def chapter_position_edit(request, pk):
    chapter_position = get_object_or_404(ChapterPosition, pk=pk)
    if request.method == "POST":
        chapter_position.Chapterposition = request.POST.get('Chapterposition')
        chapter_position.is_chapter = request.POST.get('is_chapter') == 'on'
        chapter_position.lastupdateddate = now()
        chapter_position.save()
        return redirect('chapter_position_list')
    return render(request, 'custom_admin/chapter/chapter_position/chapter_position_form.html', {'chapter_position': chapter_position})

# Delete a ChapterPosition entry
def chapter_position_delete(request, pk):
    chapter_position = get_object_or_404(ChapterPosition, pk=pk)
    if request.method == "POST":
        chapter_position.delete()
        return redirect('chapter_position_list')
    return render(request, 'custom_admin/chapter/chapter_position/chapter_position_confirm_delete.html', {'chapter_position': chapter_position})
