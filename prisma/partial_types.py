from prisma.models import User

# user with only email and name
User.create_partial('UserInLogin', include={'email', 'name'})

# user with a non-optional email field
User.create_partial('UserWithEmail', required={'email'})

# normal user model without an email
User.create_partial('UserWithoutEmail', exclude={'email'})

# user with a non-optional profile
# User.create_partial('UserWithProfile', required={'profile'})

# user with an optional name
User.create_partial('UserWithOptionalName', optional={'name'})

# user without any relational fields (in this case without the profile and posts fields)
User.create_partial('UserWithoutRelations', exclude_relational_fields=True)
