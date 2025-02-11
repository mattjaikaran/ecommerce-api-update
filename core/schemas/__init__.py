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
    FeedbackSchema,
    FeedbackCreateSchema,
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
    FeedbackSchema,
    FeedbackCreateSchema,
]
