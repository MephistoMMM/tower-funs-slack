# Tower-Funs-Slack

This project is forked from [tower-slack](https://github.com/lepture/tower-slack), but I almost rewrite it using flask in python3. It is deployed by [funs](https://github.com/MephistoMMM/funs), so you could deploy it on any vps via docker.


![Slack Message Example](https://cloud.githubusercontent.com/assets/290496/10628183/a9b02d5c-77f4-11e5-9894-faf7b2ede82e.png)


## Usage

Create a new **Incoming Webhook** on Slack, then get its **Webhook URL**:

e.g.

```
https://hooks.slack.com/services/T0DRRRYS1/C9XZ5VL2/bqiCkTrLYMpJcDaKG9HaS4yu
```

Replace the link of **incoming webhook url** with the link of **tower-funs-slack**:

e.g.

```
https://tower-funs-slack.avosapps.us/T0DRRRYS1/C9XZ5VL2/bqiCkTrLYMpJcDaKG9HaS4yu
```

Add **webhook** on Tower.im, full it with the link of **tower-funs-slack**

![tower slack](https://cloud.githubusercontent.com/assets/290496/10625797/59b64710-77da-11e5-90dc-e496113aceab.png)

## Deploy

Clone this repository to your vps, and init **funs**:

```
git clone https://github.com/MephistoMMM/tower-funs-slack.git
./init.sh
```

Create virtual env and install dependences:

*I hope your virtualenv is installed by pip3*

```
virtualenv ./venv
source ./venv/bin/activate
pip3 install  -r ./requirements.md
deactivate
```

Change the ports in **docker-compose.yml** , then:

```
docker-compose up -d
```

If you don't want to pull docker image from dockerhub (for its speed...), you could build docker by yourself:

```
cd dockerfiles
docker build -t mpsss/funs .
cd ..
```

More configurations, you should see on [funs](https://github.com/MephistoMMM/funs).

## License

MIT
