# Please change once all PR changes are final, so it reads from shankari/e-mission-server
# FROM shankari/e-mission-server:master_2024-02-10--19-38
FROM mukuflash03/e-mission-server:image-push-merge_2024-04-16--42-27

ENV DASH_DEBUG_MODE True
ENV SERVER_PORT 8050

# copy over setup files
WORKDIR /usr/src/app/dashboard_setup
COPY requirements.txt nrel_dash_components-0.0.1.tar.gz docker/setup.sh ./

# install requirements.txt
WORKDIR /usr/src/app
RUN bash -c "./dashboard_setup/setup.sh"

# copy over dashboard code
WORKDIR /usr/src/app/pages
COPY ./pages ./
WORKDIR /usr/src/app/utils
COPY ./utils ./
WORKDIR /usr/src/app
COPY app.py app_sidebar_collapsible.py globals.py globalsUpdater.py Procfile ./

WORKDIR /usr/src/app/assets
COPY assets/ ./
RUN mkdir qrcodes

# copy over test data
WORKDIR /usr/src/app/data
COPY data ./

# open listening port, this may be overridden in docker-compose file
EXPOSE ${SERVER_PORT}

# run the dashboard
WORKDIR /usr/src/app/dashboard_setup
COPY docker/start.sh ./
WORKDIR /usr/src/app
CMD ["/bin/bash", "/usr/src/app/dashboard_setup/start.sh"]
