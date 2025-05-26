ARG VARIANT=2.4.0-latest
FROM checkmk/check-mk-cloud:${VARIANT}

EXPOSE 5000

RUN /docker-entrypoint.sh /bin/true

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends nodejs gcc

ADD requirements.txt /tmp/requirements.txt
USER cmk
RUN PATH="/omd/sites/cmk/bin:${PATH}" \
    OMD_ROOT="/omd/sites/cmk" \
    /omd/sites/cmk/bin/pip3 install \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --index-url https://pypi.org/simple \
    --cert /etc/ssl/certs/ca-certificates.crt \
    -r /tmp/requirements.txt

ENTRYPOINT ["/bin/bash"]
