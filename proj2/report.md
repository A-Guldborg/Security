# Security mini project 2

Made by Andreas Guldborg Hansen

## Program files

To run the program, python3 must be installed. Note that this was written with Python 3.11.6.

Furthermore a certificate must be generated. We use the same certificate/key pair for all clients/hosts. These should be saved in files `server_cert.pem` and `server_key.pem`. With `openssl` installed on your system, the following command will generate one without a password (use default values in the following prompt):

`openssl req -x509 -newkey rsa:2048 -keyout server_key.pem -out server_cert.pem -days 365 -nodes`

After generating the `.pem`-files, run the program with `python3 .\main.py`

This will give a terminal output for multiple threads. Each client will announce:
- their secret value (for debugging, ofc!)
- Every value they send and the target port
- The aggregate sum of the received values plus their own share

Likewise, the hospital announces when they receive a value and when they have calculated the aggregate sum.

Lastly, the God of TLS announces the three (secret) heights and their sum (for easy debugging purposes, ofc!)

## Building blocks

### Threads

To be easy to run the program, I have defined a main file which handles creating threads for one hospital and three clients, and once they host a server, then the main program also asks all three clients to start the aggregate computing algorithm. To utilize threads I use the `threading` module.

Likewise, hosting servers happens on threads (so a thread starts a client, but the client thread spawns a new thread hosting the server). The server-hosting threads are responsible to listen for incoming communications, such that we do not need to consider the order of who sends values when.

By having threads only accept one incoming connection (socket) at a time, and closing this connection before accepting a new, then the program is thread-safe by not trying to read and/or write to the aggregate values/shares that they receive during the algorithm.

### TLS

Using the `ssl` and `socket` modules from python, my solution implements the TLS protocol.
TLS ensures encryption, authentication and integrity, though by using self-signing certificates the "authentication" part is not quite true - only in the context of our own certificate chain (which has length 1). As we host all clients on the same machine, for practical reasons the solution only uses one pair of certificate and key files but in a real world example on an actually distributed network over the internet would have had seperate pairs for each node (i.e. each client and hospital).

To create a socket in python for hosting with TLS, we create a standard socket and an sslcontext with the `ssl.PROTOCOL_TLS_SERVER` protocol and our certificate/key pair. Finally we use the sslcontext to wrap "around" the socket, such that we now have a socket that uses TLS.

To create a socket to be used for connecting to a server, we also create a standard socket that we can connect to the host server, and where the context is similar to the server-context but also specifying that we do not care about the servername and verification of the certificate (thus allowing self-signed certificates) before wrapping the socket in the TLS client protocol.

Then we can use the standard features of the socket library to send and receive values as data.

### Aggregate Computing (Secure Multiparty Communication)

Each person, Alice, Bob and Charlie, splits their height (sensitive data) into three parts such that part 1, 2 and 3 sums to the height.
They then keep one part to themselves and sends the two parts to the other people, one to each.

Thus we have Alice's height as a_1, a_2 and a_3, and likewise with b_1..3 and c_1..3 for Bob and Charlie.

After splitting their heights into three different parts and sending them to eachother, we have that they all have one part from each person but no one has the same parts, i.e.:
- Alice: a_1, b_1 & c_1
- Bob: a_2, b_2 & c_2
- Charlie: a_3, b_3 & c_3

Lastly, each individual computes the sum of these three values and sends to the Hospital:
- Alice: a_1 + b_1 + c_1 = val_1
- Bob: ... = val_2
- Charlie: ... = val_3

When the Hospital receives these three values, the Hospital can calculate the aggregate sum and thus also the aggregate average, despite having no knowledge of either of the three individual's sensitive data/height.

## Adversary model

From the assumptions of the assignment, Alice, Bob & Charlie are all good-doers but communicating on an open network and thus we are susceptible for man-in-the-middle attacks. Some of these attacks include:

- Eavesdropping (Overhearing messages in order to obtain secret data)
- Interception and change data (Changing the data while it is being sent from one person to another)
- Denial of Service (Preventing messages to be received or services to work)

## Security against adversary

- Eavesdropping: Using aggregate computing, eavesdropping on individual messages does not reveal any sensitive data as this data is semi-randomly generated. Though eavesdropping on multiple or all messages can lead to revealing the sensitive data. Instead, our TLS grants us the confidentiality needed by symmetric encryption.
- Interception: Data integrity is given by the TLS protocol, which uses a message authentication code (MAC) such that the receiver can verify the sender of the data.
- Denial of Service: The building blocks does not defend against these types of attacks, but for instance the Hospital could have multiple servers to ensure that a DDoS attack cannot hit all their servers at once.
