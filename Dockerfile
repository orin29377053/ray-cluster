FROM rayproject/ray:nightly-py311-aarch64

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
COPY --chmod=755 entrypoint.sh /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
