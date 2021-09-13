        _fetch = function(i,src){
          return fetch(src).then(function(response) {
            if(!response.ok) throw new Error("No image in the response");
            var headers = response.headers;
            var ct = headers.get('Content-Type');
            var contentType = 'image/png';
            if(ct !== null){
              contentType = ct.split(';')[0];
            }
            
            return response.blob().then(function(blob){
              return {
                'blob': blob,
                'mime': contentType,
                'i':i,
              };
            });
          });
        };
        
        _read = function(response){
          return new Promise(function(resolve, reject){
            var blob = new Blob([response.blob], {type : response.mime});
            var reader = new FileReader();
            reader.onload = function(e){
              resolve({'data':e.target.result, 'i':response.i});
            };
            reader.onerror = reject;
            reader.readAsDataURL(blob);
          });
        };
        
        _replace = function(){
            for (var i = 0, len = q.length; i < len; i++) {imgs[q[i].item].src = q[i].data;}
        }
        
        var q = [];
        var imgs = document.querySelectorAll('img');
        for (var i = 0, len = imgs.length; i < len; i++) {
                _fetch(i,imgs[i].src).then(_read).then(function(data){
            q.push({
              'data': data.data,
              'item': data.i,
            });
          });
            }
        setTimeout(_replace, 1000 );
