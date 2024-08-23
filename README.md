# ml_iot

## Huffman coding

Example showing Huffman coding being used to compress IoT telemetry messages.

```
export IOTMSG='{"deviceId":"01:23:45:67:89:AB","timestamp":"2024-08-22T12:34:56Z","data":[{"sensorId":"temp_sensor_1","type":"temperature","value":22.5,"unit":"C"},{"sensorId":"humidity_sensor_1","type":"humidity","value":55.2,"unit":"%"},{"sensorId":"pressure_sensor_1","type":"pressure","value":1013.25,"unit":"hPa"},{"sensorId":"motion_sensor_1","type":"motion","value":true,"unit":"boolean"}],"location":{"latitude":37.7749,"longitude":-122.4194},"status":{"battery":{"level":87,"unit":"%"},"connectivity":"WiFi","signalStrength":{"value":-45,"unit":"dBm"}},"deviceConfig":{"sampleRate":{"value":60,"unit":"seconds"},"reportingInterval":{"value":300,"unit":"seconds"}}}'	

python3 huffman.py \
        -m $IOTMSG \
        -w '"version"' '"deviceId":"' '"data"' '"sensorId":"' '"ts"' '"timestamp"' '"type"' '"value"' '"unit"' '"status"' '"location":{' '"latitude":{' ',"longitude":' '"battery"' '"level"' '"connectivity"' '"signalStrength"' '"deviceConfig"' '"sampleRate"' '"reportingInterval"' '"other"' \
        "_sensor_" "temp" "humidity" "pressure" "motion" \
        '"unit":"boolean"' '"unit":"hPa"' '"unit":"%"' '"unit":"C"' '"unit:"dBm"' '"unit":"seconds"' \
        "[{" "}]" "},{" "\",\"" "\":\"" "{" \
        "0.0" ":0," \
        "tion" "ther" "with" "ment" "that" \
        "the" "and" "ing" "her" "hat" "his" "tha" "ere" "ent" "ion" \
        "th" "he" "in" "er" "an" "re" "on" "at" "en" "nd" \
         "ai" "ea" "ie" "ou" "qu" "tr" "gr" "pl" \
         " s" " c" " a" " m" " r" " t" " b" " e" " w"
```
