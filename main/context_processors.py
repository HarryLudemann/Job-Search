from register.models import Themes

# Checks theme
def CheckDarkTheme(response):
    obj = Themes.objects.all()
    if (obj.filter(userid=response.user.id).exists()):
        obj = obj.filter(userid=response.user.id)
        for item in obj:
            if (item.theme == "dark"):
                return 'dark'
            else:
                return 'light'
    else:
        return 'light'

def add_variable_to_context(request):
    Theme = CheckDarkTheme(request)
    return {
        'theme': Theme
    }
