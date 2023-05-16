FROM public.ecr.aws/docker/library/python:3.10-slim-bullseye

ARG USER=signal-aichat
ARG HOME_DIR=/home/$USER

RUN adduser \
	--disabled-password \
	--uid 1000 \
	$USER

USER $USER
WORKDIR $HOME_DIR

COPY requirements.txt ai.py signal-aichat.py ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "signal-aichat.py"]
