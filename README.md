# architecture-cloud

This GitHub Repository describes how we want to protect all users from navigating on internet.
So we decided to create a DNS server which works thanks to an AWS server.

This Readme explains how to create this server using terraform, and how it works and why we decided this configuration.


## Overview

1. [Installation](#installation)
2. [Architecture](#architecture)
3. [How did we design our architecture?](#how-did-we-design-our-architecture)
    1. [Goal of our Project](#goal-of-our-project)
    2. [The prediction](#the-prediction)
    3. [Saving old Predictions](#saving-old-predictions)
    4. [Refitting our AI](#refitting-our-ai)
4. [Links](#links)

## Architecture

Our final architecture can be resumed into 5 different apps connected to 2 databases:
if you want details about how we design our system, see the topic 
[How did we design our architecture?](#how-did-we-design-our-architecture).

```mermaid
flowchart TB

a1[APP1] 
a2[APP2] 
a3[APP3] 
a4[APP4] 
a5[APP5]

d1[(Reject List)]
d2[(Accept List)]

usr[User]

s1([sqs1])
s2([sqs2])
s3([sqs3])
s4([sqs4])

subgraph DNS
    a1 -->|url| s1
    s1 -->|url| a2 
    a2 -->|http-packet & url| s2 
    s2 -->|http-packet & url| a3 
    a3 -->|http-packet & url & prediction| s3 
    s3 -->|http-packet & url & prediction| a4 
    a4 --> |url & prediction| s4 
    s4 --> |url & prediction| a5
end

usr ==> |url| a1
a1 ==> |url| usr

a1 -.-> |GET| d1
a2 -.-> |GET| d2
a5 -.-> |PUT| d1
a5 -.-> |PUT| d2
```

## Installation

First, you need to clone this git by typing in the terminal
`git clone https://github.com/maaelle/architecture_network_analysis.git`

Then, you have to register to AWS CLI, so type in the terminal `aws configure` and put your IAM key.

Once you finished to register to AWS CLI, you can type in the terminal `terraform init` and then `terraform apply`

> **Warning**
> don't use `terraform apply` for now because it's not finished

## How did we design our architecture?
> **Note**
> The AI is available in this [GitHub repository](https://github.com/clementreiffers/network_analysis).

### Goal of our Project

The goal of our project is to protect the final user.
So our project could be simplified by this bloc-schema below :

```mermaid
graph LR

USR[user]
DNS[is the website malicious ?]

USR --> |Give his target URL| DNS
DNS --> |Yes| USR
DNS --> |No| USR
```

If the URL is malicious, so we send a warning to the user, otherwise we permit the direct access to the URL.

### The prediction

Our first idea was the prediction of all URL that all user wanted.
It could work but all networks catching and predictions cost a lot of execution time, so it harms the final user
who just wanted to be safe. We want the fastest system.
So we searched a solution to resolve this problem.

```mermaid 
flowchart LR
USR[User]
L1[Catching network packet]
L2[Prediction kind of app]
L3[Is it malicious?]

USR --> L1
L1 --> L2
L2 --> L3
L3 --> |YES| USR
L3 --> |No| USR
```

### Saving old Predictions

So we add 2 databases to this architecture as below:

![saving old predictions](docs/saving-old-predictions.png)


This 2 databases serve to save to kind of data :

- the first one serve to store all rejected URL
- the second serve to store all accepted URL

This architecture permits to not predict 2 times the same URL, the user isn't harm by an execution cost provided by
the prediction and the network catching.

There is 2 ways for the user :

- If a URL is in the reject list, the user receive a warning.
- If a URL is not in the reject list, so the URL will fill an AWS SQS and will be verified by the AI in order to fill
  the databases, there is 2 ways for this URL:
    - If it has been accepted before, we analyse the next URL in the AWS SQS
    - If it has not been accepted before, so the URL is totally unknown, so it pass in the 2 lambdas seen before, so
      the network catching and the prediction. If the AI predicted this URL as a bad one, it fills the reject list
      otherwise it fills the accepted list.

This architecture save a lot of time for the user, but we need to improve continually our AI, we need refitting, so we
searched ways to improve this AI.

### Refitting our AI

To refitting the AI, we created this architecture below:
![refitting AI](docs/refitting-ai.png)

The AI will be refitted all along the utilization of the DNS. For that, we added an AWS dynamodb, which stores all
network packets from unknown URL.

### complete arch


```mermaid
flowchart TB

l1[is-url-rejected]
l2[warning-or-target]
l3[url-accepted]
l4[catching-network-packets]
l5[prediction]
l6[refit]
l7[fill db]

style l1 fill:#D86613,color:white
style l2 fill:#D86613,color:white
style l3 fill:#D86613,color:white
style l4 fill:#D86613,color:white
style l5 fill:#D86613,color:white
style l6 fill:#D86613,color:white
style l7 fill:#D86613,color:white

s1[sqs1]
s2[sqs2]
s3[sqs3]
s4[sqs4]

style s1 fill:yellow,color:black
style s2 fill:yellow,color:black
style s3 fill:yellow,color:black
style s4 fill:yellow,color:black

d1[(reject list)]
d2[(accept list)]

style d1 fill:#92D050,color:black
style d2 fill:#00B0F0,color:black

subgraph DNS
    subgraph app1
        l1 --> |bool|l2
    end
    
    app1 --> |url| s1 --> app2
    
    subgraph app2
        l3 --> |url| l4
    end
    
    app2 --> |network-packet & url| s2 --> app3 
     
    subgraph app3
        l5
    end   
    
    app3 --> |network-packet & url & prediction| s3 --> app4
    
    subgraph app4
        l6
    end 
    
    app4 --> |url & prediction| s4 --> app5
    
    subgraph app5
        l7
    end
    
    app5 -.-> |PUT| d1 & d2
    app1 -.-> |GET| d1
    app2 -.-> |GET| d2   
end


user ==> |url| app1
app1 ==> |url| user

style DNS fill:transparent
```

### Detailed description of our architecture

![detailed-description](docs/detailed-description.png)

| bloc | Description                                                                                                                                     |
|:----:|:------------------------------------------------------------------------------------------------------------------------------------------------|
|  1   | All our architecture is in an AWS EC2, we will use all our AWS Lambda inside of it                                                              |
|  2   | We get the target URL and verify if it has been rejected in the past. This lambda send a boolean                                                |
|  3   | It represents our reject list in mongodb. it's outside the EC2 because it's hosted by mongo atlas                                               |
|  4   | It send a warning if the bloc 2 send "false" otherwise it send the target URL to the user                                                       |
|  5   | This is an AWS SQS of all URL which aren't in the reject list                                                                                   |
|  6   | This lambda verify if the URL is in the accepted list                                                                                           |
|  7   | This bloc represents the AWS dynamodb used to store all accepted URL.                                                                           |
|  8   | This lambda listen the network and will compute a GET HTTP to the target URL. It catches network packets                                        |
|  9   | This lambda is our AI. It predicts the network packets received from bloc 8, predicts the kind of app and fills reject/accept db in consequence |
|  10  | This bloc represents cache used to refit our AI. It will be empty once the refitting finished                                                   |
|  11  | It refits the AI with data from bloc 10                                                                                                         |
|  12  | It store the AI used for predictions and refitting.                                                                                             |

## Links

### AWS

1. [AWS lambda](https://aws.amazon.com/fr/lambda/)
2. [AWS SQS](https://aws.amazon.com/fr/sqs/)
3. [AWS S3](https://aws.amazon.com/fr/s3/)
4. [AWS dynamodb](https://aws.amazon.com/fr/dynamodb/)
5. [AWS EC2](https://aws.amazon.com/fr/ec2/)

### Databases
1. [Mongodb](https://www.mongodb.com/fr-fr)
2. [AWS dynamodb](https://aws.amazon.com/fr/dynamodb/)

### Terraform
1. [Terraform](https://www.terraform.io/)

### Contributors

Clément Reiffers:
- @clementreiffers
- <https://github.com/clementreiffers>

Maelle Marcelin:
- @maaelle
- <https://github.com/maaelle>

Camille Bayon de Noyer:
- @Kamomille
- <https://github.com/kamomille>

Sonia Moghraoui:
- @SoniaMogh
- <https://github.com/SoniaMogh>

[![GitHub contributors](https://contrib.rocks/image?repo=maaelle/architecture_network_analysis)](https://github.com/maaelle/architecture_network_analysis/graphs/contributors) 
