from wambda.shortcuts import redirect

def home(master):
  """Redirect to frontend SPA"""
  return redirect("/app/")