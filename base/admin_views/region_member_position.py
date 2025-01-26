from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from base.models import User, RegionPosition, RegionMemberPosition

# Edit RegionMemberPosition
def edit_member_position(request, member_position_id):
    if request.method == "POST":
        member_position = get_object_or_404(RegionMemberPosition, id=member_position_id)
        user_id = request.POST.get("user_id")
        position_id = request.POST.get("position_id")

        # Update the RegionMemberPosition
        user = get_object_or_404(User, id=user_id)
        position = get_object_or_404(RegionPosition, id=position_id)
        member_position.user = user
        member_position.position = position
        member_position.save()

        return JsonResponse({
            "id": member_position.id,
            "user": str(user),
            "position": str(position)
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def manage_member_positions(request):
    if request.method == "POST":
        try:
            # Retrieve user and position from POST data
            user_id = request.POST.get("user_id")
            position_id = request.POST.get("position_id")

            # Fetch the user and position objects
            user = get_object_or_404(User, id=user_id)
            position = get_object_or_404(RegionPosition, id=position_id)

            # Create a new RegionMemberPosition
            member_position = RegionMemberPosition.objects.create(user=user, position=position)
            
            print(member_position.position)

            # Respond with success and the created data
            return JsonResponse({
                "id": str(member_position.id),
                "user": user.username,
                "position": position.RegionpositionName
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)


# Delete RegionMemberPosition
def delete_member_position(request, member_position_id):
    if request.method == "POST":
        member_position = get_object_or_404(RegionMemberPosition, id=member_position_id)
        member_position.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)