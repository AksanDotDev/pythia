# Stage 1
FROM python:latest AS compiler
COPY requirements.txt .

RUN pip install --user -r requirements.txt

#Stage 2
FROM python:alpine
WORKDIR /code

COPY --from=compiler /root/.local /root/.local
COPY ./src .

ENV PATH=/root/.local:$PATH

CMD [ "python", "./heart.py" ]