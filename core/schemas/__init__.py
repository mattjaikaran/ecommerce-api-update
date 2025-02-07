from .users import (
    UserSchema,
    UserSignupSchema,
    UserLoginSchema,
    UserLogoutSchema,
    UserUpdateSchema,
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
    UserUpdateSchema,
    AddressSchema,
    AddressCreateSchema,
    FeedbackSchema,
    FeedbackCreateSchema,
]
