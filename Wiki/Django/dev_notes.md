### Nested Apps
When creating nested apps, you need to update app name in `apps.py`, by default Django sets the default app name, but it should be edited 
full path info should be added here. i.e if an app named `digital` is created inside a container folder called custom_apps, then app name 
in apps.py should say `name = 'custom_apps.digital'`