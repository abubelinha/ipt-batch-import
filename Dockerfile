FROM maven:3.6.3-jdk-8-slim

RUN mkdir /app

COPY src /app/src
COPY pom.xml /app/pom.xml
COPY convert-dwca-to-ipt /app/convert-dwca-to-ipt

WORKDIR /app
RUN mvn clean install

RUN mkdir /dataset
RUN mkdir /app/results

RUN ln -s /app/results /result

VOLUME /dataset
VOLUME /result

RUN /app/convert-dwca-to-ipt /dataset

CMD ["/app/convert-dwca-to-ipt", "/dataset"]
