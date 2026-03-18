from .hindi import hindi_lesson_plan
from .new import new_lesson_plan

def get_t0_lesson_plan_for_language(language):
    if language == "hindi":
        return hindi_lesson_plan
    if language == "italian":
        return hindi_lesson_plan
    if language == "spanish":
        return hindi_lesson_plan
    if language == "japanese":
        return new_lesson_plan
    return hindi_lesson_plan