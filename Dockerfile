FROM python:3
RUN mkdir -p /tmp/vmtauto
WORKDIR /tmp/vmtauto
COPY ./requirements.txt /tmp/vmtauto
COPY ./Config.py /tmp/vmtauto
COPY ./vmt_autoupdate.py /tmp/vmtauto
COPY ./AVAXAPI.py /tmp/vmtauto

RUN pip install --no-cache-dir -r /tmp/vmtauto/requirements.txt

CMD [ "python", "/tmp/vmtauto/vmt_autoupdate.py" ]
