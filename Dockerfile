# Use the official Python image as the base image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /APITestProject
WORKDIR /gorestapiautomation

# Copy the current directory contents into the container at /APITestProject
COPY . /gorestapiautomation

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenJDK (try default-jre)
RUN apt-get update && apt-get install -y default-jre


# Install Allure command line
RUN apt-get update && apt-get install -y wget unzip && \
    wget -O allure-commandline.zip https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.14.0/allure-commandline-2.14.0.zip \
    && unzip allure-commandline.zip -d /opt/ \
    && ln -s /opt/allure-2.14.0/bin/allure /usr/bin/allure \
    && rm allure-commandline.zip


#setting the allure path
ENV PATH="/opt/allure-2.14.0/bin:${PATH}"

# Set the Java home environment variable
ENV JAVA_HOME /usr/lib/jvm/default-java
ENV PATH $JAVA_HOME/bin:$PATH

# Give permission to the reports file
RUN chmod -R +r /gorestapiautomation/reports

# Create a directory to store reports
RUN mkdir -p /gorestapiautomation/reports/gorestapi-report

# Set the working directory to /gorestapiautomation/tests
WORKDIR /gorestapiautomation/tests

# Define the CMD command
CMD ["sh", "-c", "if [ -n \"$TEST_FILE\" ]; then pytest $TEST_FILE -s -v ${MARKER_NAME:+-m $MARKER_NAME} --alluredir='/gorestapiautomation/reports/allure-reports'; else pytest -s -v ${MARKER_NAME:+-m $MARKER_NAME} --alluredir='/gorestapiautomation/reports/allure-reports'; fi ; allure generate '/gorestapiautomation/reports/allure-reports' -o '/gorestapiautomation/reports/generated-reports' ; allure-combine '/gorestapiautomation/reports/generated-reports' --dest '/gorestapiautomation/reports/gorestapi-report'"]

