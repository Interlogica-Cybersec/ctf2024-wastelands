# Wastelands CTF

Here you will find instructions on how to start each challenge and links to the respective walkthroughs.

## Starting the Challenges

To start a challenge that requires a docker instance follow these steps:

1. Open a terminal.
2. Navigate to the directory of the challenge you want to start using the `cd` command.
3. Run the `docker-compose up -d` command to start the challenge.

Example:
```sh
cd aerial
docker-compose up -d
```

Note: In case a challenge has a "file requirement" you will find it in the `challenge_information/attachments/` directory.
Note2: You can find the exposed ports by running `docker-compose ps` looking at the column "PORTS"

Example:

```sh
docker-compose ps
NAME           IMAGE                 COMMAND                  SERVICE   CREATED              STATUS              PORTS
sim_emulator   sim-of-the-dead-sim   "/bin/sh -c 'python3…"   sim       About a minute ago   Up About a minute   0.0.0.0:9000->9000/tcp, :::9000->9000/tcp
```

## List of Walkthroughs

Below is a list of all the challenges with links to their respective walkthroughs:

- [Aerial](aerial/challenge_information/walkthrough.md) - Network - [by elpubedeoro]
- [Atlas](atlas/challenge_information/walkthrough.md) - Network - [by caigoshinobi]
- [Blessings for the Future](blessings-for-the-future/challenge_information/walkthrough.md) - Stego - [by xenobyte]
- [Echoes of the Past](echoes-of-the-past/challenge_information/walkthrough.md) - Stego - [by xenobyte]
- [Eerie Sound](eerie-sound/challenge_information/walkthrough.md) - Stego - [by ShotokanZH]
- [Gifts of the Present](gifts-of-the-present/challenge_information/walkthrough.md) - Stego - [by xenobyte]
- [Groundstation](groundstation/challenge_information/walkthrough/walkthrough.md) - Network - [by caigoshinobi]
- [Hydroponics](hydroponics/challenge_information/walkthrough/walkthrough.md) - Web - [by elpubedeoro]
- [Keeper](keeper/challenge_information/walkthrough.md) - Web - [by elpubedeoro]
- [Mechcore](mechcore/challenge_information/walkthrough.md) - PWN - [by xenobyte]
- [Medpod](medpod/challenge_information/walkthrough.md) - Web - [by elpubedeoro]
- [Memory dump](memory-dump/challenge_information/walkthrough.md) - Reversing - [by GPericol!!1!]
- [Prologue: The library](demo/challenge_information/walkthrough.md) - PWN - [by elpubedeoro & caigoshinobi]
- [Radio](radio/challenge_information/walkthrough.md) - Network - [by ShotokanZH]
- [Reactor](reactor/challenge_information/walkthrough.md) - Web - [by elpubedeoro]
- [Shipyard](shipyard/challenge_information/walkthrough.md) - ???? - [by elpubedeoro]
- [Sim of the Dead](sim-of-the-dead/challenge_information/walkthrough.md) - Network - [by ShotokanZH]
- [Survivors hub](survivors-hub/challenge_information/walkthrough.md) - Web - [by xenobyte]
- [Unauthorized](unauthorized/challenge_information/walkthrough.md) - Web - [by caigoshinobi]
- [Vending machine](vending-machine/challenge_information/walkthrough.md) - PWN - [by caigoshinobi]
- [Warehouse](warehouse/challenge_information/walkthrough.md) - Web - [by elpubedeoro]
- [Warmachine](warmachine/challenge_information/walkthrough.md) - PWN - [by xenobyte]
- [Wartank](wartank/challenge_information/walkthrough.md) - PWN - [by xenobyte]
- [Whispers of the Past](whispers-of-the-past/challenge_information/walkthrough.md) - Stego - [by xenobyte]
- [Wifi](wifi/challenge_information/walkthrough.md) - Network - [by ShotokanZH]

## Creators

- caigoshinobi
    - [Linkedin](https://it.linkedin.com/in/campanellimattia)
    - [Github](https://github.com/caigoshinobi)
- elpubedeoro
    - [Linkedin](https://it.linkedin.com/in/fabrizio-roman-396295b5)
    - [Github](https://github.com/elpube)
- GPericol!!1!
    - [Linkedin](https://www.linkedin.com/in/gianluca-p-46935a45)
    - [Github](https://github.com/gpericol)
- ShotokanZH
    - [Linkedin](https://it.linkedin.com/in/roberto-bindi)
    - [Github](https://github.com/ShotokanZH)
- xenobyte
    - [Linkedin](https://it.linkedin.com/in/matteo-papa-3694a075)
    - [Github](https://github.com/xb8)

## LICENSE
[CTF 2024 Wastelands](https://github.com/Interlogica-Cybersec/ctf2024-wastelands) © 2024 by [Interlogica](https://interlogica.it) is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1).