FROM rasa/rasa-sdk:2.6.2

#COPY actions.py /app/actions.py
#COPY requirements-actions.txt /app

#USER root

RUN pip install --no-cache-dir -r requirements-actions.txt

#USER 1001

CMD ["start", "--actions", "actions"]