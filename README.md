# Flask Soft Serve monitor

[Soft Sevre](https://github.com/charmbracelet/soft-serve) is a very nice git server. It offers a really nice TUI to browse the repositories on the server. Unfortunately, it does not offers a web interface. Here, I want to try to make a tiny web interface to present the git server and list the repositories there.

## Configuration

To tell the web server what files to monitor and how to login to the Soft Serve server, a JSON configuration file is needed. The JSON file needs the following fields:
| Field name   | Description                                                   | Example                  |
|--------------|---------------------------------------------------------------|--------------------------|
| `ss_host`    | The host name of URL of the Soft Serve server.                | "git.bobignou.red"       |
| `ss_port`    | The port used by the Soft Serve server.                       | 23231                    |
| `repos_path` | The path to the folder where the git repositories are located | "/srv/soft-serve/.repos" |

This JSON file should be given as argument when running the Flask server executable.

## Running the server
