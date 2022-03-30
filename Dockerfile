# instala la imagen de la distro alpine en el contenedor
FROM alpine:3.15

# instala python3 y pip3
RUN apk add --no-cache python3 && apk add py3-pip 

# actualiza el pip y lee los requerimientos
RUN  pip3 install --no-cache-dir --upgrade pip 

# crea una carpeta en la que se almacenaran los archivos en el sistema linux
WORKDIR /app

# copia los archivos del proyecto al directorio /app
COPY . /app

# instala todos los modulos requeridos para iniciar la app
RUN pip3 --no-cache-dir install -r requirements.txt


CMD ["python3", "db/seeder.py", "app.py"]