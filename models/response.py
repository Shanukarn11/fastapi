def Response(data, code, message, error):
    return {
        "data": data,
        "code": code,
        "message": message,
        "error": error
    }



# class User(BaseModel):

#     PrimaryContactEmailAddress: EmailStr = Field(None, title="Email")
#     FirstName:str = Field(
#         None, title="FirstName", max_length=100
#     )
#     LastName :str = Field(
#         None, title="FirstName", max_length=100
#     )
#     Password:str = Field(
#         None, title="FirstName", max_length=300
#     )
#     PrimaryContactPhoneNumber= Field(
#         None, title="FirstName", max_length=300
#     )
    
#     Status:str= Field(
#         None, title="FirstName", max_length=300
#     )
#     Type:str= Field(
#         None, title="FirstName", max_length=300
#     )