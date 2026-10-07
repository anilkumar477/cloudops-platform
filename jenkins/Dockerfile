FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates \
        curl && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg \
        -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
        > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*


# Install Ansible in an isolated virtual environment
RUN python3 -m venv /opt/ansible-venv && \
    /opt/ansible-venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/ansible-venv/bin/pip install --no-cache-dir \
        ansible-core==2.16.14 \
        requests \
        docker \
        kubernetes && \
    /opt/ansible-venv/bin/ansible-galaxy collection install \
        community.docker:3.13.3 \
        kubernetes.core \
        -p /usr/share/ansible/collections

RUN curl -LO "https://dl.k8s.io/release/v1.34.0/bin/linux/amd64/kubectl" && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
    rm kubectl
ENV PATH="/opt/ansible-venv/bin:${PATH}"
USER jenkins
