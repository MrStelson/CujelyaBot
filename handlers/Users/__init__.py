from .contacts import user_contracts_router
from .help import user_help_router
from .start import user_start_router
from .questions import user_questions_router
from .resume import user_resume_router
from .feedback import user_feedback_router

user_routers = [
    user_contracts_router,
    user_help_router,
    user_start_router,
    user_questions_router,
    user_resume_router,
    user_feedback_router,
]
