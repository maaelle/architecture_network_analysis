FROM python:3.11

RUN apt update && apt upgrade -y

RUN apt install make -y

COPY ./ ./

RUN make install_libs

RUN make install_deps

CMD ["main.lambda_handler"]