ARG GRAALVM_VERSION=22.3.3
ARG GRAALVM_JDK_VERSION=java11
FROM ghcr.io/graalvm/graalvm-ce:ol8-${GRAALVM_JDK_VERSION}-${GRAALVM_VERSION} AS graal-jdk-image

FROM debian:bullseye-slim

LABEL maintainer="Erivando Sena <erivandosena@gmail.com>"
LABEL version="1.0"
LABEL description="Ambiente JupyterLab com suporte para GraalVM (Java), Python e R."

ENV JAVA_HOME=/opt/java/graalvm
ENV PATH=${JAVA_HOME}/bin:$PATH
ENV USER=jupyter
ENV WORKDIR=/home/${USER}
ENV JUPYTER_CONFIG_DIR=${WORKDIR}/.jupyter

COPY --from=graal-jdk-image /opt/graalvm-ce-* /opt/java/graalvm

RUN apt-get update && \
    apt-get install -y nodejs npm curl && \
    npm install -g n && \
    n stable && \
    apt-get purge -y npm

# Instalar dependências e pacotes necessários (Python, R, JupyterLab, Pacotes de Grafo)
RUN apt-get update && \
    apt-get install -y bash curl unzip python3 python3-dev python3-pip r-base && \
    pip3 install --no-cache --upgrade pip && \
    pip3 install --no-cache jupyterlab==4.3.0 jupyter notebook py2neo neo4j networkx matplotlib pyvis yfiles_jupyter_graphs graphdatascience python-louvain openai && \
    rm -rf /var/lib/apt/lists/* /tmp/*

RUN pip3 install --upgrade openai

RUN pip3 install --no-cache-dir jupyterlab-link-share

RUN curl -L https://github.com/SpencerPark/IJava/releases/download/v1.3.0/ijava-1.3.0.zip -o ijava.zip && \
    unzip ijava.zip -d /opt/java-kernel && \
    python3 /opt/java-kernel/install.py --sys-prefix && \
    rm ijava.zip

RUN mkdir -p /usr/local/share/jupyter/kernels/java && \
    echo '{ \
      "argv": [ \
        "/opt/java/graalvm/bin/java", \
        "-XX:+UnlockExperimentalVMOptions", \
        "-XX:+EnableJVMCI", \
        "-XX:+UseJVMCICompiler", \
        "-jar", "/opt/java-kernel/ijava-1.3.0.jar", \
        "{connection_file}" \
      ], \
      "display_name": "Java (GraalVM)", \
      "language": "java" \
    }' > /usr/local/share/jupyter/kernels/java/kernel.json

# Instalar IRKernel para R
RUN R -e "install.packages('IRkernel', repos='http://cran.r-project.org')" && \
    R -e "IRkernel::installspec(user = FALSE)"

RUN adduser --disabled-password --gecos "" ${USER}

WORKDIR ${WORKDIR}

RUN chown -R ${USER}:${USER} ${WORKDIR}

EXPOSE 8888

RUN mkdir -p ${JUPYTER_CONFIG_DIR} && \
    jupyter server --generate-config && \
    python3 -c "from jupyter_server.auth import passwd; print(passwd('Password1'))" > ${JUPYTER_CONFIG_DIR}/.jupyter_password && \
    echo "c.PasswordIdentityProvider.hashed_password = open('${JUPYTER_CONFIG_DIR}/.jupyter_password').read().strip()" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.ServerApp.open_browser = False" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.ServerApp.allow_origin = '*'" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.ServerApp.allow_credentials = True" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.ServerApp.websocket_compression_options = None" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.ServerApp.disable_check_xsrf = True" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.ServerApp.allow_remote_access = True" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py

USER ${USER}

ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser", "--IdentityProvider.token=''"]
