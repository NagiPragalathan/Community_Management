from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from base.models import ChapterMemberPosition, ChapterPosition, Chapter, User

# List all ChapterMemberPosition entries
def list_chapter_member_positions(request):
    chapter_member_positions = ChapterMemberPosition.objects.all()
    return render(request, 'custom_admin/chapter/chapter_member_positions/chapter_member_positions_list.html', {'chapter_member_positions': chapter_member_positions})

# Create a new ChapterMemberPosition
def create_chapter_member_position(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        position_id = request.POST.get('position')
        chapter_id = request.POST.get('chapter')

        user = get_object_or_404(User, id=user_id)
        position = get_object_or_404(ChapterPosition, id=position_id)
        chapter = get_object_or_404(Chapter, id=chapter_id)

        ChapterMemberPosition.objects.create(user=user, position=position, chapter=chapter)
        return redirect('list_chapter_member_positions')

    users = User.objects.all()
    positions = ChapterPosition.objects.all()
    chapters = Chapter.objects.all()
    return render(request, 'custom_admin/chapter/chapter_member_positions/chapter_member_positions_create.html', {'users': users, 'positions': positions, 'chapters': chapters})

# Edit an existing ChapterMemberPosition
def edit_chapter_member_position(request, id):
    chapter_member_position = get_object_or_404(ChapterMemberPosition, id=id)

    if request.method == 'POST':
        user_id = request.POST.get('user')
        position_id = request.POST.get('position')
        chapter_id = request.POST.get('chapter')

        user = get_object_or_404(User, id=user_id)
        position = get_object_or_404(ChapterPosition, id=position_id)
        chapter = get_object_or_404(Chapter, id=chapter_id)

        chapter_member_position.user = user
        chapter_member_position.position = position
        chapter_member_position.chapter = chapter
        chapter_member_position.save()

        return redirect('list_chapter_member_positions')

    users = User.objects.all()
    positions = ChapterPosition.objects.all()
    chapters = Chapter.objects.all()
    return render(request, 'custom_admin/chapter/chapter_member_positions/chapter_member_positions_edit.html', {
        'chapter_member_position': chapter_member_position,
        'users': users,
        'positions': positions,
        'chapters': chapters
    })

# Delete a ChapterMemberPosition
def delete_chapter_member_position(request, id):
    chapter_member_position = get_object_or_404(ChapterMemberPosition, id=id)
    chapter_member_position.delete()
    return redirect('list_chapter_member_positions')
