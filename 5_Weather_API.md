1. Create an Account
   - go to : https://home.openweathermap.org/
2. Get Create an API key
   e.g my API Key : 95b9aaca4c4d70262e60f63f8f3393ff
3. Requests
3.1 Using Latitute and Latitude
    - format : https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
    - example : https://api.openweathermap.org/data/2.5/weather?lat=-25.7523712&lon=29.715950&appid=95b9aaca4c4d70262e60f63f8f3393ff
    - results : open example link in browser and you get
       - 
      //
         {"coord":{"lon":29.716,"lat":-25.7524},"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],"base":"stations","main":
         {"temp":291.2,"feels_like":290.16,"temp_min":291.2,"temp_max":291.2,"pressure":1016,"humidity":42,"sea_level":1016,"grnd_level":840},"visibility":10000,"wind":
         {"speed":6.05,"deg":147,"gust":4.66},"clouds":{"all":11},"dt":1697532294,"sys":
         {"country":"ZA","sunrise":1697513096,"sunset":1697558874},"timezone":7200,"id":976361,"name":"Middelburg","cod":200}
      //
   
