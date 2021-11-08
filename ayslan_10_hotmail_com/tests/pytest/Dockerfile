FROM python:3.8-slim

# set the working directory in the container
WORKDIR /up9

# install dependencies
RUN pip3 install apiritif jsonpath_ng lxml pytest ddt

# copy the dependencies file to the working directory
ADD  data data
COPY authentication.py .
COPY tests.py .
COPY up9lib.py .

# command to run on container start
CMD [ "pytest", "tests.py" ]
