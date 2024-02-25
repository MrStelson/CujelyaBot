from .start_admin import admin_start_router
from .add_feedback import admin_add_feedback_router
from .show_feedbacks import admin_show_feedback_router
from .delete_feedback import admin_delete_feedback_router
from .update_status import admin_update_feedback_router

admin_routers = [
    admin_start_router,
    admin_add_feedback_router,
    admin_show_feedback_router,
    admin_delete_feedback_router,
    admin_update_feedback_router,
]
