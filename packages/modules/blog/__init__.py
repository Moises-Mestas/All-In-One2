from packages.modules.blog.module import Module
from packages.modules.blog.models import Category, Post

class BlogModule(Module):
    name = "Blog"
    slug = "blog"
    version = "1.0.0"
    description = "Sistema de blog con posts y categorías"
    icon = "article"
    is_system = True

    def get_models(self):
        from .models import Post, Category
        return [Post, Category]

    def get_schemas(self):
        from .schemas import PostSchema, CategorySchema
        return [PostSchema, CategorySchema]


blog_module = BlogModule()
