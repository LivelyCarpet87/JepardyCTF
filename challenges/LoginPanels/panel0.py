from serverBackend import data

def panel0(user,pwd):
    return True, "This page is just a sanity test.", "Test Message: This page is just a sanity test."
name="panel0"
data.enrollChallenge("loginPanels",name,"N/A",
{
    "1": "This page is just a sanity test.",
    "2": "Just try entering anything!",
    "3": "Why would you ever need more hints?"
},
0,{
    "filter":{}
})
