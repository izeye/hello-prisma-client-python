import asyncio
from prisma import Prisma
from prisma.partials import UserInLogin


async def main() -> None:
    db = Prisma()
    await db.connect()

    post = await db.post.create(
        {
            'title': 'Hello from prisma!',
            'desc': 'Prisma is a database toolkit and makes databases easy.',
            'published': True,
        }
    )
    print(f'created post: {post.json(indent=2, sort_keys=True)}')

    found = await db.post.find_unique(where={'id': post.id})
    assert found is not None
    print(f'found post: {found.json(indent=2, sort_keys=True)}')

    post = await db.post.create({
        'title': 'My new post',
        'published': True,
    })
    print(f'post: {post.json(indent=2)}\n')

    first = await db.comment.create({
        'content': 'First comment',
        'post': {
            'connect': {
                'id': post.id,
            },
        },
    })
    print(f'first comment: {first.json(indent=2)}\n')

    second = await db.comment.create({
        'content': 'Second comment',
        'post': {
            'connect': {
                'id': post.id,
            },
        },
    })
    print(f'second comment: {second.json(indent=2)}\n')

    first = await db.comment.create(
        data={
            'content': 'First comment',
            'post': {
                'create': {
                    'title': 'My new post',
                    'published': True,
                },
            },
        },
        include={'post': True}
    )
    second = await db.comment.create({
        'content': 'Second comment',
        'post': {
            'connect': {
                'id': first.post.id
            }
        }
    })

    # find all comments on a post
    comments = await db.comment.find_many(
        where={
            'post_id': post.id
        }
    )
    print(f'comments of post with id {post.id}')
    for comment in comments:
        print(comment.json(indent=2))

    # find at most 3 comments on a post
    filtered = await db.comment.find_many(
        where={
            'post_id': post.id
        },
        take=3
    )
    print(f'filtered comments of post with id {post.id}')
    for comment in filtered:
        print(comment.json(indent=2))

    post = await db.post.find_unique(
        where={
            'id': post.id,
        },
        include={
            'comments': {
                'take': 3,
            },
        },
    )
    print(post)

    user = await db.query_first(
        'SELECT name, email FROM User WHERE id = ?',
        'abc',
        model=UserInLogin,
    )
    if user is None:
        print('Did not find user')
    else:
        print(f'Found user: name={user.name}, email={user.email}')

    await db.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
