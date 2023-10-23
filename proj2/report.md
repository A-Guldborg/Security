TLS encryption on each individual computation to the hospital, so an adversary (Dolev Yao) cannot reconstruct the data in the same way as the Hospital.

# Security mini project 2

Made by Andreas Guldborg Hansen

## Program files

To run the program, python3 must be installed. Note that this was written with Python 3.11.6.

Furthermore a certificate must be generated. We use the same certificate/key pair for all clients/hosts. These should be saved in files `server_cert.pem` and `server_key.pem`. With `openssl` installed on your system, the following command will generate one without a password (use default values in the following prompt):

`openssl req -x509 -newkey rsa:2048 -keyout server_key.pem -out server_cert.pem -days 365 -nodes`

After generating the `.pem`-files, run the program with `python3 .\main.py`

## Building blocks

### TLS

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
