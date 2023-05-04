FROM python:3.10

ARG USER=signal-aichat
ARG HOME_DIR=/home/$USER

RUN adduser \
	--disabled-password \
	--uid 1000 \
	$USER

USER $USER
WORKDIR $HOME_DIR

RUN pip install \
	EdgeGPT \
	langchain \
	openai \
	semaphore-bot

COPY signal-aichat.py .

ENTRYPOINT ["python3", "signal-aichat.py"]
