from django.shortcuts import render
from profiles.models import Profile
from profiles.models import Profile
from .filters import ProfileFilter, GenderlessProfileFilter
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Поиск людей по указанным фильтрам
@login_required
def search(request):
    min_height = request.GET.get('height_min')
    max_height = request.GET.get('height_max')

    user_gender = "MALE" if request.user.profile.gender == "MALE" else "FEMALE"
    qs = Profile.objects.filter(Q(looking_for=user_gender)).exclude(user_id=request.user.id)

    sexuality_query = Q()
    sexuality_query.add(~Q(looking_for=F('gender')), Q.AND)
    qs = qs.filter(sexuality_query)

    if min_height:
        qs = qs.filter(height__gte=min_height)
    if max_height:
        qs = qs.filter(height__lte=max_height)

    gender_check = "MALE" if request.user.profile.looking_for == "MALE" else "FEMALE"
    qs = qs.filter(gender=gender_check)
    filtered_result = GenderlessProfileFilter(request.GET, queryset=qs)

    search_paginated = Paginator(filtered_result.qs, 1)
    try:
        search_page = search_paginated.page(request.GET.get('page'))
    except PageNotAnInteger:
        search_page = search_paginated.page(1)
    except EmptyPage:
        search_page = search_paginated.page(search_paginated.num_pages)

    context = {
        'filtered_result': filtered_result,
        'search_page': search_page,
        'min_height': min_height,
        'max_height': max_height,
    }
    return render(request, 'search.html', context)
