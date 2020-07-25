FROM python:3.7-slim-stretch

WORKDIR /app/

# install dependencies
ADD ./requirements.txt /app/
RUN pip install -r /app/requirements.txt

# add code
ADD ./code/server/ /app/server/
ADD ./code/client/ /app/client/

# add shared code
ENV PYTHONPATH "${PYTHONPATH}:/app/lib:/app/.generated"
ADD ./code/cos_helpers /app/lib/cos_helpers/
ADD ./.generated /app/.generated

WORKDIR /app/server
