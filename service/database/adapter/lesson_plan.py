from . import DBAdapter
from ..firebase.lesson_plan.get_lesson_plan_from_firebase import get_lesson_plan_from_firebase
from ..firebase.lesson_plan.update_lesson_plan_to_firebase import update_lesson_plan_to_firebase

class LessonPlan(DBAdapter):

    def read_lesson_plan(self):
        lesson_plan = get_lesson_plan_from_firebase(self.chat_id, self.language)
        return lesson_plan

    def update_lesson_plan(self, lesson_plan: dict):
        update_lesson_plan_to_firebase(self.chat_id, self.language, lesson_plan)
