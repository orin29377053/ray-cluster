FROM rayproject/ray:nightly-py311-aarch64

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
USER root
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY --chmod=755 entrypoint.sh /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
