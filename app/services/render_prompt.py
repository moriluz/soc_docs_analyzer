from jinja2 import FileSystemLoader, Environment


def render_prompt(template_name):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)

    return template.render()
