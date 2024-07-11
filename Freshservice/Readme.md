Readme

# Freshservice Integration with Okta Access Request Flow (App Request)

This integration enables Freshservice to operate in two distinct patterns for managing access requests:

1. **Okta-Initiated Requests**: Access requests begin in Okta's Access Request Flow, and corresponding tickets are created in Freshservice to track approvals.
2. **Freshservice-Initiated Requests**: Access requests start in Freshservice, which then initiates, processes, and closes an Okta request in the background. The result is synchronized back to Freshservice.

## Okta-Initiated Request

### Access Request Started with Sequences

1. Upon Access Request initiation in Okta Access Request, the sequence calls this delegated flow.
2. The flow gathers all the information from the access request and populates a Freshservice ticket with all the necessary resource and user details.
3. A Freshservice Ticket is then created.

### Closing the Freshservice Ticket

1. **Track Ticket ID**: Track the appropriate ticket ID by creating a table with Ticket ID and Resource Name.
2. **Match Details**: Match the user, resource name, and ticket ID.
3. **Close Ticket**: Close the ticket once matched.

## Freshservice-Initiated Request

### Access Request Created with AtSpoke

1. **Trigger Access Request**: Use the Trigger for Access Request Created and filter data.
2. **Populate Ticket Description**: Call Read User and Read Manager to populate the ticket description.
3. **Create Freshservice Ticket**: Create a ticket in Freshservice.
4. **Log Details**: Create a row in the table for Ticket ID, Email, and Application Name.

### Access Request Resolved - Close Ticket

1. **Trigger Access Request Resolved**: Use the Access Request Resolved Trigger and pull Access Request ID.
2. **Read Access Request**: Call the OIG API to read Access Request and search the table for primary email and application name to get the Freshservice ticket number.
3. **Update Ticket**: Update the Freshservice ticket with 'resolved' status and update the description with the approval decision.

