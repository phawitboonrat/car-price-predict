var firebaseConfig = {
    apiKey: "AIzaSyBGv_05cA2Qm1QEuKUZ4U-hFCiyxc1e_8A",
    authDomain: "car-price-bbaa2.firebaseapp.com",
    databaseURL: "https://car-price-bbaa2.firebaseio.com",
    projectId: "car-price-bbaa2",
    storageBucket: "car-price-bbaa2.appspot.com",
    messagingSenderId: "1037650573971",
    appId: "1:1037650573971:web:3340cfcafbe4cc5f9c6b66",
    measurementId: "G-VH5FGK3CBV"
};
firebase.initializeApp(firebaseConfig);
firebase.analytics();

function writeData(time,brand,year,mile,colour,province) {
    firebase.database().ref('events/'+time).set({
      brand: brand,
      year: year,
      mile: mile,
      colour: colour,
      province: province,
      y: -1

    });
}


function okBtn() {
    console.log('okBtn');

    brand = document.getElementById("brand").value;
    province = document.getElementById("province").value;
    colour = document.getElementById("colour").value;
    mile = document.getElementById("mile").value;
    year = document.getElementById("year").value;
    price = document.getElementById("price").value;

    if(brand == 'ยี่ห้อ' || province == 'เขตพื้นที่' || colour == 'สี' || mile == '' || year == 'ปี'){
      document.getElementById("price").value = "please fill all input";
      return;
    }

    mile_ = parseInt(mile)
    if(!(mile_>0 && mile_<1000000)){
      console.log('mile must between 0-1000000');
      document.getElementById("price").value = "mile must between 0-1000000";
      return;
    }
    document.getElementById("price").value = "Predicting.....";
   

    time = String(new Date().getTime());

    console.log(time+'/'+brand+'/'+year+'/'+mile+'/'+colour+'/'+province)

    writeData(time,brand,year,mile,colour,province);


    setTimeout(() => { 
      var ref = firebase.database().ref('events/'+time+"/y");
      ref.on("value", function(snapshot) {
        p = snapshot.val()
        console.log('price : '+p);
        
        if(p != -1){
          document.getElementById("price").value = p;
        }

      }, function (errorObject) {
        console.log("The read failed: " + errorObject.code);
      });
      
    }, 300);




}

function cancleBtn() {
  console.log('cancleBtn');

  document.getElementById("brand").value = "ยี่ห้อ";
  document.getElementById("province").value = "เขตพื้นที่";
  document.getElementById("colour").value = "สี";
  document.getElementById("mile").value = "";
  document.getElementById("year").value = "ปี";
  document.getElementById("price").value = "";
   

}


