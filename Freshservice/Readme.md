Readme

Freshservice Integration with Okta Access Request Flow (App Request)
This integration enables Freshservice to operate in two distinct patterns for managing access requests:
1. Okta-Initiated Requests: Access requests begin in Okta's Access Request Flow, and corresponding tickets are created in Freshservice to track approvals.
2. Freshservice-Initiated Requests: Access requests start in Freshservice, which then initiates, processes, and closes an Okta request in the background. The result is synchronized back to Freshservice.

Okta Initiated Request
Access Request Started with Sequences

1. Upon Access Request initiation in Okta Access Request, the sequence calls to a this delegated flow
2. The flow gathers all the information from the access request and populates a Freshservice ticket with all the resource and user details necessary
3. Freshservice Ticket is then created

Closing the Freshservice Ticket
1. How would we track the appropriate ticket ID? Ticket ID created + Resource Name in a table
2. Match user + resource name and ticket id?
3. Close ticket

Accesss Request created with atspoke
1. Use the Trigger for Access Request Created and Filter data
2. Call Read User and Read Manager to populate the ticket description
3. Create Freshservice Ticket
4. Create Row in Table for Ticket ID, Email, Application Name

Closing ticket
