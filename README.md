# CIS457-NUSA
Elijah Morgan\
CIS 457 01


The first project for CIS457: Data Communication.
It's an implementation of a rudimentary MSA which only communicates with a Mail User Agent. After receiving the "end of message" marker, a real Message Submission Agent will ship the message to the destination SMTP server.\
Your MSA implementation will not push the incoming messages to the actual mail transport network. It will perform the following tasks:

[Here's an outline of project requirements and expectations.](https://dulimarta-teaching.netlify.app/cs457/p1-nsa.html)



## Complete

* Verify the recipient address (provided in RCPT TO) satisfy the following rules for a valid email:
  * Ends with .com, .org, .net, .edu, .io, .app
  * It contains exactly one @ character separating the username and domain name
  * The domain name (the string between @ and the last .) is not empty and contains only alphanumeric characters.
  * The username (the string before the @) is not empty 

    When any of these rules is not satisfied, the MSA must respond with 550 status that includes the nature of the error after the numeric code, such as 550 Unknown TLD

* Verify that the client does not attempt to send the message to more than five recipient. Otherwise, respond with 550 status that includes the nature of the error after the numeric code, such as 550 Too many recipients.

* Verify the subject line (embedded in the message header) is not blank.
  * The RFC5321 standard specifies several possible error codes when handling the DATA command: 450, 451, 452, 550, 552, and 554. Among these options, 451 error code seems to be the most appropriate.

* Print the entire message body to stdout. Your code shall be able to consume message body beyond the buffer size used for reading incoming bytes from the socket.

* In addition, your MSA implementation must be able to handle:

  * message of any size, specifically your program should not have a limit on the size of message body provided between the DATA command and the end of message marker. Recall that your program is not required to save the message body anywhere, but it must be able to "consume" any amount of bytes from its socket and correctly.
  
  * Any type of attachment in the message body

 * It shall be designed to handle several MUA client connections simultaneously. Use Python thread and use a new thread to execute the function that handles individual client interactions. Refer to the section Using Thread below.

## Incomplete

### Extra Credit
For an extra credit, parse the message body for attachments and count the number of attached files. Respond with an error code 550 if too many files (> 5) are attached in the message.

Refer to RFC 2045 to understand how attachments are identified both in the message header and message body. This document is actually the first part of five:

    RFC2045: MIME Part 1: Format of Internet Message Bodies
    RFC2046: MIME Part 2: Media Types
    RFC2047: MIME Part 3: Message Header Extensions for Non-ASCII Text
    RFC2048: MIME Part 4: Registration Procedure
    RFC2049: MIME Part 5: Conformance Criteria and Examples

You may be interested in reading Part 1 and Part 5, and skip Part 2-Part 4. In particular, Part 5 shows an example of embedding attachments in the message body.