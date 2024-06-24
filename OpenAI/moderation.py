from django.conf import settings
from openai import OpenAI

from accounts.models import Penalty


def content_check(input: str):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.moderations.create(input=input)
    categories = response.results[0].categories
    categories_dict = {
        'hate/threatening': categories.hate_threatening,
        'self-harm/instructions': categories.self_harm_instructions,
        'harassment/threatening': categories.harassment_threatening
    }
    block = any(categories_dict[cat] for cat in categories_dict)
    categories_to_increase = [cat for cat, flagged in categories_dict.items() if flagged]

    return {'block': block, 'categories': categories_to_increase}


def increase_penalty_count(user, categories):
    for category in categories:
        simplified_category = category.split('/')[0] if category in ['hate/threatening', 'self-harm/instructions', 'harassment/threatening'] else category
        penalty, _ = Penalty.objects.get_or_create(user=user, category=simplified_category)
        penalty.count += 1
        penalty.save()

        if penalty.count >= 25 and simplified_category != category:
            penalty.count = 0
            penalty.save()
            red_penalty, _ = Penalty.objects.get_or_create(user=user, category=f'{category}/threatening')
            red_penalty.count += 1
            red_penalty.save()