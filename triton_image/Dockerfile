FROM nvcr.io/nvidia/tritonserver:21.05-py3

# INSTALL AWS CLI
RUN apt-get update && apt-get install -y \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -f awscliv2.zip

# COPY ENTRYPOINT FILE
COPY run.sh /tmp/run.sh
RUN chmod +x /tmp/run.sh