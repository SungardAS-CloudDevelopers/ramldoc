import unittest2 as unittest
from  ramldoc.raml_builder import build_documentation
from ramldoc.get_annotation import AnnotatedClass
import string

# Decorators:
from ramldoc.annotations import path, description, response, body, responses, queryparameter

#Examples:
# Use this for raml decorators, as well as unit tests!!!1

user_example = {
    "company_guid" : "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5",
    "business_title" : "Cloud Software Engineer",
    "first_name" : "Eric",
    "last_name" : "Chazan",
    "street_address" : "401 North Broad Street",
    "city" : "Philadelphia",
    "state" : "PA",
    "zip" : "19108"
}

registration_example = {
    "RegistrationRequest": {
        
        "invitation_token" : "fa2a3fc0-f79a-4da9-925c-53fe10bc0019",
        "user_data" : {
                "company_guid" : "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5",
                "business_title" : "Cloud Software Engineer",
                "first_name" : "Eric",
                "last_name" : "Chazan",
                "street_address" : "401 North Broad Street",
                "city" : "Philadelphia",
                "state" : "PA",
                "zip" : "19108",
                "country" : "USA"
        },

       "billing_data" : {
            "Fields TBD" : "???"
        }
    }
}

invitation_example = {
    "user_email": "eric.chazan@sungardas.com",
    "company_guid" : "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5"
}

invitation_new_example = {
    "user_email": "eric.chazan@sungardas.com",
    "company_guid" : "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5",
    "token" : "63324f27-8fce-4a85-b7fc-cde17194dd50",
    "time_sent" : "2015-03-27 16:11:29.791974",
    "status" : "invited"
}

invitation_list_example = {
    "invitations":
    [
        {
            "user_email": "eric.chazan@sungardas.com",
            "company_guid" : "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5",
            "token" : "63324f27-8fce-4a85-b7fc-cde17194dd50",
            "time_sent" : "2015-03-27 16:11:29.791974",
            "status" : "invited"
        },
        {
            "user_email": "alex.ough@sungardas.com",
            "company_guid" : "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5",
            "token" : "26002db3-8fb3-4cf9-b2e8-990e5cdc6a19",
            "time_sent" : "2015-01-27 16:11:29.791974",
            "status" : "expired"        
        }
    ]  
}

error_example = {
    "error" : {
        "message" : "Something went horribly wrong!",
        "stack_trace" : [
            "Traceback (most recent call last):",
            "  File '<do_something.py>', line 87, in <module> do_a_thing()",
            "  File '<oh_noes.py>', line 10, in <module>    uh_oh()",
            "IndexError: tuple index out of range"
        ]
    }
}

company_example = {
    "guid" : "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5",
    "name" : "Sungard Availablilty Services"
}

company_new_example = {
    "name" : "Sungard Availablilty Services"
}

company_list_example = {
    "companies":
    [
        {
            "guid" : "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5",
            "name" : "Sungard Availablilty Services"
        },
        {
            "guid" : "63324f27-8fce-4a85-b7fc-cde17194dd50",
            "name" : "Apple"
        }
    ]
}

#Schemas:
# A pile of json Schemas for documenting things.
# It would be nice to move to and from objects in python, but, well, I dont see a nice way to do something like this right now.
# I am not too worried about it because dictionaries are really functional:

registration= {
    "title": "RegistrationRequest",
    "$schema": "http://json-schema.org/draft-03/schema",
    "id": "http://jsonschema.net",
    "required": True,
    "type": "object",
    "properties": {
        
        "invitation_token" : {
            "description" : "The token from the invitation",
            "type" : "string",
            "required" : True
        },
        
        "user_data" : {
            "$ref" : "UserData"
        },
            
       "billing_data" : {
            "description" : "the data required to pass to the biller.  Details TBD",
            "type" : "object",
            "properties" : {
                "Fields TBD" : {
                    "type" : "string",
                    "required" : False
                }
            }
        }
    }
}

user = {
    "title" : "UserData",
    "$schema": "http://json-schema.org/draft-03/schema",
    "id": "http://jsonschema.net",   
    "required": True,
    "type": "object",           
    "properties" : {
        "description" : "The user to register",
        "type" : "object",
        "required" : True,
               
        "properties" : {           
            "company_guid" : {
                    "description" : "UUID for the company",
                    "type" : "string",
                    "required" : True
                },
            "business_title" : {
                "description" : "Title for the user",
                "type" : "string",
                "required" : True
            },                       
            "first_name" : {
                "description" : "The First Name",
                "type" : "string",
                "required" : True
            }, 
            "last_name" : {
                "description" : "The Last Name",
                "type" : "string",
                "required" : True
            },            
            "street_address" : {
                "description" : "Business Street Address",
                "type" : "string",
                "required" : True
            },           
            "city" : {
                "description" : "Business City",
                "type" : "string",
                "required" : True
            },
             "state" : {
                "description" : "Business State",
                "type" : "string",
                "required" : True
            },          
             "zip" : {
                "description" : "Business Zip Code",
                "type" : "string",
                "required" : True
            },        
             "country" : {
                "description" : "Business Country",
                "type" : "string",
                "required" : True
            }
        }
    }
}

invitation = {
    "title": "Invitation",
    "$schema": "http://json-schema.org/draft-03/schema",
    "id": "http://jsonschema.net",
    "required": True,
    "type": "object",
    
    "properties": {
        "user_email": {
            "description" : "email address of the user",
            "type": "string",
            "required": True
        },
        
        "company_guid" : {
            "description" : "uuid of the company",
            "type" : "string",
            "required" : True
        },
        
        "token" : {
            "description" : "uuid of the token",
            "type" : "string",
            "required" : True
        },
        
        "time_sent" : {
            "description" : "timestamp of send time of the email (ISO 8604 format)",
            "type" : "string"
        },
        
        "status" : {
            "description": "current status of the invitation must be one of [invited, expired, error]",
            "type" : "string"
        }
    }
}

invitations = {
    "title": "Invitations",
    "$schema": "http://json-schema.org/draft-03/schema",
    "id": "http://jsonschema.net",
    "required": True,
    "type": "array",
    
    "items": { 
        "$ref" : "Invitation"
    }
}

error = {
    "title": "Error",
    "$schema": "http://json-schema.org/draft-03/schema",
    "id": "http://jsonschema.net",
    "required": True,
    "type": "object",
    
    "properties": {
        "error" : {
            "description" : "A description of the error",
            "type" : "object",
            "required" : True,
            "properties" : {
                "message" : {
                    "type" : "string",
                    "required" : True
                },
                "stack_trace" : {
                    "type" : "array",
                    "required" : False,
                    "items": {
                        "type": "string"
                    }
                }
            }
        }
    }
}

company = {
    "title": "Company",
    "$schema": "http://json-schema.org/draft-03/schema",
    "id": "http://jsonschema.net",
    "required": True,
    "type": "object",
    
    "properties": {
        "name" : {
            "description" : "The name of the company",
            "type" : "string",
            "required" : True
        },
        
        "guid" : { 
            "description" : "The UUID of the company",
            "type" : "string"
        }
    }
}

companies = {
    "title": "Companies",
    "$schema": "http://json-schema.org/draft-03/schema",
    "id": "http://jsonschema.net",
    "required": True,
    "type": "array",
    
    "items": { 
        "$ref" : "Company"
    }
}

# Class Definitions:
@path("companies/")
class CompanyInvitationRoot(AnnotatedClass):
    @description("List all companies")
    @response(200,
              "Successful Result, company objects returned",
              companies,
              company_list_example)
    def get(self): 
        pass
  
    @description("Create a company")
    @body(company, company_new_example)
    @responses([response(
                        200,
                        "Successful Result, company object returned",
                        company,
                        company_example),
                response(400, "Error", error, error_example)])
    def post(self):
        pass

@path("companies/{company_uid}/")
class CompanyInvitationId(AnnotatedClass):
    @description( "Retrieves a specific company")
    @response(200,
              "Successful Result, company object returned",
              company,
              company_example)
    @response(400, "Error", error, error_example)
    def get(self, company_uid):
        pass

@path("registration-requests/")
class RegistrationService(AnnotatedClass):

    @description("Creates a registration")
    @body (registration, registration_example)
    @response(200, "Successful Result, user object returned", registration, user)
    @response(400, "Unable to generate a registration", error, error_example)
    def post(self, json_data):
        pass
    
@path("user_invitations/")
class UserInvitationRoot(AnnotatedClass):
    
    @description("Retrieves a list of pending and expired invitations")
    @response(200,"An array of invitation objects",invitations,invitation_list_example)
    def get(self):
        pass

    @description("Issues an invitation")
    @response(200,
              "A copy of the invitation object",
              invitation,
              invitation_example)
    @response(400,
              "An Error",
              error,
              error_example)    
    @body (invitation, invitation_new_example)
    def post(self, post_data):
        pass

@path("user_invitations/{invitationId}/")
class UserInvitationId(AnnotatedClass):
    @description("Retrieve an invitation by id")
    @response(200,
              "A copy of the invitation",
              invitation,
              invitation_new_example)
    @response(404,
              "An Error",
              error,
              error_example)
    #Note that the variable name matches the variable name in the path.
    def get(self,invitationId):
        pass
    @queryparameter("os_domain_id", "OpenStack domain id",
                    True, "uuid")
    @queryparameter("status_as", "Search by invitation status",
                    False)    
    @description("delete an invitation by id")
    @response(200, "Successful Deletion")
    @response(404,
          "An Error",
          error,
          error_example)
    def delete(self, invitationId):
        pass
    
modules = [CompanyInvitationId,
           CompanyInvitationRoot,
           UserInvitationId,
           UserInvitationRoot,
           RegistrationService]

expected_value = """#%RAML 0.8
---
title: Unit Test Service
baseUri: sungardas.com/unit-test-doc/{version}
version: 14.4

/companies:
  get:
    description: List all companies
    responses:
      200:
        description: Successful Result, company objects returned
        body:
          application/json:
            schema: |
              {"title": "Companies", "items": {"$ref": "Company"}, "required": true, "$schema": "http://json-schema.org/draft-03/schema", "type": "array", "id": "http://jsonschema.net"}
            example: |
              {"companies": [{"guid": "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5", "name": "Sungard Availablilty Services"}, {"guid": "63324f27-8fce-4a85-b7fc-cde17194dd50", "name": "Apple"}]}

  post:
    description: Create a company
    body:
      application/json:
        schema: |
          {"title": "Company", "required": true, "properties": {"guid": {"type": "string", "description": "The UUID of the company"}, "name": {"required": true, "type": "string", "description": "The name of the company"}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
        example: |
          {"name": "Sungard Availablilty Services"}
    responses:
      200:
        description: Successful Result, company object returned
        body:
          application/json:
            schema: |
              {"title": "Company", "required": true, "properties": {"guid": {"type": "string", "description": "The UUID of the company"}, "name": {"required": true, "type": "string", "description": "The name of the company"}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
            example: |
              {"guid": "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5", "name": "Sungard Availablilty Services"}
      400:
        description: Error
        body:
          application/json:
            schema: |
              {"title": "Error", "required": true, "properties": {"error": {"required": true, "type": "object", "description": "A description of the error", "properties": {"stack_trace": {"items": {"type": "string"}, "required": false, "type": "array"}, "message": {"required": true, "type": "string"}}}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
            example: |
              {"error": {"stack_trace": ["Traceback (most recent call last):", "  File '<do_something.py>', line 87, in <module> do_a_thing()", "  File '<oh_noes.py>', line 10, in <module>    uh_oh()", "IndexError: tuple index out of range"], "message": "Something went horribly wrong!"}}

  /{company_uid}:
    get:
      description: Retrieves a specific company
      responses:
        200:
          description: Successful Result, company object returned
          body:
            application/json:
              schema: |
                {"title": "Company", "required": true, "properties": {"guid": {"type": "string", "description": "The UUID of the company"}, "name": {"required": true, "type": "string", "description": "The name of the company"}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
              example: |
                {"guid": "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5", "name": "Sungard Availablilty Services"}
        400:
          description: Error
          body:
            application/json:
              schema: |
                {"title": "Error", "required": true, "properties": {"error": {"required": true, "type": "object", "description": "A description of the error", "properties": {"stack_trace": {"items": {"type": "string"}, "required": false, "type": "array"}, "message": {"required": true, "type": "string"}}}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
              example: |
                {"error": {"stack_trace": ["Traceback (most recent call last):", "  File '<do_something.py>', line 87, in <module> do_a_thing()", "  File '<oh_noes.py>', line 10, in <module>    uh_oh()", "IndexError: tuple index out of range"], "message": "Something went horribly wrong!"}}

/registration-requests:
  post:
    description: Creates a registration
    body:
      application/json:
        schema: |
          {"title": "RegistrationRequest", "required": true, "properties": {"billing_data": {"type": "object", "description": "the data required to pass to the biller.  Details TBD", "properties": {"Fields TBD": {"required": false, "type": "string"}}}, "user_data": {"$ref": "UserData"}, "invitation_token": {"required": true, "type": "string", "description": "The token from the invitation"}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
        example: |
          {"RegistrationRequest": {"billing_data": {"Fields TBD": "???"}, "user_data": {"last_name": "Chazan", "city": "Philadelphia", "first_name": "Eric", "business_title": "Cloud Software Engineer", "zip": "19108", "country": "USA", "company_guid": "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5", "state": "PA", "street_address": "401 North Broad Street"}, "invitation_token": "fa2a3fc0-f79a-4da9-925c-53fe10bc0019"}}
    responses:
      200:
        description: Successful Result, user object returned
        body:
          application/json:
            schema: |
              {"title": "RegistrationRequest", "required": true, "properties": {"billing_data": {"type": "object", "description": "the data required to pass to the biller.  Details TBD", "properties": {"Fields TBD": {"required": false, "type": "string"}}}, "user_data": {"$ref": "UserData"}, "invitation_token": {"required": true, "type": "string", "description": "The token from the invitation"}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
            example: |
              {"title": "UserData", "required": true, "properties": {"required": true, "type": "object", "description": "The user to register", "properties": {"last_name": {"required": true, "type": "string", "description": "The Last Name"}, "city": {"required": true, "type": "string", "description": "Business City"}, "first_name": {"required": true, "type": "string", "description": "The First Name"}, "business_title": {"required": true, "type": "string", "description": "Title for the user"}, "zip": {"required": true, "type": "string", "description": "Business Zip Code"}, "country": {"required": true, "type": "string", "description": "Business Country"}, "company_guid": {"required": true, "type": "string", "description": "UUID for the company"}, "state": {"required": true, "type": "string", "description": "Business State"}, "street_address": {"required": true, "type": "string", "description": "Business Street Address"}}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
      400:
        description: Unable to generate a registration
        body:
          application/json:
            schema: |
              {"title": "Error", "required": true, "properties": {"error": {"required": true, "type": "object", "description": "A description of the error", "properties": {"stack_trace": {"items": {"type": "string"}, "required": false, "type": "array"}, "message": {"required": true, "type": "string"}}}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
            example: |
              {"error": {"stack_trace": ["Traceback (most recent call last):", "  File '<do_something.py>', line 87, in <module> do_a_thing()", "  File '<oh_noes.py>', line 10, in <module>    uh_oh()", "IndexError: tuple index out of range"], "message": "Something went horribly wrong!"}}

/user_invitations:
  get:
    description: Retrieves a list of pending and expired invitations
    responses:
      200:
        description: An array of invitation objects
        body:
          application/json:
            schema: |
              {"title": "Invitations", "items": {"$ref": "Invitation"}, "required": true, "$schema": "http://json-schema.org/draft-03/schema", "type": "array", "id": "http://jsonschema.net"}
            example: |
              {"invitations": [{"status": "invited", "time_sent": "2015-03-27 16:11:29.791974", "token": "63324f27-8fce-4a85-b7fc-cde17194dd50", "company_guid": "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5", "user_email": "eric.chazan@sungardas.com"}, {"status": "expired", "time_sent": "2015-01-27 16:11:29.791974", "token": "26002db3-8fb3-4cf9-b2e8-990e5cdc6a19", "company_guid": "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5", "user_email": "alex.ough@sungardas.com"}]}

  post:
    description: Issues an invitation
    body:
      application/json:
        schema: |
          {"title": "Invitation", "required": true, "properties": {"status": {"type": "string", "description": "current status of the invitation must be one of [invited, expired, error]"}, "time_sent": {"type": "string", "description": "timestamp of send time of the email (ISO 8604 format)"}, "token": {"required": true, "type": "string", "description": "uuid of the token"}, "company_guid": {"required": true, "type": "string", "description": "uuid of the company"}, "user_email": {"required": true, "type": "string", "description": "email address of the user"}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
        example: |
          {"status": "invited", "time_sent": "2015-03-27 16:11:29.791974", "token": "63324f27-8fce-4a85-b7fc-cde17194dd50", "company_guid": "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5", "user_email": "eric.chazan@sungardas.com"}
    responses:
      200:
        description: A copy of the invitation object
        body:
          application/json:
            schema: |
              {"title": "Invitation", "required": true, "properties": {"status": {"type": "string", "description": "current status of the invitation must be one of [invited, expired, error]"}, "time_sent": {"type": "string", "description": "timestamp of send time of the email (ISO 8604 format)"}, "token": {"required": true, "type": "string", "description": "uuid of the token"}, "company_guid": {"required": true, "type": "string", "description": "uuid of the company"}, "user_email": {"required": true, "type": "string", "description": "email address of the user"}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
            example: |
              {"company_guid": "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5", "user_email": "eric.chazan@sungardas.com"}
      400:
        description: An Error
        body:
          application/json:
            schema: |
              {"title": "Error", "required": true, "properties": {"error": {"required": true, "type": "object", "description": "A description of the error", "properties": {"stack_trace": {"items": {"type": "string"}, "required": false, "type": "array"}, "message": {"required": true, "type": "string"}}}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
            example: |
              {"error": {"stack_trace": ["Traceback (most recent call last):", "  File '<do_something.py>', line 87, in <module> do_a_thing()", "  File '<oh_noes.py>', line 10, in <module>    uh_oh()", "IndexError: tuple index out of range"], "message": "Something went horribly wrong!"}}

  /{invitationId}:
    delete:
      description: delete an invitation by id
      queryParameters:
        status_as:
          description: Search by invitation status
          required: false
          type: string
        os_domain_id:
          description: OpenStack domain id
          required: true
          type: uuid
      responses:
        200:
          description: Successful Deletion
        404:
          description: An Error
          body:
            application/json:
              schema: |
                {"title": "Error", "required": true, "properties": {"error": {"required": true, "type": "object", "description": "A description of the error", "properties": {"stack_trace": {"items": {"type": "string"}, "required": false, "type": "array"}, "message": {"required": true, "type": "string"}}}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
              example: |
                {"error": {"stack_trace": ["Traceback (most recent call last):", "  File '<do_something.py>', line 87, in <module> do_a_thing()", "  File '<oh_noes.py>', line 10, in <module>    uh_oh()", "IndexError: tuple index out of range"], "message": "Something went horribly wrong!"}}

    get:
      description: Retrieve an invitation by id
      responses:
        200:
          description: A copy of the invitation
          body:
            application/json:
              schema: |
                {"title": "Invitation", "required": true, "properties": {"status": {"type": "string", "description": "current status of the invitation must be one of [invited, expired, error]"}, "time_sent": {"type": "string", "description": "timestamp of send time of the email (ISO 8604 format)"}, "token": {"required": true, "type": "string", "description": "uuid of the token"}, "company_guid": {"required": true, "type": "string", "description": "uuid of the company"}, "user_email": {"required": true, "type": "string", "description": "email address of the user"}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
              example: |
                {"status": "invited", "time_sent": "2015-03-27 16:11:29.791974", "token": "63324f27-8fce-4a85-b7fc-cde17194dd50", "company_guid": "bccc9cb0-176e-4022-9a50-28fc4d7dfbd5", "user_email": "eric.chazan@sungardas.com"}
        404:
          description: An Error
          body:
            application/json:
              schema: |
                {"title": "Error", "required": true, "properties": {"error": {"required": true, "type": "object", "description": "A description of the error", "properties": {"stack_trace": {"items": {"type": "string"}, "required": false, "type": "array"}, "message": {"required": true, "type": "string"}}}}, "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "id": "http://jsonschema.net"}
              example: |
                {"error": {"stack_trace": ["Traceback (most recent call last):", "  File '<do_something.py>', line 87, in <module> do_a_thing()", "  File '<oh_noes.py>', line 10, in <module>    uh_oh()", "IndexError: tuple index out of range"], "message": "Something went horribly wrong!"}}                """

def compare_ignore_whitespace(s1, s2):
    remove = string.punctuation + string.whitespace
    return s1.translate(None, remove) == s2.translate(None, remove)

#We can actually just call the builder, and evaluate it against the expected result :)
class TestBaseService(unittest.TestCase):

    def setUp(self):
        pass

    def test_raml_builder(self):
        output = build_documentation(modules, "Unit Test Service", "sungardas.com/unit-test-doc", "14.4")
        
        if compare_ignore_whitespace(expected_value, output) == False:
            print "I PARSED THIS:"
            print output
            
            print "I expected this: "
            print expected_value
            raise Exception("Unexpected Difference!")
         
if __name__ == '__main__':
    unittest.main()