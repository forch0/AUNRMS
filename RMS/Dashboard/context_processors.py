from .sidebar_config import get_sidebar_items_for_role

def sidebar_context(request):
    """Context processor to add sidebar items based on the user's role."""
    return {
        'sidebar_items': get_sidebar_items_for_role(request.user)
    }


def get_navigation(user):
    """Generate the sidebar items dynamically based on the user's roles."""
    return get_sidebar_items_for_role(user)  # 
