from dataclasses import dataclass

import graphene


class SuccessErrorMutationMixin:
    success = graphene.Boolean()
    message = graphene.String(required=False)
    error_code = graphene.String(required=False)


@dataclass
class ServiceResult:
    success: bool = False
    message: str = None
    error_code: str = None
    data: any = None
