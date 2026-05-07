En la configuración del ArduinoIDE se ha de considerar lo siguiente:
Placa: "ESP32S3 Dev Module" 
USB CDC On Boot: Enabled
Flash Mode: QIO 80MHz
Partition Scheme: Huge APP (3MB No OTA...)

Adicionalmente, En "Gestor de URLs Adicionales de Tarjetas", se usó:
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
