import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect

from .models import Post, Comment

def api_like(request):
    """ This api function adds like/unlike by a user to the database
    and returns response containing
    1)request status
    2)like status
    3)number of likes on the post after refreshing it from database
    """
    jsonresponse = {'success':True}
    
    data = json.loads(request.body)
    like_status = data['likeStatus']
    user_id = data['userId']
    post_id = data['postId']

    post = Post.objects.get(id=post_id)
    user = User.objects.get(id=user_id)
    
    print(data)

    if like_status == 'Like':
        post.likes.add(user)
        likeStatus = 'Unlike'

    elif like_status == 'Unlike':
        post.likes.remove(user)
        likeStatus = 'Like'

    post_likes = post.likes.count()
    jsonresponse['likeStatus'] = likeStatus
    jsonresponse['post_likes'] = post_likes
    
    return JsonResponse(jsonresponse)


def api_comment(request):
    """ This API function takes comment, comment author and post
    stores it to database and returns updated list of comments 
    to reactively change the comments list using vue """
    data = json.loads(request.body)
    print(data)
    user_id = data['userId']
    post_id = data['postId']
    comment_text = data['comment']

    user = User.objects.get(id=user_id)
    post = Post.objects.get(id=post_id)

    Comment.objects.create(commentator=user, blog=post,
                           comment=comment_text)

    all_comments = post.comment_set.all().values()
    jsonresponse = {'success':True, 'all_comments': list(all_comments)}
    print('*'*10, "Success")
    return JsonResponse(jsonresponse)