curl -X POST -H "Content-Type: application/json" -d '{
  "greeting":[
    {
      "locale":"default",
      "text":"Hi there!\n\nMy name is sigma, your personal financial assistant!"
    }
  ] 
}' "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAADMZBDhEKOoBAOZCgvKHj6tlf8lQTMNB6MUvPTQQEgluJCXt4VZAH7zTx25NnPD25TOp1ZAG5p0ayksyfjGUMrmeIfVy5tqQq7yMKM27LWx1nfZBVEpn4zQfLXrIzo8FC5RmKywQumyswxp1dDcjqvyFqaNoKFnuq0ucfvGv6QZDZD"
