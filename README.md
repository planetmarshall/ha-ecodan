ha-ecodan
=========

A [Home Assistant](https://www.home-assistant.io/)
integration for the [Mitsubishi Ecodan](https://les.mitsubishielectric.co.uk/products/residential-heating/outdoor)
Heatpumps


pyecodan
--------

A client for interacting with the MELCloud service for controlling the heatpump.
The intention is for this to be replaced by a local controller as detailed by
@rbroker in [ecodan-ha-local](https://github.com/rbroker/ecodan-ha-local)


Development
-----------

Development is based on [HACS](https://hacs.xyz/docs/categories/integrations/)

### Testing

A Dockerfile is provided for testing in an isolated Home Assistant instance.

```
docker build . -t hass
docker run --rm -it -p 8123:8123 -v ${PWD}:/hass /bin/bash

$ source /opt/hass/core/venv/bin activate
$ ./scripts/develop
```

Then open a web browser at `http://localhost:8123`


See Also
--------

Home Assistant Core includes a mature integration using MELCloud with support for
heat pumps and air conditioners, however the underlying Python library (`pymelcloud`)
is no longer under active development.
