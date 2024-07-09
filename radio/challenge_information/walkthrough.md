## Radio

Let's perform a quick nmap scan:

    nmap -sV [IP] -p1883 -Pn

We notice that port `1883` is a mqtt service, relaying all the data received by the radio "tower".\
We can connect to it with mosquitto and listen to all the topics.

```bash
mosquitto_sub -v -t "#" -h [IP]
```

We will notice two messages, being relayed every 10 seconds, from topic:
- `frequency/1337/read`
- `frequency/3137/read`

Both of them are encoded in base64.
We can retrieve the first one of them with:

```bash
mosquitto_sub -t "frequency/1337/read" -h [IP] -C 1 | base64 -d > client.py
```

The first message will be a python script to connect to the mqtt server and communicate with it, the second message is a base64 of a wav containing a morse code message.

The client will do the whole encoding/decoding for us, specifying the frequency:

```bash
python3 -BO client.py [IP] 1883 3137
```
The client will throw a lot of errors, but eventually will print the correct message.

```
Connected with result code 0
Enter the message to publish (or 'exit' to quit):
>Exception in thread Thread-2 (_thread_main):
Traceback (most recent call last):
  File "/usr/lib/python3.10/threading.py", line 1016, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.10/threading.py", line 953, in run
    self._target(*self._args, **self._kwargs)
  File "/home/shotokan/.local/lib/python3.10/site-packages/paho/mqtt/client.py", line 3591, in _thread_main
    self.loop_forever(retry_first_connection=True)
  File "/home/shotokan/.local/lib/python3.10/site-packages/paho/mqtt/client.py", line 1756, in loop_forever
    rc = self._loop(timeout)
  File "/home/shotokan/.local/lib/python3.10/site-packages/paho/mqtt/client.py", line 1164, in _loop
    rc = self.loop_read()
  File "/home/shotokan/.local/lib/python3.10/site-packages/paho/mqtt/client.py", line 1556, in loop_read
    rc = self._packet_read()
  File "/home/shotokan/.local/lib/python3.10/site-packages/paho/mqtt/client.py", line 2439, in _packet_read
    rc = self._packet_handle()
  File "/home/shotokan/.local/lib/python3.10/site-packages/paho/mqtt/client.py", line 3041, in _packet_handle
    return self._handle_suback()
  File "/home/shotokan/.local/lib/python3.10/site-packages/paho/mqtt/client.py", line 3237, in _handle_suback
    (mid, packet) = struct.unpack(pack_format, self._in_packet['packet'])
struct.error: bad char in struct format
Connected with result code 0
< SEND I HAVE SURVIVED TO 28497
```
Let's send the message `I HAVE SURVIVED` to `28497`:
```
python3 -BO morseclient.py [IP] 1883 28497
Connected with result code 0
Enter the message to publish (or 'exit' to quit):
>I HAVE SURVIVED
>< HI HUUSV8I  YOF ARE READING THIS I AM DEAD IF YOU NEEB CAR COMPONENTS CHECX THE GARAGE TO GET THE CODE SEND THE FOLLOWING PASSWORD TO 24148 TEST123
I HAVE SURVIVED
>< HI SURVIVOR IF YOU AFE RIADING NH I RM DIND IF QU NEED CAR CZMPONENTS CHEK AHE GARAGE TO GET THE CODE SEND THE FOLLOWING PASSWORD TO 24148 TEST123
```
Let's send `TEST123` to `24148`:
```
python3 -BO morseclient.py [IP] 1883 24148
Connected with result code 0
Enter the message to publish (or 'exit' to quit):
>TEST123
>TEST123
>
```
So strange! nothing is happening.\
That's actually a bug for the library `morse_audio_decoder`:
```python
>>> import morseclient
>>> w = morseclient.text_to_wav("TEST123")
>>> morseclient.wav_to_text(w.read())
'TEEEETETTTTEETTTEEETT'
```
`morse_audio_decoder` can't decode properly `TEST123` in morse, as it's transmitted too fast.

Recreating a wav file with a slower morse code will help the remote library understand what we are transmitting.\
7WPM @1000Hz it's proven to work perfectly.

An online service like [this](https://www.meridianoutpost.com/resources/etools/calculators/calculator-morse-code.php) can be used to create a valid wav file.
we can then replace the `text_to_wav` function in the script:
```python
def text_to_wav(text:str) -> io.BytesIO:
    # morse = text_to_morse(text)
    # return morse_to_wav(morse)
    return open('test.wav','rb')
```
And it will work perfectly.

```
Connected with result code 0
Enter the message to publish (or 'exit' to quit):
>
>TEST1< FFAG NTGC L0RS31A35DUP
< FLAG NTRLGC L0LM0RS315M3553DUP
```
The flag turns out to be `NTRLGC{L0LM0RS315M3553DUP}`.