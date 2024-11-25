# Base image
ARG GRAALVM_VERSION=22.3.3
ARG GRAALVM_JDK_VERSION=java11
FROM ghcr.io/graalvm/graalvm-ce:ol8-${GRAALVM_JDK_VERSION}-${GRAALVM_VERSION} AS graal-jdk-image

FROM debian:bullseye-slim

# Metadata
LABEL maintainer="Erivando Sena <erivandosena@gmail.com>"
LABEL version="1.0"
LABEL description="JupyterLab environment with support for GraalVM (Java), Python, R and specific libraries for graphs."

# Environment variables
ENV JAVA_HOME=/opt/java/graalvm
ENV PATH=${JAVA_HOME}/bin:$PATH
ENV USER=jupyter
ENV WORKDIR=/home/${USER}
ENV JUPYTER_CONFIG_DIR=${WORKDIR}/.jupyter
ENV LABCONFIG_DIR=$JUPYTER_CONFIG_DIR/labconfig
ENV PATH="/opt/conda/bin:$PATH"

# Copy GraalVM
COPY --from=graal-jdk-image /opt/graalvm-ce-* /opt/java/graalvm

# Installing system dependencies
RUN apt-get update && \
    apt-get install -y \
        jq \
        sudo \
        bash \
        curl \
        unzip \
        python3 \
        python3-dev \
        python3-pip \
        r-base && \
    rm -rf /var/lib/apt/lists/* /tmp/*

# Instale o Miniconda
RUN curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh && \
    /opt/conda/bin/conda init && \
    ln -s /opt/conda/bin/conda /usr/local/bin/conda && \
    /opt/conda/bin/conda config --set always_yes yes --set changeps1 no && \
    /opt/conda/bin/conda update -q conda

# Mamba update and installation
RUN /opt/conda/bin/conda update -n base -c defaults conda && \
    echo "Conda atualizado com sucesso" && \
    /opt/conda/bin/conda install -n base -c conda-forge mamba

# Configuring channels using Conda
RUN /opt/conda/bin/conda config --add channels conda-forge && \
    echo "Canal conda-forge adicionado com sucesso" && \
    /opt/conda/bin/conda config --add channels defaults && \
    echo "Canal defaults adicionado com sucesso" && \
    /opt/conda/bin/conda config --set channel_priority strict

# Cache clearing using Mamba
RUN /opt/conda/bin/mamba clean --all --yes

# Install packages using mamba
RUN /opt/conda/bin/mamba install -c conda-forge \
    python=3.10 \
    jupyterlab=4.2.6 \
    jupyter \
    notebook \
    py2neo \
    networkx \
    matplotlib \
    seaborn \
    pyvis \
    graphdatascience \
    python-louvain \
    r-base \
    r-irkernel \
    scikit-learn && \
    /opt/conda/bin/mamba clean -afy

# Install unavailable packages in Conda via pip
RUN pip install \
    neo4j \
    yfiles_jupyter_graphs \
    ipycytoscape \
    jupyterlab-link-share \
    openai \
    python-lsp-server \
    nbimporter

RUN pip3 install --upgrade openai

# Cannot detect language. Please choose it manually
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get update && \
    apt-get install -y nodejs && \
    npm install -g npm@latest && \
    npm install -g yarn

RUN pip install \
    jupyterlab_widgets \
    yfiles_jupyter_graphs

# Cannot detect language. Please choose it manually
RUN curl -L https://github.com/SpencerPark/IJava/releases/download/v1.3.0/ijava-1.3.0.zip -o ijava.zip && \
    unzip ijava.zip -d /opt/java-kernel && \
    python3 /opt/java-kernel/install.py --sys-prefix && \
    rm ijava.zip

# Cannot detect language. Please choose it manually.
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

RUN adduser --disabled-password --gecos "" ${USER} && \
    usermod -aG sudo ${USER} && \
    echo "${USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    mkdir -p ${WORKDIR}/works

USER ${USER}

RUN mkdir -p ${JUPYTER_CONFIG_DIR} && \
    yes "y" | jupyter server --generate-config && \
    ## Uncomment the two lines below to enable password login.
    # python3 -c "from jupyter_server.auth import passwd; print(passwd('Password1'))" > ${JUPYTER_CONFIG_DIR}/.jupyter_password && \
    # echo "c.PasswordIdentityProvider.hashed_password = open('${JUPYTER_CONFIG_DIR}/.jupyter_password').read().strip()" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.ServerApp.open_browser = False" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.ServerApp.allow_origin = '*'" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.ServerApp.allow_credentials = True" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.ServerApp.websocket_compression_options = None" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.ServerApp.disable_check_xsrf = True" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.ServerApp.allow_remote_access = True" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.ServerApp.trust_xheaders = True" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.MappingKernelManager.default_kernel_name = 'python3'" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py && \
    echo "c.FileContentsManager.max_upload_size = 0" >> ${JUPYTER_CONFIG_DIR}/jupyter_server_config.py

# Create/update page_config.json
RUN mkdir -p ${LABCONFIG_DIR} && \
    echo '{ \
            "lockedExtensions": {}, \
            "allowLargeFileUpload": true, \
            "showPrompts": false, \
            "disablePopups": true \
          }' > ${LABCONFIG_DIR}/page_config.json

WORKDIR ${WORKDIR}/works
USER ${USER}
EXPOSE 8888

ENTRYPOINT ["bash", "-c", "\
    sudo chown -Rf ${USER}:${USER} ${WORKDIR} && \
    ## Uncomment the line below to disable root in production
    # sudo sed -i '/jupyter ALL=(ALL) NOPASSWD:ALL/d' /etc/sudoers && \
    jupyter lab --ip=0.0.0.0 --allow-root --no-browser --IdentityProvider.token='' \
"]
