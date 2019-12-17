from django.http import JsonResponse
from rest_framework.parsers import JSONParser


def test(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':# 这里应该是model对应的所有字段
        # 返回
        return JsonResponse({'data': ['1', '2'], 'status': 1}, safe=False)

