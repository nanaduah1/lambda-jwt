import graphene

from auth.common import SuccessErrorMutationMixin
from auth.queries import UserObject
from auth.services import AUTH_TOKEN
from auth.services import UserAccountService


class ObtainJwt(graphene.Mutation, SuccessErrorMutationMixin):
    class Arguments:
        username = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserObject)
    access_token = graphene.String()

    def mutate(cls, obj, info, username: str, password: str):
        account_service = UserAccountService()
        result = account_service.authenticate(username, password)
        if not result.success:
            return cls(
                success=result.success,
                error_code=result.error_code,
                message="Invalid username or password",
            )

        else:
            access_token = account_service.generate_token(result.data, AUTH_TOKEN)
            return cls(
                success=result.success,
                user=result.data,
                access_token=access_token,
            )


class VerifyAccount(graphene.Mutation, SuccessErrorMutationMixin):
    class Arguments:
        username = graphene.String()
        token = graphene.String()

    user = graphene.Field(UserObject)
    password_token = graphene.String(required=False)

    @classmethod
    def mutate(cls, parent, info, username: str, token: str):
        account_service = UserAccountService()
        v_result = account_service.verify_account(token=token, username=username)
        return cls(
            success=v_result.success,
            error_code=v_result.error_code,
            message=v_result.message,
            **(v_result.data or {}),
        )


class SetPassword(graphene.Mutation, SuccessErrorMutationMixin):
    class Arguments:
        username = graphene.String()
        token = graphene.String()
        password = graphene.String()

    @classmethod
    def mutate(cls, parent, info, username: str, token: str, password: str):
        account_service = UserAccountService()
        result = account_service.set_password(
            token=token, username=username, password=password
        )
        return cls(
            success=result.success,
            error_code=result.error_code,
            message=result.message,
        )


class AuthMutation(graphene.ObjectType):
    token_auth = ObtainJwt.Field()
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field()
    # verify_account = VerifyAccount.Field()
    # set_password = SetPassword.Field()
