from django.shortcuts import render, redirect, get_object_or_404
from base.models import ChapterName

# List View
def chapter_name_list(request):
    chapters = ChapterName.objects.all()
    return render(request, 'custom_admin/chapter/chapter_name/chapter_list.html', {'chapters': chapters})

# Create View
def chapter_name_create(request):
    if request.method == 'POST':
        chapter_name = request.POST.get('chapter_name')
        if chapter_name:
            ChapterName.objects.create(chapter_name=chapter_name)
        return redirect('chapter_list')
    return render(request, 'custom_admin/chapter/chapter_name/chapter_create.html')

# Edit View
def chapter_name_edit(request, pk):
    chapter = get_object_or_404(ChapterName, pk=pk)
    if request.method == 'POST':
        chapter_name = request.POST.get('chapter_name')
        if chapter_name:
            chapter.chapter_name = chapter_name
            chapter.save()
        return redirect('chapter_list')
    return render(request, 'custom_admin/chapter/chapter_name/chapter_edit.html', {'chapter': chapter})

# Delete View
def chapter_name_delete(request, pk):
    chapter = get_object_or_404(ChapterName, pk=pk)
    if request.method == 'POST':
        chapter.delete()
        return redirect('chapter_list')
    return render(request, 'custom_admin/chapter/chapter_name/chapter_delete.html', {'chapter': chapter})
