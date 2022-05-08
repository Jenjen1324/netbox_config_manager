ARG VERSION=latest
FROM netboxcommunity/netbox:$VERSION

ENV UID=1000
ENV GID=1000

# For development
RUN addgroup -g $GID -S netbox && adduser -S netbox -G netbox --uid $UID

RUN chown $UID:$GID -R /opt/netbox
RUN chown $UID:$GID -R /opt/unit
USER $UID

## Activate venv
ENV VIRTUAL_ENV=/opt/netbox/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

## Install extra dev requirements
COPY ./requirements.txt /opt/netbox
RUN pip install --no-warn-script-location -r /opt/netbox/requirements.txt

## Add configuration file
COPY --chown=$UID:$GID ./netbox_config.py /etc/netbox/config/extra.py

## Setup plugins
COPY --chown=$UID:$GID ./plugins /opt/netbox/plugins
COPY --chown=$UID:$GID ./docker/install_plugins.sh /opt/netbox

RUN cd /opt/netbox && bash /opt/netbox/install_plugins.sh


COPY --chown=$UID:$GID ./netbox/netbox/extras/plugins/urls.py /opt/netbox/netbox/extras/plugins/urls.py