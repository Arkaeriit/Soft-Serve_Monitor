# Soft Serve monitor

[Soft Sevre](https://github.com/charmbracelet/soft-serve) is a very nice git server. It offers a really nice TUI to browse the repositories on the server. Unfortunately, it does not offers a web interface. Here, I want to try to make a tiny web interface to present the git server and list the repositories there.

## Configuration

To tell the web server what files to monitor and how to login to the Soft Serve server, a JSON configuration file is needed. The JSON file needs the following fields:

| Field name     | Description                                                   | Example                  |
|----------------|---------------------------------------------------------------|--------------------------|
| `ss_host`      | The host name of URL of the Soft Serve server.                | "git.bobignou.red"       |
| `ss_port`      | The port used by the Soft Serve server.                       | 23231                    |
| `repos_path`   | The path to the folder where the git repositories are located | "/srv/soft-serve/.repos" |
| `monitor_port` | Port uses by the Flask web server.                            | 8080                     |
| `monitor_name` | A name to display to describe the server.                     | Bobignou                 |

This JSON file should be given as argument when running the Flask server executable.

An example is given as `config.json` in this repository.

## Running the server

This server depends on the following python libraries:
* Flask
* markdown
You need to install them before being able to run it.

Running this server is as easy as running any other Flask server. I use the following systemd service to run it on [my personal server](https://git.bobignou.red).
```
[Unit]
Description=A soft-serve web interface
After=network.target

[Service]
Type=simple
# Another Type: forking
User=root
Group=root
WorkingDirectory=/srv/data/soft-serve
ExecStart=/srv/soft-serve/soft-serve_monitor/soft-serve_monitor.py /srv/soft-serve/soft-serve_monitor/config.json
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

