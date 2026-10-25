from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.test import TestCase
from django.urls import reverse

from .models import PasswordResetRequest, PendingRegistration

User = get_user_model()


class RegistrationFlowTests(TestCase):
    @patch("accounts.views.secrets.randbelow", return_value=0)
    def test_signup_stores_pending_registration_in_database(self, _randbelow):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "newuser",
                "first_name": "New",
                "last_name": "User",
                "phone_number": "09123456789",
                "password1": "StrongPassword!456",
                "password2": "StrongPassword!456",
            },
        )

        pending = PendingRegistration.objects.get(username="newuser")
        self.assertRedirects(
            response,
            reverse("accounts:verify_email", kwargs={"token": pending.token}),
        )
        self.assertTrue(check_password("100000", pending.code))
        self.assertTrue(check_password("StrongPassword!456", pending.password))
        self.assertFalse(User.objects.filter(username="newuser").exists())
        self.assertFalse(
            any(key.startswith("signup_") for key in self.client.session.keys())
        )

    def test_verification_creates_user_from_pending_registration(self):
        password = "StrongPassword!456"
        pending = PendingRegistration.objects.create(
            username="verifieduser",
            first_name="Verified",
            last_name="User",
            phone_number="09123456789",
            password=make_password(password),
            code=make_password("123456"),
        )
        response = self.client.post(
            reverse("accounts:verify_email", kwargs={"token": pending.token}),
            {f"code{index + 1}": digit for index, digit in enumerate("123456")},
        )

        self.assertRedirects(response, reverse("accounts:login"))
        user = User.objects.get(username="verifieduser")
        self.assertTrue(user.check_password(password))
        self.assertFalse(PendingRegistration.objects.filter(pk=pending.pk).exists())

    def test_invalid_code_increments_database_attempt_count(self):
        pending = PendingRegistration.objects.create(
            username="pendinguser",
            phone_number="09123456789",
            password=make_password("StrongPassword!456"),
            code=make_password("123456"),
        )

        response = self.client.post(
            reverse("accounts:verify_email", kwargs={"token": pending.token}),
            {f"code{index + 1}": digit for index, digit in enumerate("000000")},
        )

        pending.refresh_from_db()
        self.assertEqual(pending.attempts, 1)
        self.assertContains(response, "کد تأیید اشتباه است.")


class PasswordResetFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="resetuser",
            phone_number="09123456789",
            password="OldPassword!456",
        )

    @patch("accounts.views.secrets.randbelow", return_value=12)
    def test_forgot_password_creates_database_request(self, _randbelow):
        response = self.client.post(
            reverse("accounts:forgot_password"),
            {"phone_number": self.user.phone_number},
        )

        reset_request = PasswordResetRequest.objects.get(user=self.user)
        self.assertRedirects(
            response,
            reverse(
                "accounts:verify_forgot_password",
                kwargs={"token": reset_request.token},
            ),
        )
        self.assertTrue(check_password("100012", reset_request.code))
        self.assertFalse(
            any(key.startswith("forgot_") for key in self.client.session.keys())
        )

    def test_valid_code_changes_password_and_removes_request(self):
        reset_request = PasswordResetRequest.objects.create(
            user=self.user,
            code=make_password("123456"),
        )
        response = self.client.post(
            reverse(
                "accounts:verify_forgot_password",
                kwargs={"token": reset_request.token},
            ),
            {
                **{f"code{index + 1}": digit for index, digit in enumerate("123456")},
                "new_password1": "BrandNewPassword!789",
                "new_password2": "BrandNewPassword!789",
            },
        )

        self.assertRedirects(response, reverse("accounts:profile"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("BrandNewPassword!789"))
        self.assertFalse(
            PasswordResetRequest.objects.filter(pk=reset_request.pk).exists()
        )
        self.assertEqual(
            self.client.session["_auth_user_id"],
            str(self.user.pk),
        )

    def test_invalid_code_increments_attempts_without_changing_password(self):
        reset_request = PasswordResetRequest.objects.create(
            user=self.user,
            code=make_password("123456"),
        )
        response = self.client.post(
            reverse(
                "accounts:verify_forgot_password",
                kwargs={"token": reset_request.token},
            ),
            {
                **{f"code{index + 1}": digit for index, digit in enumerate("000000")},
                "new_password1": "BrandNewPassword!789",
                "new_password2": "BrandNewPassword!789",
            },
        )

        reset_request.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(reset_request.attempts, 1)
        self.assertTrue(self.user.check_password("OldPassword!456"))
        self.assertContains(response, "کد وارد شده اشتباه است.")

# Create your tests here.
