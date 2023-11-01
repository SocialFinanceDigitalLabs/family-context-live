# Example Infrastructure

The files here are for example or testing purposes only, and shouldn't be used in a production environment
without some sort of review or assessment for security. 

## AWS
The scripts held here are using CloudFormation. Once you log into your AWS account, go to
the cloudformation panel and use the file as a template to create the infrastructure
needed to run the service.

This isn't yet plug-and-play and some things will need to be configured to get it working. The 
following should be done *first* before using this script:
1. The Cognito SSO configuration is not part of this script
2. The SSL Certificate needs to be loaded into Certificate Manager (AWS) and the ARN linked in
as a variable.
3. The database configuration isn't part of this script and the script should be changed to make
sure the needed configuration is added in. 