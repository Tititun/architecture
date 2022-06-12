FROM python
LABEL maintainer=vinniopo@mail.ru
WORKDIR /usr/app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8001
CMD ["gunicorn", "-b", "0.0.0.0", "main:app"]

# docker container run -p 8001:8001 -v C:\Users\vinni\PycharmProjects\architecture\lesson_6:/usr/app -it my_server:1.0 /bin/bash
# gunicorn -b 0.0.0.0:8001 main:app