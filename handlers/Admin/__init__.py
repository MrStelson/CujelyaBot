from .start_admin import admin_start_router
from .add_feedback import admin_add_feedback_router
from .show_feedbacks import admin_show_feedback_router
from .delete_feedback import admin_delete_feedback_router
from .update_status import admin_update_feedback_router
from .get_all_users import admin_get_all_users_router
from .change_img_size import admin_change_img_size

admin_routers = [
    admin_start_router,
    admin_add_feedback_router,
    admin_show_feedback_router,
    admin_delete_feedback_router,
    admin_update_feedback_router,
    admin_get_all_users_router,
    admin_change_img_size,
]
