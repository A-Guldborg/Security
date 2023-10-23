from os import name
import threading
import time
from hospital import Hospital
from client import Person


# Begin with the Hospital
h = Hospital(port=9000)


# Create three people each listening on an arbitrary port

a = Person("Alice", port=9001)
b = Person("Bob", port=9002)
c = Person("Charlie", port=9003)

# Start serving servers for all people
for person in [a, b, c]:
    thread = threading.Thread(target=person.serve, daemon=True)
    thread.start()

time.sleep(2) # Allow people to setup communication sockets

# Send values to other people but not themself
for person in [a, b, c]:
    people = [a, b, c]
    people.remove(person)
    
    # Not using threads as only doing one at a time increases chances our program does not run into race condition issues
    person.send_values(list(map(lambda person: person.port, people)))


time.sleep(2)
# "God" is an entity that writes debug statements and does not interfere in the algorithm but lets the observer know the expected values
print(f"God: The (secret) heights are {a.height}, {b.height} and {c.height} giving a total of {sum([a.height, b.height, c.height])}")