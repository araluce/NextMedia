
$(document).ready(function() {
    $.ajax({
        url: "/visitas_usuarios",
        type: 'get',
        success: function(datos) {
            Visualiza_datos(datos);
        },
        failure: function(datos) {
            alert('fallo');
        }
    });
    function Visualiza_datos(datos) {
        var chart = {
            type: 'bar'
        };
        var xAxis = {
            categories: datos[0]
        };
        var yAxis = {
            title: {
                text: 'Usuarios visitados'
      }
   };


   var series =  [
      {
         name: 'Visitas',
         data: datos[1]
      }
   ];

   var title = {
       text: 'Número de visitas por usuario'
   }

   var json = {};

   json.title = title;
   json.chart = chart;
   json.xAxis = xAxis;
   json.yAxis = yAxis;
   json.series = series;

   $('#visitas_usuarios').highcharts(json);

 }
});

$(document).ready(function() {
    $.ajax({
        url: "/likes_videos",
        type: 'get',
        success: function(datos) {
            Visualiza_datos(datos);
        },
        failure: function(datos) {
            alert('fallo');
        }
    });
    function Visualiza_datos(datos) {
        var chart = {
            type: 'bar'
        };
        var xAxis = {
            categories: datos[0]
        };
        var yAxis = {
            title: {
                text: 'Vídeos'
      }
   };


   var series =  [
      {
         name: 'Likes',
         data: datos[1]
      }
   ];

   var title = {
       text: 'Número de likes por video'
   }

   var json = {};

   json.title = title;
   json.chart = chart;
   json.xAxis = xAxis;
   json.yAxis = yAxis;
   json.series = series;

   $('#likes_videos').highcharts(json);

 }
});

$(document).ready(function() {
    $.ajax({
        url: "/dislikes_videos",
        type: 'get',
        success: function(datos) {
            Visualiza_datos(datos);
        },
        failure: function(datos) {
            alert('fallo');
        }
    });
    function Visualiza_datos(datos) {
        var chart = {
            type: 'bar'
        };
        var xAxis = {
            categories: datos[0]
        };
        var yAxis = {
            title: {
                text: 'Vídeos'
      }
   };


   var series =  [
      {
         name: 'Dislikes',
         data: datos[1]
      }
   ];

   var title = {
       text: 'Número de dislikes por video'
   }

   var json = {};

   json.title = title;
   json.chart = chart;
   json.xAxis = xAxis;
   json.yAxis = yAxis;
   json.series = series;

   $('#dislikes_videos').highcharts(json);

 }
});