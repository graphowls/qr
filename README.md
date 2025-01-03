# QR | Graph Owls

Generate QR codes

## Usage

```bash
# venv
pip install "qrcode[pil]"
```

```bash
# square QR code
python3 ./generate.py "$URL"
# rounded QR code
python3 ./generate.py -r "$URL"
# rounded and masked QR code 
python3 ./generate.py -r -m "$URL"
```
