from lebonplantapi.adapters.database import (
    CommentRepository,
    PostRepository,
    ProductRepository,
    UserRepository,
)


user_repository = UserRepository()
product_repository = ProductRepository()
post_repository = PostRepository()
comment_repository = CommentRepository()
