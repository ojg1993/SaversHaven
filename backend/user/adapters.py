from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data
        # default fields
        user = super().save_user(request, user, form, False)
        # extra fields
        user_field(user, 'nickname', data.get('nickname') )
        user_field(user, 'first_name', data.get('first_name') )
        user_field(user, 'last_name', data.get('last_name') )
        user_field(user, 'phone_number', data.get('phone_number') )
        user.save()
        return user
