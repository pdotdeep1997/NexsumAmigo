from .. import db
from service.database.in_memory.lesson_plans.adapter import get_t0_lesson_plan_for_language

COLLECTION_NAME = "nexsum_lesson_plan"

def get_lesson_plan_from_firebase(chat_id: str, language: str):
    doc_ref = db.collection(COLLECTION_NAME).document(str(chat_id))
    t0_lesson_plan = get_t0_lesson_plan_for_language(language=language)
    doc = doc_ref.get()
    language_plan_t0 = {
        "plan": [
            {**l, "count": 0} for l in t0_lesson_plan
        ],
        "current": 0
    }
    print(language_plan_t0)
    
    if doc.exists:
        print("Found smt")
        print(f"Document data: {doc.to_dict()}")
        all_language_plan = doc.to_dict()
        if language in all_language_plan:
            return all_language_plan.get(language)
        else:
            db.collection(COLLECTION_NAME).document(chat_id).update({
                language: language_plan_t0
            })
            return language_plan_t0
    else:
        db.collection(COLLECTION_NAME).document(chat_id).set({
            language: language_plan_t0
        })

        
        print("No such document!")
        return language_plan_t0