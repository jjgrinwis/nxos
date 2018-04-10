from jinja2 import Environment, FileSystemLoader

def create_config(dir, template, dict):
    # Create the jinja2 environment.
    # used trim_blocks so our for-loop in jinja template doesn't create whitespaces
    j2_env = Environment(loader=FileSystemLoader(dir),
                         trim_blocks=True)

    # now get template from our environment and render the dict into template
    try:
        return j2_env.get_template(template).render(dict)
    except:
        print "something went wrong!!!!"