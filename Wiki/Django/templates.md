#### Custom Tags
To create custom tags, create a folder named `templatetags` and place your custom tag python file here, user register from `template.Library()` 
to register your tag, django provdies two decorator methods to register `tag simple_tag` (Processes the data and returns a string)
& `inclusion_tag` (Processes the data and returns a rendered template)
```shell
@register.simple_tag
def total_posts():
    return Post.publisher.count()
```
The above code will register tag as simple tag and `total_posts` will be the name of the tag, if you want to change the name pass it 
in simple_tag decorator, i.e `@register.simple_tag(name="my_tag")`. Custom tags should be loaded using `{% load file_name_of_tags %}`.
Inclusion tags have to return a dictionary of values, which is used as the context to render the specified template.