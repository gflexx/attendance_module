Install requirents with python by typing
pip install -r requirents.txt 

Neo 4j db server must be running to create db items
https://neo4j.com/download/

Run django 
python manage.py runserver

To connect to the API inject your header with
the authentication token provided during
login in and registration

// JAVA ANDROID
URL url = new URL(API_URL);
urlConnection = (HttpURLConnection)url.openConnection();
urlConnection.setRequestProperty("Authorization","Token " + auth_token );
urlConnection.connect();

// ANGULAR OR REACT 
let authHeaders = new Headers({ Authorization: "Token " + localStorage.getItem("authToken")});
const requestOptions: RequestOptionsArgs = { headers: authHeaders };
return this.http.get("/api/users/profile", requestOptions);

