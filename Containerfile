ARG ICORN_VERSION=3.23

FROM docker.io/gautada/icorn:$ICORN_VERSION as BUILD

ARG GITHUB_TAG=dev

RUN apk add --no-cache \
    python3 py3-pip python3-dev \
    build-base musl-dev linux-headers \
    libffi-dev openssl-dev \
    curl uv
WORKDIR /opt/icorn
COPY . .
# RUN git clone --branch ${GITHUB_TAG} https://github.com/gautada/icorn.git icorn \
RUN chown icorn:icorn -R /opt/icorn 
# WORKDIR /opt/icorn
USER icorn
RUN uv venv .venv \
 && uv sync --frozen --no-dev

################################################################################

FROM docker.io/gautada/icorn:$ICORN_VERSION as CONTAINER

ARG IMAGE_NAME=pastebin
ARG IMAGE_VERSION=0.0.1

# ╭――――――――――――――――――――╮
# │ METADATA           │
# ╰――――――――――――――――――――╯
LABEL org.opencontainers.image.title="${IMAGE_NAME}"
LABEL org.opencontainers.image.description="A ${IMAGE_NAME} server"
LABEL org.opencontainers.image.url="https://hub.docker.com/r/gautada/${IMAGE_NAME}"
LABEL org.opencontainers.image.source="https://github.com/gautada/${IMAGE_NAME}"
LABEL org.opencontainers.image.version="${IMAGE_VERSION}"
LABEL org.opencontainers.image.license="Upstream"

# # ╭――――――――――――――――――――╮
# # │ USER               │
# # ╰――――――――――――――――――――╯
ARG USER=icorn
# RUN /usr/sbin/usermod -l $USER alpine \
# && /usr/sbin/usermod -d /home/$USER -m $USER \ 
# && /usr/sbin/groupmod -n $USER alpine \
# && /bin/echo "$USER:$USER" | /usr/sbin/chpasswd 

# ╭――――――――――――――――――――╮
# │ CONTAINER          │
# ╰――――――――――――――――――――╯
# COPY uvicorn.s6 /etc/services.d/uvicorn/run
# RUN apk add --no-cache python3 uv libffi openssl ca-certificates
# # Copy the venv and app code from builder
COPY --from=BUILD /opt/icorn /opt/icorn
COPY --from=BUILD /home/icorn/.local /home/${USER}/.local
RUN chown ${USER}:${USER} -R /opt/icorn /home/${USER}
WORKDIR /home/${USER}
# RUN ln -fsv /home/${USER}/.local/share/uv/python/cpython-3.13.11-linux-aarch64-musl/bin/python3.13 /opt/icorn/.venv/bin/python

