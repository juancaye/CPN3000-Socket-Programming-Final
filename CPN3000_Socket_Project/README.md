# CPN3000 Socket Programming

Socket programming project for CPN3000, in two phases:

- **Phase 1** – TCP and UDP echo client/server pairs, with a Wireshark capture and documentation.
- **Phase 2** – the TCP echo application upgraded to TLS (encrypted, server authenticated by certificate), with a Wireshark capture of the TLS handshake.

All programs use only the Python standard library (`socket`, `ssl`).

## Project structure

| Path | Description |
|------|-------------|
| `tcp_server.py`, `tcp_client.py` | Phase 1 TCP echo server and client |
| `udp_server.py`, `udp_client.py` | Phase 1 UDP echo server and client |
| `Phase2_TLS/tls_server.py`, `Phase2_TLS/tls_client.py` | Phase 2 TLS echo server and client (TLS 1.2+) |
| `Phase2_TLS/server.crt` | Self-signed certificate (public, safe to commit) |
| `Phase2_TLS/server.key` | **Private key – not committed; you must generate it** |
| `CPN3000_Phase1_Documentation.pdf`, `Phase2_TLS/Project.pdf` | Project documentation |
| `WiresharkCaptureSaved.pcapng`, `Phase2_TLS/*.png` | Packet captures / screenshots |

## Requirements

- Python 3.8+
- OpenSSL (to generate the certificate)

## Running the TCP application

Open two terminals in the project root:

```powershell
python tcp_server.py
```
```powershell
python tcp_client.py
```

The UDP pair works the same way (`udp_server.py`, `udp_client.py`).
The servers listen on `127.0.0.1`; see the constants at the top of each file for ports.

## Generating a self-signed TLS certificate

`server.key` is intentionally excluded from the repository. Generate your own
key and certificate inside `Phase2_TLS/`:

```powershell
cd Phase2_TLS
openssl req -x509 -newkey rsa:2048 -nodes -days 365 `
  -keyout server.key -out server.crt `
  -subj "/CN=localhost" `
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```

The client connects with `server_hostname="localhost"`, so the certificate must
contain `localhost` (the `subjectAltName` above covers this).
**Never commit `server.key`.**

## Running the TLS application

Run both from inside `Phase2_TLS/` (the certificate paths are relative):

```powershell
cd Phase2_TLS
python tls_server.py
```
```powershell
cd Phase2_TLS
python tls_client.py
```

Expected client output:

```
Enter a message: Hello TLS Server
Connected securely to TLS server.
TLS version: TLSv1.3
Message sent to server.
Server replied: Hello TLS Server
Client socket closed.
```

The client loads `server.crt` as its trusted certificate and verifies the
server's identity; certificate verification is not disabled. Do not use the
plain `tcp_client.py` against the TLS server – it does not perform a handshake.
