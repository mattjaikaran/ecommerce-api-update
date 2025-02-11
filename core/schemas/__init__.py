from .users import (
    UserSchema,
    UserSignupSchema,
    UserLoginSchema,
    UserLogoutSchema,
    UserUpdateSchema,
)
from .auth import (
    PasswordlessLoginRequest,
    PasswordlessLoginVerify,
)
from .address import (
    AddressSchema,
    AddressCreateSchema,
)
from .feedback import (
    CustomerFeedbackSchema,
    CustomerFeedbackCreateSchema,
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
]
