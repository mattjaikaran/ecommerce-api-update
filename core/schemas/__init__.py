from .address_schema import (
    AddressCreateSchema,
    AddressSchema,
)
from .auth_schema import (
    PasswordlessLoginRequest,
    PasswordlessLoginVerify,
)
from .customer_schema import (
    CustomerCreateSchema,
    CustomerSchema,
    CustomerUpdateSchema,
)
from .feedback_schema import (
    CustomerFeedbackCreateSchema,
    CustomerFeedbackSchema,
)
from .user_schema import (
    UserLoginSchema,
    UserLogoutSchema,
    UserSchema,
    UserSignupSchema,
    UserUpdateSchema,
)

all = [
    UserSchema,
    UserSignupSchema,
    UserLoginSchema,
    UserLogoutSchema,
    PasswordlessLoginRequest,
    PasswordlessLoginVerify,
    UserUpdateSchema,
    AddressSchema,
    AddressCreateSchema,
    CustomerFeedbackSchema,
    CustomerFeedbackCreateSchema,
    CustomerSchema,
    CustomerCreateSchema,
    CustomerUpdateSchema,
]
