from .address import (
    AddressCreateSchema,
    AddressSchema,
)
from .auth import (
    PasswordlessLoginRequest,
    PasswordlessLoginVerify,
)
from .customer import (
    CustomerCreateSchema,
    CustomerSchema,
    CustomerUpdateSchema,
)
from .feedback import (
    CustomerFeedbackCreateSchema,
    CustomerFeedbackSchema,
)
from .users import (
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
