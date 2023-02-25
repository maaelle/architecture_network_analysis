# architecture-cloud

This GitHub Repository describes how we want to protect all users from navigating on internet.
So we decided to create a DNS server which works thanks to an AWS server.

This Readme explains how to create this server using terraform, and how it works and why we decided this configuration.


## Overview

1. [Installation](#installation)
2. [Architecture](#architecture)
    1. [General Schema](#general-schema)
3. [How did we design our architecture?](#how-did-we-design-our-architecture)
    1. [Goal of our Project](#goal-of-our-project)
    2. [The prediction](#the-prediction)
    3. [Saving old Predictions](#saving-old-predictions)
    4. [Refitting our AI](#refitting-our-ai)
4. [Links](#links)

## Architecture

Our final architecture can be resumed into 5 different apps connected to 2 databases.
If you want any details about how we designed our system, see the topic 
[How did we design our architecture?](#how-did-we-design-our-architecture).

### General schema

```mermaid
flowchart TB

CLI([CLIENT DNS])

DB1[(unknown_url)]
DB2[(malicious_url)]
DB3[(accepted_url)]

L1(empty unkown URL db)
L2(catch TCP/UDP packet)
L3(predict the kind of app)
L4(refit the AI)
L5(fill DB)

USER --> |localhost:53| CLI

CLI --> |url| DB1
CLI <--> |url| DB2
L1 <--> |url| DB1

L5 --> |url| DB2
L5 --> |url| DB3

subgraph cloud 
    L1 --> |url| L2 --> |url & tcp packet| L3 --> |url & tcp & kind| L4 --> |url & kind| L5
end

subgraph mongo
    DB1
    DB2
    DB3
end

style DB1 fill:#92D050,color:black,stroke:black
style DB2 fill:#92D050,color:black,stroke:black
style DB3 fill:#92D050,color:black,stroke:black

style L1 fill:#D86613,color:white,stroke:#D86613
style L2 fill:#D86613,color:white,stroke:#D86613
style L3 fill:#D86613,color:white,stroke:#D86613
style L4 fill:#D86613,color:white,stroke:#D86613
style L5 fill:#D86613,color:white,stroke:#D86613

style CLI fill:blue,color:white,stroke:blue

style USER fill:yellow,color:black,stroke:black
```

the graph above describes how our solution works.

First we have created a CLI app [hosted here](https://github.com/clementreiffers/dns-server), this app 
once installed, will ask you which dns server do you want, and if you choose `127.0.0.1`, your entire 
OS will use this DNS server.

If the OS use this DNS server, so the CLI app, it will listen which URL you consult and fill databases with it, 
in respect of RGPD laws. We only recuperate the URLs in order to prevent people from bad URLs using AI.

the cloud part, is divided into 5 parts.

The first part is triggered automatically n times per hours, it served only to empty the mongodb database, and 
then fill an SQS to be processed after.

The second part, catch the TCP packet of the related URL if it is possible and fill an SQS to be analyzed by an AI.

the third part, predicts the kind of app using AI, and the fourth part refit this AI with its prediction.

the final part fill the mongo database with url depending if the url is malicious or not.

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
So our project could be simplified by this flowchart below :

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
L3[Send warning or target url]

USR --> |URL| L1
L1 --> L2
L2 --> L3
L3 --> |URL| USR
```


### Saving old Predictions

So we add 2 databases to this architecture as below:

```mermaid
flowchart TB

l1(is-url-rejected)
l2(warning-or-target)
l3(url-accepted)
l4(catching-network-packets)
l5(prediction)
l7(fill db)

style l1 fill:#D86613,color:white
style l2 fill:#D86613,color:white
style l3 fill:#D86613,color:white
style l4 fill:#D86613,color:white
style l5 fill:#D86613,color:white
style l7 fill:#D86613,color:white

s1([sqs1])
s2([sqs2])
s3([sqs3])

style s1 fill:yellow,color:black
style s2 fill:yellow,color:black
style s3 fill:yellow,color:black

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
        l7
    end
    
    app4 -.-> |PUT| d1 & d2
    app1 -.-> |GET| d1
    app2 -.-> |GET| d2   
end


user ==> |url| app1
app1 ==> |url| user

style DNS fill:transparent
```


This 2 databases serve to save two kind of data :

- the first one serves to store all rejected URL
- the second serves to store all accepted URL

This architecture permits to not predict 2 times the same URL, the user isn't harm by an execution cost provided by
the prediction and the network catching.

This architecture save a lot of time for the user, but we need to improve continually our AI, we need refitting, so we
searched ways to improve this AI.

### Refitting our AI

To refitting the AI, we created this architecture below:
```mermaid
flowchart TB

l1(is-url-rejected)
l2(warning-or-target)
l3(url-accepted)
l4(catching-network-packets)
l5(prediction)
l6(refit)
l7(fill db)

style l1 fill:#D86613,color:white
style l2 fill:#D86613,color:white
style l3 fill:#D86613,color:white
style l4 fill:#D86613,color:white
style l5 fill:#D86613,color:white
style l6 fill:#D86613,color:white
style l7 fill:#D86613,color:white

s1([sqs1])
s2([sqs2])
s3([sqs3])
s4([sqs4])

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

The AI will be refitted all along the utilization of the DNS. For that, we added an AWS dynamodb, which stores all
network packets from unknown URL.

## the CLI app

In order to reduce the consumption of resources on cloud and permit all people to have good performance, 
we decided to create a CLI app, which manages the listening and the management of the user directly in his OS.
To see how it has been refactoring, see the [General Schema](#general-schema)

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
