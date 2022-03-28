import json
from datetime import datetime
from datetime import timedelta
from typing import List

import jwt
from common import ServiceResult
from models import User

from auth.hasher import hasher
from auth.models import Group
from auth.models import UserGroup
from config import CONFIG
from config import SECRET_KEY

USER_ALREADY_EXISTS = "username_exists"
INVALID_AUTH_TOKEN = "invalid_auth_token"

AUTH_TOKEN = "auth"
ACCOUNT_VERIFICATION_TOKEN = "verify"

TOKEN_CONTEXTS = (AUTH_TOKEN, ACCOUNT_VERIFICATION_TOKEN)

HASH_ALGORITHM = "HS256"
TOKEN_EXPIRATION_SECONDS = CONFIG.get("JWT_EXPIRATION_SECONDS", 14400)


class UserAccountService:
    def create_account(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        roles: List[str] = None,
    ) -> ServiceResult:

        user, created = User.get_or_create(
            username=username,
            defaults=dict(
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=False,
            ),
        )

        if created:
            user.set_password(password)
            user.save()

        self.assign_roles(user, roles)

        error_code = None if created else USER_ALREADY_EXISTS
        message = "Created" if created else "Existing user loaded"
        return ServiceResult(
            success=created, data=user, message=message, error_code=error_code
        )

    def authenticate(self, username, password):
        """Find an active user with the given username and password"""

        user: User = (
            User.select()
            .where(User.username == username & User.is_active == True)
            .get()
        )

        if not user or not user.password:
            return ServiceResult()

        if not hasher.verify(password, user.password):
            # password given is incorrect
            return ServiceResult()

        # Username and password matched a user
        return ServiceResult(success=True, data=user)

    def generate_token(self, user: User, context: str):
        expires_at = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION_SECONDS)
        user_data = dict(
            username=user.username,
            user_id=user.id,
            context=context,
            expires_at=expires_at.isoformat(),
        )
        return jwt.encode(user_data, key=SECRET_KEY, algorithm=HASH_ALGORITHM)

    def authenticate_by_token(self, token: str) -> ServiceResult:
        user_data = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=HASH_ALGORITHM)
        try:
            expires_at = datetime.fromisoformat(user_data.pop("expires_at"))
            if expires_at <= datetime.utcnow():
                return ServiceResult()
            user = (
                User.select()
                .where(User.id == user_data.get("user_id") & User.is_active == True)
                .get()
            )

            if not user:
                return ServiceResult()

            return ServiceResult(success=True, data=user)
        except:
            return ServiceResult()

    def verify_account(self, token: str, username: str) -> ServiceResult:
        return ServiceResult()

    def set_password(self, token: str, username: str, password: str):
        return ServiceResult()

    def assign_roles(self, user: User, roles: List[str]):
        if not roles or not user:
            return

        for role in roles:
            group, _ = Group.get_or_create(name=role)
            UserGroup.get_or_create(user=user, group=group)
