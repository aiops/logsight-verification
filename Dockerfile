# docker build -t logsight/logsight-result-api .

# set base image (host OS)
FROM python:3.9-slim

ENV LDFLAGS="-L/usr/lib/x86_64-linux-gnu"
ENV CFLAGS="-I/usr/include"

# set the working directory in the container
WORKDIR /code
COPY ./main.py .
COPY ./utils.py .
# install dependencieshttps://github.com/user/repository/archive/branch.zip
RUN pip install --no-cache-dir PyGithub https://github.com/aiops/logsight-sdk-py/archive/demo.zip

#
## copy code
#COPY ../logsight-verification-action .
#COPY ../logsight-verification-action/entrypoint.sh /
#RUN chmod +x /entrypoint.sh
#
## Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["python3", "./main.py"]
