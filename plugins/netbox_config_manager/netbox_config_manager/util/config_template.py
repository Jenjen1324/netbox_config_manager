import re

import jinja2
from netaddr.ip import IPNetwork


def _regex_replace(subject: str, search: str, replace: str):
    return re.sub(re.compile(search), replace, subject)


def _cisco_iface(subject: str):
    parts = re.match(r'^([A-Za-z]+)(.+)$', subject)
    return {
        'class': parts.group(1),
        'number': parts.group(2)
    }


def _ip(address):
    return IPNetwork(address)


def render_template(template_content: str, context_data, filter_empty=True):
    env = jinja2.Environment()

    env.filters['regex_replace'] = _regex_replace
    env.filters['cisco_iface'] = _cisco_iface
    env.filters['ip'] = _ip

    tmpl = env.from_string(template_content)
    data = tmpl.render(**context_data)
    if filter_empty:
        # Filter empty lines
        data = "\n".join(filter(lambda x: not re.match(r'^\s*$', x), data.split('\n')))
    return data
