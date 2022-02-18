Install requirents with python by typing
pip install -r requirents.txt 

Run django 
python manage.py runserver

// JAVA ANDROID
URL url = new URL(API_URL);
urlConnection = (HttpURLConnection)url.openConnection();
urlConnection.setRequestProperty("Authorization","Token " + auth_token );
urlConnection.connect();

// ANGULAR OR REACT 
let authHeaders = new Headers({ Authorization: "Token " + localStorage.getItem("authToken")});
const requestOptions: RequestOptionsArgs = { headers: authHeaders };
return this.http.get("/api/users/profile", requestOptions);

