# apiai-smooch-docker
Your [API.ai](https://api.ai) integrated with smooch.io wrappered in a deployable docker container.

Smooch is a very easy to use and install message framework for websites to collect and communicate with visitors. dronze.com thought it was a perfect framework to get our bot talking to people quickly.

apiai-smooch-docker a fully functional robot you can wire up to your webpage written in python that works with your API.ai agent. apiai-smooch-docker is completely data driven, that is you don't need to program it for it to have conversations with people, just a working API.ai agent. That makes it less smart than the other bots at [dronze.com](https://dronze.co ) that are powered by the artificial intelligence technologies of NLP (natural language processing) and deep learning.

# Configuring The Application
The application configuration is crucial for the robot to run properly. The configuration will get used by the docker instance in the mnt directory mounted by the docker instance. You should have two files in the configuration dir:

* smoochbot-apiai.properties - The application configuration. An example of this can be found [here](./data/example_app_config.properties).

```
# provided by smooch web api so the application can create the webhook and postback
SMOOCH_KEY_ID="your key id"
SMOOCH_SECRET="your secret"

# this is where events will be sent to
SMOOCH_WEBOOK_ENDPOINT="https://smoochbot.yourdomain.com/smooch/events"

# these configurations are for the robot itself
SMOOCHBOT_NAME="smoochbot"
API_AI_TOKEN="soopersecret"
DEBUG="False"
```

# Running The Docker image
The smoochbot will use the configuration and brain graph you provide.

```
docker run -t -d --name apiai-smooch-docker -v ${CONFIG_DIR}:/mnt/config -p 8079:8079 claytantor/apiai-smooch-docker:latest
```

This will start the container up, but since there is no way for smooch to know to send events to this instance we need to initialize the application.

This is easy because we created a method to check if the webhook exists and if it doesn't then we will create it automatically. Initialize this by making sure the app is healthy (health check)

```
$ curl http://localhost:8079/hc
{"message": "succeed"}
```

and in the container logs you should see something like:

```
creating webhook: https://smoochbot.yourdomain.com/smooch/events
```

You can check that your webhook is correctly created by using [the smooch REST api](http://docs.smooch.io/rest/).


# Verifying that You Have Webhooks Configured Correctly For Smooch

```
creating webhook: http://ec2-35-163-72-62.us-west-2.compute.amazonaws.com:8079/smooch/events

{u'webhook': {u'secret': u'84da7soopers3krit6be65c86a553b6c3e7f3a16746051a', u'_id': u'58101ee22332463f000313b61', u'target': u'http://ec2-35-163-72-62.us-west-2.compute.amazonaws.com:8079/smooch/events', u'triggers': [u'message:appUser', u'postback']}}
```


# Using the CLI to test your Robot
If your want to test your script we created a simple CLI to let you do it. You can press :q to quit the conversation.

```
$ python client-cli ./data/example_app_config.properties
starting.
hello
user: hello
robot: Hello, I am friendly. What is your name?
tell me about your products
user: tell me about your products
robot: Well we have a great product, we are innovating Propulsion and we would love to talk to you about it in person. Can I get your email address so somebody on our team can tell you more?
:q
goodbye.
```

# Helpful Links

* [Dronze](https://dronze.com) - This robot was built by the bot genesis team at dronze.
* [Smooch REST API](http://docs.smooch.io/rest/) - This bot uses the Smooch REST API to create your bots ears and mouth to the smooch dialog.
* [API.ai REST API](https://docs.api.ai/docs/reference) - how to make calls to the API.ai REST endpoints for conversations.
