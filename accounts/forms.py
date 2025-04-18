from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "email",
            "job",
            "gender",
        ]

    def init(self, args, **kwargs):
        super().init(args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )

        self.fields["gender"].widget.attrs.update({"class": "form-select"})
        self.fields["job"].widget.attrs.update({"class": "form-select"})
